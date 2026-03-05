import time
import socketio

CONTROLLER_IP = "192.168.2.41"
SERVER_URL = f"http://{CONTROLLER_IP}:5000"

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def connect():
    print("[TEST] Connected to controller server")

@sio.event
def disconnect():
    print("[TEST] Disconnected")

def main():
    sio.connect(SERVER_URL)

    print("[TEST] Sending lockDoor to server")
    sio.emit("lockDoor", {})
    time.sleep(2)

    print("[TEST] Sending unlockDoor to server")
    sio.emit("unlockDoor", {})
    time.sleep(2)

    sio.disconnect()

if __name__ == "__main__":
    main()
