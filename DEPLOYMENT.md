# Deployment Guide for Classroom Emotions Analyzer

## Deploying on Render

### Prerequisites
1. A GitHub account
2. Your code pushed to a GitHub repository
3. A Render account (free at [render.com](https://render.com))

### Step 1: Prepare Your Repository
1. Make sure all files are committed and pushed to GitHub
2. Ensure your repository is public (or you have a paid Render plan)

### Step 2: Deploy on Render

#### Option A: Using render.yaml (Recommended)
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` file
5. Click "Apply" to deploy

#### Option B: Manual Deployment
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `classroom-emotions-analyzer`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### Step 3: Environment Variables
Render will automatically set:
- `PORT`: The port your app runs on
- `PYTHON_VERSION`: Python version (3.9.16)

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for the build to complete (5-10 minutes)
3. Your app will be available at the provided URL

## Important Notes

### File Size Limitations
- The `yolov8x.pt` model file is 131MB
- Render has a 500MB build size limit on free tier
- If you encounter issues, consider:
  - Using a smaller YOLO model
  - Upgrading to a paid plan
  - Using model hosting services

### Database Considerations
- The current setup uses SQLite (file-based)
- For production, consider using PostgreSQL
- Render provides PostgreSQL databases

### Static Files
- Uploaded images are stored locally
- For production, consider using cloud storage (AWS S3, Cloudinary)

## Alternative Deployment Options

### Railway
- Similar to Render
- Good for Python apps
- Pay-as-you-use pricing

### Heroku
- Classic choice
- Requires credit card verification
- Good free tier

### DigitalOcean App Platform
- Professional hosting
- Good performance
- Reasonable pricing

## Troubleshooting

### Common Issues
1. **Build Failures**: Check requirements.txt compatibility
2. **Memory Issues**: YOLO model requires significant RAM
3. **File Upload Errors**: Check static folder permissions
4. **Database Errors**: Ensure SQLite file is writable

### Support
- Check Render logs in the dashboard
- Review build output for errors
- Ensure all dependencies are compatible

## Post-Deployment

1. Test your application thoroughly
2. Monitor performance and logs
3. Set up monitoring and alerts
4. Consider setting up a custom domain
5. Implement proper error handling and logging
