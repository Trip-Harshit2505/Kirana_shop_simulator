from app.utils.distance import calculate_distance

# Test cases for distance calculation utility function in app/utils/distance.py

def test_distance_zero():
    distance = calculate_distance(10, 10, 10, 10)
    assert round(distance, 2) == 0

def test_distance_positive():
    distance = calculate_distance(12.9716, 77.5946, 28.7041, 77.1025)
    assert distance > 0