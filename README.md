
# Flask Challenge

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)

A simple Flask web application for handling file uploads, querying a MongoDB database, and more.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Client Script](#client)

## Features

- Upload files to the server.
- Store uploaded data in a MongoDB database.
- Query the database using different criteria.
- Pagination of query results.
- Error handling and validation.
- Docker support for easy deployment.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your local machine.
- Docker and Docker Compose installed (optional, for running in a containerized environment).

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/gamorales/flask-challenge.git
   cd flask-challenge
   ```

2. Build and run the project using Docker:
   ```bash
   docker-compose up -d
   ```

## Usage:
   By default, the application will be accessible at http://localhost:5001

## Endpoints:
1. File Upload
- Endpoint: `/upload`
- HTTP Method: POST
- Description: Upload a file to the server, which will be parsed and stored in the MongoDB database.
- Usage: Send a POST request with a file attached. The uploaded file should be in CSV format.

2. Query
- Endpoint: `/query`
- HTTP Method: POST
- Description: Query the MongoDB database for movie records based on specified criteria.
- Request Format:
    ```json
    {
        "field": "field_name",    // Field to query (e.g., "title")
        "value": "search_value",  // Value to search for
        "page": 1,                // Page number (default is 1)
        "quantity": 10            // Number of results per page (default 10)
    }
    ```
## Client Script
1. Create a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required Python packages:
    ```bash
    pip3 install requests
    ```

3. Run the client script:
    ```bash
    python flask-app/client.py
    ```


