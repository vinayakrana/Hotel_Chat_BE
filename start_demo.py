"""
Quick start script to run both API and Streamlit servers
"""
import subprocess
import sys
import time
import os

def check_port(port):
    """Check if a port is already in use"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def main():
    print("="*60)
    print("🏨 Hotel Chatbot - Starting Servers")
    print("="*60)
    print()
    
    # Check if API is already running
    if check_port(8000):
        print("⚠️  Port 8000 already in use (API might be running)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    # Check if Streamlit is already running
    if check_port(8501):
        print("⚠️  Port 8501 already in use (Streamlit might be running)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    print("\n🚀 Starting API Server on http://localhost:8000")
    print("📝 API Docs will be at http://localhost:8000/docs")
    print()
    
    # Start API server
    api_process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("⏳ Waiting for API to start...")
    time.sleep(3)
    
    # Check if API started successfully
    if check_port(8000):
        print("✅ API Server started successfully!")
    else:
        print("❌ Failed to start API server")
        print("Please check the logs and try starting manually:")
        print("   python main.py")
        api_process.terminate()
        return
    
    print()
    print("🎨 Starting Streamlit App on http://localhost:8501")
    print()
    
    # Start Streamlit
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("="*60)
    print("✅ Both servers are running!")
    print()
    print("🌐 Open your browser and go to:")
    print("   http://localhost:8501")
    print()
    print("📚 Demo Credentials:")
    print("   Guest: guest@hotel.com / guest123")
    print("   Staff: staff@hotel.com / staff123")
    print()
    print("Press Ctrl+C to stop both servers")
    print("="*60)
    
    try:
        # Keep both processes running
        api_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        api_process.terminate()
        streamlit_process.terminate()
        print("✅ Servers stopped!")

if __name__ == "__main__":
    main()
