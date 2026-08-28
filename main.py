from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from speedtest_client import get_latest_result

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def homepage():
    result = get_latest_result()    
    if result is None:
        return "<h1>Could not fetch speedtest data</h1>"
    return f"""
    <h1>Download: {result['download']}</h1>
    <h1>Upload: {result['upload']}</h1>
    <h1>Ping: {result['ping']} ms</h1>
    <p>Last updated: {result['created_at']}</p>
    """