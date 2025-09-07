# Your AI Assistant

Your AI Assistant is a web application designed to extract text from PDF documents, store the content in a PostgreSQL database, and provide an interactive chatbot experience for querying the uploaded content. This project integrates Flask for backend operations, a PostgreSQL database, and a user-friendly frontend for seamless interaction.

---

## Features
- **PDF Text Extraction**: Upload PDF files, extract their text content, and store it in a database.
- **Content Querying**: Search through uploaded PDF content and get answers via an AI-powered chatbot.
- **Interactive Chat Interface**: Simple and engaging UI for chatting with the AI assistant.
- **Database Management**: PostgreSQL integration for efficient data storage and retrieval.

---

## Installation

Follow these steps to set up the project on your local machine:

### Prerequisites
- Python 3.8+
- Docker

### Steps
1. Clone this repository:
    ```bash
    git clone https://github.com/yigitcanbltc/pdf-reader-ai.git
    cd <repository_name>
    ```

2. Set up the PostgreSQL database using Docker:
    ```bash
    docker run -d \
      -e POSTGRES_DB=ai \
      -e POSTGRES_USER=ai \
      -e POSTGRES_PASSWORD=ai \
      -e PGDATA=/var/lib/postgresql/data/pgdata \
      -v pgvolume:/var/lib/postgresql/data \
      -p 5532:5432 \
      --name pgvector \
      phidata/pgvector:16
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask application:
    ```bash
    python main.py
    ```

5. Upload a PDF file through the on your local host.

6. Open index.html and test application.

---

## Project Structure
- `main.py`: Contains backend logic and API endpoints.
- `script.js`: Handles frontend interactivity for the chatbot.
- `index.html`: The main HTML file for the user interface.
- `style.css`: Manages the visual styling of the application, including the chat interface and upload forms.
- `pdfs/`: Directory for storing uploaded PDF files.
- `uploads/`: Temporary folder for handling file uploads.

---

## Screenshots
Here are some screenshots showcasing the application:
1. **Results**:
   ![qa1](https://github.com/user-attachments/assets/d2f5e75f-67f0-4c8d-ab59-1a23c03a8c9d)
   ![q1](https://github.com/user-attachments/assets/600943cb-29a5-4e6f-aa75-39e96a3aec83)
   ![qa2](https://github.com/user-attachments/assets/2581fc47-d008-4e39-a0b0-00426b470f7b)
   ![q2](https://github.com/user-attachments/assets/d791909f-8773-4f4f-8eff-e1ef8d9b882b)
   ![qa3](https://github.com/user-attachments/assets/10fccbe5-9e5a-4a44-925a-3dfa8282f758)
   ![q3](https://github.com/user-attachments/assets/4fefc8fe-7d92-4084-9e42-d77f4e4706ad)

---

## Requirements

A `requirements.txt` file is included in the repository. It contains all the dependencies required to run the project. Install these packages using the command:

```bash
pip install -r requirements.txt
```

---

## Contributing
Feel free to contribute to this project by submitting issues or pull requests.

---



