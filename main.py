from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Import hardware driver or go to mock mode for laptop testing
try:
    from robot import RobotClass
except (ModuleNotFoundError, ImportError):
    class RobotClass:
        def execute_command(self, action: str):
            print(f"[MOCK HARDWARE] Command sent: {action.upper()}")
            return True, f"Rover action: {action.upper()}"

app = FastAPI()
robot = RobotClass()

# Serve static assets (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the main dashboard page
@app.get("/")
def home():
    return FileResponse("static/index.html")

# Receive motor commands from dashboard
@app.post("/cmd/{action}")
def handle_command(action: str):
    cmd = action.upper()
    result = robot.execute_command(cmd)

    if isinstance(result, tuple):
        _, message = result
    else:
        message = f"Rover action: {cmd}"

    print(f"Hardware executed: {cmd}")
    return {"status": message}
