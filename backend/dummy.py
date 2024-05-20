from helper import unzip_resumes,get_text,preprocess_text,get_jd_text,get_embedding,get_question,get_score
import os
import warnings
warnings.filterwarnings("ignore")

def upload_pdf():
    output=[]
    unzip_resumes() # from frontend
    print("unzip done")
    jd_text=get_jd_text("job_desc/jd_qa_sr.pdf") # get_name from frontend
    jd_res=preprocess_text(jd_text)
    jd_emb=get_embedding(jd_res)
    print("JD done")
    for filename in os.listdir("resumes/"):
        file_path = os.path.join("resumes/", filename)
        if os.path.isfile(file_path):
            print(f"{filename} Started")
            res_text=get_text(file_path)
            res_res=preprocess_text(res_text)
            question=get_question(res_text)
            res_emb=get_embedding(res_res)
            print("embedding done")
            score=get_score(res_emb,jd_emb)
            output.append({"name":filename,"questions":question,"score":score,"path":file_path})
            sorted_output = sorted(output, key=lambda x: x['score'], reverse=True)
            print(f"{filename} done")
    return sorted_output

op=upload_pdf()
for i in op:
    print(i["name"], "****",i["score"],"********",i['path'])
