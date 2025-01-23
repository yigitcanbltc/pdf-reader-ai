import os
import PyPDF2
import logging
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app)

os.makedirs('pdfs', exist_ok=True)
os.makedirs('uploads', exist_ok=True)


Base = declarative_base()
engine = create_engine('postgresql://ai:ai@localhost:5532/ai', echo=True)
Session = sessionmaker(bind=engine)

class Document(Base):
    __tablename__ = 'document'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    source = Column(String)

Base.metadata.create_all(engine)


API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def extract_pdf_text(pdf_path):
    """Extract text from PDF with robust method"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""
            for page in reader.pages:
                page_text = page.extract_text() or ''
                full_text += page_text + "\n"
        return full_text.strip()
    except Exception as e:
        logger.error(f"PDF text extraction error: {e}")
        raise

def add_document_to_knowledge_base(content, source):
    """Add document to knowledge base"""
    session = Session()
    try:
        new_doc = Document(content=content, source=source)
        session.add(new_doc)
        session.commit()
        logger.info(f"Document {source} added to knowledge base")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        session.close()

@app.route('/', methods=['GET'])
def upload_form():
    """Render PDF upload form"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <body>
        <h2>PDF Upload</h2>
        <form action="/upload_pdf" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf">
            <input type="submit" value="Upload PDF">
        </form>
    </body>
    </html>
    ''')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    """PDF upload endpoint"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['file']
    
    if pdf_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    pdf_path = os.path.join('pdfs', pdf_file.filename)
    pdf_file.save(pdf_path)

    try:
        pdf_text = extract_pdf_text(pdf_path)
        
        if not pdf_text:
            return jsonify({'error': 'Could not extract text'}), 400

        add_document_to_knowledge_base(pdf_text, pdf_file.filename)
        
        return jsonify({
            'message': 'PDF uploaded successfully',
            'filename': pdf_file.filename,
            'text_length': len(pdf_text)
        })
    except Exception as e:
        logger.error(f"Upload error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    user_question = request.json.get('question', '')

    session = Session()
    try:
        results = session.query(Document).filter(Document.content.like(f'%{user_question}%')).all()
        context = [doc.content for doc in results]
    except SQLAlchemyError as e:
        logger.error(f"Database query error: {e}")
        return jsonify({'error': 'Database query failed'}), 500
    finally:
        session.close()

    try:
        full_prompt = f"Context: {context or 'No context found'}\n\nQuestion: {user_question}"
        response = model.generate_content(full_prompt)
        return jsonify({'answer': response.text})
    except Exception as e:
        logger.error(f"Generation error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)