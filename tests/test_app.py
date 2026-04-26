import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Original activities data for reset
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and creative arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Act in plays and improve theatrical skills",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:00 PM - 4:30 PM",
        "max_participants": 14,
        "participants": []
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to original state before each test"""
    activities.clear()
    activities.update(ORIGINAL_ACTIVITIES)

client = TestClient(app)

def test_get_root():
    """Test GET / serves the index.html page"""
    # Arrange: No special setup needed

    # Act: Make GET request to root
    response = client.get("/")

    # Assert: Should return 200 and the HTML content
    assert response.status_code == 200
    assert "<title>Mergington High School Activities</title>" in response.text

def test_get_activities():
    """Test GET /activities returns all activities"""
    # Arrange: Activities are reset to original state

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Should return 200 and the activities dict
    assert response.status_code == 200
    data = response.json()
    assert data == ORIGINAL_ACTIVITIES

def test_signup_successful():
    """Test POST /activities/{name}/signup for successful signup"""
    # Arrange: Use an activity with empty participants
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 200 and add participant
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate():
    """Test POST /activities/{name}/signup prevents duplicate signup"""
    # Arrange: Use an activity with existing participants
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    """Test POST /activities/{name}/signup for non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_successful():
    """Test DELETE /activities/{name}/signup for successful unregistration"""
    # Arrange: Use an activity with existing participants
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 200 and remove participant
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]

def test_unregister_not_signed_up():
    """Test DELETE /activities/{name}/signup for participant not signed up"""
    # Arrange: Use an activity and email not in participants
    activity_name = "Basketball Team"
    email = "notsignedup@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 400 with error message
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    """Test DELETE /activities/{name}/signup for non-existent activity"""
    # Arrange: Use invalid activity name
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"

    # Act: Make DELETE request to unregister
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: Should return 404 with error message
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]