import os
from flask import Flask, flash, request, redirect, url_for
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from helper import unzip_resumes,get_text,preprocess_text,get_jd_text,get_embedding,get_question,get_score
import warnings
warnings.filterwarnings("ignore")

# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app = Flask(__name__)

@app.route('/upload_file', methods=['POST'])
def upload_pdf():
    output=[]
    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file part'}), 400
    # file = request.files['file']
    # if file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400
    unzip_resumes() # from frontend
    jd_text=get_jd_text("job_desc/jd_qa_sr.pdf") # get_name from frontend
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

if __name__ == '__main__':
    app.run(debug=True)

