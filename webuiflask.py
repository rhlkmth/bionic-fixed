from flask import Flask, request, render_template, send_file
import tempfile
import os
from your_script_name import convert_book  # Make sure to import your conversion function

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if file:
        # Save the uploaded file to a temporary file
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, file.filename)
        output_path = os.path.join(temp_dir, "converted-" + file.filename)
        file.save(input_path)
        
        # Convert the book
        convert_book(input_path, output_path)  # Adjust this call to match your function's requirements
        
        # Send the converted file back to the user
        return send_file(output_path, as_attachment=True)
    
    return "No file provided", 400

if __name__ == "__main__":
    app.run(debug=True)