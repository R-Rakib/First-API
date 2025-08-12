Insurance Premium Checker 🏥💰
This project is a FastAPI-based web application that predicts insurance premiums based on patient data.
It was built as a hands-on learning project for FastAPI, Docker, and deployment-ready Python services.

Features
FastAPI backend — lightweight, fast, and easy-to-use Python framework.

Predictive model — calculates insurance premiums using patient details such as age, gender, BMI, smoking status, and region.

Interactive API docs — powered by FastAPI’s built-in Swagger UI.

Dockerized application — runs in any environment without setup issues.

RESTful endpoints for easy integration with other services.

Tech Stack
Python (FastAPI, Pydantic, scikit-learn / model dependencies)

FastAPI for API development

Docker for containerization

Uvicorn as the ASGI server

How It Works
Input: Send patient information via API request.

Processing: The backend processes input through a trained model.

Output: Returns an estimated insurance premium in JSON format.

Getting Started
bash
Copy
Edit
# Clone the repository
git clone <repo-url>

# Build the Docker image
docker build -t insurance-premium-checker .

# Run the container
docker run -p 8000:8000 insurance-premium-checker
Open your browser at http://localhost:8000/docs to explore the API.
