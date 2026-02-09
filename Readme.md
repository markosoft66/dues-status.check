# CoSSA Portal - Dues Checker

A secure student dues verification system built with Flask.

 **Full documentation and setup instructions are available in [dueschecker/README.md](dueschecker/README.md)**

## Quick Start

```
cd dueschecker
pip install -r requirements.txt
flask run
```

Then navigate to 
```http://127.0.0.1:5000```

## Key Features

-  Secure admin login with brute force protection
-  Fast search by student ID or name
-  Real-time Google Sheets integration
-  Smart 10-minute caching for performance
-  Auto-logout after 10 minutes of inactivity

## Project Structure

```
dueschecker/                    # Main application folder
 app.py                      # Flask application
 data_handler.py             # Data fetching & caching
 requirements.txt            # Dependencies
 README.md                   # Full documentation
 templates/                  # HTML templates
```

See [dueschecker/README.md](dueschecker/README.md) for complete setup and deployment instructions.
