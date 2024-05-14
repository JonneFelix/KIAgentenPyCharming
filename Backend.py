from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import fitz

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    # Echos die erhaltene Nachricht zur�ck an den Absender
    emit('message', f'Echo: {msg}', broadcast=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)


def open_pdf_button(pdf_path):
    text = pdf_ocr(pdf_path)
    json_file_path = "Json Files/myfile.json"
    save_text_as_json(text, json_file_path)
    # Example print to check if it works
    with open('Json Files/myfile.json', 'r') as file:
        data = json.load(file)

    print(json.dumps(data, indent=4))


def pdf_ocr(pdf_path):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Initialize an empty string to store extracted text
    text = ""

    # Iterate through each page in the PDF
    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Extract text from the page
        text += page.get_text()

    # Close the PDF
    pdf_document.close()

    return text

def save_text_as_json(text, json_file_path):
    # Create a dictionary to store the text
    data = {'text': text}

    # Write the dictionary to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file)


# Example usage
#pdf_path = "PDF Example Files/Estimation of the Gross Fixed Kapital using linear Regression.pdf"
#open_pdf_button(pdf_path)


