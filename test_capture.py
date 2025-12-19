#!/usr/bin/env python3
"""
Test script for screen capture functionality
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from screen_capture.stealth_capture import StealthScreenCapture, test_capture_system
import cv2
import time

def main():
    print("=" * 60)
    print("📸 TESTING SCREEN CAPTURE SYSTEM")
    print("=" * 60)
    
    # Option 1: Use test function
    print("\nOption 1: Running built-in test...")
    test_capture_system()
    
    # Option 2: Manual test
    print("\nOption 2: Manual test...")
    capture = StealthScreenCapture(platform="pokerstars", stealth_level="MEDIUM")
    
    if capture.initialize():
        print("✅ Capture system initialized")
        
        # Capture and display
        screenshot = capture.capture_screen()
        if screenshot is not None:
            print(f"✅ Screenshot captured: {screenshot.shape}")
            
            # Save
            os.makedirs("debug", exist_ok=True)
            cv2.imwrite("debug/test_manual.png", screenshot)
            print("💾 Saved to: debug/test_manual.png")
            
            # Display info
            height, width = screenshot.shape[:2]
            print(f"📊 Resolution: {width}x{height}")
        else:
            print("❌ Failed to capture screenshot")
    else:
        print("❌ Failed to initialize capture system")
    
    print("\n" + "=" * 60)
    print("✅ Test completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
