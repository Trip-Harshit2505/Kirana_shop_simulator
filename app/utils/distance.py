import math

# Distance calculation using Haversine formula

# This utility function calculates the distance between two geographical points (latitude and longitude) using the Haversine formula, which accounts for the curvature of the Earth. The distance is returned in kilometers. This function is used in both warehouse_service and shipping_service to determine distances for finding nearest warehouses and calculating shipping charges based on distance. 

# **(use Chatgpt to explain the code in more detail)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c