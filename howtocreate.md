Here’s a step-by-step guide to set up a chatbot with a REST API using **ChatGPT**, **LangGraph**, **Python**, and **FastAPI**.

---

### Step 1: **Create a Git Repository**

1. Create a repository on GitHub or your preferred platform with a name like `chatbot-langgraph-restapi`.
2. Clone the repository locally:
   ```bash
   git clone https://github.com/yourusername/chatbot-langgraph-restapi.git
   cd chatbot-langgraph-restapi
   ```

---

### Step 2: **Set Up the Python Environment**

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Upgrade `pip` and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install openai langchain langgraph fastapi uvicorn python-dotenv
   ```
3. Save dependencies:
   ```bash
   pip freeze > requirements.txt
   ```

---

### Step 3: **Set Up Environment Variables**

1. Create a `.env` file:
   ```bash
   touch .env
   ```
2. Add your API keys to `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   LANGGRAPH_API_KEY=your_langgraph_api_key
   ```
3. Add `.env` to `.gitignore`:
   ```bash
   echo ".env" >> .gitignore
   ```

---

### Step 4: **Organize the Project**

Create the following structure:

```
chatbot-langgraph-restapi/
├── .env
├── .gitignore
├── requirements.txt
├── main.py       # FastAPI application
├── chatbot.py    # Chatbot logic
└── tests/        # Directory for unit tests
```

---

### Step 5: **Implement the Chatbot Logic**

1. Create `chatbot.py`:

   ```python
   import openai
   import os
   from dotenv import load_dotenv

   load_dotenv()

   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

   openai.api_key = OPENAI_API_KEY

   def get_chatbot_response(prompt):
       try:
           response = openai.Completion.create(
               engine="text-davinci-003",
               prompt=prompt,
               max_tokens=150
           )
           return response.choices[0].text.strip()
       except Exception as e:
           return str(e)
   ```

---

### Step 6: **Build the REST API**

1. Create `main.py`:

   ```python
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   from chatbot import get_chatbot_response

   app = FastAPI()

   class ChatRequest(BaseModel):
       message: str

   class ChatResponse(BaseModel):
       reply: str

   @app.post("/chat", response_model=ChatResponse)
   async def chat(request: ChatRequest):
       user_message = request.message
       try:
           bot_reply = get_chatbot_response(user_message)
           return ChatResponse(reply=bot_reply)
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   @app.get("/")
   async def root():
       return {"message": "Welcome to the Chatbot API!"}
   ```

---

### Step 7: **Run the API Locally**

1. Start the FastAPI server using `uvicorn`:
   ```bash
   uvicorn main:app --reload
   ```
2. The server will run at `http://127.0.0.1:8000`.

---

### Step 8: **Test the API**

1. **Test the API** using tools like **Postman**, **cURL**, or your browser:
   - **GET** request to `http://127.0.0.1:8000/`:
     ```json
     { "message": "Welcome to the Chatbot API!" }
     ```
   - **POST** request to `http://127.0.0.1:8000/chat` with body:
     ```json
     {
       "message": "Hello, chatbot!"
     }
     ```
     Response:
     ```json
     {
       "reply": "Hello! How can I assist you today?"
     }
     ```

---

### Step 9: **Commit and Push Changes**

1. Add your changes:
   ```bash
   git add .
   git commit -m "Add chatbot REST API with FastAPI"
   ```
2. Push to your remote repository:
   ```bash
   git push origin main
   ```

---

### Step 10: **Enhancements**

1. **Add Swagger Documentation**:
   - Visit `http://127.0.0.1:8000/docs` for automatic API documentation.
2. **Write Tests**:
   - Add test cases in the `tests/` directory using `pytest` or `unittest`.
3. **Deploy the API**:
   - Use **Docker**, **Heroku**, **AWS Lambda**, or **Google Cloud Run** for deployment.

---

### Optional: **Dockerize the Project**

1. Create a `Dockerfile`:

   ```dockerfile
   FROM python:3.10-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Build and run the Docker container:
   ```bash
   docker build -t chatbot-api .
   docker run -p 8000:8000 chatbot-api
   ```

Would you like help with deployment, testing, or writing additional features?
