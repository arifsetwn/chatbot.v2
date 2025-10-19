"""
OpenAI API Client Wrapper
Handles communication with OpenAI API (ChatGPT)
"""
import os
from typing import Optional, Dict, Any, List
from openai import OpenAI, OpenAIError, RateLimitError, APIError, APIConnectionError


class OpenAIClient:
    """
    Wrapper for OpenAI API with error handling and configuration
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key. If None, reads from environment
            model_name: Model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name
        
        # Default parameters
        self.default_temperature = 0.7
        self.default_max_tokens = 2048
        self.default_top_p = 0.95
    
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate response from OpenAI
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Override default temperature
            max_tokens: Override default max tokens
            conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
            
        Returns:
            Dict with 'response' (str), 'model' (str), 'error' (bool), 'error_message' (str)
        """
        try:
            # Build messages array
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user prompt
            messages.append({"role": "user", "content": prompt})
            
            # Set parameters
            temp = temperature if temperature is not None else self.default_temperature
            max_tok = max_tokens if max_tokens is not None else self.default_max_tokens
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temp,
                max_tokens=max_tok,
                top_p=self.default_top_p
            )
            
            # Extract response
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                finish_reason = response.choices[0].finish_reason
                
                return {
                    "response": content,
                    "model": self.model_name,
                    "error": False,
                    "error_message": None,
                    "finish_reason": finish_reason,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
            else:
                return {
                    "response": None,
                    "model": self.model_name,
                    "error": True,
                    "error_message": "No response generated",
                    "finish_reason": "NO_RESPONSE"
                }
        
        except RateLimitError as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"Rate limit exceeded: {str(e)}",
                "finish_reason": "RATE_LIMIT"
            }
        
        except APIConnectionError as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"Connection error: {str(e)}",
                "finish_reason": "CONNECTION_ERROR"
            }
        
        except APIError as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"API error: {str(e)}",
                "finish_reason": "API_ERROR"
            }
        
        except OpenAIError as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"OpenAI error: {str(e)}",
                "finish_reason": "OPENAI_ERROR"
            }
        
        except Exception as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"Unexpected error: {str(e)}",
                "finish_reason": "ERROR"
            }
    
    def generate_streaming_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ):
        """
        Generate streaming response from OpenAI (for real-time display)
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Override default temperature
            conversation_history: List of previous messages
            
        Yields:
            Chunks of text as they are generated
        """
        try:
            # Build messages array
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            if conversation_history:
                messages.extend(conversation_history)
            
            messages.append({"role": "user", "content": prompt})
            
            # Set parameters
            temp = temperature if temperature is not None else self.default_temperature
            
            # Call OpenAI API with streaming
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temp,
                max_tokens=self.default_max_tokens,
                stream=True
            )
            
            # Yield chunks as they arrive
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content:
                        yield delta.content
        
        except Exception as e:
            yield f"\n\n[Error: {str(e)}]"
    
    def count_tokens(self, text: str, model: Optional[str] = None) -> int:
        """
        Count tokens in text (approximate for GPT models)
        
        Args:
            text: Text to count tokens for
            model: Model name (uses self.model_name if not provided)
            
        Returns:
            Approximate token count
        """
        # Rough estimate: 1 token ≈ 4 characters for English
        # For more accurate counting, use tiktoken library
        return len(text) // 4
    
    def test_connection(self) -> bool:
        """
        Test if API connection is working
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            test_response = self.generate_response("Hello, this is a test.")
            return not test_response["error"]
        except Exception:
            return False
