# Wedding Website

A wedding RSVP web application for Isabella and Joshua's engagement party and wedding.

## Features

- RSVP forms for engagement party (23 May 2026) and wedding (22 May 2027)
- Registry page with QR code
- Admin dashboard for viewing and exporting RSVPs

## Tech Stack

- **Frontend**: Vue 3, Tailwind CSS, Vite
- **Backend**: Python FastAPI, SQLAlchemy, SQLite

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
# Edit .env to set your ADMIN_PASSWORD, SECRET_KEY, and REGISTRY_URL

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install

# Create .env file from example
cp .env.example .env

# Run development server
npm run dev
```

## Configuration

### Backend (.env)

```
ADMIN_PASSWORD=your_secure_password
SECRET_KEY=your_random_secret_key
REGISTRY_URL=https://your-registry-url.com
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:8000/api
```

## Usage

1. Start the backend server (runs on http://localhost:8000)
2. Start the frontend dev server (runs on http://localhost:5173)
3. Visit http://localhost:5173 to view the site
4. Access admin dashboard at /admin with your configured password
