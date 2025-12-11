# 💰 Expense Tracker Dashboard

A modern, full-stack expense tracking application with email OTP authentication, beautiful UI, and comprehensive analytics.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 Authentication
- **Email OTP Verification** - Secure signup with 6-digit OTP sent to email
- **JWT Token Authentication** - Secure session management
- **Persistent Sessions** - Stay logged in across browser sessions

### 💸 Expense Management
- **Add Expenses** - Track date, category, amount, and notes
- **List & Filter** - View all expenses with filtering by date range and category
- **Edit & Delete** - Full CRUD operations on expenses
- **Multiple Categories** - Food, Transport, Entertainment, Shopping, Bills, Healthcare, Education, Other

### 📊 Analytics Dashboard
- **Total Spending** - Real-time calculation of all expenses
- **Category-wise Summary** - Breakdown by spending categories
- **Interactive Charts** - Pie charts and bar graphs with Chart.js
- **Monthly Statistics** - Track current month spending
- **Average Calculations** - Average expense per entry

### 🎨 User Experience
- **Beautiful Modern UI** - Professional gradient design with smooth animations
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Toast Notifications** - Real-time feedback for all actions
- **Loading States** - Visual feedback during API calls
- **Indian Rupee (₹) Support** - Localized currency formatting

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with type hints
- **SQLite** - Lightweight database
- **JWT (Jose)** - Token-based authentication
- **Argon2** - Secure password hashing
- **SMTP** - Email sending for OTP verification
- **Python-dotenv** - Environment configuration

### Frontend
- **Vanilla JavaScript (ES6+)** - No framework dependencies
- **HTML5 & CSS3** - Modern web standards
- **Chart.js** - Beautiful, responsive charts
- **Font Awesome** - Icon library
- **Google Fonts (Inter)** - Professional typography

## 📋 Requirements

- Python 3.10 or higher
- Gmail account (for sending OTP emails)
- Modern web browser

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd expense-tracker
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Edit the `.env` file with your credentials:

```env
# Email Configuration (Required for OTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com

# Security
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///./expenses.db
```

**📧 Gmail Setup:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Step Verification
3. Go to [App Passwords](https://myaccount.google.com/apppasswords)
4. Generate an app password for "Mail"
5. Use that 16-character password as `SMTP_PASSWORD`

> **Note:** If SMTP credentials are empty, OTPs will print to the backend console (development mode)

### 5. Run the Application

**Start Backend (Terminal 1):**
```bash
uvicorn backend.main:app --reload
```
Backend runs at: http://127.0.0.1:8000

**Start Frontend (Terminal 2):**
```bash
python serve_frontend.py
```
Frontend runs at: http://localhost:3000

### 6. Access the Application

Open your browser and go to: **http://localhost:3000**

## 📖 Usage Guide

### First Time Setup
1. **Sign Up:**
   - Enter your email address
   - Receive 6-digit OTP via email
   - Enter OTP, choose username and password
   - Account created and auto-logged in!

2. **Add Your First Expense:**
   - Click "Add Expense" in navigation
   - Fill in date, category, amount, and optional note
   - Submit the form

3. **View Analytics:**
   - Navigate to "Analytics" to see spending insights
   - View pie charts and category breakdowns

### Returning Users
- **Login:** Use your username and password
- **Logout:** Click logout button in top-right corner

## 📁 Project Structure

```
expense-tracker/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLModel database models
│   ├── schemas.py           # Pydantic request/response schemas
│   ├── database.py          # Database connection and setup
│   ├── config.py            # Configuration and environment variables
│   ├── dependencies.py      # JWT authentication dependencies
│   ├── email_utils.py       # Email sending and OTP generation
│   └── routers/
│       ├── users.py         # User authentication endpoints
│       ├── expenses.py      # Expense CRUD endpoints
│       └── analytics.py     # Analytics and reporting endpoints
├── web-frontend/
│   ├── index.html           # Main HTML structure
│   ├── app.js               # Frontend logic and API calls
│   └── styles.css           # Styling and animations
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
├── serve_frontend.py        # Frontend development server
└── README.md               # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /users/send-otp` - Send OTP to email
- `POST /users/verify-otp-signup` - Verify OTP and create account
- `POST /users/login` - Login with username/password

### Expenses
- `POST /expenses/expenses` - Create new expense
- `GET /expenses/expenses` - List all expenses (with filters)
- `PUT /expenses/expenses/{id}` - Update expense
- `DELETE /expenses/expenses/{id}` - Delete expense

### Analytics
- `GET /analytics/analytics` - Get spending analytics

## 🔒 Security Features

- **Argon2 Password Hashing** - Industry-standard password security
- **JWT Tokens** - Secure stateless authentication
- **OTP Verification** - Email-based signup verification
- **CORS Configuration** - Controlled cross-origin access
- **Environment Variables** - Sensitive data protection

## 🎯 Future Enhancements

- [ ] Budget setting and alerts
- [ ] Recurring expense tracking
- [ ] Export to CSV/PDF
- [ ] Multi-currency support
- [ ] Receipt image uploads
- [ ] Expense categories customization
- [ ] Monthly/yearly comparisons
- [ ] Email expense reports
- [ ] Mobile app version

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for efficient expense tracking

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Happy Expense Tracking! 💰📊**