import re
import PyPDF2
import requests
import os
import json
import logging
import pickle
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
OUTPUT_FOLDER = 'output'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Check if the upload folder exists, if not, create it
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
# Check if the output folder exists, if not, create it
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to check if the uploaded file is of an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to validate a PDF file
def validate_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if len(reader.pages) > 0:
                return True
    except Exception as e:
        logger.error(f"File validation error: {e}")
        return False
    return False

# Function to extract text from a PDF file
def pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(reader.pages)):
            try:
                page_text = reader.pages[page_num].extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                logger.error(f"Error extracting text from page {page_num}: {e}")
    return text

# Function to clean text by removing specific unicode patterns and extra whitespace
def clean_text(text):
    clean_text = re.sub(r'\\u\w{4}', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()


def generation2(VectorStore, query):
    retriever = VectorStore.as_retriever(search_type="similarity", search_kwargs={"k": chunk_amount})
    model = OpenAI(model_name="qwen1.5-72b-chat", openai_api_key=API_KEY, openai_api_base=BASE_URL)
    qa = RetrievalQA.from_chain_type(llm=model, chain_type="refine", retriever=retriever, return_source_documents=False,
                                     verbose=True)

    prompt = '''
Extract the following key values from the provided PDF content and format them strictly as a JSON object. 
Ensure the JSON is valid, properly formatted, and includes all keys even if their values are empty. 
If certain values are not available, leave them as empty strings.

{
    "name": "NAME_OF_THE_DOC",
    "CO2": "",
    "NOX": "",
    "Number_of_Electric_Vehicles": "",
    "Impact": "",
    "Risks": "",
    "Opportunities": "",
    "Strategy": "",
    "Actions": "",
    "Adopted_policies": "",
    "Targets": ""
}

PDF Content:
'''

    # calling relevant Chunks
    relevant_chunks = retriever.get_relevant_documents(query)
    logger.info(f"Number of relevant chunks retrieved: {len(relevant_chunks)}")

    # Combining the Text of all relevant Chunks
    pdf_content = "\n".join(chunk.page_content for chunk in relevant_chunks)

    # Combining the Prompt with the PDF Content
    full_prompt = prompt + pdf_content

    result = qa.run({"query": full_prompt})

    # Extracting the JSON from the result
    json_start = result.find('{')
    json_end = result.rfind('}') + 1
    json_string = result[json_start:json_end]

    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        logger.error(f"JSON Decode Error: {e}")
        return {"error": "Invalid JSON format in response"}

    return json_data


# Route to render the home page
@app.route("/")
def home_route():
    return render_template("home.html")

# Route to handle the chat page
@app.route("/chat")
def chat_route():
    pdf_filename = request.args.get('pdf', None)
    pdf_text = ""
    if pdf_filename:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        pdf_text = pdf_to_text(pdf_path)
    return render_template("chat.html", pdf_filename=pdf_filename, pdf_text=pdf_text)

# Route to serve uploaded files from the UPLOAD_FOLDER directory
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Handel Chat messages and responses
@app.route("/api/chat", methods=["POST"])
def chat_api():
    #get the message
    user_message = request.json.get("message")
    model = request.json.get("model", "qwen1.5-72b-chat")
    # get the chunks most similar to the user message
    vector_store = load_vector_store('vector_store.pkl')
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": chunk_amount})
    retrieved_docs = retriever.invoke(user_message)

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    #check for old messages. If message 3 or more:
    if os.path.exists(os.path.join(app.config['OUTPUT_FOLDER'], 'prompt2.json')):
        #get old messages and respones
        prompt_text1 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'prompt1.json')).read()
        prompt_text2 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'prompt2.json')).read()
        response_text1 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'response1.json')).read()
        response_text2 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'response2.json')).read()
        #create prompt with old messages and responses
        prompt = (
            f"The folowing PDF was uploaded:\n\n{retrieved_docs}\n\n"
            f"Our conversation until this point:\n\nQuestion 1:{prompt_text2} Answer 1: {response_text2}\n"
            f"Question 2:{prompt_text1} Answer 2: {response_text1}\n"
            f"with all given Information answer this Question:{user_message}"
        )
    #check for old messages. If message 2:
    elif os.path.exists(os.path.join(app.config['OUTPUT_FOLDER'], 'prompt1.json')):
        #get old messages and respones
        prompt_text1 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'prompt1.json')).read()
        response_text1 = open(os.path.join(app.config['OUTPUT_FOLDER'], 'response1.json')).read()
        #create prompt with old messages and responses
        prompt = (
            f"The folowing PDF was uploaded:\n\n{retrieved_docs}\n\n"
            f"Our conversation until this point:\n\nQuestion 1:{prompt_text1} Answer 1: {response_text1}\n"
            f"with all given Information answer this Question:{user_message}"
        )
    #first message
    else:
        #prompt without old messages
        prompt = f"The folowing PDF was uploaded:\n\n{retrieved_docs}\n\nwith the given Information answer this Question:{user_message}"

    print(prompt)
    save_prompt([user_message])

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    #get response from API
    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    response_data = response.json()

    save_response(response_data)

    #return response
    logger.info(f"API response: {response_data}")
    return jsonify(response_data)

#save the text chunks
def save_chunks(chunks, filename):
    chunk_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{filename}_chunks.pkl")
    with open(chunk_file, 'wb') as f:
        pickle.dump(chunks, f)

#handeling an pdf upload
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['file']
        if file and allowed_file(file.filename):
            #get the chunksize and get the chunkamount arcorrding to the chunksize to avoid to long prompts
            global chunk_size, chunk_amount
            chunk_size = int(request.form.get('chunk_size'))
            chunk_amount = determine_chunk_amount(chunk_size)
            logger.info(f"Chunk size: {chunk_size}")
            #delete old files to make checks for first question possible
            delete_files_in_folder(app.config['UPLOAD_FOLDER'])
            delete_files_in_folder(app.config['OUTPUT_FOLDER'])
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if not os.path.exists(filepath):
                logger.error("File not saved properly")
                return jsonify({"error": "File not saved properly"}), 500

            logger.info("File saved successfully")

            if not validate_pdf(filepath):
                logger.error("Invalid or corrupted PDF file")
                return jsonify({"error": "Invalid or corrupted PDF file"}), 400
            #get text on pdf
            text = pdf_to_text(filepath)
            #store pdf text in chunks off selected chunksize
            chunks = chunk_processing(text, chunk_size)
            save_chunks(chunks, filename)
            vector_store = embeddings(chunks)
            save_vector_store(vector_store, 'vector_store.pkl')

            #return pdf text
            return jsonify({"filename": filename, "text": text})
        return jsonify({"error": "Invalid file format"}), 400
    except Exception as e:
        logger.error(f"Exception during file upload: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/download-json", methods=["GET"])
def download_json():
    pdf_filename = request.args.get('pdf', None)
    if not pdf_filename:
        return jsonify({"error": "No PDF file specified"}), 400

    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    if not os.path.exists(pdf_path):
        return jsonify({"error": "PDF file not found"}), 404

    vector_store = load_vector_store('vector_store.pkl')  # Laden des VectorStore
    query = "Extract key values from the PDF"  # Beispiel-Abfrage, anpassen falls notwendig
    result = generation2(vector_store, query)  # Korrekte Aufruf von generation2

    if "error" in result:
        logger.error(f"Failed to extract key values: {result['error']}")
        return jsonify(result), 500

    output_file = os.path.join(app.config['OUTPUT_FOLDER'], 'extracted_key_values.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)

    return send_file(output_file, as_attachment=True)



# Function to split text into chunks, called with selected chunksize
def chunk_processing(text,chunk_s):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_s,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text=text)
    return chunks

#embeddings for the chunks
def embeddings(chunks):
    embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store

#save and load the vectorstore
def save_vector_store(vector_store, filename):
    directory = 'vectorStore'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        pickle.dump(vector_store, f)

def load_vector_store(filename):
    directory = 'vectorStore'
    filepath = os.path.join(directory, filename)
    with open(filepath, 'rb') as f:
        return pickle.load(f)

#save and load the prompt and response
def save_response(response_data):
    output_folder = app.config['OUTPUT_FOLDER']
    response1_path = os.path.join(output_folder, 'response1.json')
    response2_path = os.path.join(output_folder, 'response2.json')

    if os.path.exists(response2_path):
        os.remove(response2_path)

    if os.path.exists(response1_path):
        os.rename(response1_path, response2_path)

    with open(response1_path, 'w') as f:
        json.dump(response_data, f)

def save_prompt(prompt_data):
    output_folder = app.config['OUTPUT_FOLDER']
    prompt1_path = os.path.join(output_folder, 'prompt1.json')
    prompt2_path = os.path.join(output_folder, 'prompt2.json')

    if os.path.exists(prompt2_path):
        os.remove(prompt2_path)

    if os.path.exists(prompt1_path):
        os.rename(prompt1_path, prompt2_path)

    prompt_data_list = list(prompt_data)

    with open(prompt1_path, 'w') as f:
        json.dump(prompt_data_list, f)

#delete files in folder
def delete_files_in_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"Skipping non-file item: {file_path}")
    except Exception as e:
        print(f"Error: {e}")

#determine the amount of chunks acording to the chunksize
def determine_chunk_amount(size):
    if size == 200:
        amount = 5
    elif size == 300:
        amount = 4
    elif size == 400:
        amount = 3
    elif size == 500:
        amount = 2
    return amount

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="127.0.0.1", port=5004)
