import os
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from helper import unzip_resumes,get_text,get_jd_text,get_embedding,get_score
from LLM_module import get_question

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    unzip_resumes("zip")
    res_text=get_text("filename")
    jd_text=get_jd_text("filename")
    res_emb=get_embedding(res_text)
    jd_emb=get_embedding(jd_text)
    score=get_score(res_emb,jd_emb)
    question=get_question(res_text)
    output=0
    return output

if __name__ == '__main__':
    app.run(debug=True)

