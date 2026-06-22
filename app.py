from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def vercel_home():
    return """
    <html>
        <head>
            <title>Salon Solutions</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 720px;
                    margin: 64px auto;
                    padding: 0 24px;
                    line-height: 1.5;
                }
                code {
                    background: #f3f4f6;
                    padding: 2px 6px;
                    border-radius: 4px;
                }
            </style>
        </head>
        <body>
            <h1>Salon Solutions</h1>
            <p>
                This repository contains a Streamlit application. Vercel's Python runtime
                needs an ASGI/WSGI <code>app</code> entrypoint, so this module exports one
                for deployment compatibility.
            </p>
            <p>
                To run the actual ERP UI, use Streamlit locally or deploy it on a platform
                that supports persistent Streamlit processes.
            </p>
        </body>
    </html>
    """

