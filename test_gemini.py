"""
Test Gemini API Connection
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)
print("Testing Gemini API Connection")
print("=" * 50)

# Check API key
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not gemini_key:
    print("❌ No Gemini API key found!")
    print("Set GEMINI_API_KEY or GOOGLE_API_KEY in .env")
    exit(1)

print(f"✓ API Key found: {gemini_key[:20]}...")

# Try to import and test
try:
    import google.generativeai as genai
    print("✓ google-generativeai imported successfully")
    
    # Configure
    genai.configure(api_key=gemini_key)
    print("✓ API configured")
    
    # Create model - try different model names
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    model = None
    
    for model_name in model_names:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✓ Model created: {model_name}")
            break
        except Exception as e:
            print(f"  - {model_name}: {e}")
            continue
    
    if not model:
        raise Exception("Could not create any model")
    
    # Test generation
    print("\nTesting generation...")
    response = model.generate_content("Say 'Hello, I am working!' in one sentence.")
    
    if response.text:
        print(f"✅ SUCCESS! Response received:")
        print(f"   {response.text}")
        print("\n✅ Gemini API is working correctly!")
    else:
        print("⚠️ No response text received")
        print(f"Response: {response}")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nPossible causes:")
    print("- Invalid API key")
    print("- API key quota exceeded")
    print("- Network connection issue")
    print("- google-generativeai not installed")
    
print("\n" + "=" * 50)
