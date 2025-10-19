"""
LLM Manager - Unified interface for managing multiple LLM providers
Provides abstraction layer for easy model switching
"""
import os
from typing import Optional, Dict, Any, List
from enum import Enum
from dotenv import load_dotenv

from .gemini_client import GeminiClient
from .openai_client import OpenAIClient


class ModelProvider(Enum):
    """Enum for supported LLM providers"""
    GEMINI = "gemini"
    OPENAI = "openai"


class LLMManager:
    """
    Unified interface for managing multiple LLM providers
    Handles model selection, fallback, and error handling
    """
    
    def __init__(
        self,
        primary_provider: ModelProvider = ModelProvider.GEMINI,
        fallback_provider: Optional[ModelProvider] = None,
        gemini_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None,
        gemini_model: str = "gemini-pro",
        openai_model: str = "gpt-3.5-turbo"
    ):
        """
        Initialize LLM Manager
        
        Args:
            primary_provider: Primary LLM provider to use
            fallback_provider: Fallback provider if primary fails
            gemini_api_key: Gemini API key (reads from env if None)
            openai_api_key: OpenAI API key (reads from env if None)
            gemini_model: Gemini model name
            openai_model: OpenAI model name
        """
        load_dotenv()
        
        self.primary_provider = primary_provider
        self.fallback_provider = fallback_provider
        
        # Initialize clients
        self.clients = {}
        
        # Initialize Gemini if key available
        try:
            self.clients[ModelProvider.GEMINI] = GeminiClient(
                api_key=gemini_api_key,
                model_name=gemini_model
            )
        except Exception as e:
            print(f"Warning: Could not initialize Gemini client: {e}")
        
        # Initialize OpenAI if key available
        try:
            self.clients[ModelProvider.OPENAI] = OpenAIClient(
                api_key=openai_api_key,
                model_name=openai_model
            )
        except Exception as e:
            print(f"Warning: Could not initialize OpenAI client: {e}")
        
        if not self.clients:
            raise ValueError("No LLM providers could be initialized. Check API keys.")
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        provider: Optional[ModelProvider] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate response using specified or primary provider with fallback
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            provider: Override primary provider
            conversation_history: Previous conversation (for OpenAI)
            
        Returns:
            Dict with response and metadata
        """
        # Determine which provider to use
        target_provider = provider or self.primary_provider
        
        # Try primary provider
        if target_provider in self.clients:
            client = self.clients[target_provider]
            
            # Call appropriate client
            if target_provider == ModelProvider.OPENAI:
                result = client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_history=conversation_history
                )
            else:  # Gemini
                result = client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_history=conversation_history  # Now Gemini also gets history!
                )
            
            # If successful, return
            if not result["error"]:
                result["provider"] = target_provider.value
                return result
            
            # If error and no fallback, return error
            if not self.fallback_provider:
                result["provider"] = target_provider.value
                return result
            
            # Try fallback
            print(f"Primary provider ({target_provider.value}) failed, trying fallback...")
        
        # Try fallback provider
        if self.fallback_provider and self.fallback_provider in self.clients:
            fallback_client = self.clients[self.fallback_provider]
            
            if self.fallback_provider == ModelProvider.OPENAI:
                result = fallback_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_history=conversation_history
                )
            else:  # Gemini
                result = fallback_client.generate_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    conversation_history=conversation_history  # Fallback also gets history!
                )
            
            result["provider"] = self.fallback_provider.value
            result["used_fallback"] = True
            return result
        
        # All providers failed
        return {
            "response": None,
            "model": "none",
            "provider": "none",
            "error": True,
            "error_message": "All providers failed or unavailable",
            "finish_reason": "ALL_FAILED"
        }
    
    def generate_streaming_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        provider: Optional[ModelProvider] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ):
        """
        Generate streaming response
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Temperature for generation
            provider: Override primary provider
            conversation_history: Previous conversation (for OpenAI)
            
        Yields:
            Chunks of text as they are generated
        """
        target_provider = provider or self.primary_provider
        
        if target_provider not in self.clients:
            yield "[Error: Provider not available]"
            return
        
        client = self.clients[target_provider]
        
        try:
            if target_provider == ModelProvider.OPENAI:
                for chunk in client.generate_streaming_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    conversation_history=conversation_history
                ):
                    yield chunk
            else:  # Gemini
                for chunk in client.generate_streaming_response(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature
                ):
                    yield chunk
        except Exception as e:
            yield f"\n\n[Error: {str(e)}]"
    
    def get_available_providers(self) -> List[str]:
        """
        Get list of available providers
        
        Returns:
            List of provider names
        """
        return [provider.value for provider in self.clients.keys()]
    
    def test_provider(self, provider: ModelProvider) -> bool:
        """
        Test if a provider is working
        
        Args:
            provider: Provider to test
            
        Returns:
            True if provider is working, False otherwise
        """
        if provider not in self.clients:
            return False
        
        return self.clients[provider].test_connection()
    
    def test_all_providers(self) -> Dict[str, bool]:
        """
        Test all available providers
        
        Returns:
            Dict mapping provider names to their status
        """
        results = {}
        for provider in self.clients.keys():
            results[provider.value] = self.test_provider(provider)
        return results
    
    @staticmethod
    def from_env() -> "LLMManager":
        """
        Create LLMManager from environment variables
        
        Environment variables:
            - ACTIVE_MODEL: 'gemini' or 'openai'
            - GEMINI_API_KEY: Gemini API key
            - OPENAI_API_KEY: OpenAI API key
            - GEMINI_MODEL: Gemini model name (default: gemini-pro)
            - OPENAI_MODEL: OpenAI model name (default: gpt-3.5-turbo)
            
        Returns:
            Configured LLMManager instance
        """
        load_dotenv()
        
        active_model = os.getenv("ACTIVE_MODEL", "gemini").lower()
        
        # Determine primary and fallback providers
        # Check for Gemini key (try both GEMINI_API_KEY and GOOGLE_API_KEY)
        has_gemini_key = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
        has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
        
        if active_model == "openai":
            primary = ModelProvider.OPENAI
            fallback = ModelProvider.GEMINI if has_gemini_key else None
        else:  # default to gemini
            primary = ModelProvider.GEMINI
            fallback = ModelProvider.OPENAI if has_openai_key else None
        
        return LLMManager(
            primary_provider=primary,
            fallback_provider=fallback,
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-pro"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        )
