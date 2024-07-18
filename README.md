# ResourceHub 

ResourceHub is a web application designed to streamline the distribution of educational materials within educational institutions. It allows institutions to manage departments, teachers, and learners, while providing a platform for teachers to create and share resources and for learners to access those resources seamlessly.


## Table of Content

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Deployment](#deployment)
- [Using the API documentation](#using-the-api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)


## Features
### Institution Dashboard

Institutions can:
- Manage Departments: Create and delete departments.
- Manage Teachers: Create and delete teachers.
- Manage Learners: Create and delete learners.

### Teacher Dashboard
Teachers can:
- Manage resources: Create and delete resources.
- View Resources: View resources they have created.
- Specific Resource Riew: View detailed content of a resource.

### Learner Dashboard
- View Resources: Access all resources available in their department.
- Detailed Resource View: Click on a resource to view its detailed content.
- User authentication and authorization

### Authentication and Access Control
- Role-Based Access: Different dashboards and functionalities are accessible based on the user's role (Institution, Teacher, Learner).
- User Authentication: Secure login and logout functionalities.


## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML5, CSS, Flask, Jinja2
- **Database**: MySQL (development), POSTGRESQL (production)
- **Server**: Gunicorn
- **Deployment**: The application was deployed on render.com. [Visit the live app](https://resourcehub-0szu.onrender.com/)


## Setup and Installation
### Prerequisites

- Python 3.8 or higher
- Virtualenv
- MySQL (for development)

### Installation

Follow these steps to run the application on your local machine.
1. Clone the repository:
    ```bash
    git clone https://github.com/NiniolaX/ResourceHub.git
    cd ResourceHub
    ```

2. Run the setup script:
    ```bash
    ./setup/setup.sh
    ```
   This script:
	- installs the python venv package on your system if it doesn't exist,
	- creates a virtual environment named *hub_env*,
	- activates the virtual environment and installs the app dependencies (defined in setup/requirements.txt) in it, and
	- closes the virtual environment.

3. Start the virtual environment:
    ```bash
    source hub_env/bin/activate
    ```

4. Set up the database:
    ```bash
    cat setup/setup_mysql_db.sql | sudo mysql -p
    OR
    cat setup/setup_mysql_test.sql | sudo mysql -p (Use this when running unittests, all database entries are deleted at the end of the tests)
    ```

5. Start the *API* on one terminal:
    ```bash
    HUB_MYSQL_USER=hub_dev HUB_MYSQL_PWD=hub_dev_pwd HUB_MYSQL_HOST=localhost HUB_MYSQL_DB=hub_dev_db python3 -m api.api
    ```
    The API is configured to run on port 5001 of your machine, so ensure nothing else is running on that port. You can modify this setting in the *api/api.py* file.

6. Start the *app* on another terminal:
    ```bash
    HUB_MYSQL_USER=hub_dev HUB_MYSQL_PWD=hub_dev_pwd HUB_MYSQL_HOST=localhost HUB_MYSQL_DB=hub_dev_db API_URL=http://127.0.0.1:5001/api python3 -m app.app
    ```
    The app is configured to run on port 5000 of your machine, so ensure nothing else is running on that port. You can modify this setting in the *app/app.py* file.

7. Run the application:
Open your browser and navigate to http://127.0.0.1:5000/ to start using the app.


## Deployment
The application is deployed on [Render](https://render.com/). You can access it [here](https://resourcehub-0szu.onrender.com/).


# Using the API Documentation
To use the API documentation, follow the following steps:
1. Start the *API*:
    ```bash
   HUB_MYSQL_USER=hub_dev HUB_MYSQL_PWD=hub_dev_pwd HUB_MYSQL_HOST=localhost HUB_MYSQL_DB=hub_dev_db python3 -m api.api
    ```
    The API is configured to run on port 5001 of your machine, so ensure nothing else is running on that port. You can modify this setting in the *api/api.py* file.

2. Open your browser and navigate to http://127.0.0.1:5001/apidocs/ to use the interactive API documentation on Swagger UI.


## Testing
You can run the unit tests in the tests/ folder, like so:
    ```bash
    HUB_ENV=test HUB_MYSQL_USER=hub_test HUB_MYSQL_PWD=hub_test_pwd HUB_MYSQL_HOST=localhost HUB_MYSQL_DB=hub_test_db API_URL=http://127.0.0.1:5001/api python3 -m unittest discover tests
    ```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
