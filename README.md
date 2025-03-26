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
1. FastAPI
2. Uvicorn
3. JSON
4. Pydantic
5. Postman

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