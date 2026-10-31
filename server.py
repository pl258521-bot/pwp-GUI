from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GigaBite Rover Controller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attempt physical Raspberry Pi connection; fallback to Mock mode on PC
try:
    from robot import RobotClass
    robot = RobotClass()
    print("[SYSTEM] PHYSICAL HARDWARE DETECTED: Connected to Raspberry Pi motors.")
except Exception as error:
    print(f"[SYSTEM] HARDWARE NOT DETECTED ({error}). Running in Mock Mode on laptop.")

    class MockRobot:
        def __init__(self):
            self.current_command = "STOP"

        def execute_command(self, command: str):
            self.current_command = command
            print(f"[MOCK HARDWARE] Motor state changed -> {command}")
            return True, f"Mock {command} executed successfully."

        def get_status(self):
            return {"command": self.current_command, "simulation": True}

    robot = MockRobot()

@app.post("/fwd")
def move_forward():
    success, message = robot.execute_command("FWD")
    return {"success": success, "message": message}

@app.post("/backwd")
def move_backward():
    success, message = robot.execute_command("BACKWD")
    return {"success": success, "message": message}

@app.post("/left")
def turn_left():
    success, message = robot.execute_command("LEFT")
    return {"success": success, "message": message}

@app.post("/right")
def turn_right():
    success, message = robot.execute_command("RIGHT")
    return {"success": success, "message": message}

@app.post("/stop")
def stop_rover():
    success, message = robot.execute_command("STOP")
    return {"success": success, "message": message}

@app.get("/status")
def get_status():
    return {"success": True, "status": robot.get_status()}
