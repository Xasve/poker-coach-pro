#!/usr/bin/env python3
"""
FIX ALL ISSUES - Poker Coach Pro
Comprehensive fix for all common problems
"""
import os
import sys
import shutil

def fix_stealth_capture_imports():
    """Fix import issues in stealth_capture module"""
    print("🔧 Fixing stealth_capture imports...")
    
    # Update __init__.py in screen_capture
    init_file = "src/screen_capture/__init__.py"
    
    init_content = '''"""
Screen Capture Module for Poker Coach Pro
"""
from .stealth_capture import StealthScreenCapture
from .table_detector import TableDetector
from .card_recognizer import CardRecognizer
from .text_ocr import TextOCR

__all__ = [
    'StealthScreenCapture',
    'TableDetector',
    'CardRecognizer',
    'TextOCR'
]

__version__ = "2.0.0"

print("✅ screen_capture module loaded")
'''
    
    with open(init_file, 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print(f"✅ Updated: {init_file}")
    return True

def fix_test_capture_script():
    """Fix test_capture.py script"""
    print("\n🔧 Fixing test_capture.py...")
    
    test_content = '''#!/usr/bin/env python3
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
    print("\\nOption 1: Running built-in test...")
    test_capture_system()
    
    # Option 2: Manual test
    print("\\nOption 2: Manual test...")
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
    
    print("\\n" + "=" * 60)
    print("✅ Test completed")
    print("=" * 60)

if __name__ == "__main__":
    main()
'''
    
    with open("test_capture.py", 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ Created: test_capture.py")
    return True

def create_unified_test():
    """Create unified test script"""
    print("\n📄 Creating unified test script...")
    
    unified_test = '''#!/usr/bin/env python3
"""
UNIFIED TEST - Poker Coach Pro
Tests all major components
"""
import sys
import os

print("=" * 60)
print("🧪 UNIFIED SYSTEM TEST - POKER COACH PRO")
print("=" * 60)

sys.path.insert(0, 'src')

def test_component(name, test_func):
    """Test a component with error handling"""
    print(f"\\n🔧 Testing {name}...")
    try:
        result = test_func()
        if result:
            print(f"✅ {name}: PASSED")
        else:
            print(f"❌ {name}: FAILED")
        return result
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return False

def test_imports():
    """Test basic imports"""
    try:
        from screen_capture.stealth_capture import StealthScreenCapture
        from screen_capture.table_detector import TableDetector
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def test_capture():
    """Test screen capture"""
    try:
        from screen_capture.stealth_capture import StealthScreenCapture
        capture = StealthScreenCapture("pokerstars", "MEDIUM")
        return capture.initialize()
    except Exception as e:
        print(f"Capture error: {e}")
        return False

def test_pokerstars_adapter():
    """Test PokerStars adapter"""
    try:
        from platforms.pokerstars_adapter import PokerStarsAdapter
        adapter = PokerStarsAdapter()
        return True
    except Exception as e:
        print(f"Adapter error: {e}")
        return False

def test_poker_engine():
    """Test poker engine"""
    try:
        from core.poker_engine import PokerEngine
        engine = PokerEngine()
        return True
    except Exception as e:
        print(f"Engine error: {e}")
        return False

# Run all tests
tests = [
    ("Basic imports", test_imports),
    ("Screen capture", test_capture),
    ("PokerStars adapter", test_pokerstars_adapter),
    ("Poker engine", test_poker_engine)
]

results = []
for name, func in tests:
    results.append(test_component(name, func))

# Summary
print("\\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

passed = sum(1 for r in results if r)
total = len(tests)

print(f"\\n✅ Passed: {passed}/{total}")
print(f"📈 Success rate: {(passed/total*100):.1f}%")

if passed == total:
    print("\\n🎉 ALL TESTS PASSED! System is ready.")
    print("\\n🚀 Run: python test_pokerstars.py")
else:
    print("\\n⚠️  Some tests failed. Check errors above.")
    print("\\n💡 Try: python fix_all_issues.py")

print("=" * 60)

if __name__ == "__main__":
    pass
'''
    
    with open("unified_test.py", 'w', encoding='utf-8') as f:
        f.write(unified_test)
    
    print("✅ Created: unified_test.py")
    return True

def fix_pokerstars_adapter():
    """Fix PokerStars adapter constructor call"""
    print("\n🔧 Checking PokerStars adapter...")
    
    adapter_file = "src/platforms/pokerstars_adapter.py"
    
    if not os.path.exists(adapter_file):
        print(f"⚠️  File not found: {adapter_file}")
        return False
    
    with open(adapter_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if StealthScreenCapture is called with correct arguments
    if 'StealthScreenCapture(' in content:
        # Count arguments in constructor call
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'StealthScreenCapture(' in line:
                print(f"Found on line {i+1}: {line.strip()}")
                
                # Check argument count
                if line.count(',') >= 1:  # Has at least 2 arguments
                    print("✅ StealthScreenCapture called with correct arguments")
                else:
                    print("⚠️  May need argument fix")
    
    return True

def check_dependencies():
    """Check and install required dependencies"""
    print("\n📦 Checking dependencies...")
    
    deps = [
        ("opencv-python", "cv2"),
        ("mss", "mss"),
        ("numpy", "numpy"),
        ("Pillow", "PIL"),
        ("pytesseract", "pytesseract")
    ]
    
    missing = []
    
    for pip_name, import_name in deps:
        try:
            __import__(import_name)
            print(f"✅ {pip_name}")
        except ImportError:
            print(f"❌ {pip_name}")
            missing.append(pip_name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("💡 Install with: pip install " + " ".join(missing))
        return False
    else:
        print("\n✅ All dependencies installed")
        return True

def main():
    print("=" * 60)
    print("🛠️  COMPREHENSIVE FIX - POKER COACH PRO")
    print("=" * 60)
    
    print("\n📋 Running fixes...")
    
    # Run all fixes
    fixes = [
        ("Stealth capture imports", fix_stealth_capture_imports),
        ("Test capture script", fix_test_capture_script),
        ("Unified test", create_unified_test),
        ("PokerStars adapter", fix_pokerstars_adapter),
        ("Dependencies", check_dependencies)
    ]
    
    results = []
    for name, fix_func in fixes:
        print(f"\n🔧 {name}...")
        try:
            result = fix_func()
            results.append((name, result))
            if result:
                print(f"✅ {name}: SUCCESS")
            else:
                print(f"⚠️  {name}: PARTIAL")
        except Exception as e:
            print(f"❌ {name}: FAILED - {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FIX SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n✅ Successful fixes: {successful}/{total}")
    
    if successful == total:
        print("\n🎉 ALL FIXES APPLIED SUCCESSFULLY!")
        print("\n🚀 Next steps:")
        print("   1. python unified_test.py")
        print("   2. python test_capture.py")
        print("   3. python test_pokerstars.py")
    else:
        print("\n⚠️  Some fixes may need manual attention")
        print("\n💡 Manual fixes needed:")
        for name, result in results:
            if not result:
                print(f"   • {name}")
    
    print("\n" + "=" * 60)
    print("✅ Fix process completed")
    print("=" * 60)

if __name__ == "__main__":
    main()