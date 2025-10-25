# backend/tests/test_users.py

from fastapi.testclient import TestClient
from backend.app.main import app # Go up one level (from tests/ to backend/) and import main # Your main FastAPI application instance

# 1. Initialize the Test Client
client = TestClient(app)

# Note: For real-world testing with database changes, you should override 
# the `get_db` dependency to use a separate, temporary test database 
# (e.g., SQLite in-memory). For simplicity here, we assume a fresh start or 
# will clean up between tests.

# backend/tests/test_users.py (continued)

def test_register_user_success():
    # Arrange: Define the valid input data
    new_user_data = {
        "name": "Jane Doe",  # <--- CHANGED FROM "full_name"
        "email": "jane.doe@smartbank.com",
        "password": "Secure6!"
    }
    
    # Act: Send the POST request to the /register endpoint
    response = client.post("/auth/register", json=new_user_data)

    if response.status_code == 422:
        print("\n--- 422 Validation Error Details ---")
        print(response.json())
        print("------------------------------------")
    
    # Assert 1: Check the HTTP status code
    assert response.status_code == 200 
    
    # Assert 2: Check the response data structure (schemas.UserOut)
    response_data = response.json()
    assert "id" in response_data
    assert response_data["email"] == "jane.doe@smartbank.com"
    assert response_data["full_name"] == "Jane Doe"
    
    # Assert 3: Crucially, ensure the password field is NOT returned
    assert "password" not in response_data
    assert "hashed_password" not in response_data

# backend/tests/test_users.py (continued)

def test_register_user_already_exists():
    # Arrange: Define the user data
    existing_user_data = {
        "name": "Existing User", # <--- CHANGED FROM "full_name"
        "email": "exists@smartbank.com",
        "password": "Secure6!"
    }
    
    # Setup: Register the user first to make them "exist"
    # We use client.post directly to set up the necessary state
    client.post("/auth/register", json=existing_user_data) 
    
    # Act: Attempt to register the SAME user email again
    response = client.post("/auth/register", json=existing_user_data)
    
    # Assert 1: Check the HTTP status code (should be 400 Bad Request)
    assert response.status_code == 400
    
    # Assert 2: Check the error detail message
    assert response.json()["detail"] == "Email already registered"