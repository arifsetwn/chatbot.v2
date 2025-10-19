import streamlit_authenticator as stauth
import inspect

# Check the login method signature
print("Login method signature:")
print(inspect.signature(stauth.Authenticate.login))
print("\nLogin method help:")
help(stauth.Authenticate.login)
