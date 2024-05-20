import logo from './logo.svg';
import './App.css';
import React, { useState,useEffect } from 'react';
import axios from 'axios';
// import { Document, Page } from 'react-pdf-js';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';


function App() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [pdfUrl, setPdfUrl] = useState("");
  const [viewPdf, setViewPdf] = useState(null);
  const [responseData, setResponseData] = useState(null)

  useEffect(() => {
    if (file1) {
        const reader = new FileReader();
        
        reader.onload = (event) => {
            const url = event.target.result;
            setPdfUrl(url);
            if (url !== "") {
                setViewPdf(url);
            } else {
                setViewPdf(null);
            }
        };
        reader.readAsDataURL(file1);
    }
}, [file1]);

  const handleFile1Change = (e) => {
      setFile1(e.target.files[0]);
  };

  const handleFile2Change = (e) => {
      setFile2(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(file1)
    const formData = new FormData();
    formData.append('pdf', file1);
    formData.append('zip', file2);
    for (let [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
  }
    try {
      
        // const response = await axios.post('http://localhost:5000/upload_file', formData, {
        //     headers: {
        //         'Content-Type': 'multipart/form-data',
        //         'Access-Control-Allow-Origin': '*'
        //     },
        // });
        // console.log('Files successfully uploaded', response.data);
        // setResponseData(response.data);
        setResponseData([{'name': 'resume52.pdf', 'questions': '1. Can you elaborate on your experience using Celonis for cost optimization?\n2. How did you utilize UiPath bots to enhance operational efficiency?\n3. Describe your role in implementing IBM Watson for sentiment analysis.\n4. Can you provide details on the ML dashboards you developed for RPA monitoring?\n5. How did you leverage ABBYY FlexiCapture to improve fraud detection capabilities?', 'score': 91.75, 'path': 'resumes/resume52.pdf'}, {'name': 'resume54.pdf', 'questions': '1. Describe your experience in identifying cost-saving opportunities.\n2. Can you provide an example of how you improved a business process?\n3. How do you manage relationships with clients and stakeholders?\n4. How do you stay up-to-date on industry trends and best practices?\n5. Tell me about your experience leading a team of business analysts.', 'score': 90.25, 'path': 'resumes/resume54.pdf'}, {'name': 'resume55.pdf', 'questions': '1. Describe your experience using JDA software for report customization.\n\n2. How did you integrate SAP ERP into your supply chain management strategy?\n\n3. Explain the impact of Tableau on your inventory analysis.\n\n4. What specific improvements did you implement in Fishbowl Inventory?\n\n5. How did you utilize Google Workspace to streamline supplier communication?', 'score': 89.35, 'path': 'resumes/resume55.pdf'}])
        // console.log(pdfUrl)
        // if(pdfUrl!==""){
        //     setViewPdf(pdfUrl)
        // }
        // else{
        //     setViewPdf(null)
        // }
    } catch (error) {
        console.error('Error uploading files', error);
    }
};
  return (
    <div className="App">
        <div className='navbar'>
            <img src="https://img.freepik.com/premium-photo/there-is-3d-image-cube-with-lot-cubes-generative-ai_900321-47544.jpg" alt="" className='logo'/>
        <h1>Resume Match</h1>
        </div>
        <hr />

        <div className="container">
            <div className='steps'>
            Revolutionize your hiring process! Upload job description & candidate Resumes. Get instant scores!
            <br />
            Three Easy Steps:
            <ol>
                <li>Upload Job Description</li>
                <li>Upload Candidate Resumes (in a .zip file)</li>
                <li>Click "Submit' for Instant Scores!</li>
            </ol>
                Simplify your recruitement journey today
            </div>
        <form onSubmit={handleSubmit} className='form-container'>   
        <div className="uploads">
        <div>
            <img src="https://www.svgrepo.com/show/73906/cloud-upload.svg" alt="" className='cloudlogo'/>
            <label htmlFor="">Upload JD</label>
            <input type="file" id="pdf" accept=".pdf" onChange={handleFile1Change} />
        </div>
        <div>
            <img src="https://www.svgrepo.com/show/73906/cloud-upload.svg" alt="" className='cloudlogo'/>
            <label htmlFor="">Upload Resume Zip</label>
            <input type="file" id="file2" onChange={handleFile2Change} />
        </div>
        </div>
        <div>
        <button type="submit" className='btn'>Submit</button>
        </div>
            {viewPdf ? (
                <div className='pdf'>
                    <Worker workerUrl={`https://unpkg.com/pdfjs-dist@2.6.347/build/pdf.worker.min.js`}>
                        <Viewer fileUrl={viewPdf} plugins={[defaultLayoutPlugin]} />
                    </Worker>
                </div>
            ) : (
                <p>No PDF to display</p>
            )}
            {responseData && responseData.length > 0 && (
                <div>
                    <h2>Response Data</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Filename</th>
                                <th>Score</th>
                                <th>Path</th>
                                <th>Question</th>
                            </tr>
                        </thead>
                        <tbody>
                            {responseData.map((row, index) => (
                                <tr key={index}>
                                    <td>{row.name}</td>
                                    <td>{row.score}</td>
                                    <td>{row.path}</td>
                                    <td>{row.questions}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </form>
        </div>
    </div>  
);
}

export default App;
