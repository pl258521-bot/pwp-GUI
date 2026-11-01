from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from robot import RobotClass

app = FastAPI()
robot = RobotClass()


@app.post("/cmd/{action}")
def handle_command(action: str):
    robot.execute_command(action)
    print(f"Hardware executed: {action.upper()}")
    return {"status": f"Rover action: {action.upper()}", "action": action.upper()}


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rover Control Dashboard</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background-color: #0f172a; color: white; font-family: sans-serif; padding: 15px; }

            .dashboard-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 15px;
                height: 95vh;
            }

            .card {
                background-color: #1e293b;
                border: 2px solid #334155;
                padding: 20px;
                border-radius: 8px;
                display: flex;
                flex-direction: column;
            }

            .card h2 {
                margin-bottom: 12px;
                font-size: 1.2rem;
                color: #94a3b8;
                border-bottom: 1px solid #334155;
                padding-bottom: 8px;
            }

            /* QUADRANT 1: CAMERA STREAM */
            .camera-box {
                flex: 1;
                background-color: #020617;
                border: 1px dashed #475569;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #64748b;
            }

            /* QUADRANT 2: CONTROLS */
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
                background-color: #2563eb;
                transition: background-color 0.2s;
            }

            button:hover { background-color: #1d4ed8; }
            button.stop { background-color: #dc2626; }
            button.stop:hover { background-color: #b91c1c; }

            #status-display {
                margin-top: 15px;
                font-weight: bold;
                color: #38bdf8;
                text-align: center;
            }

            /* QUADRANT 3: TELEMETRY */
            .telemetry-list {
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 10px;
            }

            .stat-row {
                display: flex;
                justify-content: space-between;
                background-color: #0f172a;
                padding: 10px;
                border-radius: 4px;
            }

            .stat-value { font-weight: bold; color: #4ade80; }

            /* QUADRANT 4: SYSTEM LOGS */
            #log-console {
                flex: 1;
                background-color: #020617;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
                font-size: 0.85rem;
                color: #38bdf8;
                overflow-y: auto;
                max-height: 250px;
            }

            .log-entry { margin-bottom: 4px; }
        </style>
    </head>
    <body>

        <div class="dashboard-grid">
            <!-- Quadrant 1: Camera Feed -->
            <div class="card">
                <h2>Quadrant 1: Camera Stream</h2>
                <div class="camera-box">
                    <p>[ LIVE STREAM PLACEHOLDER ]</p>
                </div>
            </div>

            <!-- Quadrant 2: Rover Controls -->
            <div class="card">
                <h2>Quadrant 2: Controls</h2>
                <div class="d-pad">
                    <button onclick="sendCmd('forward')">FORWARD</button>
                    <div class="row">
                        <button onclick="sendCmd('left')">LEFT</button>
                        <button class="stop" onclick="sendCmd('stop')">STOP</button>
                        <button onclick="sendCmd('right')">RIGHT</button>
                    </div>
                    <button onclick="sendCmd('backward')">BACKWARD</button>
                </div>
                <p id="status-display">Status: Standing by...</p>
            </div>

            <!-- Quadrant 3: Telemetry Readout -->
            <div class="card">
                <h2>Quadrant 3: Telemetry</h2>
                <div class="telemetry-list">
                    <div class="stat-row">
                        <span>Connection:</span>
                        <span class="stat-value">ONLINE (Wi-Fi)</span>
                    </div>
                    <div class="stat-row">
                        <span>Battery Voltage:</span>
                        <span class="stat-value">7.4 V</span>
                    </div>
                    <div class="stat-row">
                        <span>Motor Duty Cycle:</span>
                        <span class="stat-value">100%</span>
                    </div>
                    <div class="stat-row">
                        <span>CPU Temp:</span>
                        <span class="stat-value">42°C</span>
                    </div>
                </div>
            </div>

            <!-- Quadrant 4: System Console Logs -->
            <div class="card">
                <h2>Quadrant 4: Activity Log</h2>
                <div id="log-console">
                    <div class="log-entry">[SYSTEM INITIALIZED] Ready for input.</div>
                </div>
            </div>
        </div>

        <script>
            async function sendCmd(command) {
                const response = await fetch('/cmd/' + command, { method: 'POST' });
                const data = await response.json();

                // Update Quadrant 2 status
                document.getElementById('status-display').innerText = "Status: " + data.status;

                // Append timestamped log entry to Quadrant 4
                const logConsole = document.getElementById('log-console');
                const timeString = new Date().toLocaleTimeString();
                const newLog = document.createElement('div');
                newLog.className = 'log-entry';
                newLog.innerText = `[${timeString}] Command executed: ${data.action}`;

                logConsole.appendChild(newLog);
                logConsole.scrollTop = logConsole.scrollHeight; // Auto-scroll to latest log
            }
        </script>

    </body>
    </html>
    """
