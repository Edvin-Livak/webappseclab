#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

BASE = "http://localhost:3000"

def get_flash_messages(html: str):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    return text

def signup_probe(username: str, password: str, plate: str):
    data = {
        "username": username,
        "password": password,
        "plate": plate,
    }
    r = requests.post(f"{BASE}/signup", data=data, allow_redirects=True)
    text = get_flash_messages(r.text)
    return r.status_code, text

def login(session: requests.Session, username: str, password: str):
    data = {
        "username": username,
        "password": password,
    }
    r = session.post(f"{BASE}/login", data=data, allow_redirects=True)
    return r.status_code, get_flash_messages(r.text)

def park_probe(session: requests.Session, plate: str, location: str, mintime: str = "1"):
    data = {
        "licensePlate": plate,
        "location": location,
        "mintime": mintime,
    }
    r = session.post(f"{BASE}/park", data=data, allow_redirects=True)
    return r.status_code, get_flash_messages(r.text)

if __name__ == "__main__":
    print("Testing signup oracle...")
    code, text = signup_probe("tmpuser123", "Passw0rd!", "ABC123")
    print(code)
    print(text[:1000])

    print("\nTesting logged-in parking oracle...")
    s = requests.Session()
    code, text = login(s, "yourtestuser", "yourtestpassword")
    print(code)
    print(text[:1000])

    code, text = park_probe(s, "ABC123", "1")
    print(code)
    print(text[:1000])