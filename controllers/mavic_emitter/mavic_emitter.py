# =====================================================================
# FILE: mavic_emitter.py
# =====================================================================
import sys
import time
import math
import random
import socket
import json

# Configuration for UDP Broadcasting
TARGET_IP = "127.0.0.1"
TARGET_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def run_emitter(drone_id):
    print(f"[MAVIC_{drone_id}] Emitter online. Tracking GPS and broadcasting...")
    
    # Base offsets to form a tracking triangle formation around the convoy center
    offsets = {
        'A': {"x": -2.0, "y": 2.0,  "z": 1.5},
        'B': {"x": 2.0,  "y": 2.0,  "z": 1.5},
        'C': {"x": 0.0,  "y": -2.0, "z": 1.8}
    }
    
    my_offset = offsets.get(drone_id, {"x": 0, "y": 0, "z": 1.0})
    step = 0
    convoy_speed = 0.15

    while True:
        step += 1
        
        # Calculate the moving center of the convoy convoy
        convoy_x = 0.02 * math.sin(step * 0.05)
        convoy_y = step * convoy_speed
        
        # Calculate this specific drone's absolute position with a tiny bit of flight drift
        current_x = convoy_x + my_offset["x"] + random.uniform(-0.01, 0.01)
        current_y = convoy_y + my_offset["y"] + random.uniform(-0.01, 0.01)
        current_z = my_offset["z"] + random.uniform(-0.005, 0.005)
        
        # Pack the telemetry data packet
        telemetry = {
            "drone_id": drone_id,
            "x": round(current_x, 4),
            "y": round(current_y, 4),
            "z": round(current_z, 4),
            "step": step
        }
        
        # Send data packet over UDP to the Triangulation Controller
        message = json.dumps(telemetry).encode('utf-8')
        try:
            sock.sendto(message, (TARGET_IP, TARGET_PORT))
        except Exception as e:
            print(f"[MAVIC_{drone_id}] Send Error: {e}")
            
        time.sleep(0.1) # Broadcast rate: 10Hz

if __name__ == "__main__":
    # Fallback to random assignment if no argument is passed by the manager script
    if len(sys.argv) > 1:
        drone_name = sys.argv[1].upper()
    else:
        drone_name = random.choice(['A', 'B', 'C'])
        
    run_emitter(drone_name)