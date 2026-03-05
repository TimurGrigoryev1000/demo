import RPi.GPIO as GPIO
import socketio

# ===============================
# CONFIG
# ===============================
CONTROLLER_IP = "192.168.2.41"
SERVER_URL = f"http://{CONTROLLER_IP}:5000"
ROOM = "door_lock"
LOCK_PIN = 17  # BCM pin to MOSFET gate

# ===============================
# GPIO SETUP
# ===============================
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK_PIN, GPIO.OUT)
GPIO.output(LOCK_PIN, GPIO.LOW)  # start unlocked

# ===============================
# SOCKET.IO CLIENT
# ===============================
sio = socketio.Client()

# ===============================
# LOCK / UNLOCK FUNCTIONS
# ===============================
def lockDoor():
    try:
        GPIO.output(LOCK_PIN, GPIO.HIGH)
        print("[LOCK] Door Locked")
        return True
    except Exception as e:
        print("[ERROR] Lock:", e)
        return False

def unlockDoor():
    try:
        GPIO.output(LOCK_PIN, GPIO.LOW)
        print("[UNLOCK] Door Unlocked")
        return True
    except Exception as e:
        print("[ERROR] Unlock:", e)
        return False

# ===============================
# SOCKETIO EVENT HANDLERS
# ===============================
@sio.event
def connect():
    print("[INFO] Connected to Controller")
    sio.emit("subscribe", ROOM)   # <-- this is the important part

@sio.on("lockDoor")
def handle_lock(data=None):
    print("[RX] lockDoor command", data)
    return lockDoor()

@sio.on("unlockDoor")
def handle_unlock(data=None):
    print("[RX] unlockDoor command", data)
    return unlockDoor()

@sio.event
def disconnect():
    print("[INFO] Disconnected from Controller")

# ===============================
# MAIN
# ===============================
def main():
    try:
        sio.connect(SERVER_URL)
        sio.wait()
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
