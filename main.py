# Parallax - A simple astronomy information collector
# Author: Gyalecta (Domenico)
# Date: 05/07/2026

import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo
from geopy.geocoders import Nominatim

load_dotenv()
api_key = os.getenv("SOLAR_API_KEY")

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def fetch_planet(name):
    """
    Retrieves a planet's data from the API by name.

    Args:
        name: the planet's name (string).

    Returns:
        The JSON containing the planet, or None if it doesn't exist / the call fails.
    """
    url = f"https://api.le-systeme-solaire.net/rest/bodies/{name.lower()}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()
    return None

def positions(lon, lat, elev, zone, date_str):
    """
    Calculates the astronomical positions of the Sun, Moon, and planets.

    Args:
        lon: longitude.
        lat: latitude.
        elev: elevation in meters (usually 0).
        zone: UTC timezone offset in hours.
        date_str: datetime formatted to the API standard.

    Returns:
        The JSON with each body's position (right ascension, declination,
        azimuth, altitude), or None if the call fails.
    """
    if lon is None or lat is None or elev is None or zone is None:
        return None
    url = f"https://api.le-systeme-solaire.net/rest/positions"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    params = {
        "lon": lon,
        "lat": lat,
        "elev": elev,
        "zone": zone,
        "datetime": date_str,
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code == 200:
        return response.json()
    return None

def get_coordinates(place):
    """
    Converts a place name into geographic coordinates. Uses Nominatim (OpenStreetMap) via geopy for geocoding.
    
    Args:
        place: name of the location to search for (e.g., "Quarto, Naples").

    Returns: 
        A (latitude, longitude) tuple, or None if the location can't be found.
    """
    geolocator = Nominatim(user_agent="parallax-astronomy-cli")
    location = geolocator.geocode(place)

    if location is None:
        return None
    
    return (location.latitude, location.longitude)

def print_visible(data):
    """
    Prints the visible bodies from the response of the "positions" function.

    Args:
        data: dictionary containing the bodies' positions.

    Prints:
        One line for each visible body (those with non-negative altitude).
    """
    if data is None:
        print("Error in retrieving the positions.")
        return
    for body in data["positions"]:
        alt = body["alt"]
        if not alt.startswith("-"):
            print(f"{body['name']}: alt {body['alt']}, az {body['az']}")


def print_planet(data):
    """
    Prints the data of a specific planet requested by the user.

    Args:
        data: the planet's data returned by fetch_planet.

    Returns:
        None. Prints the planet's name, gravity and mass, or an error
        message if data is None.
    """
    if data is not None:
        print(f"\n{GREEN}Planet found:{RESET}")
        print(f"{YELLOW}Name:{RESET} {data.get('englishName', 'Unknown')}")
        print(f"{YELLOW}Gravity:{RESET} {data.get('gravity', 'N/A')} m/s²")
        print(f"{YELLOW}Mass:{RESET} {data.get('mass', {}).get('massValue', 'N/A')} × 10^24 kg")
    else:
        print(f"\n{RED}Planet not found.{RESET}")


def show_menu():
    # Displays the main menu
    print(f"\n{CYAN}╔══════════════════════════════╗")
    print(f"║ {GREEN}PARALLAX - Astronomy Explorer{RESET}{CYAN}║")
    print(f"╚══════════════════════════════╝{RESET}")
    print("1. Search a planet")
    print("2. Visible planets")
    print("3. Exit")

while True:
    show_menu()
    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        name = input("Enter planet name: ").strip()
        data = fetch_planet(name)
        print_planet(data)
    elif choice == "2":
        place = input("\nInsert your location: ").strip()
        location = get_coordinates(place)
        if location is None:
            print("Location not found.")
        else:
            lat, lon = location
            elev = 0
            now = datetime.now(ZoneInfo("Europe/Rome"))
            zone = int(now.utcoffset().total_seconds() / 3600)
            now_str = now.strftime("%Y-%m-%dT%H:%M:%S")
            data = positions(lon, lat, elev, zone, now_str)
            print_visible(data)
    elif choice in {"3", "q", "quit"}:
        print("\nGoodbye!")
        break
    else:
        print(f"{RED}Invalid option. Try again.{RESET}")