"""Intelligent context gathering for ticket execution.

Pre-processes tickets to gather relevant context from the codebase,
including similar code, dependencies, framework patterns, and project structure.
This context helps the AI generate better, more consistent implementations.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict

from claude_dev_cli.tickets.backend import Ticket
from claude_dev_cli.core import ClaudeClient


@dataclass
class CodeContext:
    """Context gathered from existing codebase."""
    
    # Project structure
    project_root: Path
    language: str
    framework: Optional[str] = None
    
    # Dependencies
    dependencies: List[str] = field(default_factory=list)
    installed_packages: Dict[str, str] = field(default_factory=dict)  # name: version
    
    # Similar code
    similar_files: List[Dict[str, Any]] = field(default_factory=list)  # path, similarity, purpose
    similar_functions: List[Dict[str, Any]] = field(default_factory=list)  # name, file, signature
    similar_patterns: List[str] = field(default_factory=list)  # patterns found in codebase
    
    # Project conventions
    naming_conventions: Dict[str, str] = field(default_factory=dict)  # type: pattern
    directory_structure: Dict[str, List[str]] = field(default_factory=dict)  # purpose: paths
    common_imports: List[str] = field(default_factory=list)
    
    # Related files
    related_models: List[str] = field(default_factory=list)
    related_views: List[str] = field(default_factory=list)
    related_controllers: List[str] = field(default_factory=list)
    related_tests: List[str] = field(default_factory=list)
    
    # Configuration
    config_files: List[str] = field(default_factory=list)
    env_variables: List[str] = field(default_factory=list)
    
    def format_for_prompt(self) -> str:
        """Format context for AI prompt."""
        sections = []
        
        sections.append(f"## Project Context\n")
        sections.append(f"**Language:** {self.language}")
        if self.framework:
            sections.append(f"**Framework:** {self.framework}")
        sections.append(f"**Root:** {self.project_root}\n")
        
        if self.dependencies:
            sections.append(f"\n## Dependencies ({len(self.dependencies)})")
            for dep in self.dependencies[:20]:  # Limit to 20
                version = self.installed_packages.get(dep, "unknown")
                sections.append(f"- {dep} ({version})")
        
        if self.directory_structure:
            sections.append(f"\n## Project Structure")
            for purpose, paths in self.directory_structure.items():
                sections.append(f"**{purpose}:** {', '.join(paths[:5])}")
        
        if self.naming_conventions:
            sections.append(f"\n## Naming Conventions")
            for type_name, pattern in self.naming_conventions.items():
                sections.append(f"- {type_name}: {pattern}")
        
        if self.similar_files:
            sections.append(f"\n## Similar Existing Code")
            for file_info in self.similar_files[:5]:
                sections.append(f"- {file_info['path']}: {file_info['purpose']}")
        
        if self.similar_functions:
            sections.append(f"\n## Related Functions")
            for func in self.similar_functions[:10]:
                sections.append(f"- {func['name']} in {func['file']}")
        
        if self.common_imports:
            sections.append(f"\n## Common Imports")
            sections.append(", ".join(self.common_imports[:15]))
        
        if self.related_models or self.related_views or self.related_controllers:
            sections.append(f"\n## Related Files")
            if self.related_models:
                sections.append(f"Models: {', '.join(self.related_models[:5])}")
            if self.related_views:
                sections.append(f"Views: {', '.join(self.related_views[:5])}")
            if self.related_controllers:
                sections.append(f"Controllers: {', '.join(self.related_controllers[:5])}")
        
        return "\n".join(sections)


class TicketContextGatherer:
    """Gathers relevant context for ticket implementation.
    
    Analyzes the existing codebase to provide context that helps
    the AI generate better, more consistent code.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """Initialize context gatherer.
        
        Args:
            project_root: Root of the project (default: current directory)
        """
        self.project_root = project_root or Path.cwd()
        self._file_cache: Dict[str, str] = {}
        self._extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.go': 'Go',
            '.rs': 'Rust',
            '.java': 'Java',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.cpp': 'C++',
            '.c': 'C'
        }
    
    def gather_context(self, ticket: Ticket, ai_client: Optional[ClaudeClient] = None) -> CodeContext:
        """Gather all relevant context for implementing a ticket.
        
        Args:
            ticket: Ticket to gather context for
            ai_client: Optional AI client for semantic analysis
            
        Returns:
            CodeContext with all gathered information
        """
        context = CodeContext(project_root=self.project_root, language=self._detect_language())
        
        # Gather different types of context
        context.framework = self._detect_framework(context.language)
        context.dependencies = self._find_dependencies(context.language)
        context.installed_packages = self._get_installed_packages(context.language)
        context.directory_structure = self._analyze_directory_structure()
        context.naming_conventions = self._detect_naming_conventions(context.language)
        context.common_imports = self._find_common_imports(context.language)
        context.config_files = self._find_config_files()
        
        # Find similar code based on ticket description
        if ticket.description or ticket.title:
            search_terms = self._extract_search_terms(ticket)
            context.similar_files = self._find_similar_files(search_terms, context.language)
            context.similar_functions = self._find_similar_functions(search_terms, context.language)
            context.similar_patterns = self._find_patterns(search_terms)
        
        # Find related files based on ticket type
        if ticket.ticket_type in ['feature', 'bug', 'refactor']:
            context.related_models = self._find_models(context.language, context.framework)
            context.related_views = self._find_views(context.language, context.framework)
            context.related_controllers = self._find_controllers(context.language, context.framework)
            context.related_tests = self._find_tests(context.language)
        
        # Use AI for semantic similarity (optional)
        if ai_client:
            context = self._enhance_with_ai(context, ticket, ai_client)
        
        return context
    
    def _detect_language(self) -> str:
        """Detect primary programming language."""
        extensions_count = defaultdict(int)
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                ext = file_path.suffix.lower()
                if ext in self._extension_map:
                    extensions_count[ext] += 1
        
        if not extensions_count:
            return "Unknown"
        
        primary_ext = max(extensions_count, key=extensions_count.get)
        return self._extension_map.get(primary_ext, "Unknown")
    
    def _detect_framework(self, language: str) -> Optional[str]:
        """Detect framework being used."""
        framework_indicators = {
            'Python': {
                'Django': ['manage.py', 'settings.py', 'wsgi.py'],
                'Flask': ['app.py', 'wsgi.py', '__init__.py'],
                'FastAPI': ['main.py', 'app.py'],
            },
            'JavaScript': {
                'React': ['package.json'],  # Check for "react" in package.json
                'Vue': ['vue.config.js', 'package.json'],
                'Express': ['package.json'],  # Check for "express"
            },
            'TypeScript': {
                'Next.js': ['next.config.js', 'next.config.ts'],
                'NestJS': ['nest-cli.json'],
            },
            'Go': {
                'Gin': ['go.mod'],  # Check imports
                'Echo': ['go.mod'],
            },
            'Ruby': {
                'Rails': ['Gemfile', 'config.ru', 'app/'],
            }
        }
        
        if language not in framework_indicators:
            return None
        
        for framework, files in framework_indicators[language].items():
            if all((self.project_root / f).exists() or 
                   any(self.project_root.rglob(f)) for f in files):
                return framework
        
        return None
    
    def _find_dependencies(self, language: str) -> List[str]:
        """Find project dependencies."""
        dep_files = {
            'Python': ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile'],
            'JavaScript': ['package.json'],
            'TypeScript': ['package.json'],
            'Go': ['go.mod'],
            'Ruby': ['Gemfile'],
            'PHP': ['composer.json'],
            'Rust': ['Cargo.toml'],
            'Java': ['pom.xml', 'build.gradle'],
        }
        
        dependencies = []
        
        for dep_file in dep_files.get(language, []):
            file_path = self.project_root / dep_file
            if file_path.exists():
                deps = self._parse_dependency_file(file_path, language)
                dependencies.extend(deps)
        
        return list(set(dependencies))  # Remove duplicates
    
    def _parse_dependency_file(self, file_path: Path, language: str) -> List[str]:
        """Parse a dependency file to extract package names."""
        try:
            content = file_path.read_text()
            deps = []
            
            if file_path.name == 'requirements.txt':
                for line in content.splitlines():
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Extract package name (before ==, >=, etc.)
                        pkg = re.split(r'[=<>!]', line)[0].strip()
                        deps.append(pkg)
            
            elif file_path.name == 'package.json':
                import json
                data = json.loads(content)
                deps.extend(data.get('dependencies', {}).keys())
                deps.extend(data.get('devDependencies', {}).keys())
            
            elif file_path.name == 'pyproject.toml':
                # Simple parsing - look for dependencies section
                in_deps = False
                for line in content.splitlines():
                    if 'dependencies' in line:
                        in_deps = True
                    elif in_deps and '=' in line:
                        pkg = line.split('=')[0].strip(' "\'')
                        if pkg and not pkg.startswith('['):
                            deps.append(pkg)
                    elif in_deps and line.strip().startswith('['):
                        in_deps = False
            
            return deps
        
        except Exception:
            return []
    
    def _get_installed_packages(self, language: str) -> Dict[str, str]:
        """Get currently installed packages with versions."""
        # This would ideally check the actual environment
        # For now, return empty dict (can be enhanced later)
        return {}
    
    def _analyze_directory_structure(self) -> Dict[str, List[str]]:
        """Analyze project directory structure."""
        structure = defaultdict(list)
        
        common_patterns = {
            'models': ['models/', 'model/', 'entities/', 'domain/'],
            'views': ['views/', 'templates/', 'pages/'],
            'controllers': ['controllers/', 'handlers/', 'routes/'],
            'services': ['services/', 'business/', 'logic/'],
            'utils': ['utils/', 'helpers/', 'common/'],
            'tests': ['tests/', 'test/', '__tests__/', 'spec/'],
            'config': ['config/', 'settings/', 'conf/'],
            'static': ['static/', 'public/', 'assets/'],
        }
        
        for purpose, patterns in common_patterns.items():
            for pattern in patterns:
                paths = list(self.project_root.glob(f"**/{pattern}"))
                if paths:
                    structure[purpose].extend([str(p.relative_to(self.project_root)) for p in paths[:5]])
        
        return dict(structure)
    
    def _detect_naming_conventions(self, language: str) -> Dict[str, str]:
        """Detect naming conventions used in the project."""
        conventions = {}
        
        # Sample files to detect patterns
        sample_files = list(self.project_root.rglob('*.py' if language == 'Python' else '*'))[:50]
        
        # Detect function naming
        func_names = []
        class_names = []
        
        for file_path in sample_files:
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    content = file_path.read_text()
                    
                    # Extract function names
                    func_names.extend(re.findall(r'def\s+(\w+)\s*\(', content))
                    func_names.extend(re.findall(r'function\s+(\w+)\s*\(', content))
                    
                    # Extract class names
                    class_names.extend(re.findall(r'class\s+(\w+)', content))
                
                except Exception:
                    continue
        
        # Analyze patterns
        if func_names:
            if all('_' in name or name.islower() for name in func_names[:10]):
                conventions['functions'] = 'snake_case'
            elif all(name[0].islower() and any(c.isupper() for c in name[1:]) for name in func_names[:10] if len(name) > 1):
                conventions['functions'] = 'camelCase'
        
        if class_names:
            if all(name[0].isupper() for name in class_names[:10]):
                conventions['classes'] = 'PascalCase'
        
        return conventions
    
    def _find_common_imports(self, language: str) -> List[str]:
        """Find most commonly used imports."""
        import_counts = defaultdict(int)
        
        sample_files = list(self.project_root.rglob('*.py' if language == 'Python' else '*'))[:100]
        
        for file_path in sample_files:
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    content = file_path.read_text()
                    
                    if language == 'Python':
                        imports = re.findall(r'(?:from|import)\s+([\w.]+)', content)
                        for imp in imports:
                            import_counts[imp.split('.')[0]] += 1
                    
                except Exception:
                    continue
        
        # Return top 15 most common
        sorted_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)
        return [imp[0] for imp in sorted_imports[:15]]
    
    def _find_config_files(self) -> List[str]:
        """Find configuration files."""
        config_patterns = [
            'config.*', 'settings.*', '.env*', '*.config.*',
            'docker-compose.yml', 'Dockerfile', 'Makefile'
        ]
        
        config_files = []
        for pattern in config_patterns:
            config_files.extend(str(p.relative_to(self.project_root)) 
                              for p in self.project_root.glob(pattern))
        
        return config_files[:10]
    
    def _extract_search_terms(self, ticket: Ticket) -> List[str]:
        """Extract key search terms from ticket."""
        text = f"{ticket.title} {ticket.description}"
        
        # Extract important words (exclude common words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        return [w for w in words if w not in stop_words][:10]
    
    def _find_similar_files(self, search_terms: List[str], language: str) -> List[Dict[str, Any]]:
        """Find files with similar purpose."""
        similar = []
        
        ext = '.py' if language == 'Python' else '.*'
        files = list(self.project_root.rglob(f'*{ext}'))[:200]
        
        for file_path in files:
            if file_path.is_file() and not self._should_ignore(file_path):
                rel_path = str(file_path.relative_to(self.project_root))
                
                # Check if filename or path contains search terms
                matches = sum(1 for term in search_terms if term in rel_path.lower())
                
                if matches > 0:
                    similar.append({
                        'path': rel_path,
                        'similarity': matches,
                        'purpose': self._guess_file_purpose(file_path)
                    })
        
        # Sort by similarity
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar[:5]
    
    def _find_similar_functions(self, search_terms: List[str], language: str) -> List[Dict[str, Any]]:
        """Find functions with similar names or purposes."""
        functions = []
        
        ext = '.py' if language == 'Python' else '.*'
        files = list(self.project_root.rglob(f'*{ext}'))[:100]
        
        for file_path in files:
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    content = file_path.read_text()
                    
                    # Extract function definitions
                    func_matches = re.findall(r'def\s+(\w+)\s*\((.*?)\):', content)
                    
                    for func_name, params in func_matches:
                        if any(term in func_name.lower() for term in search_terms):
                            functions.append({
                                'name': func_name,
                                'file': str(file_path.relative_to(self.project_root)),
                                'signature': f"{func_name}({params})"
                            })
                
                except Exception:
                    continue
        
        return functions[:10]
    
    def _find_patterns(self, search_terms: List[str]) -> List[str]:
        """Find code patterns related to search terms."""
        # This could be enhanced with more sophisticated pattern detection
        patterns = []
        
        # Look for common patterns like decorators, base classes, etc.
        # For now, return empty (can be enhanced)
        
        return patterns
    
    def _find_models(self, language: str, framework: Optional[str]) -> List[str]:
        """Find model files."""
        return self._find_files_by_pattern(['models/', 'model/', 'entities/'], language)
    
    def _find_views(self, language: str, framework: Optional[str]) -> List[str]:
        """Find view/template files."""
        return self._find_files_by_pattern(['views/', 'templates/', 'pages/'], language)
    
    def _find_controllers(self, language: str, framework: Optional[str]) -> List[str]:
        """Find controller/handler files."""
        return self._find_files_by_pattern(['controllers/', 'handlers/', 'routes/'], language)
    
    def _find_tests(self, language: str) -> List[str]:
        """Find test files."""
        return self._find_files_by_pattern(['tests/', 'test/', '__tests__/'], language)
    
    def _find_files_by_pattern(self, patterns: List[str], language: str) -> List[str]:
        """Find files matching directory patterns."""
        files = []
        
        for pattern in patterns:
            paths = list(self.project_root.glob(f"**/{pattern}**"))
            files.extend(str(p.relative_to(self.project_root)) 
                        for p in paths if p.is_file())
        
        return files[:10]
    
    def _guess_file_purpose(self, file_path: Path) -> str:
        """Guess the purpose of a file from its path and content."""
        path_str = str(file_path).lower()
        
        if 'model' in path_str:
            return 'Data model'
        elif 'view' in path_str or 'template' in path_str:
            return 'View/Template'
        elif 'controller' in path_str or 'handler' in path_str:
            return 'Controller/Handler'
        elif 'service' in path_str:
            return 'Business logic'
        elif 'util' in path_str or 'helper' in path_str:
            return 'Utility functions'
        elif 'test' in path_str:
            return 'Tests'
        else:
            return 'General code'
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored."""
        ignore_patterns = [
            '.git', '__pycache__', 'node_modules', '.venv', 'venv',
            'dist', 'build', '.pytest_cache', '.mypy_cache', '.ruff_cache',
            '.tox', 'htmlcov', '.coverage', '*.pyc', '*.pyo', '*.egg-info'
        ]
        
        path_str = str(path)
        return any(pattern in path_str for pattern in ignore_patterns)
    
    def _enhance_with_ai(
        self,
        context: CodeContext,
        ticket: Ticket,
        ai_client: ClaudeClient
    ) -> CodeContext:
        """Use AI to enhance context with semantic understanding."""
        # Could use AI to:
        # 1. Identify most relevant files semantically
        # 2. Suggest architectural patterns
        # 3. Find non-obvious related code
        
        # For now, return as-is (can be enhanced later)
        return context
