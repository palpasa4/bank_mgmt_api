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
Start by cloning the project repository to your local machine. Run the following command in terminal:
```git clone https://github.com/palpasa4/bank_mgmt_api```

2. Set up a virtual environment:
Run the following command in the terminal to set up a virtual environment and activate it.
#Create a virtual environment
```python -m venv .venv```
#Activate the virtual environment
```venv\Scripts\activate```

2. Install FastAPI and Uvicorn
After activating the virtual environment, install FastAPI and Uvicorn:
```pip install "fastapi[standard]" uvicorn```

3. Run the FastAPI Application
Start the FastAPI app using the development server:
```fastapi dev server.py```

4. Test the APIs in Postman:
- Open Postman.
- Use the URL: http://127.0.0.1:8000 to make requests.
- You can also access the interactive docs at: http://127.0.0.1:8000/docs to view and test the API.


### Usage 

While making requests in Postman:

1. Login to obtain a token as response: 
- Send a POST request to the login endpoint with valid credentials.
- The response contains an ID (token), used in making further requests. 

2. Use tokens for API requests: 
- Tokens obtained in response after a valid login are used to access protected endpoints.

Example:
An admin makes a post request to /admin/login with valid credentials and obtains a response as:
```{"message": "Login Success", "admin_id": AD-12345678}```
This ID should be passed as an authentication header in subsequent API requests, (for eg: to access the endpoint: /admin/create_users.)