#!/usr/bin/env python3
"""
Quizify One-Command Launch Script
Starts the 100% Python-based Quizify server with real QR codes and responsive interface.
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.config import config
from backend.app import app

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("QUIZIFY -- ACADEMIC EXAMINATION & ROTATING QR PLATFORM")
    print("=" * 70)
    print(f"Server starting on http://{config.HOST}:{config.PORT}")
    print(f"Network Access URL: {config.LAN_BASE_URL}")
    print(f"Configured Base URL: {config.APP_BASE_URL}")
    print("To scan QRs on phone, ensure your phone is connected to the same Wi-Fi")
    print("=" * 70 + "\n")

    app.run(host=config.HOST, port=config.PORT, debug=True)
