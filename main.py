from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from speedtest_client import get_latest_result, get_stats

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def homepage() -> str:
    result = get_latest_result()    
    stats = get_stats()
    if result is None:
        return "<h1>Could not fetch speedtest data</h1>"
    if stats is None:
        return "<h1>Could not fetch stats</h1>"
    return f"""
    <h1>Download: {result['download']}</h1>
    <h1>Upload: {result['upload']}</h1>
    <h1>Ping: {result['ping']} ms</h1>
    <p>Last updated: {result['created_at']}</p>

    <h1>Average Download: {stats['download']['avg_bits_human']}</h1>
    <h1>Mininmum Download: {stats['download']['min_bits_human']}</h1>
    <h1>Maximum Download: {stats['download']['max_bits_human']}</h1>

    <h1>Average Ping: {stats['ping']['avg']} ms</h1>
    <h1>Minimum Ping: {stats['ping']['min']} ms</h1>
    <h1>Maximum Ping: {stats['ping']['max']} ms</h1>

    <h1>Average Upload: {stats['upload']['avg_bits_human']}</h1>
    <h1>Maximum Upload: {stats['upload']['max_bits_human']}</h1>

    <p>Total Results: {stats['total_results']}</p>
    """
