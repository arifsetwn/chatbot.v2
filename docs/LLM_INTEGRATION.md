# LLM Integration Documentation

## Overview

Chatbot Algoritma menggunakan sistem modular untuk integrasi LLM (Large Language Model) yang mendukung multiple providers dengan fallback otomatis.

## Supported Providers

### 1. Google Gemini
- Model: `gemini-pro`
- API Key: Diperlukan dari Google AI Studio
- Rate Limit: Tergantung tier akun

### 2. OpenAI
- Model: `gpt-3.5-turbo`, `gpt-4`
- API Key: Diperlukan dari OpenAI Platform
- Rate Limit: Tergantung tier akun

## Architecture

```
utils/
├── llm/
│   ├── __init__.py
│   ├── gemini_client.py      # Gemini API wrapper
│   ├── openai_client.py      # OpenAI API wrapper
│   └── llm_manager.py         # Unified interface
└── rate_limiter.py            # Rate limiting implementation
```

## Configuration

### Environment Variables (.env)

```bash
# Primary Model Selection
ACTIVE_MODEL=gemini  # or 'openai'

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Model Selection
GEMINI_MODEL=gemini-pro
OPENAI_MODEL=gpt-3.5-turbo

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10      # Per user
RATE_LIMIT_PER_HOUR=100       # Per user
GLOBAL_RATE_LIMIT=60          # Total requests per minute
```

## Usage Examples

### Basic Usage

```python
from utils.llm.llm_manager import LLMManager

# Initialize from environment
llm = LLMManager.from_env()

# Generate response
result = llm.generate_response(
    prompt="Jelaskan binary search",
    system_prompt="Kamu adalah guru algoritma",
    temperature=0.7
)

if not result["error"]:
    print(result["response"])
else:
    print(f"Error: {result['error_message']}")
```

### Streaming Response

```python
# For real-time display
for chunk in llm.generate_streaming_response(
    prompt="Jelaskan sorting algorithms",
    system_prompt="Kamu adalah guru algoritma"
):
    print(chunk, end="", flush=True)
```

### With Rate Limiting

```python
from utils.rate_limiter import RateLimiter

rate_limiter = RateLimiter.from_env()

# Check before making request
check = rate_limiter.check_limit(user_id="student_123")

if check["allowed"]:
    result = llm.generate_response(prompt="...")
else:
    print(f"Rate limit: {check['reason']}")
    print(f"Wait: {check['wait_time']} seconds")
```

## Error Handling

The system includes comprehensive error handling:

### Error Types

1. **API Quota Exceeded**
   - Automatically tries fallback provider
   - Returns error message if all providers fail

2. **Invalid Request**
   - Returns detailed error message
   - Logs error for debugging

3. **Connection Error**
   - Retries with fallback provider
   - Returns user-friendly error message

4. **Content Safety Blocked**
   - Returns safety violation message
   - Logs blocked content type

### Example Error Response

```python
{
    "response": None,
    "model": "gemini-pro",
    "provider": "gemini",
    "error": True,
    "error_message": "API quota exceeded: ...",
    "finish_reason": "QUOTA_EXCEEDED"
}
```

## Rate Limiting

### Token Bucket Algorithm

The rate limiter uses token bucket algorithm with three levels:

1. **Global Limit**: Total requests across all users
2. **Per-User Minute**: Requests per user per minute
3. **Per-User Hour**: Requests per user per hour

### Configuration

```python
rate_limiter = RateLimiter(
    global_requests_per_minute=60,
    user_requests_per_minute=10,
    user_requests_per_hour=100
)
```

### Checking Status

```python
status = rate_limiter.get_user_status(user_id="student_123")
print(f"Available requests this minute: {status['user_minute_available']}")
print(f"Available requests this hour: {status['user_hour_available']}")
```

## System Prompt

The system prompt is loaded from `data/system_prompt.txt` and defines the chatbot's behavior:

- Guided learning approach (Socratic method)
- No direct answers for homework/exams
- Friendly, supportive tone
- Step-by-step explanations

## Testing

### Test API Connection

```python
# Test specific provider
if llm.test_provider(ModelProvider.GEMINI):
    print("Gemini is working")

# Test all providers
results = llm.test_all_providers()
for provider, status in results.items():
    print(f"{provider}: {'✓' if status else '✗'}")
```

### Get Available Providers

```python
providers = llm.get_available_providers()
print(f"Available: {', '.join(providers)}")
```

## Fallback Mechanism

When primary provider fails:

1. System logs the error
2. Automatically switches to fallback provider
3. Returns response with `used_fallback: True` flag
4. Admin dashboard shows fallback usage statistics

## Best Practices

1. **Always check rate limits** before making requests
2. **Use streaming** for better user experience
3. **Handle errors gracefully** with user-friendly messages
4. **Monitor API usage** in admin dashboard
5. **Set appropriate temperature** (0.7 for creative, 0.3 for factual)
6. **Include system prompt** for consistent behavior
7. **Test connections** before deployment

## Security Considerations

1. **API Keys**: Never commit to git, use `.env`
2. **Rate Limiting**: Prevent abuse and manage costs
3. **Input Validation**: Sanitize user input before sending to API
4. **Content Safety**: Gemini includes built-in safety filters
5. **Error Messages**: Don't expose internal details to users

## Troubleshooting

### "No LLM providers could be initialized"
- Check if API keys are set in `.env`
- Verify API keys are valid
- Check internet connection

### "Rate limit exceeded"
- Wait for the specified time
- Increase limits in `.env` if needed
- Consider upgrading API tier

### "Connection error"
- Check internet connection
- Verify firewall/proxy settings
- Check API service status

### "Content blocked by safety"
- Rephrase the prompt
- Check safety settings in `gemini_client.py`
- Review content policy

## Future Enhancements

- [ ] Add support for Claude (Anthropic)
- [ ] Implement caching for repeated queries
- [ ] Add token counting and cost estimation
- [ ] Implement conversation memory management
- [ ] Add fine-tuning support
- [ ] Implement A/B testing framework
