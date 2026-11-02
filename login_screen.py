from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def home():
  return """
   <!DOCTYPE html>
    <html>
    <head>
    
      
