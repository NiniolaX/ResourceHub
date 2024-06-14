# ResourceHub Learning App Repository ALX Portolio Project

Welcome to the ResourceHub !
This platform is designed to help learners, teachers and institutions access, manage, and interact with learning materials efficiently.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- CRUD operations for learning materials
- User profile management
- Responsive web design
- Search and filter functionality

## Technology Stack

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL (development), MySQL (production)
- **Server**: Gunicorn
- **Reverse Proxy**: Nginx

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtualenv
- MySQL (for production)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your_project_name.git
    cd ResourceHub
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv hub_env
    source hub_env/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    sudo ./setup_dev_
    ```

## Configuration

Configuration files are located in the `/config` directory. You can set up different configurations for development and production.

### Development Configuration

Edit `config/development.py` to set your development configurations.

### Production Configuration

Edit `config/production.py` to set your production configurations.

## Running the Application

### Development

Run the Flask development server:

```bash
flask run
```

Start the Gunicorn server 
```
gunicorn -w 4 -b 127.0.0.1:8000 wsgi:app

```

