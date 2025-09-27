#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    # Get port from environment or default to 8000
    port = os.getenv('PORT', '8000')
    
    # Ensure port is valid
    try:
        port_int = int(port)
        if not (1 <= port_int <= 65535):
            raise ValueError("Port out of range")
    except ValueError:
        print(f"Invalid port: {port}, defaulting to 8000")
        port = '8000'
    
    # Set PYTHONPATH
    app_dir = os.path.dirname(os.path.abspath(__file__))
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    
    print(f"🚀 Starting PawSense Backend on port {port}...")
    
    # Start uvicorn
    cmd = [
        sys.executable, '-m', 'uvicorn',
        'app.main:app',
        '--host', '0.0.0.0',
        '--port', port
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Server stopped by user")
        sys.exit(0)

if __name__ == '__main__':
    main()