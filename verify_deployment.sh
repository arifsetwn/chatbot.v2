#!/bin/bash
# Pre-deployment verification script
# Run this before pushing to GitHub for Streamlit Cloud deployment

echo "============================================"
echo "Pre-Deployment Verification"
echo "============================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Check 1: requirements.txt doesn't contain sqlite3
echo "📋 Checking requirements.txt..."
if grep -q "sqlite3" requirements.txt; then
    echo -e "${RED}❌ ERROR: requirements.txt contains 'sqlite3' (built-in module)${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No sqlite3 in requirements.txt${NC}"
fi

# Check 2: requirements.txt doesn't contain pathlib2
if grep -q "pathlib2" requirements.txt; then
    echo -e "${RED}❌ ERROR: requirements.txt contains 'pathlib2' (not needed for Python 3.4+)${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No pathlib2 in requirements.txt${NC}"
fi

# Check 3: streamlit-authenticator has exact version
if grep -q "streamlit-authenticator==0.4.2" requirements.txt; then
    echo -e "${GREEN}✅ streamlit-authenticator version pinned correctly${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: streamlit-authenticator should be ==0.4.2${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 4: .gitignore contains secrets.toml
echo ""
echo "🔒 Checking .gitignore..."
if grep -q ".streamlit/secrets.toml" .gitignore; then
    echo -e "${GREEN}✅ secrets.toml is in .gitignore${NC}"
else
    echo -e "${RED}❌ ERROR: .streamlit/secrets.toml not in .gitignore${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check 5: Essential files exist
echo ""
echo "📁 Checking essential files..."
FILES=("app.py" "pages/1_Chat.py" "pages/2_Admin.py" "data/system_prompt.txt")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
    else
        echo -e "${RED}❌ ERROR: $file missing${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check 6: Utils modules exist
echo ""
echo "🔧 Checking utils modules..."
UTILS=(
    "utils/__init__.py"
    "utils/llm/__init__.py"
    "utils/llm/gemini_client.py"
    "utils/llm/openai_client.py"
    "utils/llm/llm_manager.py"
    "utils/algorithm_simulator.py"
    "utils/question_detector.py"
    "utils/code_analyzer.py"
    "utils/rate_limiter.py"
)
for util in "${UTILS[@]}"; do
    if [ -f "$util" ]; then
        echo -e "${GREEN}✅ $util exists${NC}"
    else
        echo -e "${YELLOW}⚠️  WARNING: $util missing${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
done

# Check 7: No hardcoded API keys in Python files
echo ""
echo "🔐 Checking for hardcoded secrets..."
if grep -r "AIza" --include="*.py" . 2>/dev/null | grep -v "example" | grep -v ".md" | grep -v "#"; then
    echo -e "${RED}❌ ERROR: Found hardcoded Gemini API key in Python files${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No hardcoded Gemini API keys${NC}"
fi

if grep -r "sk-proj" --include="*.py" . 2>/dev/null | grep -v "example" | grep -v ".md" | grep -v "#"; then
    echo -e "${RED}❌ ERROR: Found hardcoded OpenAI API key in Python files${NC}"
    ERRORS=$((ERRORS + 1))
else
    echo -e "${GREEN}✅ No hardcoded OpenAI API keys${NC}"
fi

# Check 8: Test imports
echo ""
echo "🐍 Testing Python imports..."
if python3 -c "from utils.algorithm_simulator import AlgorithmSimulator" 2>/dev/null; then
    echo -e "${GREEN}✅ AlgorithmSimulator imports successfully${NC}"
else
    echo -e "${RED}❌ ERROR: Cannot import AlgorithmSimulator${NC}"
    ERRORS=$((ERRORS + 1))
fi

if python3 -c "from utils.llm.gemini_client import GeminiClient" 2>/dev/null; then
    echo -e "${GREEN}✅ GeminiClient imports successfully${NC}"
else
    echo -e "${RED}❌ ERROR: Cannot import GeminiClient${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check 9: Git status
echo ""
echo "📦 Checking git status..."
if [ -z "$(git status --porcelain)" ]; then
    echo -e "${GREEN}✅ Working tree is clean${NC}"
else
    echo -e "${YELLOW}⚠️  WARNING: You have uncommitted changes${NC}"
    git status --short
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "============================================"
echo "Summary"
echo "============================================"
echo -e "Errors: ${RED}$ERRORS${NC}"
echo -e "Warnings: ${YELLOW}$WARNINGS${NC}"
echo ""

if [ $ERRORS -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 All checks passed! Ready to deploy.${NC}"
        echo ""
        echo "Next steps:"
        echo "1. git add ."
        echo "2. git commit -m 'Fix: Ready for Streamlit Cloud deployment'"
        echo "3. git push origin main"
        echo "4. Deploy on Streamlit Cloud"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Passed with warnings. Review warnings before deploying.${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Failed with $ERRORS error(s). Fix errors before deploying.${NC}"
    exit 1
fi
