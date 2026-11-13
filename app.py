"""
PACD-RAG Platform Master Unified Runner
=============================================================================
Dual-Port Runner:
  - Unified Dashboard:     http://localhost:8000/ and http://localhost:8002/
  - Student Portal View:   http://localhost:8000/#student and http://localhost:8002/#student
  - Faculty Console View:  http://localhost:8000/#faculty and http://localhost:8002/#faculty
  - REST & Agent API Docs: http://localhost:8000/docs and http://localhost:8002/docs
=============================================================================
"""

import os
import sys
import threading
import uvicorn
from dotenv import load_dotenv

root_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(root_dir, ".env"))
sys.path.insert(0, root_dir)
sys.path.insert(0, os.path.join(root_dir, "student_success_platform", "src"))

if __name__ == "__main__":
    banner = """
    =============================================================================
    SMART CAMPUS INTELLIGENCE & AUTONOMOUS FACULTY PLATFORM (PACD-RAG)
    =============================================================================
    [+] Primary Web Portal:   http://localhost:8000/
    [+] Secondary Web Portal: http://localhost:8002/
    [+] Student Portal:       http://localhost:8000/#student (or :8002)
    [+] Faculty Console:      http://localhost:8000/#faculty (or :8002)
    [+] API Documentation:    http://localhost:8000/docs (or :8002/docs)
    =============================================================================
    """
    print(banner)

    from student_success_platform.src.api_server import app

    def run_secondary_listener():
        try:
            cfg = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="warning")
            srv = uvicorn.Server(cfg)
            srv.run()
        except Exception as e:
            print(f"[!] Warning: Port 8000 listener could not bind: {e}")

    # Launch Port 8000 in background daemon thread
    t = threading.Thread(target=run_secondary_listener, daemon=True)
    t.start()

    # Launch Port 8002 in main thread
    uvicorn.run(app, host="0.0.0.0", port=8002, log_level="info")
