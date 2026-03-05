from .extensions import socketio
from flask_socketio import emit, join_room, leave_room
from database import write_temperature
import sqlite3

DATABASE = "history.db"

@socketio.on("subscribe")
def handle_subscription(message):
    """
    client joins socket channel (room)
    """
    node_id = message
    join_room(node_id)
    print(f"node_id: [{node_id}] sucessfully subscribed!")

@socketio.on("unsubscribe")
def handle_unsubscription(message):
    """
    client leaves socket channel (room)
    """
    node_id = message
    leave_room(node_id)
    print(f"node_id: [{node_id}] sucessfully unsubscribed!")

@socketio.on("temperature_reading")
def handle_temperature_reading(message: dict):
    """
    receive temperature reading from kitchen client
    """
    node_id = message["node_id"]
    dt = message["dt"]
    temp = float(message["temp"])
    print(f"received [{node_id}] {dt} -> {temp}")

    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    write_temperature(node_id, dt, temp, cursor)

    db.commit()
    db.close()

@socketio.on("latch_reading")
def handle_latch_sensor_reading(data):
    """
    receive latch data from socketio client (important: not a flask_socketio client)
    """
    print(f"data: {data}")

@socketio.on("sendFall")
def handle_fall_event(data):
    """
    receive fall detection event from fall detection node
    """
    print(f"FALL EVENT RECEIVED: {data}")

@socketio.on("door_lock_ack")
def handle_door_lock_ack(data):
    """
    receive acknowledgement from Door Lock node after lock/unlock
    """
    print(f"[DOOR ACK] {data}")

# ----------------------------------------------------
# IMPORTANT: Forward door commands to the door_lock room
# (Because python-socketio CLIENT cannot emit with to=room)
# ----------------------------------------------------

@socketio.on("lockDoor")
def forward_lock(_data=None):
    socketio.emit("lockDoor", {}, to="door_lock")
    print("[CTRL] forwarded lockDoor -> door_lock")

@socketio.on("unlockDoor")
def forward_unlock(_data=None):
    socketio.emit("unlockDoor", {}, to="door_lock")
    print("[CTRL] forwarded unlockDoor -> door_lock")
