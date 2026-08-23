# FitFusion API

FitFusion API is a Python-based fitness planning service that provides structured, personalized fitness analysis, nutrition recommendations, workout plans, and complete fitness plans through a tool-based REST API.

The project demonstrates:

- REST API development
- Modular Python architecture
- Input validation
- Automated unit and API testing
- Docker containerization
- Kubernetes deployment
- Horizontal Pod Autoscaling
- ConfigMap-based configuration
- CI/CD with GitHub Actions
- End-to-end testing
- Basic load testing

---

# Architecture

```text
Client
   |
   v
+----------------------+
|   FitFusion API      |
|                      |
|  Azure Functions     |
|                      |
|  /health             |
|  /api/tools          |
|  /api/tools/execute  |
+----------+-----------+
           |
           v
+----------------------+
|    Tool Registry     |
+----------+-----------+
           |
           v
+----------------------+
|   Fitness Tools      |
|                      |
| analyze.py           |
| recommend.py         |
| workout.py           |
| plan.py              |
+----------------------+

The API uses a tool registry pattern to dynamically expose and execute fitness-related tools.
Available Tools

The API currently provides four tools.

1. Fitness Analysis

Tool:

fitness.analyze

Analyzes a user's fitness profile.

Input
{
  "name": "Vijay",
  "age": 35,
  "gender": "male",
  "weight": 72,
  "height": 175,
  "activity_level": "moderate",
  "goal": "fat_loss"
}
Output

The analysis includes:

BMI
BMI category
BMR
Maintenance calories
Target calories
Protein target
Fat target
Carbohydrate target
Goal-based recommendation

Example:

{
  "name": "Vijay",
  "profile": {
    "age": 35,
    "gender": "male",
    "weight_kg": 72,
    "height_cm": 175,
    "activity_level": "moderate",
    "goal": "fat_loss"
  },
  "analysis": {
    "bmi": 23.51,
    "bmi_category": "normal",
    "bmr_calories": 1644,
    "maintenance_calories": 2548,
    "target_calories": 2038,
    "macros": {
      "protein_g": 144,
      "fat_g": 58,
      "carbohydrates_g": 235
    }
  }
}
2. Nutrition Recommendation

Tool:

fitness.recommend

Generates nutrition and training recommendations based on:

Fitness goal
Diet preference
Daily calorie target
Input
{
  "goal": "fat_loss",
  "diet_preference": "vegetarian",
  "daily_calories": 2000
}
3. Workout Plan

Tool:

fitness.workout_plan

Generates a workout plan based on:

Fitness goal
Experience level
Training days per week
Available equipment
Input
{
  "goal": "fat_loss",
  "experience_level": "intermediate",
  "days_per_week": 5,
  "equipment": "gym"
}
4. Complete Fitness Plan

Tool:

fitness.complete_plan

Combines fitness analysis, nutrition recommendations, and workout planning into a complete personalized fitness plan.

Input
{
  "name": "Vijay",
  "age": 35,
  "gender": "male",
  "weight": 72,
  "height": 175,
  "activity_level": "moderate",
  "goal": "fat_loss",
  "diet_preference": "vegetarian",
  "experience_level": "intermediate",
  "days_per_week": 5,
  "equipment": "gym"
}
Project Structure
fitfusion-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── kustomization.yaml
│   ├── namespace.yaml
│   └── service.yaml
│
├── scripts/
│   ├── e2e_pipeline.py
│   └── load_test.py
│
├── tests/
│   ├── __init__.py
│   ├── test_analyze.py
│   ├── test_api.py
│   ├── test_complete_plan.py
│   ├── test_recommend.py
│   └── test_workout.py
│
├── tools/
│   ├── fitness/
│   │   ├── __init__.py
│   │   ├── analyze.py
│   │   ├── plan.py
│   │   ├── recommend.py
│   │   └── workout.py
│   │
│   ├── __init__.py
│   ├── registry.py
│   ├── router.py
│   └── validators.py
│
├── .dockerignore
├── .funcignore
├── .gitignore
├── Dockerfile
├── function_app.py
├── host.json
├── README.md
├── requirements.txt
└── test.json
API Endpoints
Health Check
GET /health

Example response:

{
  "status": "healthy",
  "service": "FitFusion API"
}
List Available Tools
GET /api/tools

Example response:

{
  "tools": [
    {
      "name": "fitness.analyze"
    },
    {
      "name": "fitness.recommend"
    },
    {
      "name": "fitness.workout_plan"
    },
    {
      "name": "fitness.complete_plan"
    }
  ],
  "count": 4
}
Execute Tool
POST /api/tools/execute
Request Format
{
  "tool": "fitness.analyze",
  "arguments": {
    "name": "Vijay",
    "age": 35,
    "gender": "male",
    "weight": 72,
    "height": 175,
    "activity_level": "moderate",
    "goal": "fat_loss"
  }
}

The API validates the request and routes execution to the appropriate tool.

Local Development
Clone Repository
git clone <your-repository-url>
cd fitfusion-api
Create Virtual Environment

Windows PowerShell:

python -m venv .venv

Activate:

.venv\Scripts\Activate.ps1
Install Dependencies
pip install -r requirements.txt
Run the API Locally

Start the Azure Functions application:

func start

The API can then be accessed locally.

Example:

http://localhost:7071

Health check:

Invoke-RestMethod http://localhost:7071/health
Docker

The application can be packaged as a Docker container.

Build Image
docker build -t fitfusion-api:latest .
Run Container
docker run -p 8080:80 fitfusion-api:latest

The API will then be accessible at:

http://localhost:8080

Verify:

Invoke-RestMethod http://localhost:8080/health

Expected response:

{
  "status": "healthy",
  "service": "FitFusion API"
}
Kubernetes Deployment

The project includes Kubernetes manifests for deploying FitFusion API.

The Kubernetes configuration includes:

Namespace
ConfigMap
Deployment
Service
Horizontal Pod Autoscaler
Kustomization
Kubernetes Directory
k8s/
├── configmap.yaml
├── deployment.yaml
├── hpa.yaml
├── kustomization.yaml
├── namespace.yaml
└── service.yaml
Deploy to Kubernetes

Apply the complete configuration:

kubectl apply -k k8s/

Verify resources:

kubectl get all -n fitfusion

You can also check individual resource types:

kubectl get pods -n fitfusion
kubectl get deployments -n fitfusion
kubectl get services -n fitfusion
kubectl get hpa -n fitfusion
Port Forwarding

To access the Kubernetes service locally:

kubectl port-forward service/fitfusion-api-service 8080:80 -n fitfusion

The API will then be available at:

http://localhost:8080

Test the health endpoint:

Invoke-RestMethod http://localhost:8080/health
Automated Testing

The project contains unit tests and API integration tests.

Test categories include:

Fitness analysis
Nutrition recommendation
Workout generation
Complete fitness plan
API tool execution
Unknown tool validation
Missing tool validation
Missing arguments validation
Invalid arguments validation
Invalid request body validation
Run All Tests
pytest -v

The test suite currently verifies the complete application logic.

Example successful result:

115 passed
API Integration Tests

The API tests support configuration using the BASE_URL environment variable.

For local Azure Functions:

$env:BASE_URL = "http://localhost:7071"
pytest tests/test_api.py -v

For Docker or Kubernetes port-forwarding:

$env:BASE_URL = "http://localhost:8080"
pytest tests/test_api.py -v

This avoids hardcoding the environment inside the test suite.

End-to-End Testing

The project includes an end-to-end pipeline:

scripts/e2e_pipeline.py

The pipeline verifies the complete workflow.

Pipeline Steps
STEP 1
Health Check

↓

STEP 2
Tool Discovery

↓

STEP 3
Fitness Analysis

↓

STEP 4
Nutrition Recommendation

↓

STEP 5
Workout Plan

↓

STEP 6
Complete Fitness Plan
Run E2E Pipeline

Set the API target:

$env:BASE_URL = "http://localhost:8080"

Run:

python .\scripts\e2e_pipeline.py

Example successful output:

FITFUSION END-TO-END PIPELINE COMPLETED

ALL TESTS PASSED SUCCESSFULLY

Verified:
✓ Kubernetes service connectivity
✓ Health endpoint
✓ Tool discovery
✓ Fitness analysis
✓ Nutrition recommendation
✓ Workout plan
✓ Complete fitness plan

The end-to-end pipeline verifies that the deployed service works as a complete system rather than testing individual functions in isolation.

Load Testing

A basic concurrent load test is included.

scripts/load_test.py

The load test sends multiple requests to:

POST /api/tools/execute

The current test configuration uses:

Total Requests: 5000
Concurrent Users: 100
Run Load Test

First ensure the API is accessible on port 8080.

For Kubernetes:

kubectl port-forward service/fitfusion-api-service 8080:80 -n fitfusion

Then run:

python .\scripts\load_test.py

Example output:

============================================================
FitFusion API Load Test
============================================================

Target URL: http://localhost:8080/api/tools/execute
Total Requests: 5000
Concurrent Users: 100

============================================================
LOAD TEST RESULTS
============================================================

Total Requests : 5000
Successful     : <successful requests>
Failed         : <failed requests>
Duration       : <duration> seconds
Requests/sec   : <requests per second>
CI/CD Pipeline

The project includes a GitHub Actions workflow.

Location:

.github/workflows/ci.yml

The pipeline automatically runs when changes are pushed to the repository.

The CI workflow validates the project by running the automated test suite.

Typical flow:

Developer Push
      |
      v
GitHub Repository
      |
      v
GitHub Actions
      |
      v
Install Dependencies
      |
      v
Run Tests
      |
      v
Build Validation
      |
      v
Pipeline Result
Validation

The API validates requests before tool execution.

Examples of invalid scenarios handled by the API:

Unknown Tool
{
  "tool": "unknown.tool",
  "arguments": {}
}
Missing Tool
{
  "arguments": {}
}
Missing Arguments
{
  "tool": "fitness.analyze"
}
Invalid Arguments
{
  "tool": "fitness.recommend",
  "arguments": {
    "goal": 123,
    "diet_preference": "vegetarian",
    "daily_calories": 2000
  }
}

The validation layer prevents invalid requests from reaching the business logic.

Technology Stack
Category	Technology
Language	Python
API Platform	Azure Functions
Testing	Pytest
HTTP Client	Requests
Containerization	Docker
Orchestration	Kubernetes
Scaling	Horizontal Pod Autoscaler
Configuration	Kubernetes ConfigMap
CI/CD	GitHub Actions
Deployment Flow

The complete deployment flow is:

Python Application
        |
        v
Automated Tests
        |
        v
Docker Image
        |
        v
Kubernetes Deployment
        |
        v
Service
        |
        v
Port Forward / External Access
        |
        v
API Integration Tests
        |
        v
End-to-End Pipeline
        |
        v
Load Test
Useful Commands
Git

Check repository status:

git status

View latest commit:

git show --stat --oneline HEAD

List tracked files:

git ls-files

View commit history:

git log --oneline
Kubernetes

View all resources:

kubectl get all -n fitfusion

View pods:

kubectl get pods -n fitfusion

View deployments:

kubectl get deployments -n fitfusion

View services:

kubectl get services -n fitfusion

View HPA:

kubectl get hpa -n fitfusion

View logs:

kubectl logs deployment/fitfusion-api -n fitfusion

Apply configuration:

kubectl apply -k k8s/

Delete configuration:

kubectl delete -k k8s/
Engineering Focus

This project was built as an end-to-end engineering exercise demonstrating how an API can move through the complete delivery lifecycle:

Application Development
        ↓
Unit Testing
        ↓
API Integration Testing
        ↓
Docker Containerization
        ↓
Kubernetes Deployment
        ↓
Service Networking
        ↓
Configuration Management
        ↓
Horizontal Scaling
        ↓
CI/CD
        ↓
End-to-End Validation
        ↓
Load Testing

The project demonstrates not only application development but also the operational workflow required to package, deploy, validate, and test an API in a containerized Kubernetes environment.

Current Verification Status

The following components have been successfully verified:

✓ Unit tests
✓ API integration tests
✓ Health endpoint
✓ Tool discovery
✓ Fitness analysis
✓ Nutrition recommendation
✓ Workout plan generation
✓ Complete fitness plan generation
✓ Docker container execution
✓ Kubernetes deployment
✓ Kubernetes service connectivity
✓ Kubernetes port forwarding
✓ End-to-end pipeline
✓ GitHub Actions CI workflow
✓ Load testing setup
Future Improvements

Potential next steps include:

OpenAPI / Swagger documentation
Structured logging
Prometheus metrics
Grafana dashboards
Distributed tracing
API authentication
Rate limiting
Helm charts
Cloud container registry integration
Managed Kubernetes deployment
Automated Docker image build and push
Kubernetes deployment through CI/CD
Contract testing
Performance monitoring
More advanced load testing
License

This project is intended for learning, demonstration, and engineering portfolio purposes.