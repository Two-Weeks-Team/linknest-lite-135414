import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from models import Base, engine
from routes import router

app = FastAPI(title="LinkNest Lite API", version="0.1.0")

# Create tables at startup
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

# Health check
@app.get("/health", response_model=dict)
def health() -> dict:
    return {"status": "ok"}

# Landing page – dark themed
@app.get("/", response_class=HTMLResponse)
def root() -> str:
    html = """
    <html>
    <head>
        <title>LinkNest Lite</title>
        <style>
            body {background-color:#121212;color:#e0e0e0;font-family:Arial,Helvetica,sans-serif;margin:0;padding:2rem;}
            a {color:#90caf9;}
            h1 {color:#ffcc80;}
            .box {background:#1e1e1e;padding:1rem;margin-top:1rem;border-radius:8px;}
            table {width:100%;border-collapse:collapse;}
            th, td {padding:0.5rem;border:1px solid #333;}
            th {background:#2c2c2c;}
        </style>
    </head>
    <body>
        <h1>LinkNest Lite</h1>
        <p>Simple bookmark saver with instant search – no login, no AI, just fast access.</p>
        <div class="box">
            <h2>API Endpoints</h2>
            <table>
                <tr><th>Method</th><th>Path</th><th>Description</th></tr>
                <tr><td>GET</td><td>/health</td><td>Health check</td></tr>
                <tr><td>POST</td><td>/api/bookmarks</td><td>Create a new bookmark</td></tr>
                <tr><td>GET</td><td>/api/bookmarks</td><td>List bookmarks (optional ?q=keyword)</td></tr>
                <tr><td>GET</td><td>/api/bookmarks/{id}</td><td>Retrieve a bookmark</td></tr>
                <tr><td>PUT</td><td>/api/bookmarks/{id}</td><td>Update a bookmark</td></tr>
                <tr><td>DELETE</td><td>/api/bookmarks/{id}</td><td>Delete a bookmark</td></tr>
                <tr><td>POST</td><td>/api/ai/generate-tags</td><td>Generate AI tags for a URL</td></tr>
                <tr><td>POST</td><td>/api/ai/semantic-search</td><td>Semantic search over bookmarks</td></tr>
            </table>
        </div>
        <div class="box">
            <h2>Tech Stack</h2>
            <ul>
                <li>FastAPI 0.115.0 (Python 3.13)</li>
                <li>PostgreSQL (via SQLAlchemy 2.0.35)</li>
                <li>DigitalOcean Serverless Inference (openai-gpt-oss-120b)</li>
                <li>uvicorn 0.30.0</li>
            </ul>
        </div>
        <p>API docs: <a href="/docs">/docs</a> | <a href="/redoc">/redoc</a></p>
    </body>
    </html>
    """
    return html

# Include API router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8080)))