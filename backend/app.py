import os
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from helper import unzip_resumes,get_text,preprocess_text,get_jd_text,get_embedding,get_question,get_score
import warnings
warnings.filterwarnings("ignore")
from flask_cors import CORS

UPLOAD_FOLDER = 'resumes/'
ALLOWED_EXTENSIONS = {'pdf','zip'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)
CORS(app)
def allowed_file(filename,ext):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ext

@app.route('/upload_file', methods=['POST'])
def upload_pdf():
    output=[]
    if 'pdf' not in request.files or 'zip' not in request.files:
        return 'No file part', 400
    
    jd = request.files['pdf']
    res_zip = request.files['zip']
    
    if jd.filename == '' or res_zip.filename == '':
        return 'No selected file', 400
    
    if jd and allowed_file(jd.filename,{'pdf'}):
        jd_name = secure_filename(jd.filename)
        jd.save(os.path.join("job_desc/", jd_name))

    if res_zip and allowed_file(res_zip.filename,{'zip'}):
        zip_name = secure_filename(res_zip.filename)
        res_zip.save(os.path.join("", zip_name))
    unzip_resumes(zip_name)
    jd_text=get_jd_text(f"job_desc/{jd_name}")
    jd_res=preprocess_text(jd_text)
    jd_emb=get_embedding(jd_res)
    for filename in os.listdir("resumes/"):
        file_path = os.path.join("resumes/", filename)
        if os.path.isfile(file_path):
            print(filename)
        res_text=get_text(file_path)
        res_res=preprocess_text(res_text)
        question=get_question(res_text)
        res_emb=get_embedding(res_res)
        score=get_score(res_emb,jd_emb)
        output.append({"name":filename,"questions":question,"score":score,"path":file_path})
        sorted_output = sorted(output, key=lambda x: x['score'], reverse=True)
    return sorted_output

@app.route('/dummy', methods=['GET'])
def dummy():
    return "Hello world"
if __name__ == '__main__':
    app.run(debug=True)

