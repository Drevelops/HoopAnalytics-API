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
- Alembic for database migrations
- Pydantic for data validation

### Frontend

- React
- Chart.js/Recharts for data visualization
- React Router
- Axios for API communication

## Installation

### Setup PostgreSQL Database

1. Install PostgreSQL if not already installed

2. Create a new database:
   ...
   CREATE DATABASE hoopanalytics;
   ...

3. Create a .env file with your database credentials:
   ...
   POSTGRES_SERVER=localhost
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=hoopanalytics
   POSTGRES_PORT=5432
   ...

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

4. Run database migrations
   ...
   alembic upgrade head
   ...

5.Seed the database with initial data
...
python scripts/seed_data.py
... 6. Run the development server

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

## API Endpoints

GET /api/v1/players/: Get all players with optional filtering
GET /api/v1/players/{player_id}: Get a specific player by ID
POST /api/v1/players/create_player: Create a new player
PUT /api/v1/players/update_player/{player_id}: Update an existing player
DELETE /api/v1/players/delete_player/{player_id}: Delete a player

## Project Status

This project is currently in development.

## License

[MIT License](LICENSE)

## Contact

Andre Wheeler

Project Link: https://github.com/drevelops/hoopanalytics-api
