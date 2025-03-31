# CORS Demonstration Website

This project is a demonstration website built to showcase Cross-Origin Resource Sharing (CORS) operations across different HTTP methods. It consists of a Flask backend API with proper CORS configuration and a pure HTML/CSS/JavaScript frontend that can make cross-origin requests to test CORS functionality.

## Features

- Backend API with Flask supporting all HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
- Properly configured CORS headers on Flask backend
- Frontend built with pure HTML, CSS, and JavaScript (no frameworks)
- Interface to test different CORS operations
- Ability to tunnel the API through ngrok/localtunnel for public access
- Demonstration of successful cross-origin requests between frontend and backend
- Visualizes request and response headers for educational purposes

## Setup Instructions

1. Install required packages:
   ```bash
   pip install flask flask-cors
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Access the application:
   - The application will be available at: http://localhost:5000
   - This serves both the frontend and the API endpoints

## Tunneling Instructions

To expose your local Flask API to the public internet, you can use tunneling services like ngrok or localtunnel.

### Using ngrok

```bash
# Install ngrok
npm install -g ngrok # or download from ngrok.com

# Start your Flask API on port 5000
python main.py

# In a new terminal, start ngrok
ngrok http 5000
```

### Using localtunnel

```bash
# Install localtunnel
npm install -g localtunnel

# Start your Flask API on port 5000
python main.py

# In a new terminal, start localtunnel
lt --port 5000
```
