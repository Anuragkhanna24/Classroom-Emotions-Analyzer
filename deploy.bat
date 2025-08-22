@echo off
echo 🚀 Preparing Classroom Emotions Analyzer for deployment...

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not found. Please initialize git first:
    echo    git init
    echo    git add .
    echo    git commit -m "Initial commit"
    pause
    exit /b 1
)

REM Check if remote origin is set
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ❌ No remote origin found. Please add your GitHub repository:
    echo    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
    pause
    exit /b 1
)

echo ✅ Git repository found

REM Check if all files are committed
git status --porcelain >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Uncommitted changes found. Please commit all changes first:
    echo    git add .
    echo    git commit -m "Prepare for deployment"
    pause
    exit /b 1
)

echo ✅ All changes committed

REM Push to GitHub
echo 📤 Pushing to GitHub...
git push origin main

if errorlevel 1 (
    echo ❌ Failed to push to GitHub
    pause
    exit /b 1
)

echo ✅ Successfully pushed to GitHub
echo.
echo 🎉 Your code is now ready for deployment on Render!
echo.
echo 📋 Next steps:
echo 1. Go to https://render.com
echo 2. Sign up/Login with your GitHub account
echo 3. Click "New +" and select "Blueprint"
echo 4. Connect your GitHub repository
echo 5. Render will automatically detect render.yaml
echo 6. Click "Apply" to deploy
echo.
echo ⏱️  Deployment will take 5-10 minutes
echo 🔗 Your app will be available at the provided URL
pause
