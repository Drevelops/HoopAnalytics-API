# HoopAnalytics API

A comprehensive NBA statistics API with data analysis capabilities and interactive visualizations.

## Project Overview

HoopAnalytics API provides access to NBA player and team statistics with advanced analytics features. The project includes both a RESTful API built with FastAPI and a React frontend for data visualization.

## Features

- **Player Statistics**: Detailed player profiles, career stats, and performance metrics
- **Team Analysis**: Team performance data, lineup analysis, and historical trends
- **Advanced Analytics**: Efficiency metrics, statistical comparisons, and performance predictions
- **Visualizations**: Shot charts, performance trends, and comparative analysis
- **User Features**: Authentication, favoriting, and personalized dashboards

## Tech Stack

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pandas for data processing
- Pytest for testing

### Frontend

- React
- Chart.js/Recharts for data visualization
- React Router
- Axios for API communication

## Installation

### Setup Backend

1. Clone the repository

   ```
   git clone https://github.com/Drevelops/hoopanalytics-api.git
   cd hoopanalytics-api
   ```

2. Create and activate virtual environment

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Run the development server
   ```
   uvicorn app.main:app --reload
   ```

### Setup Frontend (once developed)

1. Navigate to frontend directory

   ```
   cd frontend
   ```

2. Install dependencies

   ```
   npm install
   ```

3. Start development server
   ```
   npm start
   ```

## API Documentation

Once the server is running, API documentation is available at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Status

This project is currently in development.

## License

[MIT License](LICENSE)

## Contact

Andre Wheeler

Project Link: https://github.com/drevelops/hoopanalytics-api
