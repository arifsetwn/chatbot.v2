# Pre-Deployment Checklist

## ✅ File Verification

### Requirements
- [ ] `requirements.txt` tidak mengandung `sqlite3`
- [ ] `requirements.txt` tidak mengandung `pathlib2`
- [ ] `requirements.txt` tidak mengandung dev dependencies
- [ ] `streamlit-authenticator==0.4.2` (exact version)
- [ ] Semua versi dependencies pinned (tidak pakai `>=`)

### Configuration
- [ ] `.streamlit/config.toml` ada dan benar
- [ ] `.streamlit/secrets.toml.example` ada sebagai template
- [ ] `.streamlit/secrets.toml` ADA DI `.gitignore`
- [ ] `.env` ADA DI `.gitignore`

### File Structure
- [ ] `app.py` ada di root
- [ ] `pages/1_Chat.py` ada
- [ ] `pages/2_Admin.py` ada
- [ ] `utils/` folder lengkap dengan semua modules
- [ ] `data/system_prompt.txt` ada

### Directories
- [ ] `data/` folder exists (buat jika belum ada)
- [ ] `logs/` folder exists (buat jika belum ada)
- [ ] `uploads/` folder exists (buat jika belum ada)

## ✅ Code Verification

### Entry Point (app.py)
- [ ] Import statements benar
- [ ] Tidak ada blocking code
- [ ] Directory creation code ada
- [ ] Redirect logic bekerja

### Pages
- [ ] `1_Chat.py` - Import semua utilities berhasil
- [ ] `2_Admin.py` - Authenticator setup benar
- [ ] No hardcoded API keys di code

### Utils
- [ ] `utils/llm/gemini_client.py` exists
- [ ] `utils/llm/openai_client.py` exists
- [ ] `utils/llm/llm_manager.py` exists
- [ ] `utils/algorithm_simulator.py` exists
- [ ] `utils/question_detector.py` exists
- [ ] `utils/code_analyzer.py` exists
- [ ] `utils/rate_limiter.py` exists
- [ ] Semua `__init__.py` ada di utils/ dan utils/llm/

## ✅ Environment Variables

### Required for Gemini-only (minimum)
- [ ] `GEMINI_API_KEY` ready
- [ ] `ADMIN_USERNAME` ready
- [ ] `ADMIN_PASSWORD` ready
- [ ] `ACTIVE_MODEL=gemini` set
- [ ] `GEMINI_MODEL=gemini-2.0-flash` set

### Optional but Recommended
- [ ] `SECRET_KEY` set (random string)
- [ ] `RATE_LIMIT_PER_MINUTE` set
- [ ] `RATE_LIMIT_PER_HOUR` set
- [ ] `GLOBAL_RATE_LIMIT` set

## ✅ Git Repository

### Before Push
- [ ] All changes committed
- [ ] No sensitive files in staging
- [ ] `.gitignore` properly configured
- [ ] Branch is clean (no uncommitted changes)

### Repository Structure
```bash
git status  # Should be clean
git log     # Check commit history
```

Expected output:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## ✅ Local Testing

### Basic Functionality
- [ ] `streamlit run app.py` works locally
- [ ] No import errors
- [ ] Chat page loads
- [ ] Admin page loads
- [ ] Can send messages (dengan API key valid)
- [ ] Algorithm simulator works
- [ ] File upload works

### Environment Test
```bash
# Test with production-like settings
cp .env .env.backup
# Set only production env vars in .env
streamlit run app.py
# Verify everything works
mv .env.backup .env
```

## ✅ Streamlit Cloud Setup

### Account Ready
- [ ] Streamlit Cloud account active
- [ ] GitHub account connected
- [ ] Repository accessible to Streamlit Cloud

### Secrets Prepared
- [ ] Secrets file formatted as TOML
- [ ] All required secrets listed
- [ ] API keys valid and tested
- [ ] No typos in secret keys

Example secrets.toml:
```toml
GEMINI_API_KEY = "AIza..."
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "secure_password_here"
ACTIVE_MODEL = "gemini"
GEMINI_MODEL = "gemini-2.0-flash"
```

## ✅ Deployment Readiness

### Pre-Deploy Commands
```bash
# 1. Verify requirements.txt
cat requirements.txt | grep -E "sqlite3|pathlib2"
# Should return nothing

# 2. Check .gitignore
cat .gitignore | grep "secrets.toml"
# Should show: .streamlit/secrets.toml

# 3. List all Python files
find . -name "*.py" -type f | head -20
# Verify all important files exist

# 4. Check for hardcoded secrets
grep -r "AIza" --include="*.py" .
grep -r "sk-proj" --include="*.py" .
# Should return nothing (or only in commented examples)

# 5. Test import statements
python3 -c "from utils.algorithm_simulator import AlgorithmSimulator; print('OK')"
python3 -c "from utils.llm.gemini_client import GeminiClient; print('OK')"
# Should print: OK
```

### Final Push
```bash
# Review changes
git status
git diff

# Add all changes
git add .

# Commit with clear message
git commit -m "Fix: Remove sqlite3 and pathlib2 for Streamlit Cloud deployment"

# Push to main branch
git push origin main

# Verify push successful
git log -1
```

## ✅ Post-Deployment Verification

### Immediately After Deploy
- [ ] App URL accessible
- [ ] No errors in Streamlit Cloud logs
- [ ] Homepage loads (redirects to Chat)
- [ ] Chat page displays correctly
- [ ] Admin page accessible

### Functional Testing
- [ ] Login to Admin works
- [ ] Send test message in Chat
- [ ] LLM responds correctly
- [ ] Algorithm simulator works
- [ ] File upload works
- [ ] Rate limiting active

### Monitor First Hour
- [ ] Check logs every 10 minutes
- [ ] Monitor for crashes
- [ ] Monitor memory usage
- [ ] Check for error patterns

## 🚨 Common Issues Checklist

If deployment fails:

- [ ] Check logs first (Streamlit Cloud → Manage App → Logs)
- [ ] Verify all files committed and pushed
- [ ] Check secrets are properly set
- [ ] Verify no syntax errors in Python files
- [ ] Check import paths are correct
- [ ] Ensure all required directories exist

## 📋 Rollback Plan

If something goes wrong:

```bash
# Revert to previous commit
git log  # Find last working commit hash
git revert <commit-hash>
git push origin main
```

Or in Streamlit Cloud:
1. Settings → Advanced
2. Redeploy from specific commit
3. Choose last working commit

## ✅ Success Criteria

Deployment is successful when:
- [ ] ✅ App loads without errors
- [ ] ✅ All pages accessible
- [ ] ✅ LLM responds to messages
- [ ] ✅ No crashes in first hour
- [ ] ✅ Memory usage stable (<500MB)
- [ ] ✅ Response time reasonable (<5s)

---

**Use this checklist before EVERY deployment!**

**Last Updated:** 19 Oktober 2025
