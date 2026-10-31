from fastapi import FastAPI
from fastapi.middleware.cors import CORSMmiddleware
from fastapi.responses import HTMLResponse

app = FastAPI(title="GigaBite Rover Controller")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hardware Detection & Fallback Mock Mode
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


@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GigaBite Rover Dashboard</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0f172a; color: #f8fafc; padding: 20px; height: 100vh; overflow: hidden; }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 16px;
            height: calc(100vh - 40px);
        }
        
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            border-bottom: 1px solid #334155;
            padding-bottom: 8px;
        }
        
        .card-title {
            font-size: 14px;
            font-weight: 700;
            color: #38bdf8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .status-badge {
            font-size: 11px;
            background: #0284c7;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
        }
        
        .feed-container {
            flex: 1;
            background: #090d16;
            border: 2px dashed #334155;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #64748b;
            font-size: 13px;
            gap: 8px;
        }
        
        .controls-wrapper {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            gap: 12px;
        }
        
        .dpad-grid {
            display: grid;
            grid-template-columns: repeat(3, 70px);
            grid-template-rows: repeat(3, 50px);
            gap: 8px;
        }
        
        .btn-ctrl {
            background: #334155;
            color: #ffffff;
            border: 1px solid #475569;
            border-radius: 6px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .btn-ctrl:hover { background: #0284c7; border-color: #38bdf8; }
        .btn-ctrl:active { transform: scale(0.96); }
        .btn-stop { background: #991b1b; border-color: #ef4444; }
        .btn-stop:hover { background: #dc2626; }
        
        .hint-text {
            font-size: 11px;
            color: #94a3b8;
            text-align: center;
        }

        .log-box {
            flex: 1;
            background: #090d16;
            border: 1px solid #334155;
            border-radius: 6px;
            padding: 10px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 12px;
            color: #4ade80;
            overflow-y: auto;
        }

        .log-entry { margin-bottom: 4px; line-height: 1.4; }
        .log-err { color: #f87171; }
        .log-time { color: #64748b; }
    </style>
</head>
<body>
    <div class="dashboard-grid">
        <!-- Top-Left Quadrant: Camera Stream 1 -->
        <div class="card">
            <div class="card-header">
                <span class="card-title">Camera Feed (Primary)</span>
                <span class="status-badge">LIVE STREAM</span>
            </div>
            <div class="feed-container">
                <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
                <span>[ Camera Stream Placeholder ]</span>
            </div>
        </div>

        <!-- Top-Right Quadrant: Movement Control Pad -->
        <div class="card">
            <div class="card-header">
                <span class="card-title">Rover Controls</span>
                <span class="status-badge">READY</span>
            </div>
            <div class="controls-wrapper">
                <div class="dpad-grid">
                    <div></div>
                    <button class="btn-ctrl" onclick="sendCmd('fwd')">▲ FWD</button>
                    <div></div>
                    <button class="btn-ctrl" onclick="sendCmd('left')">◄ LEFT</button>
                    <button class="btn-ctrl btn-stop" onclick="sendCmd('stop')">■ STOP</button>
                    <button class="btn-ctrl" onclick="sendCmd('right')">RIGHT ►</button>
                    <div></div>
                    <button class="btn-ctrl" onclick="sendCmd('backwd')">▼ BACK</button>
                    <div></div>
                </div>
                <div class="hint-text">Keyboard shortcuts: W (Fwd), A (Left), S (Back), D (Right), Space (Stop)</div>
            </div>
        </div>

        <!-- Bottom-Left Quadrant: Camera Stream 2 / Telemetry -->
        <div class="card">
            <div class="card-header">
                <span class="card-title">Telemetry & Aux Stream</span>
                <span class="status-badge">SENSOR DATA</span>
            </div>
            <div class="feed-container">
                <svg width="32" height="32" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                <span>[ Auxiliary Stream / Sensor Telemetry ]</span>
            </div>
        </div>

        <!-- Bottom-Right Quadrant: Activity Log -->
        <div class="card">
            <div class="card-header">
                <span class="card-title">System Event Log</span>
                <span class="status-badge">ACTIVE</span>
            </div>
            <div id="log-box" class="log-box">
                <div class="log-entry"><span class="log-time">[SYSTEM]</span> Web Dashboard active. Ready for commands...</div>
            </div>
        </div>
    </div>

    <script>
        async function sendCmd(endpoint) {
            const logBox = document.getElementById('log-box');
            const timeStr = new Date().toLocaleTimeString();
            try {
                const response = await fetch('/' + endpoint, { method: 'POST' });
                const data = await response.json();
                
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                entry.innerHTML = `<span class="log-time">[${timeStr}]</span> CMD: <strong>${endpoint.toUpperCase()}</strong> &rarr; ${data.message}`;
                logBox.appendChild(entry);
                logBox.scrollTop = logBox.scrollHeight;
            } catch (err) {
                const errEntry = document.createElement('div');
                errEntry.className = 'log-entry log-err';
                errEntry.innerHTML = `<span class="log-time">[${timeStr}]</span> ERROR connecting to /${endpoint}`;
                logBox.appendChild(errEntry);
                logBox.scrollTop = logBox.scrollHeight;
            }
        }

        // WASD, Arrow keys, and Spacebar bindings
        document.addEventListener('keydown', (e) => {
            if (e.repeat) return;
            const key = e.key.toLowerCase();
            if (key === 'w' || key === 'arrowup') sendCmd('fwd');
            else if (key === 'a' || key === 'arrowleft') sendCmd('left');
            else if (key === 's' || key === 'arrowdown') sendCmd('backwd');
            else if (key === 'd' || key === 'arrowright') sendCmd('right');
            else if (key === ' ' || key === 'escape') sendCmd('stop');
        });
    </script>
</body>
</html>
"""


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
