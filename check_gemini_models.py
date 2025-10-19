"""
List Available Gemini Models
"""
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 60)
print("Checking Gemini API Configuration")
print("=" * 60)

# Check API key
gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not gemini_key:
    print("❌ No Gemini API key found!")
    print("\n📝 To get a FREE API key:")
    print("1. Visit: https://aistudio.google.com/app/apikey")
    print("2. Click 'Create API Key'")
    print("3. Copy the key")
    print("4. Add to .env file:")
    print("   GEMINI_API_KEY=your_key_here")
    exit(1)

print(f"✓ API Key found: {gemini_key[:10]}...{gemini_key[-10:]}")

# Try to list models
try:
    import google.generativeai as genai
    print("✓ google-generativeai library installed")
    
    # Configure with API key
    genai.configure(api_key=gemini_key)
    print("✓ API configured")
    
    # List available models
    print("\n📋 Listing available models...")
    print("-" * 60)
    
    try:
        models = genai.list_models()
        
        found_models = []
        for model in models:
            # Check if model supports generateContent
            if 'generateContent' in model.supported_generation_methods:
                found_models.append(model.name)
                print(f"✓ {model.name}")
                print(f"  Display Name: {model.display_name}")
                print(f"  Description: {model.description[:80]}...")
                print()
        
        if found_models:
            print("=" * 60)
            print(f"✅ Found {len(found_models)} usable models!")
            print("\n🎯 Recommended model for .env:")
            print(f"GEMINI_MODEL={found_models[0].split('/')[-1]}")
            print("\nOther options:")
            for model in found_models[1:]:
                print(f"GEMINI_MODEL={model.split('/')[-1]}")
        else:
            print("⚠️ No models found that support generateContent")
            print("\nThis might mean:")
            print("- API key is invalid")
            print("- API key doesn't have access to Gemini models")
            print("- Need to enable Gemini API in Google Cloud Console")
            
    except Exception as list_error:
        print(f"❌ Could not list models: {list_error}")
        print("\n🔍 Trying direct API test...")
        
        # Try a simple test
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            response = model.generate_content("Hello")
            if response.text:
                print("✅ API is working with gemini-1.5-flash!")
                print(f"Response: {response.text[:100]}")
        except Exception as test_error:
            print(f"❌ Direct test failed: {test_error}")
            
            print("\n" + "=" * 60)
            print("❌ API KEY INVALID or NO ACCESS")
            print("=" * 60)
            print("\n📝 SOLUTION - Get a NEW API Key:")
            print("\n1. Visit: https://aistudio.google.com/app/apikey")
            print("2. Sign in with Google account")
            print("3. Click 'Create API Key' or 'Get API Key'")
            print("4. Copy the ENTIRE key (starts with AIzaSy...)")
            print("5. Replace in .env file:")
            print("   GEMINI_API_KEY=your_new_key_here")
            print("\n⚠️  Current key might be:")
            print("   - Invalid or revoked")
            print("   - From wrong project")
            print("   - Restricted API access")
            print("\n💡 Free tier gives 60 requests/minute - plenty for testing!")
        
except ImportError:
    print("❌ google-generativeai not installed!")
    print("\nInstall with:")
    print("pip install google-generativeai")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "=" * 60)
