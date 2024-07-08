Prerequisites
- Python 3.12
- Docker (optional, for containerization)
- SQLite (included with Python)
Step-by-Step Instructions

1. Clone the Repository:
```
git clone https://github.com/sherjeelaqil/mock_chatbot.git
cd mock_chatbot
```

2. Set Up a Virtual Environment:
```
python -m venv venv
venv/Scripts/activate  # On Windows, use `venv\Scripts\activate`
```
3. Install Dependencies:
```
pip install -r requirements.txt
```
4. Initialize the Database:
```
python app/database.py
```
5. Start the FastAPI Server:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
6. Start the WebSocket Server:
```
python websocket_server/server.py
```
7. Run Tests:
```
pytest -vs
```
8. Load Tests:
```
locust -f tests\locustfile.py --host=http://localhost:8000
```
