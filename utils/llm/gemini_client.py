"""
Gemini API Client Wrapper
Handles communication with Google Gemini API
"""
import os
from typing import Optional, Dict, Any, List
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions


class GeminiClient:
    """
    Wrapper for Google Gemini API with error handling and safety settings
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-pro"):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google API key. If None, reads from environment
            model_name: Model to use (default: gemini-pro)
        """
        # Try GEMINI_API_KEY first, then GOOGLE_API_KEY as fallback
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided (set GEMINI_API_KEY or GOOGLE_API_KEY)")
        
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        
        # Safety settings - prevent harmful content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        # Generation config
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate response from Gemini
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Override default temperature
            max_tokens: Override default max tokens
            conversation_history: List of previous messages for context
            
        Returns:
            Dict with 'response' (str), 'model' (str), 'error' (bool), 'error_message' (str)
        """
        try:
            # Build generation config
            gen_config = self.generation_config.copy()
            if temperature is not None:
                gen_config["temperature"] = temperature
            if max_tokens is not None:
                gen_config["max_output_tokens"] = max_tokens
            
            # Build full prompt with conversation history
            full_prompt = ""
            
            # Add system prompt at the beginning
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n"
            
            # Add conversation history for context
            if conversation_history:
                full_prompt += "=== CONVERSATION HISTORY ===\n"
                for msg in conversation_history:
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    if role == "user":
                        full_prompt += f"User: {content}\n"
                    elif role == "assistant":
                        full_prompt += f"Assistant: {content}\n"
                full_prompt += "=== END OF HISTORY ===\n\n"
            
            # Add current prompt
            full_prompt += f"User: {prompt}\nAssistant:"
            
            # Generate content
            response = self.model.generate_content(
                full_prompt,
                generation_config=gen_config,
                safety_settings=self.safety_settings
            )
            
            # Extract text from response
            if response.text:
                return {
                    "response": response.text,
                    "model": self.model_name,
                    "error": False,
                    "error_message": None,
                    "finish_reason": response.candidates[0].finish_reason if response.candidates else None
                }
            else:
                # Check if blocked by safety
                if response.prompt_feedback:
                    return {
                        "response": None,
                        "model": self.model_name,
                        "error": True,
                        "error_message": f"Content blocked: {response.prompt_feedback}",
                        "finish_reason": "SAFETY"
                    }
                else:
                    return {
                        "response": None,
                        "model": self.model_name,
                        "error": True,
                        "error_message": "No response generated",
                        "finish_reason": "OTHER"
                    }
        
        except google_exceptions.ResourceExhausted as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"API quota exceeded: {str(e)}",
                "finish_reason": "QUOTA_EXCEEDED"
            }
        
        except google_exceptions.InvalidArgument as e:
            return {
                "response": None,
                "model": self.model_name,
                "error": True,
                "error_message": f"Invalid request: {str(e)}",
                "finish_reason": "INVALID_REQUEST"
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
        temperature: Optional[float] = None
    ):
        """
        Generate streaming response from Gemini (for real-time display)
        
        Args:
            prompt: User's input prompt
            system_prompt: System instruction for the model
            temperature: Override default temperature
            
        Yields:
            Chunks of text as they are generated
        """
        try:
            # Build generation config
            gen_config = self.generation_config.copy()
            if temperature is not None:
                gen_config["temperature"] = temperature
            
            # Combine system prompt with user prompt if provided
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\n{prompt}"
            
            # Generate content with streaming
            response = self.model.generate_content(
                full_prompt,
                generation_config=gen_config,
                safety_settings=self.safety_settings,
                stream=True
            )
            
            # Yield chunks as they arrive
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            yield f"\n\n[Error: {str(e)}]"
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text (approximate)
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Approximate token count
        """
        try:
            result = self.model.count_tokens(text)
            return result.total_tokens
        except Exception:
            # Fallback: rough estimate (1 token ≈ 4 chars)
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
