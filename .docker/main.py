from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

status_data = {
    "status": "active",
    "failure": True
}

@app.get("/status")
async def get_status():
    """Get current status"""
    return JSONResponse(status_data)

@app.post("/status")
async def update_status(new_status: dict):
    global status_data 
    status_data = new_status
    return JSONResponse(status_data)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({"ok": True})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)