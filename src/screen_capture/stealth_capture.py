"""
Stealth Screen Capture Module for Poker Coach Pro
Optimized for PokerStars and GG Poker detection
"""
import mss
import cv2
import numpy as np
import time
from typing import Optional, Tuple, List, Dict
import os


class StealthScreenCapture:
    """
    Advanced screen capture system with stealth capabilities
    Optimized for poker table detection
    """
    
    def __init__(self, platform: str = "pokerstars", stealth_level: str = "MEDIUM"):
        """
        Initialize stealth screen capture
        
        Args:
            platform: "pokerstars" or "ggpoker"
            stealth_level: "LOW", "MEDIUM", "HIGH"
        """
        self.platform = platform.lower()
        self.stealth_level = stealth_level.upper()
        
        # Stealth configuration based on level
        self.stealth_config = self._get_stealth_config()
        
        # Screen capture setup
        self.sct = None
        self.last_capture_time = 0
        self.capture_count = 0
        
        # Debug settings
        self.debug_mode = True
        self.debug_dir = "debug_captures"
        os.makedirs(self.debug_dir, exist_ok=True)
        
        # Platform-specific settings
        self.platform_settings = self._get_platform_settings()
        
        print(f"🎯 StealthScreenCapture initialized for {self.platform}")
        print(f"🔰 Stealth level: {self.stealth_level}")
        print(f"⚙️  Capture delay: {self.stealth_config['capture_delay']}s")
    
    def _get_stealth_config(self) -> Dict:
        """Get stealth configuration based on level"""
        configs = {
            "LOW": {
                "capture_delay": 0.05,
                "random_delay": False,
                "save_captures": True,
                "monitor": 1
            },
            "MEDIUM": {
                "capture_delay": 0.1,
                "random_delay": True,
                "save_captures": False,
                "monitor": 1
            },
            "HIGH": {
                "capture_delay": 0.2,
                "random_delay": True,
                "save_captures": False,
                "monitor": 1,
                "vary_regions": True
            }
        }
        return configs.get(self.stealth_level, configs["MEDIUM"])
    
    def _get_platform_settings(self) -> Dict:
        """Get platform-specific settings"""
        settings = {
            "pokerstars": {
                "table_colors": {
                    "green_lower": [35, 40, 40],
                    "green_upper": [85, 255, 255]
                },
                "typical_regions": {
                    "community_cards": (0.4, 0.4, 0.6, 0.5),
                    "player_hand": (0.45, 0.7, 0.55, 0.8)
                }
            },
            "ggpoker": {
                "table_colors": {
                    "green_lower": [30, 40, 40],
                    "green_upper": [90, 255, 255]
                },
                "typical_regions": {
                    "community_cards": (0.35, 0.4, 0.65, 0.5),
                    "player_hand": (0.48, 0.75, 0.52, 0.85)
                }
            }
        }
        return settings.get(self.platform, settings["pokerstars"])
    
    def initialize(self) -> bool:
        """Initialize the screen capture system"""
        try:
            self.sct = mss.mss()
            print(f"✅ MSS initialized successfully")
            
            # Display monitor information
            monitors = self.sct.monitors
            print(f"📺 Monitors detected: {len(monitors)}")
            for i, monitor in enumerate(monitors):
                print(f"   Monitor {i}: {monitor}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize MSS: {e}")
            self.sct = None
            return False
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[np.ndarray]:
        """
        Capture screen or specific region with stealth timing
        
        Args:
            region: Optional (x1, y1, x2, y2) tuple for region capture
            
        Returns:
            numpy array of the captured image or None if failed
        """
        if self.sct is None:
            if not self.initialize():
                return None
        
        # Apply stealth timing
        self._apply_stealth_delay()
        
        try:
            # Determine capture area
            if region:
                x1, y1, x2, y2 = region
                monitor = {
                    "left": x1,
                    "top": y1,
                    "width": x2 - x1,
                    "height": y2 - y1
                }
            else:
                monitor_num = self.stealth_config.get("monitor", 1)
                if monitor_num < len(self.sct.monitors):
                    monitor = self.sct.monitors[monitor_num]
                else:
                    monitor = self.sct.monitors[1]
            
            # Capture screen
            screenshot = self.sct.grab(monitor)
            
            # Convert to numpy array
            img = np.array(screenshot)
            
            # Convert BGRA to BGR if necessary
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            self.last_capture_time = time.time()
            self.capture_count += 1
            
            # Save debug image if enabled
            if self.debug_mode and self.stealth_config.get("save_captures", False):
                self._save_debug_image(img, f"capture_{self.capture_count:04d}")
            
            return img
            
        except Exception as e:
            print(f"❌ Capture failed: {e}")
            return None
    
    def _apply_stealth_delay(self):
        """Apply stealth timing to avoid detection"""
        config = self.stealth_config
        
        # Base delay
        delay = config["capture_delay"]
        
        # Add random delay if enabled
        if config.get("random_delay", False):
            delay += np.random.uniform(0, 0.05)
        
        # Check if enough time has passed since last capture
        elapsed = time.time() - self.last_capture_time
        if elapsed < delay:
            time.sleep(delay - elapsed)
    
    def capture_table_region(self) -> Optional[np.ndarray]:
        """Capture typical table region based on platform"""
        try:
            # First capture full screen to find table
            full_screen = self.capture_screen()
            if full_screen is None:
                return None
            
            # Try to detect table
            table_region = self._detect_table_region(full_screen)
            
            if table_region:
                # Capture only table region
                return self.capture_screen(table_region)
            else:
                # Use default region based on platform
                height, width = full_screen.shape[:2]
                settings = self.platform_settings["typical_regions"]
                
                # Community cards region (center of screen)
                x1 = int(width * settings["community_cards"][0])
                y1 = int(height * settings["community_cards"][1])
                x2 = int(width * settings["community_cards"][2])
                y2 = int(height * settings["community_cards"][3])
                
                return self.capture_screen((x1, y1, x2, y2))
                
        except Exception as e:
            print(f"❌ Failed to capture table region: {e}")
            return None
    
    def _detect_table_region(self, image: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """Detect poker table region in image"""
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Get platform-specific color ranges
            colors = self.platform_settings["table_colors"]
            lower_green = np.array(colors["green_lower"])
            upper_green = np.array(colors["green_upper"])
            
            # Create mask for table color
            mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Apply morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None
            
            # Find largest contour (likely the table)
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Filter by minimum area
            min_table_area = 50000  # pixels
            if area < min_table_area:
                return None
            
            # Get bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Add some padding
            padding = 10
            x = max(0, x - padding)
            y = max(0, y - padding)
            w = min(image.shape[1] - x, w + 2 * padding)
            h = min(image.shape[0] - y, h + 2 * padding)
            
            return (x, y, x + w, y + h)
            
        except Exception as e:
            print(f"⚠️  Table detection failed: {e}")
            return None
    
    def capture_multiple_regions(self, regions: List[Tuple[int, int, int, int]]) -> List[Optional[np.ndarray]]:
        """Capture multiple regions efficiently"""
        results = []
        
        # Capture full screen once
        full_screen = self.capture_screen()
        if full_screen is None:
            return [None] * len(regions)
        
        # Extract each region from the full screen
        for region in regions:
            try:
                x1, y1, x2, y2 = region
                region_img = full_screen[y1:y2, x1:x2]
                results.append(region_img)
            except Exception as e:
                print(f"❌ Failed to extract region {region}: {e}")
                results.append(None)
        
        return results
    
    def _save_debug_image(self, image: np.ndarray, name: str):
        """Save image for debugging"""
        try:
            filename = os.path.join(self.debug_dir, f"{name}.png")
            cv2.imwrite(filename, image)
            
            if self.capture_count % 10 == 0:  # Log every 10th capture
                print(f"💾 Debug image saved: {filename}")
                
        except Exception as e:
            print(f"⚠️  Failed to save debug image: {e}")
    
    def save_image(self, image: np.ndarray, filename: str) -> bool:
        """Save image to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            cv2.imwrite(filename, image)
            print(f"💾 Image saved: {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save image {filename}: {e}")
            return False
    
    def get_screen_info(self) -> Dict:
        """Get information about available screens"""
        if self.sct is None:
            if not self.initialize():
                return {}
        
        info = {
            "monitors": len(self.sct.monitors),
            "primary_monitor": self.sct.monitors[0],
            "monitor_details": []
        }
        
        for i, monitor in enumerate(self.sct.monitors):
            info["monitor_details"].append({
                "index": i,
                "width": monitor["width"],
                "height": monitor["height"],
                "left": monitor["left"],
                "top": monitor["top"]
            })
        
        return info
    
    def test_capture(self) -> bool:
        """Test if capture system works"""
        print("\n🧪 Testing screen capture system...")
        
        try:
            # Test initialization
            if not self.initialize():
                print("❌ Failed to initialize")
                return False
            
            print("✅ MSS initialized")
            
            # Test screen capture
            screenshot = self.capture_screen()
            if screenshot is None:
                print("❌ Failed to capture screen")
                return False
            
            print(f"✅ Screen captured: {screenshot.shape}")
            
            # Test saving
            test_file = os.path.join(self.debug_dir, "test_capture.png")
            if self.save_image(screenshot, test_file):
                print(f"✅ Test image saved: {test_file}")
            else:
                print("⚠️  Could not save test image")
            
            # Test table detection
            table_region = self._detect_table_region(screenshot)
            if table_region:
                print(f"✅ Table detected: {table_region}")
            else:
                print("⚠️  No table detected (might be normal if no poker window)")
            
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def benchmark(self, iterations: int = 10) -> Dict:
        """Benchmark capture performance"""
        print(f"\n⚡ Running benchmark ({iterations} iterations)...")
        
        times = []
        successes = 0
        
        for i in range(iterations):
            start_time = time.time()
            
            screenshot = self.capture_screen()
            
            if screenshot is not None:
                successes += 1
                elapsed = time.time() - start_time
                times.append(elapsed)
                
                if (i + 1) % 5 == 0:
                    print(f"  Iteration {i + 1}/{iterations}: {elapsed:.3f}s")
        
        if times:
            avg_time = np.mean(times)
            min_time = min(times)
            max_time = max(times)
            success_rate = (successes / iterations) * 100
            
            results = {
                "iterations": iterations,
                "success_rate": success_rate,
                "avg_time": avg_time,
                "min_time": min_time,
                "max_time": max_time,
                "fps": 1 / avg_time if avg_time > 0 else 0
            }
            
            print(f"\n📊 Benchmark Results:")
            print(f"   Success rate: {success_rate:.1f}%")
            print(f"   Average time: {avg_time:.3f}s")
            print(f"   FPS: {results['fps']:.1f}")
            print(f"   Min/Max: {min_time:.3f}s / {max_time:.3f}s")
            
            return results
        else:
            print("❌ Benchmark failed - no successful captures")
            return {}


# Test function for direct execution
def test_capture_system():
    """Test function for the capture system"""
    print("=" * 60)
    print("🧪 TESTING STEALTH SCREEN CAPTURE SYSTEM")
    print("=" * 60)
    
    # Create capture instance
    capture = StealthScreenCapture(platform="pokerstars", stealth_level="MEDIUM")
    
    # Run tests
    print("\n1. Testing initialization...")
    if capture.initialize():
        print("✅ Initialization successful")
    else:
        print("❌ Initialization failed")
        return
    
    print("\n2. Testing screen capture...")
    screenshot = capture.capture_screen()
    if screenshot is not None:
        print(f"✅ Capture successful: {screenshot.shape}")
    else:
        print("❌ Capture failed")
        return
    
    print("\n3. Saving test image...")
    capture.save_image(screenshot, "debug/test_fullscreen.png")
    
    print("\n4. Testing table region capture...")
    table_img = capture.capture_table_region()
    if table_img is not None:
        print(f"✅ Table region captured: {table_img.shape}")
        capture.save_image(table_img, "debug/test_table_region.png")
    else:
        print("⚠️  Could not capture table region")
    
    print("\n5. Running benchmark...")
    capture.benchmark(iterations=5)
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    # Run tests if executed directly
    test_capture_system()