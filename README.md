# To-Do API

## Overview
This project is a RESTful API for managing a To-Do list. It is built using Flask and supports user authentication, task management, and administrative functionalities.

## Features
- User authentication with JWT
- Task management (CRUD operations)
- List management
- Admin functionalities
- Database management with SQLAlchemy
- API documentation with OpenAPI/Swagger
- CORS support
- Caching for improved performance

## Technologies Used
- **Flask** (Web framework)
- **Flask-Smorest** (Blueprints for API routing)
- **SQLAlchemy** (ORM for database management)
- **Flask-Migrate** (Database migrations)
- **Flask-JWT-Extended** (Authentication)
- **Flask-CORS** (Cross-Origin Resource Sharing)
- **Flask-Caching** (Caching support)
- **Gunicorn** (Production WSGI server)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/pariyaaf/to-do-api.git
   cd to-do-api-main
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```

4. Set up the database:
   ```sh
   flask db upgrade
   ```

5. Run the application:
   ```sh
   flask run
   ```

## API Endpoints
| Method | Endpoint          | Description              |
|--------|------------------|--------------------------|
| POST   | `/register`      | Register a new user      |
| POST   | `/login`         | User login               |
| GET    | `/tasks`         | Get all tasks            |
| POST   | `/tasks`         | Create a new task        |
| PUT    | `/tasks/<id>`    | Update a task            |
| DELETE | `/tasks/<id>`    | Delete a task            |


