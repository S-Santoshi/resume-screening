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
      
        const response = await axios.post('http://localhost:5000/upload_file', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Access-Control-Allow-Origin': '*'
            },
        });
        console.log('Files successfully uploaded', response.data);
        setResponseData(response.data);
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
        <h1>Upload Files</h1>
        <form onSubmit={handleSubmit}>
        <div>
            <label htmlFor="pdf">Choose a PDF file:</label>
            <input type="file" id="pdf" accept=".pdf" onChange={handleFile1Change} />
        </div>
        <div>
            <label htmlFor="file2">File 2:</label>
            <input type="file" id="file2" onChange={handleFile2Change} />
        </div>
            <button type="submit">Submit</button>
            {viewPdf ? (
                <div>
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
);
}

export default App;
