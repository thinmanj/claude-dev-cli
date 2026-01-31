"""Bug reporting and triage system for claude-dev-cli.

Handles bug reports independently from main project workflow,
with automatic triage, priority assignment, and categorization.
"""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from claude_dev_cli.tickets.backend import TicketBackend, Ticket
from claude_dev_cli.core import ClaudeClient
from claude_dev_cli.notifications.notifier import Notifier, NotificationPriority


class BugSeverity(Enum):
    """Bug severity levels."""
    CRITICAL = "critical"  # System down, data loss, security breach
    HIGH = "high"  # Major functionality broken
    MEDIUM = "medium"  # Functionality impaired but workaround exists
    LOW = "low"  # Minor issue, cosmetic
    TRIVIAL = "trivial"  # Typos, UI inconsistencies


class BugCategory(Enum):
    """Bug categories for classification."""
    CRASH = "crash"  # Application crashes
    DATA_LOSS = "data-loss"  # Data corruption or loss
    SECURITY = "security"  # Security vulnerabilities
    PERFORMANCE = "performance"  # Performance issues
    UI_UX = "ui-ux"  # User interface/experience issues
    INTEGRATION = "integration"  # Third-party integration issues
    FUNCTIONALITY = "functionality"  # Feature not working as expected
    DOCUMENTATION = "documentation"  # Documentation errors
    OTHER = "other"


@dataclass
class BugReport:
    """Structured bug report."""
    id: Optional[str]
    title: str
    description: str
    
    # Reproduction information
    steps_to_reproduce: List[str]
    expected_behavior: str
    actual_behavior: str
    
    # Environment
    environment: Optional[str] = None  # production, staging, development
    version: Optional[str] = None
    platform: Optional[str] = None  # OS, browser, etc.
    
    # Classification (can be auto-assigned by triage)
    severity: Optional[BugSeverity] = None
    category: Optional[BugCategory] = None
    priority: Optional[str] = None  # critical, high, medium, low
    
    # Additional context
    stack_trace: Optional[str] = None
    logs: Optional[str] = None
    screenshots: List[str] = None
    related_tickets: List[str] = None
    
    # Metadata
    reporter: Optional[str] = None
    reported_at: Optional[datetime] = None
    triaged: bool = False
    assigned_to: Optional[str] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.screenshots is None:
            self.screenshots = []
        if self.related_tickets is None:
            self.related_tickets = []
        if self.reported_at is None:
            self.reported_at = datetime.now()


class BugTriageSystem:
    """AI-powered bug triage and classification system.
    
    Automatically:
    - Classifies bug severity based on description
    - Categorizes bugs
    - Suggests priority
    - Identifies duplicate bugs
    - Recommends assignment
    """
    
    def __init__(
        self,
        ticket_backend: TicketBackend,
        ai_client: Optional[ClaudeClient] = None,
        notifier: Optional[Notifier] = None
    ):
        """Initialize bug triage system.
        
        Args:
            ticket_backend: Ticket management backend
            ai_client: AI client for triage analysis
            notifier: Notification system for critical bugs
        """
        self.ticket_backend = ticket_backend
        self.ai_client = ai_client or ClaudeClient()
        self.notifier = notifier
    
    def submit_bug(self, bug_report: BugReport, auto_triage: bool = True) -> Ticket:
        """Submit a bug report and optionally auto-triage.
        
        Args:
            bug_report: Bug report to submit
            auto_triage: Whether to automatically triage
            
        Returns:
            Created ticket
        """
        # Auto-triage if requested
        if auto_triage and not bug_report.triaged:
            bug_report = self.triage_bug(bug_report)
        
        # Create ticket in backend
        ticket = self.ticket_backend.create_task(
            story_id=None,  # Bugs are independent
            title=f"[BUG] {bug_report.title}",
            description=self._format_bug_description(bug_report),
            ticket_type="bug",
            priority=bug_report.priority or "medium",
            labels=self._get_bug_labels(bug_report),
            assignee=bug_report.assigned_to,
            requirements=bug_report.steps_to_reproduce,
            acceptance_criteria=[
                f"Expected: {bug_report.expected_behavior}",
                f"Actual: {bug_report.actual_behavior}"
            ]
        )
        
        bug_report.id = ticket.id
        
        # Add detailed comment with stack trace/logs
        if bug_report.stack_trace or bug_report.logs:
            self._add_technical_details(ticket.id, bug_report)
        
        # Notify if critical/high severity
        if bug_report.severity in [BugSeverity.CRITICAL, BugSeverity.HIGH]:
            self._notify_critical_bug(bug_report)
        
        return ticket
    
    def triage_bug(self, bug_report: BugReport) -> BugReport:
        """Use AI to automatically triage a bug report.
        
        Analyzes bug description and assigns:
        - Severity level
        - Category
        - Priority
        - Potential duplicates
        
        Args:
            bug_report: Bug report to triage
            
        Returns:
            Bug report with triage information added
        """
        triage_prompt = self._build_triage_prompt(bug_report)
        
        try:
            triage_response = self.ai_client.call(
                triage_prompt,
                system_prompt="You are an expert bug triage specialist. Analyze bugs and provide structured classification."
            )
            
            # Parse triage response and update bug report
            triage_data = self._parse_triage_response(triage_response)
            
            bug_report.severity = triage_data.get('severity')
            bug_report.category = triage_data.get('category')
            bug_report.priority = triage_data.get('priority')
            bug_report.triaged = True
            
        except Exception as e:
            # Fallback to manual triage
            print(f"Auto-triage failed: {e}. Using fallback classification.")
            bug_report = self._fallback_triage(bug_report)
        
        return bug_report
    
    def find_duplicates(self, bug_report: BugReport, threshold: float = 0.7) -> List[str]:
        """Find potential duplicate bug reports.
        
        Args:
            bug_report: Bug to check for duplicates
            threshold: Similarity threshold (0-1)
            
        Returns:
            List of ticket IDs that might be duplicates
        """
        # Get all existing bug tickets
        existing_bugs = self.ticket_backend.list_tickets(
            status="open"
        )
        
        duplicates = []
        
        # Simple keyword-based duplicate detection
        # Could be enhanced with semantic similarity
        bug_keywords = set(bug_report.title.lower().split())
        
        for ticket in existing_bugs:
            if ticket.ticket_type != "bug":
                continue
            
            ticket_keywords = set(ticket.title.lower().split())
            similarity = len(bug_keywords & ticket_keywords) / len(bug_keywords | ticket_keywords)
            
            if similarity >= threshold:
                duplicates.append(ticket.id)
        
        return duplicates
    
    def assign_bug(self, ticket_id: str, assignee: str, reason: Optional[str] = None) -> bool:
        """Assign a bug to a developer.
        
        Args:
            ticket_id: Bug ticket ID
            assignee: Developer to assign to
            reason: Optional reason for assignment
            
        Returns:
            True if successful
        """
        try:
            self.ticket_backend.update_ticket(ticket_id, assignee=assignee)
            
            if reason:
                self.ticket_backend.add_comment(
                    ticket_id,
                    f"Assigned to {assignee}\nReason: {reason}",
                    author="bug-triage-system"
                )
            
            return True
        except Exception:
            return False
    
    def escalate_bug(self, ticket_id: str, reason: str) -> bool:
        """Escalate a bug to higher priority.
        
        Args:
            ticket_id: Bug ticket ID
            reason: Escalation reason
            
        Returns:
            True if successful
        """
        try:
            # Increase priority
            ticket = self.ticket_backend.fetch_ticket(ticket_id)
            
            priority_escalation = {
                "low": "medium",
                "medium": "high",
                "high": "critical"
            }
            
            new_priority = priority_escalation.get(ticket.priority, "critical")
            
            self.ticket_backend.update_ticket(ticket_id, priority=new_priority)
            self.ticket_backend.add_comment(
                ticket_id,
                f"🚨 Bug escalated to {new_priority} priority\nReason: {reason}",
                author="bug-triage-system"
            )
            
            # Notify about escalation
            if self.notifier:
                self.notifier.send(
                    f"Bug Escalated: {ticket_id}",
                    f"Priority: {new_priority}\nReason: {reason}",
                    priority=NotificationPriority.URGENT
                )
            
            return True
        except Exception:
            return False
    
    def _build_triage_prompt(self, bug_report: BugReport) -> str:
        """Build prompt for AI triage analysis."""
        prompt = f"""Analyze this bug report and provide triage classification.

**Bug Title:** {bug_report.title}

**Description:**
{bug_report.description}

**Steps to Reproduce:**
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(bug_report.steps_to_reproduce))}

**Expected Behavior:** {bug_report.expected_behavior}
**Actual Behavior:** {bug_report.actual_behavior}

"""
        
        if bug_report.stack_trace:
            prompt += f"\n**Stack Trace:**\n```\n{bug_report.stack_trace[:500]}\n```\n"
        
        if bug_report.environment:
            prompt += f"\n**Environment:** {bug_report.environment}"
        
        prompt += """

Provide triage analysis in this format:

SEVERITY: [critical/high/medium/low/trivial]
CATEGORY: [crash/data-loss/security/performance/ui-ux/integration/functionality/documentation/other]
PRIORITY: [critical/high/medium/low]
REASONING: [Brief explanation of classification]
SUGGESTED_ACTION: [Immediate action needed, if any]
"""
        
        return prompt
    
    def _parse_triage_response(self, response: str) -> Dict[str, Any]:
        """Parse AI triage response."""
        import re
        
        result = {}
        
        # Extract severity
        severity_match = re.search(r'SEVERITY:\s*(\w+)', response, re.IGNORECASE)
        if severity_match:
            try:
                result['severity'] = BugSeverity(severity_match.group(1).lower())
            except ValueError:
                result['severity'] = BugSeverity.MEDIUM
        
        # Extract category
        category_match = re.search(r'CATEGORY:\s*([\w-]+)', response, re.IGNORECASE)
        if category_match:
            try:
                result['category'] = BugCategory(category_match.group(1).lower())
            except ValueError:
                result['category'] = BugCategory.OTHER
        
        # Extract priority
        priority_match = re.search(r'PRIORITY:\s*(\w+)', response, re.IGNORECASE)
        if priority_match:
            result['priority'] = priority_match.group(1).lower()
        
        return result
    
    def _fallback_triage(self, bug_report: BugReport) -> BugReport:
        """Fallback triage based on keywords."""
        title_lower = bug_report.title.lower()
        desc_lower = bug_report.description.lower()
        
        # Check for critical keywords
        critical_keywords = ['crash', 'data loss', 'security', 'breach', 'exploit', 'down']
        high_keywords = ['broken', 'error', 'fail', 'cannot', "doesn't work"]
        
        if any(kw in title_lower or kw in desc_lower for kw in critical_keywords):
            bug_report.severity = BugSeverity.CRITICAL
            bug_report.priority = "critical"
        elif any(kw in title_lower or kw in desc_lower for kw in high_keywords):
            bug_report.severity = BugSeverity.HIGH
            bug_report.priority = "high"
        else:
            bug_report.severity = BugSeverity.MEDIUM
            bug_report.priority = "medium"
        
        # Categorize
        if 'crash' in title_lower or 'crash' in desc_lower:
            bug_report.category = BugCategory.CRASH
        elif 'security' in title_lower or 'security' in desc_lower:
            bug_report.category = BugCategory.SECURITY
        elif 'slow' in title_lower or 'performance' in desc_lower:
            bug_report.category = BugCategory.PERFORMANCE
        else:
            bug_report.category = BugCategory.FUNCTIONALITY
        
        bug_report.triaged = True
        return bug_report
    
    def _format_bug_description(self, bug_report: BugReport) -> str:
        """Format bug report into ticket description."""
        desc = f"{bug_report.description}\n\n"
        desc += "## Reproduction Steps\n"
        for i, step in enumerate(bug_report.steps_to_reproduce, 1):
            desc += f"{i}. {step}\n"
        
        desc += f"\n## Expected Behavior\n{bug_report.expected_behavior}\n"
        desc += f"\n## Actual Behavior\n{bug_report.actual_behavior}\n"
        
        if bug_report.environment:
            desc += f"\n## Environment\n{bug_report.environment}"
        
        if bug_report.version:
            desc += f"\nVersion: {bug_report.version}"
        
        if bug_report.platform:
            desc += f"\nPlatform: {bug_report.platform}"
        
        return desc
    
    def _get_bug_labels(self, bug_report: BugReport) -> List[str]:
        """Generate labels for bug ticket."""
        labels = ["bug"]
        
        if bug_report.severity:
            labels.append(f"severity-{bug_report.severity.value}")
        
        if bug_report.category:
            labels.append(f"category-{bug_report.category.value}")
        
        if bug_report.environment:
            labels.append(f"env-{bug_report.environment}")
        
        return labels
    
    def _add_technical_details(self, ticket_id: str, bug_report: BugReport) -> None:
        """Add technical details as comment."""
        details = "## Technical Details\n\n"
        
        if bug_report.stack_trace:
            details += "### Stack Trace\n```\n"
            details += bug_report.stack_trace
            details += "\n```\n\n"
        
        if bug_report.logs:
            details += "### Logs\n```\n"
            details += bug_report.logs
            details += "\n```\n"
        
        self.ticket_backend.add_comment(ticket_id, details, author="bug-reporter")
    
    def _notify_critical_bug(self, bug_report: BugReport) -> None:
        """Send notification for critical/high severity bugs."""
        if not self.notifier:
            return
        
        severity_emoji = {
            BugSeverity.CRITICAL: "🚨",
            BugSeverity.HIGH: "⚠️"
        }
        
        emoji = severity_emoji.get(bug_report.severity, "🐛")
        
        self.notifier.send(
            f"{emoji} {bug_report.severity.value.upper()} Bug Reported",
            f"Title: {bug_report.title}\n"
            f"Category: {bug_report.category.value if bug_report.category else 'unknown'}\n"
            f"Environment: {bug_report.environment or 'unknown'}",
            priority=NotificationPriority.URGENT if bug_report.severity == BugSeverity.CRITICAL else NotificationPriority.HIGH,
            tags=["bug", "alert"]
        )
