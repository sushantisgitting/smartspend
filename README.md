# Budget App 💰

A modern full-stack budget management application built with FastAPI. Track your income, expenses, and manage multiple accounts with an intuitive mobile-first interface.

## 🌟 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Multiple Accounts**: Create and manage multiple financial accounts with custom icons
- **Category Management**: Organize transactions with customizable expense and income categories
- **Transaction Tracking**: Record and view detailed transaction history
- **Real-time Balance**: Track total budget across all accounts
- **Responsive Design**: Mobile-first design with smooth animations and intuitive UI
- **Dark Theme**: Modern dark interface optimized for readability

## 🏗️ Architecture

### Backend (FastAPI)
- **Framework**: FastAPI with SQLAlchemy ORM
- **Database**: PostgreSQL with SSL support
- **Authentication**: JWT-based authentication with Argon2 password hashing
- **Architecture**: Repository pattern with service layer separation
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

### Frontend (React)
- **Framework**: React 18 with React Router
- **State Management**: Context API for authentication
- **HTTP Client**: Axios with interceptors
- **Styling**: Pure CSS with modern design patterns
- **Responsive**: Mobile-first responsive design

## 📁 Project Structure

```
budget-app/
├── app/                          # Backend application
│   ├── core/                     # Core configuration
│   │   ├── config.py            # Settings and environment variables
│   │   └── database.py          # Database connection and session
│   ├── models/                   # SQLAlchemy models
│   │   ├── user.py              # User model
│   │   ├── account.py           # Account model
│   │   ├── category.py          # Category model
│   │   └── operation.py         # Operation/Transaction model
│   ├── repositories/             # Data access layer
│   ├── services/                 # Business logic layer
│   ├── routes/                   # API endpoints
│   ├── schemas/                  # Pydantic schemas
│   └── main.py                   # Application entry point
│
└── src/                          # Frontend application
    ├── components/               # Reusable components
    │   ├── common/              # Common UI components
    │   └── layout/              # Layout components
    ├── pages/                    # Page components
    │   ├── Auth/                # Authentication page
    │   ├── Home/                # Dashboard/Home page
    │   ├── History/             # Transaction history
    │   ├── Accounts/            # Account management
    │   ├── Settings/            # User settings
    │   └── Calculator/          # Transaction input
    ├── context/                  # React Context
    ├── services/                 # API services
    ├── routes/                   # Route configuration
    └── utils/                    # Utility functions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL database

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd budget-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ```

5. **Run the backend**
   ```bash
   uvicorn app.main:app --reload
   ```
   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd src
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure API endpoint**
   
   Update `API_BASE_URL` in `src/services/api.js` if needed

4. **Run the development server**
   ```bash
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

## 📊 Database Schema

### Users
- Email, username, and hashed password
- Created/updated timestamps

### Accounts
- User-specific accounts with name, balance, currency, and icon
- Tracks financial accounts (bank, cash, cards, etc.)

### Categories
- Expense and income categories
- Custom icons and colors
- User-specific customization

### Operations
- Financial transactions linking accounts and categories
- Amount, description, and operation date
- Automatic balance updates

## 🔐 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Users
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `DELETE /users/me` - Delete user account

### Accounts
- `GET /accounts/` - Get all user accounts
- `POST /accounts/` - Create new account
- `GET /accounts/{id}` - Get specific account
- `PUT /accounts/{id}` - Update account
- `DELETE /accounts/{id}` - Delete account
- `GET /accounts/balance` - Get total balance

### Categories
- `GET /categories/` - Get all categories
- `POST /categories/` - Create new category
- `GET /categories/with-balances` - Get categories with totals
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

### Operations
- `GET /operations/` - Get all operations (with filters)
- `POST /operations/` - Create new operation
- `GET /operations/details` - Get operations with details
- `PUT /operations/{id}` - Update operation
- `DELETE /operations/{id}` - Delete operation

## 🎨 Key Features

### Smart Calculator
- Custom calculator interface for entering transaction amounts
- Keyboard support for faster input
- Visual feedback and error handling

### Account Selector
- Visual selection of accounts when creating transactions
- Real-time balance display
- Icon-based identification

### Category Management
- Pre-populated default categories
- Custom category creation with icons
- Separate expense and income categories

### Transaction History
- Grouped by date (Today, Yesterday, specific dates)
- Color-coded by transaction type
- Detailed view with category and account information

## 🔧 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation
- **python-jose** - JWT token handling
- **passlib** - Password hashing with Argon2
- **PostgreSQL** - Production database

### Frontend
- **React** - UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Context API** - State management
- **CSS3** - Modern styling with animations

## 📱 Responsive Design

The application is fully responsive with:
- Mobile-first approach
- Tablet optimization
- Desktop layouts
- Touch-friendly interface
- Smooth animations and transitions

## 🛡️ Security

- Password hashing with Argon2
- JWT token-based authentication
- Protected API endpoints
- CORS configuration
- SQL injection prevention via ORM
- Input validation with Pydantic


-
