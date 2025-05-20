# E-Nurse Platform

An online platform for healthcare professionals to interact with patients and document diagnostics.

## Features

- Patient interaction interface
- Diagnostic documentation system
- Report summary generation
- Secure authentication system
- Real-time data storage with MongoDB Atlas

## Tech Stack

### Frontend
- React.js
- Material-UI/Tailwind CSS
- Axios for API calls

### Backend
- Flask (Python)
- MongoDB Atlas
- JWT Authentication

## Project Structure

```
e-nurse/
├── frontend/           # React frontend application
├── backend/           # Flask backend application
└── README.md         # Project documentation
```

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB Atlas credentials
   ```
5. Run the Flask server:
   ```bash
   python app.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Environment Variables

### Backend (.env)
- `MONGODB_URI`: MongoDB Atlas connection string
- `JWT_SECRET`: Secret key for JWT authentication
- `FLASK_ENV`: Development/Production environment

### Frontend (.env)
- `REACT_APP_API_URL`: Backend API URL

## API Documentation

The API documentation will be available at `/api/docs` when running the backend server.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 