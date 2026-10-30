from fastapi import FastAPI
from fastapi.middleware.cors import CORSMmiddleware
from robot import RobotClass

app = FastAPI(title="GigaBite Rover Controller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

robot = RobotClass()

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
