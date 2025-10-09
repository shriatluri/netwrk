#!/usr/bin/env python3
"""
Script to run individual microservices locally for development
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_user_service():
    """Run User Service"""
    from services.user_service.main import app
    import uvicorn
    port = int(os.getenv("USER_SERVICE_PORT", 8001))
    print(f"Starting User Service on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)

def run_profile_service():
    """Run Profile Service"""
    from services.profile_service.main import app
    import uvicorn
    port = int(os.getenv("PROFILE_SERVICE_PORT", 8002))
    print(f"Starting Profile Service on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_services.py [user|profile]")
        sys.exit(1)

    service = sys.argv[1].lower()

    if service == "user":
        run_user_service()
    elif service == "profile":
        run_profile_service()
    else:
        print(f"Unknown service: {service}")
        print("Available services: user, profile")
        sys.exit(1)
