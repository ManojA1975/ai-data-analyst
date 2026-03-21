#!/bin/bash
# ============================================================
#   AI Data Analyst — GitHub Setup Script
#   Run this script after downloading the project files
# ============================================================

set -e

echo ""
echo "🤖 AI Data Analyst — GitHub Repository Setup"
echo "=============================================="
echo ""

# 1. Ask for GitHub username
read -p "📝 Enter your GitHub username: " GITHUB_USER

# 2. Ask for repo name
read -p "📁 Repository name [ai-data-analyst]: " REPO_NAME
REPO_NAME=${REPO_NAME:-ai-data-analyst}

echo ""
echo "🔧 Initializing git repository..."
git init
git add .
git commit -m "🚀 Initial commit: AI Data Analyst app"

echo ""
echo "🌐 Creating GitHub repository..."
echo "   → Go to https://github.com/new"
echo "   → Repository name: $REPO_NAME"
echo "   → Keep it Public"
echo "   → Do NOT initialize with README"
echo "   → Click 'Create repository'"
echo ""
read -p "✅ Press Enter once you've created the repo on GitHub..."

echo ""
echo "🔗 Connecting to GitHub..."
git branch -M main
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
git push -u origin main

echo ""
echo "✅ SUCCESS! Your project is now on GitHub!"
echo "🔗 https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "🌐 To deploy on Streamlit Cloud (FREE):"
echo "   1. Go to https://share.streamlit.io"
echo "   2. Click 'New app'"
echo "   3. Select: $GITHUB_USER/$REPO_NAME → main → app.py"
echo "   4. Add secret: ANTHROPIC_API_KEY = your_key"
echo "   5. Click Deploy! 🎉"
echo ""
