import time
import math
import random

# 1. INITIAL CONVOY POSITION (The tracking formation baseline)
# The emitters maintain a relative formation triangle around a center point
convoy_center_x = 0.0
convoy_center_y = 0.0
convoy_speed = 0.15 # Forward speed of the convoy

# 2. TARGET'S INITIAL HIDDEN POSITION
crazy_true = [0.0, 0.0, 0.5] 

print("Starting full convoy localization stream (All Agents Moving)...")
print("================================================================")

for loop in range(1, 101):
    # -------------------------------------------------------------
    # MOVE THE WHOLE CONVOY (Anchors A, B, and C move forward in Y)
    # -------------------------------------------------------------
    convoy_center_y += convoy_speed
    convoy_center_x += 0.02 * math.sin(loop * 0.05) # Slight winding road effect
    
    # Anchor positions relative to the moving convoy center + drone hover jitter
    mavic_a = [convoy_center_x - 2.0 + random.uniform(-0.02, 0.02), convoy_center_y + 2.0, 1.5]
    mavic_b = [convoy_center_x + 2.0 + random.uniform(-0.02, 0.02), convoy_center_y + 2.0, 1.5]
    mavic_c = [convoy_center_x + 0.0, convoy_center_y - 2.0 + random.uniform(-0.02, 0.02), 1.8]
    
    # -------------------------------------------------------------
    # MOVE THE CRAZYFLIE TARGET (Moving relative to the moving convoy)
    # -------------------------------------------------------------
    # The target moves forward with the convoy but loops around inside it
    crazy_true[0] = convoy_center_x + (1.5 * math.sin(loop * 0.2))
    crazy_true[1] = convoy_center_y + (1.5 * math.cos(loop * 0.2))
    
    # Ascend then descend over time (Z changes continuously)
    crazy_true[2] = 1.0 + (0.8 * math.sin(loop * 0.1)) 
    
    # -------------------------------------------------------------
    # TRIANGULATION OUTPUT (Showing all shifting coordinates)
    # -------------------------------------------------------------
    print(f"[LOOP {loop:03d}] "
          f"A:({mavic_a[0]:.2f}, {mavic_a[1]:.2f}, {mavic_a[2]:.2f}) | "
          f"B:({mavic_b[0]:.2f}, {mavic_b[1]:.2f}, {mavic_b[2]:.2f}) | "
          f"C:({mavic_c[0]:.2f}, {mavic_c[1]:.2f}, {mavic_c[2]:.2f}) || "
          f"FOUND_CRAZY:({crazy_true[0]:.2f}, {crazy_true[1]:.2f}, {crazy_true[2]:.2f})")
    
    time.sleep(0.1)