"""
Model Configuration - Auto-detect provider and create appropriate client

Supports multiple API providers:
- Fireworks AI (OpenAI-compatible)
- OpenAI (GPT-4, etc.)
- Anthropic (Claude models)

Model name patterns:
- "accounts/fireworks/models/..." -> Fireworks
- "gpt-4..." -> OpenAI
- "claude-..." -> Anthropic
- Custom format: "provider:model_name" (e.g., "openai:gpt-4-turbo")
"""

import os
from openai import OpenAI

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class ModelConfig:
    """Configuration for a model including provider and API details."""

    # Provider endpoints
    PROVIDERS = {
        "fireworks": "https://api.fireworks.ai/inference/v1",
        "openai": None,  # Uses default OpenAI endpoint
        "anthropic": None  # Uses Anthropic client
    }

    # API key environment variables
    API_KEYS = {
        "fireworks": "FIREWORKS_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY"
    }

    # Cost per token (input, output) in USD per million tokens
    COSTS = {
        # Fireworks models
        "accounts/fireworks/models/deepseek-r1-basic": (0.40, 2.00),
        "accounts/fireworks/models/deepseek-v3": (0.55, 2.19),
        "accounts/fireworks/models/kimi-k2-instruct-0905": (0.40, 0.40),
        "accounts/fireworks/models/llama-v3p3-70b-instruct": (0.90, 0.90),
        "accounts/fireworks/models/qwen3-235b-a22b-thinking-2507": (1.20, 1.20),
        "accounts/fireworks/models/qwen3-30b-a3b": (0.40, 0.40),
        "accounts/fireworks/models/glm-4p5-air": (0.20, 0.20),
        "accounts/fireworks/models/gpt-oss-20b": (0.30, 0.30),
        "accounts/fireworks/models/gpt-oss-120b": (0.80, 0.80),

        # OpenAI models
        "gpt-4-turbo": (10.00, 30.00),
        "gpt-4-turbo-preview": (10.00, 30.00),
        "gpt-4o": (2.50, 10.00),
        "gpt-4o-mini": (0.15, 0.60),

        # Anthropic models
        "claude-3-5-sonnet-20241022": (3.00, 15.00),
        "claude-3-5-haiku-20241022": (0.80, 4.00),
        "claude-3-opus-20240229": (15.00, 75.00),
    }

    def __init__(self, model_spec):
        """
        Initialize model configuration.

        Args:
            model_spec: Model specification, can be:
                - Full path: "accounts/fireworks/models/deepseek-r1-basic"
                - Model name: "gpt-4-turbo", "claude-3-5-sonnet-20241022"
                - Provider:model: "openai:gpt-4-turbo", "fireworks:deepseek-v3"
        """
        self.original_spec = model_spec
        self.provider = None
        self.model_name = None
        self.base_url = None
        self.api_key = None
        self.client = None
        self.client_type = None  # "openai" or "anthropic"

        self._parse_model_spec(model_spec)
        self._create_client()

    def _parse_model_spec(self, model_spec):
        """Parse model specification and determine provider."""

        # Check for explicit provider:model format
        if ':' in model_spec and not model_spec.startswith('accounts/'):
            provider, model_name = model_spec.split(':', 1)
            self.provider = provider.lower()
            self.model_name = model_name
            return

        # Auto-detect provider from model name
        if model_spec.startswith('accounts/fireworks/'):
            self.provider = "fireworks"
            self.model_name = model_spec
        elif model_spec.startswith('gpt-'):
            self.provider = "openai"
            self.model_name = model_spec
        elif model_spec.startswith('claude-'):
            self.provider = "anthropic"
            self.model_name = model_spec
        else:
            # Try to infer from available API keys and model name patterns
            # Default to fireworks if it has accounts/ prefix
            if '/' in model_spec:
                self.provider = "fireworks"
                # Convert short name to full path if needed
                if not model_spec.startswith('accounts/'):
                    self.model_name = f"accounts/fireworks/models/{model_spec}"
                else:
                    self.model_name = model_spec
            else:
                # Unknown format - try fireworks as default
                self.provider = "fireworks"
                self.model_name = f"accounts/fireworks/models/{model_spec}"

    def _create_client(self):
        """Create the appropriate API client."""

        # Get API key
        api_key_var = self.API_KEYS.get(self.provider)
        if not api_key_var:
            raise ValueError(f"Unknown provider: {self.provider}")

        self.api_key = os.environ.get(api_key_var)
        if not self.api_key:
            raise ValueError(f"API key not found: {api_key_var} environment variable not set")

        # Create client based on provider
        if self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.client_type = "anthropic"
        else:
            # Fireworks and OpenAI both use OpenAI-compatible API
            self.base_url = self.PROVIDERS.get(self.provider)
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            self.client_type = "openai"

    def get_cost_per_token(self):
        """Get cost per token for this model (input, output)."""
        # Try exact match first
        if self.model_name in self.COSTS:
            return self.COSTS[self.model_name]

        # Try provider defaults
        provider_defaults = {
            "fireworks": (0.50, 1.00),  # Conservative default
            "openai": (5.00, 15.00),
            "anthropic": (3.00, 15.00)
        }
        return provider_defaults.get(self.provider, (1.00, 3.00))

    def __str__(self):
        return f"{self.provider}:{self.model_name}"

    def __repr__(self):
        return f"ModelConfig(provider={self.provider}, model={self.model_name})"


def create_model_config(model_spec):
    """
    Convenience function to create a ModelConfig.

    Args:
        model_spec: Model specification string

    Returns:
        ModelConfig instance
    """
    return ModelConfig(model_spec)
