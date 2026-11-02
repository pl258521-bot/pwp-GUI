from fastapi import FastAPI
from fastapi.responses import HTMLResponse

try:
    from robot import RobotClass
except (ModuleNotFoundError, ImportError):
    class RobotClass:
        def execute_command(self, action: str):
            print(f"[MOCK HARDWARE] Command sent: {action.upper()}")
            return True, f"Rover action: {action.upper()}"

app = FastAPI()
robot = RobotClass()


@app.post("/cmd/{action}")
def handle_command(action: str):
    cmd = action.upper()
    result = robot.execute_command(cmd)

    # Handle tuple returned by real robot.py vs mock fallback
    if isinstance(result, tuple):
        _, message = result
    else:
        message = f"Rover action: {cmd}"

    print(f"Hardware executed: {cmd}")
    return {"status": message}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rover Control Dashboard</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }

            body { background-color: white; color: black; font-family: sans-serif; padding: 15px; }

            .dashboard-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 15px;
                height: 95vh;
            }

            .card {
                background-color: black;
                color: white;
                padding: 20px;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
            }

            .card h2 {
                margin-bottom: 12px;
                font-size: 1.2rem;
                color: white;
                border-bottom: 1px solid #334155;
                padding-bottom: 8px;
            }

            .camera-box {
                flex: 1;
                background-color: black;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: grey;
            }

            /* controls */
            .d-pad {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 8px;
                margin-top: 10px;
            }

            .row { display: flex; gap: 8px; }

            button {
                color: white;
                border: none;
                padding: 12px 20px;
                font-weight: bold;
                cursor: pointer;
                border-radius: 6px;
                background-color: grey;
            }

            button.stop { background-color: #dc2626; }

            #status-display {
                margin-top: 15px;
                font-weight: bold;
                color: #38bdf8;
                text-align: center;
            }
        </style>
    </head>
    <body>

        <div class="dashboard-grid">
            <div class="card">
                <h2>Video Stream 1</h2>
                <div class="camera-box">
                    <p>[ LIVE STREAM 1 PLACEHOLDER ]</p>
                </div>
            </div>

            <div class="card">
                <h2>Controls</h2>
                <div class="d-pad">
                    <button onclick="sendCmd('FWD')">FORWARD</button>
                    <div class="row">
                        <button onclick="sendCmd('LEFT')">LEFT</button>
                        <button class="stop" onclick="sendCmd('STOP')">STOP</button>
                        <button onclick="sendCmd('RIGHT')">RIGHT</button>
                    </div>
                    <button onclick="sendCmd('BACKWD')">BACKWARD</button>
                </div>
                <p id="status-display">Status: Standing by...</p>
            </div>

            <div class="card">
                <h2>Video Stream 2</h2>
                <div class="camera-box">
                    <p>[ LIVE STREAM 2 PLACEHOLDER ]</p>
                </div>
            </div>

            <div class="card">
                <h2>User Log</h2>
            </div>
        </div>

        <script>
            async function sendCmd(command) {
                const response = await fetch('/cmd/' + command, { method: 'POST' });
                const data = await response.json();
                document.getElementById('status-display').innerText = "Status: " + data.status;
            }
        </script>

    </body>
    </html>
    """
