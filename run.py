from app import create_app, socketio
from database import init_db, get_temperature
from pathlib import Path
import sqlite3

DATABASE = Path(__file__).resolve().parent / "history.db"

# IMPORTANT: must match what door node subscribes to
node_id = "door_lock"

"""
Webserver gateway interface (WSGI) for bi-directional communication
with browser client and IoT node clients
"""

def control_scheduler():
    while True:
        print("requesting temperature")
        socketio.emit("temperature_sample", to=node_id)

        db = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        print("reading from the database...")
        row = get_temperature(node_id, cursor)

        db.close()

        if row:
            print(row["temp"], row["dt"])
        else:
            print("no data")

        socketio.sleep(5)

init_db()
app = create_app()

# ✅ DISABLE temperature polling for door-only testing:
# socketio.start_background_task(control_scheduler)

# IMPORTANT: host 0.0.0.0 lets other Pis connect
socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
