# CTSE-Assignment-02: Multi-Agent Travel Planner

A sophisticated travel planning system powered by multiple AI agents working collaboratively to create personalized itineraries, optimize budgets, validate constraints, and provide recommendations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Team Members](#team-members)

## 🎯 Overview

This project implements a multi-agent system that collaboratively plans travel itineraries. Using LangGraph and Ollama LLMs, multiple specialized agents work together to:

1. **Plan** travel routes and activities
2. **Calculate** and optimize budgets
3. **Validate** constraints and feasibility
4. **Recommend** improvements and alternatives

The system is built with a modern FastAPI backend and provides comprehensive REST API endpoints for integration with frontend applications.

## ✨ Features

- **Multi-Agent Architecture**: Specialized agents for different travel planning tasks
- **Collaborative Planning**: Agents work together using a state-based workflow
- **Budget Optimization**: Intelligent cost calculation and budget management
- **Constraint Validation**: Ensures itineraries meet specified requirements
- **Smart Recommendations**: AI-powered suggestions for improving plans
- **REST API**: FastAPI-based endpoints for seamless integration
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Unit Tests**: Full test coverage for all agents and tools

## 🏗️ Architecture

### Multi-Agent Workflow

The system uses a graph-based workflow where agents pass state through the pipeline:

```
User Input → Planner Agent → Budget Agent → Validator Agent → Recommendation Agent → Output
```

### Technology Stack

- **Backend Framework**: FastAPI
- **Agent Framework**: LangGraph + LangChain
- **LLM Integration**: Ollama (Local LLM support)
- **Data Validation**: Pydantic
- **Testing**: Pytest
- **Logging**: Loguru

## 📁 Project Structure

```
CTSE-Assignment-02/
├── backend/
│   ├── app/
│   │   ├── agents/              # AI agent implementations
│   │   │   ├── budget_agent.py
│   │   │   ├── planner_agent.py
│   │   │   ├── recommendation_agent.py
│   │   │   └── validator_agent.py
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── data/                # Data files
│   │   │   ├── costs.json
│   │   │   ├── destinations.json
│   │   │   └── sample_inputs.json
│   │   ├── graph/               # Workflow graph
│   │   │   ├── router.py
│   │   │   ├── state.py
│   │   │   └── workflow.py
│   │   ├── llm/
│   │   │   └── ollama_client.py # Ollama integration
│   │   ├── models/              # Request/response models
│   │   │   ├── request_models.py
│   │   │   └── response_models.py
│   │   ├── prompts/             # Agent prompts
│   │   │   ├── budget_prompt.txt
│   │   │   ├── planner_prompt.txt
│   │   │   ├── recommendation_prompt.txt
│   │   │   └── validator_prompt.txt
│   │   ├── tools/               # Utility functions for agents
│   │   │   ├── cost_calculator.py
│   │   │   ├── data_reader.py
│   │   │   ├── file_writer.py
│   │   │   └── validate_constraints.py
│   │   ├── utils/               # Helper utilities
│   │   │   ├── helpers.py
│   │   │   └── logger.py
│   │   └── main.py              # FastAPI app initialization
│   ├── tests/                   # Unit tests
│   │   ├── test_budget_agent.py
│   │   ├── test_file_writer.py
│   │   ├── test_planner_agent.py
│   │   ├── test_recommendation_agent.py
│   │   ├── test_tools.py
│   │   ├── test_validate_constraints.py
│   │   ├── test_validator_agent.py
│   │   └── test_workflow.py
│   ├── outputs/                 # Generated outputs
│   │   ├── itineraries/
│   │   └── logs/
│   ├── requirements.txt         # Python dependencies
│   └── README.md
├── frontend/                    # Frontend application
├── scripts/                     # Helper scripts
│   ├── run_backend.sh
│   ├── run_frontend.sh
│   └── seed_data.py
└── README.md                    # This file
```

## 🛠️ Prerequisites

- Python 3.8+
- Ollama (for local LLM support)
- Node.js (for frontend)
- pip package manager

### Installing Ollama

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install and run the Ollama service
3. Pull a model: `ollama pull llama2` (or your preferred model)

## 📦 Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CTSE-Assignment-02/backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (if needed)
   ```bash
   cp .env.example .env
   ```

### Frontend Setup

```bash
cd frontend
npm install
```

## 🚀 Running the Application

### Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

Interactive API documentation: `http://localhost:8000/docs`

### Using Shell Scripts

```bash
# Run backend
./scripts/run_backend.sh

# Run frontend
./scripts/run_frontend.sh
```

### Seed Sample Data

```bash
python scripts/seed_data.py
```

## 📡 API Endpoints

### Core Endpoints

- **POST** `/api/plan` - Create a travel plan
  - Input: Travel requirements and constraints
  - Output: Generated itinerary with budget breakdown

- **POST** `/api/validate` - Validate an itinerary
  - Input: Itinerary details
  - Output: Validation results and constraints check

- **POST** `/api/recommend` - Get recommendations
  - Input: Current plan
  - Output: Improvement suggestions

## 🧪 Testing

Run all tests:
```bash
cd backend
pytest -v
```

Run specific test file:
```bash
pytest -v tests/test_budget_agent.py
```

Run with coverage:
```bash
pytest --cov=app tests/
```

### Test Structure

- **test_budget_agent.py** - Budget calculation and optimization tests
- **test_planner_agent.py** - Travel planning logic tests
- **test_validator_agent.py** - Constraint validation tests
- **test_recommendation_agent.py** - Recommendation engine tests
- **test_tools.py** - Utility function tests
- **test_workflow.py** - Multi-agent workflow tests

## 👥 Team Members

| Member | Role | Components |
|--------|------|------------|
| **Ashika** | Planner Agent | `planner_agent.py`, `planner_prompt.txt`, `test_planner_agent.py` |
| **Madara** | Budget Agent | `budget_agent.py`, `cost_calculator.py`, `budget_prompt.txt`, `test_budget_agent.py` |
| **Janudi** | Validator Agent | `validator_agent.py`, `validate_constraints.py`, `validator_prompt.txt`, `test_validator_agent.py` |
| **Induwara** | Recommendation Agent | `recommendation_agent.py`, `recommendation_prompt.txt`, `file_writer.py`, `test_recommendation_agent.py` |

## 📝 Configuration

### Ollama Settings

Configure the Ollama client in `app/llm/ollama_client.py`:

```python
OLLAMA_MODEL = "llama2"  # or your preferred model
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Logging

Logs are stored in `backend/outputs/logs/` directory. Configure logging settings in `app/utils/logger.py`.

## 🔍 Troubleshooting

### Ollama Connection Issues
- Ensure Ollama service is running
- Check that the correct base URL and port are configured
- Verify the model is pulled: `ollama list`

### API Not Responding
- Check if the backend server is running on the correct port
- Verify firewall settings
- Check logs for error messages

### Test Failures
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Clear pytest cache: `pytest --cache-clear`
- Check Ollama is running for integration tests

## 📄 License

This project is part of CTSE Assignment 2 at SLIIT.

## 📞 Support

For issues or questions, please contact the team members listed above.