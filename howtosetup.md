When cloning the repository on a new computer, follow these steps to set up the project:

---

### **1. Clone the Repository**

- Open a terminal and run:

  ```bash
  git clone <repository_url>
  ```

  Replace `<repository_url>` with the URL of your Git repository.

- Navigate into the cloned directory:
  ```bash
  cd chatbot
  ```

---

### **2. Set Up a Virtual Environment**

- Create and activate a virtual environment:
  ```bash
  python3 -m venv chatbot-env
  source chatbot-env/bin/activate
  ```
  For Windows:
  ```bash
  python -m venv chatbot-env
  chatbot-env\Scripts\activate
  ```

---

### **3. Install Dependencies**

- Install the Python libraries listed in `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

---

### **4. Set Up Environment Variables**

- Create a `.env` file in the project root if it doesn’t exist:
  ```bash
  touch .env
  ```
- Add your environment-specific variables, such as the OpenAI API key:
  ```
  OPENAI_API_KEY=your_openai_api_key
  ```

---

### **5. Test the Application**

- Run the application locally to ensure it's working:
  ```bash
  uvicorn main:app --reload
  ```
- Open `http://127.0.0.1:8000/docs` in your browser to view the FastAPI Swagger documentation.

---

### **6. Set Up Git for Version Control**

- If this is a new environment, configure your Git username and email:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your_email@example.com"
  ```

---

### **7. (Optional) Docker Setup**

If you're using Docker:

1. Ensure Docker is installed and running.
2. Build the Docker image:
   ```bash
   docker build -t chatbot .
   ```
3. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 chatbot
   ```

---

### **8. Verify Functionality**

- Test API endpoints using cURL, Postman, or the FastAPI Swagger UI at `/docs`.

---

This process ensures the chatbot application is properly set up and ready to run on a new computer.
