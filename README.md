# Newsletter Project

This is a FastAPI project for managing a newsletter subscription system.

## Features
- Users can subscribe with an email address.
- Users can select topics of interest (placeholders for now).

## Getting Started

### Prerequisites

To run this project locally, you need the following:

- Python 3.7+
- Other dependencies listed in `requirements.txt`

### Installing

1. Clone this repository:
2. Create and activate a virtual environment
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```
3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```
5. (Optional) Test DynamoDB:
    ```bash
    python .\dynamo_db_test.py
    ```
