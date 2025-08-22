#!/bin/bash

echo "🚀 Preparing Classroom Emotions Analyzer for deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote origin is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    exit 1
fi

echo "✅ Git repository found"

# Check if all files are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Uncommitted changes found. Please commit all changes first:"
    echo "   git add ."
    echo "   git commit -m 'Prepare for deployment'"
    exit 1
fi

echo "✅ All changes committed"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub"
    echo ""
    echo "🎉 Your code is now ready for deployment on Render!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Go to https://render.com"
    echo "2. Sign up/Login with your GitHub account"
    echo "3. Click 'New +' and select 'Blueprint'"
    echo "4. Connect your GitHub repository"
    echo "5. Render will automatically detect render.yaml"
    echo "6. Click 'Apply' to deploy"
    echo ""
    echo "⏱️  Deployment will take 5-10 minutes"
    echo "🔗 Your app will be available at the provided URL"
else
    echo "❌ Failed to push to GitHub"
    exit 1
fi
