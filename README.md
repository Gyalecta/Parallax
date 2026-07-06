# Parallax

Parallax is a small command-line tool to fetch solar system data and check which planets and celestial bodies are visible from a given location.

## Requirements

Install dependencies (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

## API Key

Parallax uses the [Le Système Solaire](https://api.le-systeme-solaire.net/) API, which requires a free bearer token.

1. Request a key at https://api.le-systeme-solaire.net/generatekey.html (an active email is enough).
2. Create a `.env` file in the project root with:
```
SOLAR_API_KEY=your_api_key_here
```

The key is required — without it the API returns a 401 and the app won't retrieve any data.

## Usage

Run the CLI:

```bash
python main.py
```

Follow the interactive prompts to search for a planet or list the bodies currently visible from your location.

## Notes

- Geocoding is handled by Nominatim (OpenStreetMap) via `geopy`. Please respect its [usage policy](https://operations.osmfoundation.org/policies/nominatim/) — max 1 request per second.
- All functions include docstrings for easier maintenance.
