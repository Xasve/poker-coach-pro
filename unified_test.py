#!/usr/bin/env python3
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
    print(f"\n🔧 Testing {name}...")
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
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

passed = sum(1 for r in results if r)
total = len(tests)

print(f"\n✅ Passed: {passed}/{total}")
print(f"📈 Success rate: {(passed/total*100):.1f}%")

if passed == total:
    print("\n🎉 ALL TESTS PASSED! System is ready.")
    print("\n🚀 Run: python test_pokerstars.py")
else:
    print("\n⚠️  Some tests failed. Check errors above.")
    print("\n💡 Try: python fix_all_issues.py")

print("=" * 60)

if __name__ == "__main__":
    pass
