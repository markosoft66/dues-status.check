# CoSSA Portal - Student Dues Verification System

A secure Flask application for verifying student dues records from Google Sheets. Features fast search capabilities, admin authentication, and automatic data caching.

## Features

- **Secure Login**: Admin authentication with brute force protection (2-second delay on failed attempts)
- **Fast Search**: Query student records by ID or full name with 10-minute data caching
- **Real-time Data**: Syncs with multiple Google Sheets automatically
- **Session Management**: Auto-timeout after 10 minutes of inactivity
- **Responsive UI**: Clean, modern interface with instant search feedback

## Tech Stack

- **Backend**: Flask (Python)
- **Data Processing**: Pandas
- **Frontend**: HTML/CSS (Jinja2 templating)
- **Environment**: Python dotenv

## Installation

### Prerequisites
- Python 3.7+
- Google Sheets URLs (configured in `.env`)

### Setup

1. Clone the repository and navigate to the directory:
   ```bash
   cd dueschecker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with the following variables:
   ```
   FLASK_SECRET_KEY=your_secret_key_here
   ADMIN_USERNAME=your_admin_username
   ADMIN_PASSWORD=your_admin_password
   SHEET_1_URL=https://docs.google.com/spreadsheets/export?gid=0&format=csv&url=your_sheet_url
   SHEET_2_URL=https://docs.google.com/spreadsheets/export?gid=0&format=csv&url=your_sheet_url
   ```

4. Run the application:
   ```bash
   flask run
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
dueschecker/
├── app.py                 # Main Flask application
├── data_handler.py        # CSV fetching and caching logic
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── vercel.json            # Vercel deployment config
└── templates/
    ├── login.html         # Login page
    └── search.html        # Search results page
```

## How It Works

1. **Login**: Authenticate with admin credentials
2. **Initial Load**: Page loads instantly without fetching data
3. **Search**: Submit query to fetch and cache data (first search only)
4. **Cache**: Subsequent searches use cached data for 10 minutes
5. **Auto-refresh**: Data automatically updates every 10 minutes

## API Endpoints

- `GET/POST /login` - Admin login page
- `GET/POST /search` - Dues record search (requires login)
- `GET /logout` - Logout and clear session

## Performance Optimization

- **Lazy Loading**: Data only fetches on first search, not on page load
- **10-minute Cache**: Prevents excessive API calls to Google Sheets
- **Session Timeout**: 10-minute inactivity timeout for security
- **Brute Force Protection**: 2-second delay on failed login attempts

## Security Features

- Environment variable protection for sensitive data
- Session-based authentication
- CSRF protection via Flask sessions
- Rate limiting on login attempts

## Deployment

For Vercel deployment, the `vercel.json` configuration is already set up.

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `FLASK_SECRET_KEY` | Secret key for session management |
| `ADMIN_USERNAME` | Admin login username |
| `ADMIN_PASSWORD` | Admin login password |
| `SHEET_*_URL` | Google Sheets export URLs (supports multiple sheets) |

## Troubleshooting

- **Slow initial load**: This is expected on first search to fetch remote data
- **"No records found"**: Verify the search ID/Name and sheet URL configuration
- **Session timeout**: Re-login after 10 minutes of inactivity

## License

Proprietary - CoSSA Student Organization
