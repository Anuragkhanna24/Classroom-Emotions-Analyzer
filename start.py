#!/usr/bin/env python3
"""
Startup script for Render deployment
This ensures proper port binding and environment variable handling
"""

import os
import uvicorn
from main import app

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting Classroom Emotions Analyzer on port {port}")
    print(f"Environment: {os.environ.get('RENDER_ENVIRONMENT', 'development')}")
    
    # Run the FastAPI app
    uvicorn.run(
        app,
        host="0.0.0.0",  # Bind to all interfaces
        port=port,
        log_level="info"
    )
