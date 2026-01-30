"""Factory for creating AI provider instances."""

from typing import Any

from claude_dev_cli.providers.base import AIProvider, ProviderError
from claude_dev_cli.providers.anthropic import AnthropicProvider


class ProviderFactory:
    """Factory for creating AI provider instances based on configuration."""
    
    # Registry of available providers
    _PROVIDERS = {
        "anthropic": AnthropicProvider,
        # Future providers:
        # "openai": OpenAIProvider,      # v0.15.0
        # "ollama": OllamaProvider,      # v0.16.0
        # "lmstudio": LMStudioProvider,  # v0.16.0
    }
    
    @staticmethod
    def create(config: Any) -> AIProvider:
        """Create a provider instance based on configuration.
        
        Args:
            config: Provider configuration (ProviderConfig or APIConfig)
                    Must have 'provider' attribute or defaults to 'anthropic'
                    
        Returns:
            AIProvider instance
            
        Raises:
            ProviderError: If provider type is unknown or unavailable
        """
        # Determine provider type
        provider_type = getattr(config, 'provider', 'anthropic')
        
        # Look up provider class
        provider_class = ProviderFactory._PROVIDERS.get(provider_type.lower())
        
        if not provider_class:
            available = ", ".join(ProviderFactory._PROVIDERS.keys())
            raise ProviderError(
                f"Unknown provider: {provider_type}. "
                f"Available providers: {available}"
            )
        
        # Instantiate and return provider
        try:
            return provider_class(config)
        except Exception as e:
            raise ProviderError(
                f"Failed to initialize {provider_type} provider: {e}"
            )
    
    @staticmethod
    def list_providers() -> list[str]:
        """List available provider types.
        
        Returns:
            List of provider type names (e.g., ['anthropic', 'openai'])
        """
        return list(ProviderFactory._PROVIDERS.keys())
    
    @staticmethod
    def is_provider_available(provider_type: str) -> bool:
        """Check if a provider type is available.
        
        Args:
            provider_type: Provider type name (e.g., 'anthropic', 'openai')
            
        Returns:
            True if provider is available, False otherwise
        """
        return provider_type.lower() in ProviderFactory._PROVIDERS
