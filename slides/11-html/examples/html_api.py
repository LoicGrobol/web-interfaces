from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_items():
    html_content = """
    <html>
        <head>
            <title>What is the Average Flying Speed of an African Sparrow?</title>
        </head>
        <body>
            <h1>What is the Average Flying Speed of an African Sparrow?</h1>
            <p>The airspeed velocity of an unladen swallow is something like 20.1 miles per hour or 9 meters per second</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
