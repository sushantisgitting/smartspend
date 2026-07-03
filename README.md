# SmartSpend

Full-stack financial analytics platform for tracking expenses and managing personal finances.

## Tech Stack

- **Frontend**: React, Redux
- **Backend**: FastAPI, Python
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Testing**: pytest
- **Deployment**: Docker, GitHub Actions CI/CD

## Features

- Auto-categorizes transactions across 10+ categories
- Real-time expense analytics dashboard
- Secure JWT authentication with password hashing
- Optimized database queries with indexing
- Comprehensive API test coverage

## Getting Started

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

API runs on `http://localhost:8000`
Frontend runs on `http://localhost:3000`

## Project Structure

```
SmartSpend/
├── backend/          # FastAPI application
├── frontend/         # React application
└── docker-compose.yml
```

Built on open-source expense tracker implementations with custom enhancements.
