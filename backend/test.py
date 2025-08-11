import requests
import json
import random
import string

BASE_URL = "http://localhost:8000"

def generate_plane_id():
    """Generate random plane ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def test_create_plane():
    """Test creating a new plane"""
    data = {
        "plane_id": generate_plane_id(),  # Use random ID
        "state": "air",
        "position": "outer_airspace",
        "target": "runway_1"
    }
    
    response = requests.post(f"{BASE_URL}/planes", json=data)
    print(f"Create Plane Response: {response.status_code} - {response.text}")
    return data['plane_id']  # Return the ID for cleanup

def cleanup_plane(plane_id):
    """Remove test plane"""
    # You'll need to implement a DELETE endpoint or let the plane complete its cycle
    print(f"Plane {plane_id} should complete its lifecycle automatically")

if __name__ == "__main__":
    print("Testing API Endpoints\n")
    plane_id = test_create_plane()
    cleanup_plane(plane_id)