# atc_api.py
from fastapi import FastAPI, HTTPException
import uvicorn
import subprocess
import sys
import json
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlaneCreate(BaseModel):
    plane_id: str
    state: str  # 'air' or 'ground'
    position: str
    target: str
    origin_country: Optional[str] = None
    destination_country: str
    plane_model: Optional[str] = "Unknown"
    plane_size: Optional[int] = 0
    plane_pascount: Optional[int] = 0

@app.get("/planes")
async def get_planes():
    with open("data/plane_data.txt", 'r') as f:
        return json.load(f)

@app.get("/airspaces")
async def get_airspaces():
    with open("data/airspaces.txt", 'r') as f:
        return json.load(f)

@app.get("/runways")
async def get_runways():
    with open("data/runways.txt", 'r') as f:
        return json.load(f)

@app.get("/loading")
async def get_loading():
    with open("data/loading.txt", 'r') as f:
        return json.load(f)

@app.get("/messages")
async def get_messages():
    try:
        with open("data/messages.txt", 'r') as f:
            return {"messages": json.load(f)}
    except FileNotFoundError:
        return {"messages": []}

@app.get("/system-status")
async def get_system_status():
    return {
        "airplanes": json.load(open("data/plane_data.txt")),
        "airspaces": json.load(open("data/airspaces.txt")),
        "runways": json.load(open("data/runways.txt")),
        "loading": json.load(open("data/loading.txt")),
        "messages": json.load(open("data/messages.txt"))
    }

@app.post("/planes")
async def create_plane(plane: PlaneCreate):
    plane.plane_id = plane.plane_id.strip()
    
    # Validation
    if plane.state == 'air':
        if plane.position != 'outer_airspace' or plane.target not in ['runway_1', 'runway_2']:
            raise HTTPException(status_code=400, detail="For state=air, position must be 'outer_airspace' and target must be a runway")
    elif plane.state == 'ground':
        if plane.position != 'loading' or plane.target not in ['runway_1', 'runway_2']:
            raise HTTPException(status_code=400, detail="For state=ground, position must be 'loading' and target must be a runway")
    else:
        raise HTTPException(status_code=400, detail="State must be either 'air' or 'ground'")
    
    planes = json.load(open("data/plane_data.txt"))
    if plane.plane_id in planes:
        raise HTTPException(status_code=400, detail="Plane with this ID already exists")

    try:
        subprocess.Popen([
            sys.executable, 
            "airplane.py",
            plane.plane_id,
            plane.state,
            plane.position,
            plane.target,
            plane.origin_country,
            plane.destination_country
        ])
        
        planes[plane.plane_id] = {
            "plane_id": plane.plane_id,
            "state": plane.state,
            "position": plane.position,
            "target": plane.target,
            "origin_country": plane.origin_country or "",
            "destination_country": plane.destination_country or "",
            "plane_model": plane.plane_model,
            "plane_size": plane.plane_size,
            "plane_pascount": plane.plane_pascount
        }
        
        with open("data/plane_data.txt", 'w') as f:
            json.dump(planes, f, indent=4)
            
        return {"message": f"Plane {plane.plane_id} created and launched successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)