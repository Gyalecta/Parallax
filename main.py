# Parallax - A simple astronomy information collector
# Author: Gyalecta (Domenico)
# Date: 05/07/2026

import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SOLAR_API_KEY")

RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"


def fetch_planet(name):
    url = f"https://api.le-systeme-solaire.net/rest/bodies/{name.lower()}"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        return response.json()
    return None


def print_planet(data):
    if data is not None:
        print(f"\n{GREEN}Planet found:{RESET}")
        print(f"{YELLOW}Name:{RESET} {data.get('englishName', 'Unknown')}")
        print(f"{YELLOW}Gravity:{RESET} {data.get('gravity', 'N/A')} m/s²")
        print(f"{YELLOW}Mass:{RESET} {data.get('mass', {}).get('massValue', 'N/A')} × 10^24 kg")
    else:
        print(f"\n{RED}Planet not found.{RESET}")


def show_menu():
    print(f"\n{CYAN}╔══════════════════════════════╗")
    print(f"║ {GREEN}PARALLAX - Astronomy Explorer{RESET}{CYAN}║")
    print(f"╚══════════════════════════════╝{RESET}")
    print("1. Search a planet")
    print("2. Exit")


while True:
    show_menu()
    choice = input("\nChoose an option: ").strip()

    if choice == "1":
        name = input("Enter planet name: ").strip()
        data = fetch_planet(name)
        print_planet(data)
    elif choice in {"2", "q", "quit"}:
        print("\nGoodbye!")
        break
    else:
        print(f"{RED}Invalid option. Try again.{RESET}")