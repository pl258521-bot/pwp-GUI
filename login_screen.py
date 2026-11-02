from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def home():
  return """
   <!DOCTYPE html>
    <html>
    <head>
        <title>Rover Login Page</title>
        <style>
            * {
                box-sizing: border-box; 
                margin: 0; 
                padding: 0; 
                font-familly sans-serif; 
            }
            
            body {
                background-color: grey
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            
            .card {
                background-color: white;
                color: black;
                padding: 20px;
                border-radius: 8px;
                display: flex;
            }
