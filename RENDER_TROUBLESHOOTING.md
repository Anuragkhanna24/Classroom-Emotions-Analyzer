# Render Deployment Troubleshooting Guide

## Common Error: Docker Build Failure

### Error: `failed to solve: process "/bin/sh -c apt-get update && apt-get install -y...`

This error occurs when the Docker build fails during system dependency installation.

## Solutions

### Solution 1: Use render.yaml (Recommended)
The `render.yaml` file is configured to avoid Docker builds and use Render's native Python environment.

1. **Delete the Dockerfile** (not needed for render.yaml deployment)
2. **Use the render.yaml approach**:
   - Go to Render dashboard
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will auto-detect render.yaml

### Solution 2: Manual Web Service Deployment
If render.yaml doesn't work:

1. **Go to Render dashboard**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Use these settings**:
   - **Name**: `classroom-emotions-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Solution 3: Alternative Requirements File
If you still get dependency errors:

1. **Rename `requirements.txt` to `requirements-backup.txt`**
2. **Rename `requirements-simple.txt` to `requirements.txt`**
3. **This removes OpenCV and YOLO dependencies temporarily**
4. **Deploy and test basic functionality first**

## File Size Issues

### Problem: yolov8x.pt (131MB) too large
- **Solution**: The file is already in .gitignore
- **Alternative**: Use a smaller YOLO model (yolov8n.pt ~ 6MB)

## Database Issues

### Problem: SQLite file not writable
- **Solution**: SQLite files are excluded from deployment
- **Alternative**: Use Render's PostgreSQL service

## Step-by-Step Recovery

### 1. Clean Up
```bash
# Remove Dockerfile (not needed for render.yaml)
rm Dockerfile
rm Dockerfile.simple

# Keep only essential files
# - main.py
# - requirements.txt
# - templates/
# - static/
# - render.yaml
```

### 2. Test Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Test the app
python -m uvicorn main:app --reload
```

### 3. Deploy on Render
1. **Use render.yaml approach** (recommended)
2. **Or manual web service setup**
3. **Monitor build logs for errors**

## Alternative Deployment Options

### Railway
- Similar to Render
- Better Python support
- Pay-as-you-use pricing

### Heroku
- Classic choice
- Good Python support
- Requires credit card verification

## Contact Support

If issues persist:
1. **Check Render logs** in dashboard
2. **Review build output** for specific errors
3. **Consider upgrading** to paid plan for better support
4. **Use alternative platform** like Railway

## Success Checklist

- [ ] render.yaml file present
- [ ] requirements.txt compatible
- [ ] No Dockerfile (for render.yaml approach)
- [ ] All Python files committed
- [ ] Templates and static files included
- [ ] Large files excluded (.gitignore)
- [ ] Repository is public (free tier requirement)
