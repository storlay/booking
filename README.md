### Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/storlay/booking.git
    cd booking
    ```

2.  **Set up environment variables:**

    Create a `.env` file in the project's root directory. You will need to populate it with the required configuration values (e.g., database credentials, secret keys).

3.  **Build and run the application:**
    ```bash
    docker-compose -f infra/docker-compose.yml up --build
    ```

4.  **Access the application:**

    The API will be running and available at `http://127.0.0.1:8000`.

## Usage

### API Documentation

The API documentation is automatically generated and can be accessed at the following endpoints:

-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc`

## Running Tests

The project includes a separate Docker Compose configuration for running the test suite in an isolated environment.

1.  **Create a test environment file:**

    Create a `.env-test` file in the root directory with the configuration for the test database and other services.

2.  **Run the tests:**
    ```bash
    docker-compose -f infra/docker-compose.yml -f infra/docker-compose.test.yml up --build --abort-on-container-exit
    ```
    This command will spin up the necessary services, run the tests, and then automatically shut everything down.