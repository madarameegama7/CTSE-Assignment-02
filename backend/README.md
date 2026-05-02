# Backend - Multi-Agent Travel Planner

Backend implementation of the Multi-Agent Travel Planner system using FastAPI and LangGraph.

## 📋 Quick Start

### Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🏗️ Project Structure

### Core Modules

#### `/app/agents/` - AI Agents
- **planner_agent.py**: Generates travel itineraries and activity schedules
- **budget_agent.py**: Calculates costs and optimizes budget allocation
- **validator_agent.py**: Validates constraints and feasibility
- **recommendation_agent.py**: Provides improvement suggestions

#### `/app/graph/` - Workflow Engine
- **state.py**: Defines the shared state passed between agents
- **router.py**: Routes messages between agents
- **workflow.py**: Orchestrates the multi-agent workflow

#### `/app/api/` - REST API
- **routes.py**: FastAPI route definitions

#### `/app/llm/` - Language Model Integration
- **ollama_client.py**: Manages Ollama LLM connections

#### `/app/models/` - Data Models
- **request_models.py**: Input validation schemas
- **response_models.py**: Output response schemas

#### `/app/tools/` - Utility Functions
- **cost_calculator.py**: Budget calculations
- **data_reader.py**: Reads data files
- **file_writer.py**: Writes output files
- **validate_constraints.py**: Constraint checking logic

#### `/app/utils/` - Helper Utilities
- **logger.py**: Logging configuration
- **helpers.py**: General utility functions

#### `/app/data/` - Data Files
- **costs.json**: Cost information
- **destinations.json**: Destination details
- **sample_inputs.json**: Sample input data

#### `/app/prompts/` - Agent Prompts
Text prompts for each agent's LLM interactions.

### Testing (`/tests/`)

```bash
pytest -v                          # Run all tests
pytest tests/test_budget_agent.py  # Run specific test
pytest --cov=app tests/            # Run with coverage
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
OLLAMA_MODEL=llama2
OLLAMA_BASE_URL=http://localhost:11434
LOG_LEVEL=INFO
```

### Ollama Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Run Ollama service
3. Pull a model: `ollama pull llama2`

## 📡 API Overview

### Travel Planning
```bash
POST /plan-trip
Content-Type: application/json

{
  "destination": "Ella",
  "days": 3,
  "travelers": 2,
  "budget": 50000,
  "preferences": ["nature", "hiking"]
}
```

The `/plan-trip` endpoint runs the entire LangGraph multi-agent workflow:
1. Plans the itinerary
2. Calculates the budget
3. Validates constraints
4. Generates recommendations

## 🧪 Testing Guide

### Running Tests
```bash
# All tests
pytest -v

# Specific module
pytest -v tests/test_budget_agent.py

# With coverage report
pytest --cov=app tests/
```

### Test Files
- `test_budget_agent.py` - Budget calculations
- `test_planner_agent.py` - Travel planning
- `test_validator_agent.py` - Constraint validation
- `test_recommendation_agent.py` - Recommendations
- `test_tools.py` - Utility functions
- `test_workflow.py` - Agent workflow
- `test_file_writer.py` - File operations
- `test_validate_constraints.py` - Constraint logic

## 📊 Workflow

The multi-agent system follows this workflow:

1. **Input Reception**: User provides travel requirements
2. **Planning**: Planner Agent creates initial itinerary
3. **Budget Calculation**: Budget Agent calculates costs
4. **Validation**: Validator Agent checks constraints
5. **Recommendations**: Recommendation Agent suggests improvements
6. **Output Generation**: Final itinerary is returned

## 🐛 Debugging

### Enable Debug Logging
```python
# In app/utils/logger.py
LOG_LEVEL = "DEBUG"
```

### Check Logs
Logs are stored in `outputs/logs/` directory.

### Common Issues

**Issue**: Ollama connection refused
- **Solution**: Ensure Ollama service is running and accessible

**Issue**: Model not found
- **Solution**: Pull model with `ollama pull <model_name>`

**Issue**: Tests failing
- **Solution**: Clear cache with `pytest --cache-clear`

## 📦 Dependencies

See `requirements.txt` for complete list:
- fastapi - Web framework
- uvicorn - ASGI server
- langgraph - Agent workflow
- langchain - LLM integration
- langchain-ollama - Ollama support
- pydantic - Data validation
- loguru - Logging

## 📝 Development Notes

- Follow PEP 8 style guide
- Add unit tests for new features
- Update prompts in `/app/prompts/` as needed
- Keep agent interfaces consistent
- Document API endpoints in docstrings

## 🔗 Links

- Main README: [../README.md](../README.md)
- FastAPI Docs: http://localhost:8000/docs
- Ollama: https://ollama.ai
- LangGraph: https://github.com/langchain-ai/langgraph
