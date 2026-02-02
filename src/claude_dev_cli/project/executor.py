"""Ticket execution engine for automated code generation.

Fetches tickets from external systems, analyzes requirements,
generates code/tests, and updates ticket status.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime

from claude_dev_cli.tickets.backend import TicketBackend, Ticket
from claude_dev_cli.core import ClaudeClient
from claude_dev_cli.logging.logger import ProgressLogger
from claude_dev_cli.notifications.notifier import Notifier, NotificationPriority
from claude_dev_cli.vcs.manager import VCSManager
from claude_dev_cli.project.context_gatherer import TicketContextGatherer, CodeContext


class TicketExecutor:
    """Executes tickets by generating code/tests based on requirements.
    
    This is the core automation engine that:
    1. Fetches a ticket from backend (repo-tickets, Jira, etc.)
    2. Analyzes requirements and acceptance criteria
    3. Uses AI to generate implementation code
    4. Uses AI to generate tests
    5. Updates ticket status
    6. Commits changes (optional)
    7. Logs progress
    8. Sends notifications
    """
    
    def __init__(
        self,
        ticket_backend: TicketBackend,
        ai_client: Optional[ClaudeClient] = None,
        logger: Optional[ProgressLogger] = None,
        notifier: Optional[Notifier] = None,
        vcs: Optional[VCSManager] = None,
        auto_commit: bool = False,
        gather_context: bool = True,
        project_root: Optional[Path] = None
    ):
        """Initialize ticket executor.
        
        Args:
            ticket_backend: Ticket management backend
            ai_client: AI client for code generation
            logger: Progress logger
            notifier: Notification system
            vcs: VCS manager
            auto_commit: Whether to auto-commit changes
            gather_context: Whether to gather codebase context before execution
            project_root: Root of the project (default: current directory)
        """
        self.ticket_backend = ticket_backend
        self.ai_client = ai_client or ClaudeClient()
        self.logger = logger
        self.notifier = notifier
        self.vcs = vcs
        self.auto_commit = auto_commit
        self.gather_context = gather_context
        self.context_gatherer = TicketContextGatherer(project_root) if gather_context else None
    
    def execute_ticket(self, ticket_id: str) -> bool:
        """Execute a single ticket end-to-end.
        
        Args:
            ticket_id: Ticket identifier
            
        Returns:
            True if execution successful
        """
        try:
            # Step 1: Fetch ticket
            self._log(f"Fetching ticket {ticket_id}...")
            ticket = self.ticket_backend.fetch_ticket(ticket_id)
            
            if not ticket:
                self._log(f"Ticket {ticket_id} not found", level="error")
                return False
            
            self._log(f"✅ Fetched ticket: {ticket.title}", ticket_id=ticket_id, level="success")
            self._notify(f"Starting {ticket_id}", f"Task: {ticket.title}")
            
            # Step 2: Gather codebase context (optional pre-processing)
            context = None
            if self.gather_context and self.context_gatherer:
                self._log("Gathering codebase context...", ticket_id=ticket_id)
                context = self.context_gatherer.gather_context(ticket, self.ai_client)
                self._log(
                    f"✅ Context gathered: {context.language}" + 
                    (f" ({context.framework})" if context.framework else ""),
                    ticket_id=ticket_id,
                    level="success"
                )
            
            # Step 3: Analyze requirements
            self._log("Analyzing requirements...", ticket_id=ticket_id)
            requirements_prompt = self._build_requirements_prompt(ticket, context)
            
            # Step 4: Generate implementation plan
            self._log("Generating implementation plan...", ticket_id=ticket_id)
            plan = self.ai_client.call(
                requirements_prompt,
                system_prompt="You are an expert software engineer. Analyze the ticket and create a detailed implementation plan."
            )
            
            self._log("Implementation plan created", ticket_id=ticket_id, level="success")
            
            # Step 5: Generate code
            self._log("Generating code...", ticket_id=ticket_id)
            code_prompt = self._build_code_generation_prompt(ticket, plan, context)
            
            generated_code = self.ai_client.call(
                code_prompt,
                system_prompt="You are an expert software engineer. Generate clean, well-documented code based on the requirements."
            )
            
            # Extract code from response (assuming it's in markdown code blocks)
            code_files = self._extract_code_from_response(generated_code)
            
            self._log(f"Generated {len(code_files)} file(s)", ticket_id=ticket_id, files=list(code_files.keys()))
            
            # Step 6: Write files
            for file_path, code_content in code_files.items():
                self._write_file(file_path, code_content)
                self._log(f"Created {file_path}", ticket_id=ticket_id)
                
                if self.logger:
                    self.logger.link_artifact(ticket_id, file_path)
            
            # Step 7: Generate tests
            if ticket.acceptance_criteria:
                self._log("Generating tests...", ticket_id=ticket_id)
                test_prompt = self._build_test_generation_prompt(ticket, code_files)
                
                test_code = self.ai_client.call(
                    test_prompt,
                    system_prompt="You are an expert test engineer. Generate comprehensive tests based on acceptance criteria."
                )
                
                test_files = self._extract_code_from_response(test_code)
                
                for test_file, test_content in test_files.items():
                    self._write_file(test_file, test_content)
                    self._log(f"Created test: {test_file}", ticket_id=ticket_id)
            
            # Step 8: Update ticket status
            self._log("Updating ticket status...", ticket_id=ticket_id)
            self.ticket_backend.update_ticket(ticket_id, status="completed")
            
            # Add completion comment
            self.ticket_backend.add_comment(
                ticket_id,
                f"✅ Implementation completed by claude-dev-cli\n\nGenerated files:\n" +
                "\n".join(f"- {f}" for f in code_files.keys()),
                author="claude-dev-cli"
            )
            
            # Step 9: Commit changes
            if self.auto_commit and self.vcs and self.vcs.is_repository():
                self._log("Committing changes...", ticket_id=ticket_id)
                commit_message = f"feat({ticket_id}): {ticket.title}\n\nGenerated by claude-dev-cli"
                
                commit_info = self.vcs.commit(
                    commit_message,
                    co_author="Warp <agent@warp.dev>"
                )
                
                self._log(f"Committed: {commit_info.sha[:7]}", ticket_id=ticket_id, level="success")
            
            # Step 10: Final notification
            self._log(f"✅ Ticket {ticket_id} completed!", ticket_id=ticket_id, level="success")
            self._notify(
                f"✅ {ticket_id} Complete",
                f"Task: {ticket.title}\nFiles: {len(code_files)}",
                priority=NotificationPriority.HIGH
            )
            
            return True
        
        except Exception as e:
            self._log(f"Error executing ticket: {e}", ticket_id=ticket_id, level="error")
            self._notify(
                f"❌ {ticket_id} Failed",
                f"Error: {str(e)}",
                priority=NotificationPriority.URGENT
            )
            return False
    
    def _build_requirements_prompt(self, ticket: Ticket, context: Optional[CodeContext] = None) -> str:
        """Build prompt for requirements analysis.
        
        Args:
            ticket: Ticket to analyze
            context: Optional codebase context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Analyze this software development ticket and create an implementation plan.

**Ticket:** {ticket.id}
**Title:** {ticket.title}
**Description:**
{ticket.description}

**Type:** {ticket.ticket_type}
**Priority:** {ticket.priority}
"""
        
        if ticket.requirements:
            prompt += "\n**Requirements:**\n"
            for req in ticket.requirements:
                prompt += f"- {req}\n"
        
        if ticket.acceptance_criteria:
            prompt += "\n**Acceptance Criteria:**\n"
            for criteria in ticket.acceptance_criteria:
                prompt += f"- {criteria}\n"
        
        # Add codebase context if available
        if context:
            prompt += "\n\n" + "="*50 + "\n"
            prompt += "# CODEBASE CONTEXT\n"
            prompt += "="*50 + "\n\n"
            prompt += context.format_for_prompt()
            prompt += "\n\n" + "="*50 + "\n\n"
        
        prompt += "\n\nProvide a detailed implementation plan with:\n"
        prompt += "1. Technical approach\n"
        prompt += "2. Files to create/modify\n"
        prompt += "3. Key functions/classes needed\n"
        prompt += "4. Dependencies required\n"
        
        if context:
            prompt += "\n**IMPORTANT:** Follow the existing codebase patterns and conventions shown above.\n"
        
        return prompt
    
    def _build_code_generation_prompt(self, ticket: Ticket, plan: str, context: Optional[CodeContext] = None) -> str:
        """Build prompt for code generation.
        
        Args:
            ticket: Ticket to implement
            plan: Implementation plan from previous step
            context: Optional codebase context
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Generate production-ready code based on this ticket and implementation plan.

**Ticket:** {ticket.id} - {ticket.title}

**Implementation Plan:**
{plan}
"""
        
        # Add context if available
        if context:
            prompt += "\n\n" + "="*50 + "\n"
            prompt += "# EXISTING CODEBASE CONTEXT\n"
            prompt += "="*50 + "\n\n"
            
            if context.similar_files:
                prompt += "**Similar existing files to reference:**\n"
                for file_info in context.similar_files[:3]:
                    prompt += f"- {file_info['path']}: {file_info['purpose']}\n"
                prompt += "\n"
            
            if context.naming_conventions:
                prompt += "**Project naming conventions:**\n"
                for type_name, pattern in context.naming_conventions.items():
                    prompt += f"- {type_name}: {pattern}\n"
                prompt += "\n"
            
            if context.common_imports:
                prompt += f"**Common imports in this project:** {', '.join(context.common_imports[:10])}\n\n"
            
            prompt += "="*50 + "\n\n"
        
        prompt += """**Requirements:**
Generate clean, well-documented, production-quality code. Include:
- Proper error handling
- Type hints (if Python)
- Docstrings/comments
- Follow best practices
"""
        
        if context:
            prompt += "- **IMPORTANT:** Follow the existing codebase patterns and conventions shown above\n"
        
        prompt += """\nOutput the code in markdown code blocks with file names as headers.
Example:
```python path/to/file.py
# code here
```
"""
        
        return prompt
    
    def _build_test_generation_prompt(self, ticket: Ticket, code_files: dict) -> str:
        """Build prompt for test generation."""
        prompt = f"""Generate comprehensive tests for the implemented code.

**Ticket:** {ticket.id} - {ticket.title}

**Acceptance Criteria:**
"""
        for criteria in ticket.acceptance_criteria:
            prompt += f"- {criteria}\n"
        
        prompt += "\n**Generated Files:**\n"
        for file_path in code_files.keys():
            prompt += f"- {file_path}\n"
        
        prompt += "\n\nGenerate test files that verify all acceptance criteria."
        prompt += "\nUse appropriate testing framework (pytest for Python, jest for JS, etc.)"
        
        return prompt
    
    def _extract_code_from_response(self, response: str) -> dict:
        """Extract code blocks from AI response.
        
        Returns:
            Dict mapping file paths to code content
        """
        import re
        
        code_files = {}
        
        # Match markdown code blocks with file paths
        # Pattern: ```language path/to/file.ext
        pattern = r'```(?:\w+)?\s+([^\n]+)\n(.*?)```'
        
        matches = re.findall(pattern, response, re.DOTALL)
        
        for file_path, code_content in matches:
            # Clean up file path
            file_path = file_path.strip()
            code_content = code_content.strip()
            
            if file_path and code_content:
                code_files[file_path] = code_content
        
        return code_files
    
    def _write_file(self, file_path: str, content: str) -> None:
        """Write content to file, creating directories if needed."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w') as f:
            f.write(content)
    
    def _log(self, message: str, ticket_id: Optional[str] = None, level: str = "info", **metadata) -> None:
        """Log a message."""
        if self.logger:
            self.logger.log(message, ticket_id=ticket_id, level=level, **metadata)
        else:
            # Fallback to print
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {message}")
    
    def _notify(self, title: str, message: str, priority: NotificationPriority = NotificationPriority.NORMAL) -> None:
        """Send a notification."""
        if self.notifier:
            self.notifier.send(title, message, priority=priority)
