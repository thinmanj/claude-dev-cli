"""Project-level configuration for automated ticket execution.

Allows per-project customization of commit strategies, branch strategies,
environments, review gates, and notification preferences.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from enum import Enum


class CommitStrategy(Enum):
    """Strategy for committing changes."""
    SINGLE = "single"  # One commit per ticket
    ATOMIC = "atomic"  # One commit per file
    FEATURE = "feature"  # Group related changes
    DISABLED = "disabled"  # No auto-commit


class BranchStrategy(Enum):
    """Strategy for creating branches."""
    MAIN = "main"  # Work directly on main branch
    TICKET = "ticket"  # Create branch per ticket (e.g., feature/TASK-123)
    FEATURE = "feature"  # Create feature branches
    DISABLED = "disabled"  # No branch creation


class Environment(Enum):
    """Execution environment."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    LOCAL = "local"


@dataclass
class ReviewGates:
    """Review gate configuration."""
    require_tests: bool = True
    require_linting: bool = False
    require_type_checking: bool = False
    require_approval: bool = False
    run_ci: bool = False
    
    def to_dict(self) -> Dict[str, bool]:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, bool]) -> 'ReviewGates':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class ProjectConfig:
    """Project-level configuration for ticket execution."""
    
    # Project identification
    project_name: str
    project_root: Path
    
    # Execution strategies
    commit_strategy: CommitStrategy = CommitStrategy.SINGLE
    branch_strategy: BranchStrategy = BranchStrategy.MAIN
    environment: Environment = Environment.DEVELOPMENT
    
    # Review gates
    review_gates: ReviewGates = field(default_factory=ReviewGates)
    
    # Automation settings
    auto_commit: bool = False
    auto_push: bool = False
    auto_pr: bool = False
    gather_context: bool = True
    
    # Notification settings
    enable_notifications: bool = False
    notification_topic: Optional[str] = None
    notification_priorities: List[str] = field(default_factory=lambda: ["high", "critical"])
    
    # API/Model settings
    api_config: Optional[str] = None
    model: Optional[str] = None
    
    # Ticket backend
    ticket_backend: str = "markdown"
    ticket_backend_config: Dict[str, Any] = field(default_factory=dict)
    
    # Testing
    test_command: Optional[str] = None  # e.g., "pytest tests/"
    lint_command: Optional[str] = None  # e.g., "ruff check ."
    typecheck_command: Optional[str] = None  # e.g., "mypy src/"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        # Convert enums to strings
        data['commit_strategy'] = self.commit_strategy.value
        data['branch_strategy'] = self.branch_strategy.value
        data['environment'] = self.environment.value
        # Convert Path to string
        data['project_root'] = str(self.project_root)
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectConfig':
        """Create from dictionary."""
        # Convert string enums back
        if 'commit_strategy' in data:
            data['commit_strategy'] = CommitStrategy(data['commit_strategy'])
        if 'branch_strategy' in data:
            data['branch_strategy'] = BranchStrategy(data['branch_strategy'])
        if 'environment' in data:
            data['environment'] = Environment(data['environment'])
        # Convert string path back
        if 'project_root' in data:
            data['project_root'] = Path(data['project_root'])
        # Convert review_gates
        if 'review_gates' in data and isinstance(data['review_gates'], dict):
            data['review_gates'] = ReviewGates.from_dict(data['review_gates'])
        
        return cls(**data)
    
    def save(self, path: Optional[Path] = None) -> None:
        """Save configuration to file.
        
        Args:
            path: Path to save to (default: .cdc-project.json in project root)
        """
        if path is None:
            path = self.project_root / '.cdc-project.json'
        
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, path: Optional[Path] = None, project_root: Optional[Path] = None) -> Optional['ProjectConfig']:
        """Load configuration from file.
        
        Args:
            path: Path to load from (default: search from current dir upward)
            project_root: Starting directory for search
            
        Returns:
            ProjectConfig if found, None otherwise
        """
        if path is None:
            # Search upward from project_root (or cwd) for .cdc-project.json
            search_dir = project_root or Path.cwd()
            
            # Search up to 10 levels
            for _ in range(10):
                config_path = search_dir / '.cdc-project.json'
                if config_path.exists():
                    path = config_path
                    break
                
                # Move up one directory
                parent = search_dir.parent
                if parent == search_dir:  # Reached root
                    break
                search_dir = parent
        
        if path is None or not path.exists():
            return None
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    @classmethod
    def create_default(cls, project_name: str, project_root: Optional[Path] = None) -> 'ProjectConfig':
        """Create a default configuration.
        
        Args:
            project_name: Name of the project
            project_root: Root directory (default: current directory)
            
        Returns:
            New ProjectConfig with default settings
        """
        if project_root is None:
            project_root = Path.cwd()
        
        return cls(
            project_name=project_name,
            project_root=project_root,
            commit_strategy=CommitStrategy.SINGLE,
            branch_strategy=BranchStrategy.MAIN,
            environment=Environment.DEVELOPMENT,
            review_gates=ReviewGates(
                require_tests=True,
                require_linting=False,
                require_type_checking=False,
                require_approval=False,
                run_ci=False
            ),
            auto_commit=False,
            auto_push=False,
            auto_pr=False,
            gather_context=True,
            enable_notifications=False
        )


class ProjectConfigManager:
    """Manager for project configurations."""
    
    @staticmethod
    def init(project_name: str, project_root: Optional[Path] = None, **kwargs) -> ProjectConfig:
        """Initialize a new project configuration.
        
        Args:
            project_name: Name of the project
            project_root: Root directory
            **kwargs: Additional config overrides
            
        Returns:
            New ProjectConfig
        """
        config = ProjectConfig.create_default(project_name, project_root)
        
        # Apply any overrides
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        return config
    
    @staticmethod
    def get_or_create(project_root: Optional[Path] = None) -> ProjectConfig:
        """Get existing config or create default.
        
        Args:
            project_root: Root directory to search from
            
        Returns:
            Existing or new ProjectConfig
        """
        config = ProjectConfig.load(project_root=project_root)
        
        if config is None:
            # Create default config
            root = project_root or Path.cwd()
            project_name = root.name
            config = ProjectConfig.create_default(project_name, root)
        
        return config
    
    @staticmethod
    def update(config: ProjectConfig, **kwargs) -> ProjectConfig:
        """Update configuration with new values.
        
        Args:
            config: Existing configuration
            **kwargs: Fields to update
            
        Returns:
            Updated configuration
        """
        for key, value in kwargs.items():
            if hasattr(config, key):
                # Handle enum conversions
                if key == 'commit_strategy' and isinstance(value, str):
                    value = CommitStrategy(value)
                elif key == 'branch_strategy' and isinstance(value, str):
                    value = BranchStrategy(value)
                elif key == 'environment' and isinstance(value, str):
                    value = Environment(value)
                
                setattr(config, key, value)
        
        return config
