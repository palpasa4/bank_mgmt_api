# Basic Overview of the System:

### Purpose: 
A simple banking system built with FastAPI for handling basic banking operations.

### Features:
- User registration and login
- Withdraw amount
- Deposit amount
- View account details
- Save and view transactions.
- Access Control (Admin/User) using ID as tokens

### Technology Choices and Rationale:
1. FastAPI: 
A fast, modern web framework for building APIs with Python, whcih supports automatic validation and documentation generation.

2. Uvicorn: 
Uvicorn as an ASGI(Asynchronous Server Gateway Interface) server, is fast, lightweight,async-capable and provides better performance for concurrent requests.

3. JSON: 
JSON files are used as database while working with FastAPI, which works with JSON for request bodies and responses.

4. Pydantic: 
Pydantic provides data validation and parsing library, for defining data models and ensuring data integrity.

5. Postman: 
It is used as a tool for testing and interacting with APIs during development.


### Setup Instructions:

1. Clone the Repository
```git clone https://github.com/palpasa4/bank_mgmt_api```

2. Set up a virtual environment:
#Create a virtual environment
```python -m venv .venv```
#Activate the virtual environment
```venv\Scripts\activate```

2. Install FastAPI and Uvicorn
```pip install "fastapi[standard]" uvicorn```

3. Run the FastAPI Application
```fastapi dev server.py```

4. Test the APIs in Postman:
- Open Postman.
- Use the URL: http://127.0.0.1:8000 to make requests.
- You can also access the interactive docs at: http://127.0.0.1:8000/docs to view and test the API.