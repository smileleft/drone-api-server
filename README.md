# 2025-04-04

# Drone API Server

This project is a FastAPI-based server for managing drones. It integrates with MongoDB for data storage and Mosquitto as the MQTT broker for communication.

---

## Features

- **Drone Management**: Manage drone statuses such as `flying`, `landed`, and `returning`.
- **MQTT Integration**: Communicate with drones using MQTT protocol.
- **MongoDB Integration**: Store and retrieve drone data from MongoDB.
- **RESTful API**: Expose endpoints for interacting with drones.

---

## Prerequisites

- **Docker**: Ensure Docker is installed on your system.
- **Docker Compose**: Ensure Docker Compose is installed.

---

## Setup Instructions

1. **Clone the Repository**:
    
    ```bash
    git clone <https://github.com/your-repo/drone_api_server.git>
    cd drone_api_server
    ```
    
2. **Environment Variables**: Update the `docker-compose.yaml` file with the correct environment variables:
    - `MONGODB_URI`: MongoDB connection string.
    - `MQTT_BROKER`: MQTT broker connection string.
3. **Build and Start Services**: Use Docker Compose to build and start the services:
    
    docker-compose up --build
    
4. **Access the API**:
    - API Base URL: `http://localhost:8000`
    - Swagger UI: `http://localhost:8000/docs`

## **Project Structure**

.

├── Dockerfile                # Docker configuration for the API

├── [docker-compose.yaml](http://_vscodecontentref_/1)       # Docker Compose configuration

├── [main.py](http://_vscodecontentref_/2)                   # Entry point for the FastAPI application

├── domain/                   # Domain logic for drones

│   ├── drone.py              # Drone and DroneStatus classes

├── infrastructure/           # Infrastructure-related code

│   ├── [mqtt_handler.py](http://_vscodecontentref_/3)       # MQTT handler for communication

│   ├── repository/           # Repository for MongoDB interactions

│       ├── drone_repository.py

├── tests/                    # Unit tests for the application

│   ├── test_drone.py

├── [requirements.txt](http://_vscodecontentref_/4)          # Python dependencies

└── [README.md](http://_vscodecontentref_/5)                 # Project documentation

## **API Endpoints**

### **Drone Management**

- **Get Drone Status**:
    - `GET /drones/{drone_id}/status`
    - Response:
        
        {
        
        "drone_id": "drone-001",
        
        "status": "flying",
        
        "last_updated": "2025-04-05T13:28:28"
        
        }
        
- **Send Command to Drone**:
    - `POST /drones/{drone_id}/command`
    - Payload:
        
        {
        
        "command": "takeoff"
        
        }
        

---

## **MQTT Topics**

- **Command Topic**: `drone/command`
    - Used to send commands to drones.
- **Status Topic**: `drone/status`
    - Used to receive status updates from drones.

---

## **Development**

1. **Install Dependencies**:
    
    pip install -r requirements.txt
    
2. **Run Locally**:
    
    uvicorn main:app --reload
    
3. **Run Tests**:
    
    pytest
    

---

## **Troubleshooting**

- **Connection Refused**: Ensure MongoDB and Mosquitto are running and accessible.
- **Docker Issues**: Rebuild the Docker images:
    
    docker-compose build --no-cache
    

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.