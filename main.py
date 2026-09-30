from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from speedtest_client import (
    get_latest_result,
    get_result_history,
    get_stats,
    run_speedtest,
)

CSS = """
body {
    font-family: sans-serif;
    background-color: #f0f0f0;
}

h1 {
    color: #2c3e50;
    font-size: 1.5em;
}

p {
    color: #555;
}

.card {
    background-color: white;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.container {
    max-width: 800px;
    margin: 0 auto;
}
"""
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def homepage() -> str:

    latest = get_latest_result()
    stats = get_stats()
    history = get_result_history()

    if latest is None:
        return "<h1>Could not fetch latest result</h1>"
    if latest["status"] == "failed":
        return "<h1>Speedtest failed</h1>"
    if latest["status"] != "completed":
        return "<h1>Speedtest is running...</h1><meta http-equiv='refresh' content='5'>"
    if stats is None:
        return "<h1>Could not fetch stats</h1>"
    if history is None:
        return "<h1>Could not fetch history</h1>"

    history_html = ""
    failed_count = 0
    for entry in history:
        if entry["status"] == "failed":
            failed_count += 1
            continue
        if entry["status"] != "completed":
            continue
        history_html += f"<p>{entry['created_at']} — {entry['status']}: down {entry['download_bits_human']}, up {entry['upload_bits_human']}, ping {entry['ping']} ms</p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Speedtest Dashboard</title>
        <style>
        {CSS}
        </style>
    </head>
    <body>
    <div class="container">
        <div class="card">
            <h1>Download: {latest["download"]}</h1>
            <h1>Upload: {latest["upload"]}</h1>
            <h1>Ping: {latest["ping"]} ms</h1>
            <p>Last updated: {latest["created_at"]}</p>
            <p>Download elapsed: {round(latest["download_elapsed"], 2)} seconds</p>
            <p>Upload elapsed: {round(latest["upload_elapsed"], 2)} seconds</p>
            <p>Total Time elapsed: {round(latest["download_elapsed"] + latest["upload_elapsed"], 2)} seconds</p>

            <form action="/run" method="post">
                <button type="submit">Run Speedtest</button>
            </form>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <h1>Average Download: {stats["download"]["avg_bits_human"]}</h1>
            <h1>Mininmum Download: {stats["download"]["min_bits_human"]}</h1>
            <h1>Maximum Download: {stats["download"]["max_bits_human"]}</h1>

            <h1>Average Ping: {stats["ping"]["avg"]} ms</h1>
            <h1>Minimum Ping: {stats["ping"]["min"]} ms</h1>
            <h1>Maximum Ping: {stats["ping"]["max"]} ms</h1>

            <h1>Average Upload: {stats["upload"]["avg_bits_human"]}</h1>
            <h1>Maximum Upload: {stats["upload"]["max_bits_human"]}</h1>

            <p>Total Results: {stats["total_results"]}</p>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            {history_html}
            <p>Failed tests: {failed_count}</p>
        </div>
    </div>

    </body>
    </html>
    """


@app.post("/run", response_class=HTMLResponse)
def run() -> str:
    speedtest = run_speedtest()
    if speedtest is None:
        return "<h1>Could not run speedtest</h1>"
    return "<h1> Speedtest has been queued and should resolve shortly</h1><a href='/'>Back to dashboard</a>"
