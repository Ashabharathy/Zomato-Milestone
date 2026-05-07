# Project Structure Documentation

## Overview

This document outlines the complete project structure for the AI-Powered Restaurant Recommendation System, organized by phases with proper separation of source code and documentation.

## Directory Structure

```
zomato-ai-recommender/
|
|-- src/                          # All source code organized by phases
|   |-- phase1/                    # Data Ingestion and Processing
|   |   |-- data/                  # Raw and processed data files
|   |   |-- __init__.py
|   |   |-- data_pipeline.py
|   |   `-- run.py
|   |
|   |-- phase2/                    # Data Cleaning and Validation
|   |   |-- __init__.py
|   |   |-- data_cleaner.py
|   |   `-- validator.py
|   |
|   |-- phase3/                    # Candidate Retrieval
|   |   |-- __init__.py
|   |   |-- candidate_retrieval.py
|   |   `-- embedding_search.py
|   |
|   |-- phase4/                    # LLM Integration and Ranking
|   |   |-- __init__.py
|   |   |-- phase4_integration.py
|   |   |-- llm_inference.py
|   |   |-- prompt_builder.py
|   |   |-- response_parser.py
|   |   |-- guardrails.py
|   |   |-- example_usage.py
|   |   |-- live_test.py
|   |   |-- README.md
|   |   |-- requirements.txt
|   |   `-- .env
|   |
|   |-- phase5/                    # Response Assembly and Presentation
|   |   |-- __init__.py
|   |   |-- phase5_integration.py
|   |   |-- output_renderer.py
|   |   |-- summary_generator.py
|   |   |-- result_formatter.py
|   |   |-- example_usage.py
|   |   |-- README.md
|   |   `-- requirements.txt
|   |
|   `-- phase6/                    # Feedback, Evaluation, and Improvement Loop
|       |-- __init__.py
|       |-- phase6_integration.py
|       |-- feedback_collector.py
|       |-- metrics_tracker.py
|       |-- prompt_version_manager.py
|       |-- monitoring_logging.py
|       |-- example_usage.py
|       |-- README.md
|       `-- requirements.txt
|
|-- Docs/                         # All documentation organized by phases
|   |-- phase-wise-architecture.md # Overall architecture document
|   |-- problemstatement.md       # Project problem statement
|   |-- edge-cases.md             # Edge cases and considerations
|   |
|   |-- phase1/                   # Phase 1 documentation
|   |   `-- README.md
|   |
|   |-- phase2/                   # Phase 2 documentation
|   |   `-- README.md
|   |
|   |-- phase3/                   # Phase 3 documentation
|   |   `-- README.md
|   |
|   |-- phase4/                   # Phase 4 documentation
|   |   `-- README.md
|   |
|   |-- phase5/                   # Phase 5 documentation
|   |   `-- README.md
|   |
|   `-- phase6/                   # Phase 6 documentation
|       `-- README.md
|
|-- backend/                      # Backend API implementation (FastAPI)
|   |-- main.py                   # FastAPI application entry point
|   |-- core/                     # Core application components
|   |   |-- __init__.py
|   |   |-- config.py             # Configuration management
|   |   |-- database.py           # Database setup and connections
|   |   |-- logging.py            # Structured logging setup
|   |   `-- exceptions.py         # Custom exception classes
|   |
|   |-- models/                   # Database models
|   |   |-- __init__.py
|   |   |-- user.py               # User-related models
|   |   |-- restaurant.py         # Restaurant-related models
|   |   `-- recommendation.py     # Recommendation-related models
|   |
|   |-- api/                      # API endpoints
|   |   `-- v1/                   # API version 1
|   |       |-- __init__.py
|   |       |-- router.py         # Main API router
|   |       `-- endpoints/        # API endpoint modules
|   |
|   `-- requirements.txt          # Backend dependencies
|
|-- frontend/                     # Frontend implementation (React)
|   |-- src/                      # Frontend source code
|   |   |-- components/           # React components
|   |   |-- pages/               # Page components
|   |   |-- store/               # Redux store
|   |   |-- services/            # API services
|   |   |-- types/               # TypeScript types
|   |   `-- App.tsx              # Main application component
|   |
|   |-- package.json             # Frontend dependencies
|   `-- vite.config.js           # Vite configuration
|
|-- scripts/                      # Utility scripts
|   |-- setup.py                 # Project setup script
|   |-- data_processing.py       # Data processing utilities
|   `-- deployment.py            # Deployment utilities
|
|-- phase1/                       # Legacy phase folders (deprecated)
|-- phase2/                       # Legacy phase folders (deprecated)
|-- phase4/                       # Legacy phase folders (deprecated)
|-- phase5/                       # Legacy phase folders (deprecated)
|-- phase6/                       # Legacy phase folders (deprecated)
|
`-- requirements.txt              # Project-wide dependencies
```

## Phase-wise Organization

### Phase 1: Data Ingestion and Processing
**Location**: `src/phase1/`

**Purpose**: Handle raw data ingestion, cleaning, and initial processing

**Key Components**:
- `data_pipeline.py`: Main data processing pipeline
- `run.py`: Execution script for Phase 1
- `data/`: Data files (CSV, Parquet, JSON schemas)

### Phase 2: Data Cleaning and Validation
**Location**: `src/phase2/`

**Purpose**: Clean and validate processed data for quality assurance

**Key Components**:
- `data_cleaner.py`: Data cleaning utilities
- `validator.py`: Data validation logic

### Phase 3: Candidate Retrieval
**Location**: `src/phase3/`

**Purpose**: Retrieve candidate restaurants using embeddings and similarity search

**Key Components**:
- `candidate_retrieval.py`: Candidate retrieval logic
- `embedding_search.py`: Embedding-based search functionality

### Phase 4: LLM Integration and Ranking
**Location**: `src/phase4/`

**Purpose**: Integrate with LLM for intelligent restaurant ranking and recommendations

**Key Components**:
- `phase4_integration.py`: Main integration module
- `llm_inference.py`: LLM API integration
- `prompt_builder.py`: Prompt construction and management
- `response_parser.py`: LLM response parsing
- `guardrails.py`: Output validation and safety

### Phase 5: Response Assembly and Presentation
**Location**: `src/phase5/`

**Purpose**: Format and present recommendations in user-friendly formats

**Key Components**:
- `phase5_integration.py`: Main integration module
- `output_renderer.py`: Output formatting and rendering
- `summary_generator.py`: Recommendation summaries
- `result_formatter.py`: Result formatting utilities

### Phase 6: Feedback, Evaluation, and Improvement Loop
**Location**: `src/phase6/`

**Purpose**: Collect feedback, track metrics, and continuously improve the system

**Key Components**:
- `phase6_integration.py`: Main integration module
- `feedback_collector.py`: User feedback collection and analysis
- `metrics_tracker.py`: Performance metrics tracking
- `prompt_version_manager.py`: A/B testing and prompt optimization
- `monitoring_logging.py`: System monitoring and logging

## Backend API Structure

### Core Components (`backend/core/`)
- **Configuration**: Environment-based settings management
- **Database**: SQLAlchemy setup with async support
- **Logging**: Structured logging with monitoring
- **Exceptions**: Custom exception handling

### Models (`backend/models/`)
- **User**: User management and authentication
- **Restaurant**: Restaurant data and relationships
- **Recommendation**: Recommendation tracking and history

### API Endpoints (`backend/api/v1/`)
- **Authentication**: User auth and session management
- **Users**: User profile and preferences
- **Restaurants**: Restaurant data and search
- **Recommendations**: Recommendation generation and delivery
- **Analytics**: System analytics and metrics
- **Admin**: Administrative functions

## Frontend Structure

### Components (`frontend/src/components/`)
- **Layout**: Application layout and navigation
- **Common**: Reusable UI components
- **Forms**: Form components and validation

### Pages (`frontend/src/pages/`)
- **Home**: Landing page and overview
- **Search**: Restaurant search interface
- **Recommendations**: Recommendation display
- **Profile**: User profile management
- **Dashboard**: Analytics and insights

### State Management (`frontend/src/store/`)
- **Redux Toolkit**: Global state management
- **Slices**: Feature-specific state slices

## Import Path Conventions

### Phase-to-Phase Imports
```python
# Import from previous phases
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from phase4.phase4_integration import Phase4Result
from phase5.phase5_integration import Phase5Result

# Relative imports within the same phase
from .feedback_collector import FeedbackCollector
from .metrics_tracker import MetricsTracker
```

### Backend Imports
```python
# Core imports
from core.config import settings
from core.database import get_async_session
from core.logging import get_logger

# Model imports
from models.user import User
from models.restaurant import Restaurant
```

### Frontend Imports
```python
# Component imports
import { Component } from 'react';
import { Button, Card } from '@mui/material';

# Store imports
import { useDispatch, useSelector } from 'react-redux';
import { authSlice } from '../store/slices/authSlice';
```

## Documentation Structure

### Phase Documentation (`Docs/phase*/`)
Each phase has its own documentation folder containing:
- **README.md**: Phase overview, installation, and usage
- **Architecture**: Phase-specific architecture details
- **Examples**: Usage examples and tutorials

### Global Documentation (`Docs/`)
- **phase-wise-architecture.md**: Complete system architecture
- **problemstatement.md**: Project goals and objectives
- **edge-cases.md**: Edge cases and error handling

## Development Workflow

### 1. Phase Development
- Develop phase-specific code in `src/phase*/`
- Update documentation in `Docs/phase*/`
- Test with example usage scripts

### 2. Integration Testing
- Test phase-to-phase integration
- Update import paths as needed
- Validate data flow between phases

### 3. API Integration
- Integrate backend API with phase logic
- Update frontend components to use new features
- Test end-to-end functionality

### 4. Documentation Updates
- Update phase documentation
- Update global architecture docs
- Create/update examples and tutorials

## Deployment Structure

### Development Environment
```
src/phase*/           # Development code
backend/              # Development API
frontend/             # Development UI
Docs/                 # Documentation
```

### Production Environment
```
backend/              # Production API
frontend/build/       # Production UI
Docs/                 # Documentation
```

## Migration Notes

### Legacy Phase Folders
The root-level `phase*/` folders are deprecated and maintained for backward compatibility. All active development should use the `src/phase*/` structure.

### Import Path Updates
All import paths have been updated to use the new structure:
- Phase-to-phase imports use the parent directory path
- Within-phase imports use relative imports
- Backend and frontend maintain their own import conventions

### Documentation Migration
Phase-specific documentation has been moved to `Docs/phase*/` for better organization and accessibility.

## Best Practices

### Code Organization
- Keep phase-specific code in respective `src/phase*/` folders
- Use relative imports within the same phase
- Maintain clear separation between phases

### Documentation
- Keep documentation updated with code changes
- Use consistent documentation structure across phases
- Include examples and usage instructions

### Testing
- Test phase functionality independently
- Test phase-to-phase integration
- Test complete end-to-end workflows

### Version Control
- Use meaningful commit messages
- Tag releases by phase milestones
- Maintain clean branch structure

## Future Enhancements

### Planned Improvements
1. **Automated Testing**: Comprehensive test suite for all phases
2. **CI/CD Pipeline**: Automated build and deployment
3. **Performance Monitoring**: Enhanced monitoring and alerting
4. **Documentation Generation**: Automated documentation updates
5. **Code Quality**: Enhanced linting and code analysis

### Scalability Considerations
1. **Microservices**: Phase-specific microservice deployment
2. **Database Scaling**: Distributed database architecture
3. **Caching**: Enhanced caching strategies
4. **Load Balancing**: Improved load distribution
5. **Monitoring**: Advanced monitoring and observability

This structure provides a clean, organized, and scalable foundation for the AI-Powered Restaurant Recommendation System while maintaining clear separation of concerns and facilitating development and maintenance.
