# Parallax

Parallax is a small command-line tool to fetch solar system data and check which planets/bodies are visible from a given location.

## Requirements

Install dependencies (preferably in a virtual environment):

```bash
pip install -r requirements.txt
```

## Environment

Create a `.env` file (optional) with:

```
SOLAR_API_KEY=your_api_key_here
```

If `SOLAR_API_KEY` is not provided the app will still try to call the public API but without authentication.

## Usage

Run the CLI:

```bash
python main.py
```

Follow the interactive prompts to search for a planet or see visible bodies from your location.

## Notes

- The project uses Nominatim (OpenStreetMap) through `geopy` for geocoding. Respect the service's usage policy when making requests.
- The code now includes docstrings and type hints for easier maintenance.
