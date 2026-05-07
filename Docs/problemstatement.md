# Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

Build an AI-powered restaurant recommendation application inspired by Zomato.  
The system should combine structured restaurant data with a Large Language Model (LLM) to generate personalized, relevant, and easy-to-understand recommendations based on user preferences.

## Objective

Design and implement an application that:
- Accepts user preferences such as location, budget, cuisine, and minimum rating.
- Uses a real-world restaurant dataset.
- Applies an LLM to generate personalized recommendations with natural-language reasoning.
- Presents recommendations in a clear, user-friendly format.

## System Workflow

### 1) Data Ingestion
- Load and preprocess the Zomato dataset from Hugging Face:  
  https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation
- Extract key fields such as:
  - Restaurant name
  - Location
  - Cuisine
  - Estimated cost
  - Rating

### 2) User Input
Collect user preferences, including:
- Location (for example, Delhi or Bangalore)
- Budget (low, medium, high)
- Preferred cuisine (for example, Italian or Chinese)
- Minimum acceptable rating
- Optional constraints (for example, family-friendly, quick service)

### 3) Integration Layer
- Filter and prepare restaurant candidates using the user’s constraints.
- Convert filtered structured data into an LLM-friendly prompt.
- Design prompts that help the LLM compare options and rank them logically.

### 4) Recommendation Engine
Use the LLM to:
- Rank restaurants by relevance to user preferences.
- Explain why each restaurant is a good match.
- Optionally provide a short comparative summary of top choices.

### 5) Output Display
Show top recommendations in a user-friendly structure with:
- Restaurant name
- Cuisine
- Rating
- Estimated cost
- AI-generated explanation

## Related Document

For the complete implementation roadmap, see `Docs/phase-wise-architecture.md`.