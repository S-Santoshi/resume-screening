import logo from './logo.svg';
import './App.css';
import React, { useState,useEffect } from 'react';
import axios from 'axios';
// import { Document, Page } from 'react-pdf-js';
import { Worker, Viewer, classNames } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
// import PDFViewer from 'pdf-viewer-reactjs'

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

  const renderQuestions = (questions) => {
    return questions.split('\n').map((question, index) => (
      <p key={index}>{question}</p>
    ));
  };

  const handleSubmit = async (e) => {

    e.preventDefault();
    setResponseData(null);
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

const openPdfInNewTab = (pdfPath) => {
    // Open the PDF file in a new tab
    let pdfu="home/admin123/Documents/python/resume-screening/"+pdfPath
    window.open(pdfu, '_blank');
};
  return (
    <div className="App">
        <div className='navbar'>
            <img src="https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcR3z5k3t7y2-0hG7e_AWfv5zR11C5UNNREL7iZwK_8rxwWNKOZ4" alt="" className='logo'/>
        <h1>Resume Match</h1>
        </div>
        <hr />

        <div className="container">
            <div className='steps'>
            Revolutionize your hiring process! Upload job description & candidate Resumes. Get instant scores!
            <br />
            <br />
            Three Easy Steps:
            <ol>
                <li>Upload Job Description</li>
                <li>Upload Candidate Resumes (in a .zip file)</li>
                <li>Click "Submit' for Instant Scores!</li>
            </ol>
                <b>Simplify your recruitement journey today </b>
            </div>
        <form onSubmit={handleSubmit} className='form-container'>   
        <div className="uploads">
        <div>
            <div>
            <img src="https://www.svgrepo.com/show/73906/cloud-upload.svg" alt="" className='cloudlogo'/>
            <br/>
            Upload Job description PDF to get started 
            </div>
            {/* <label htmlFor="">Upload JD</label> */}
            <br/>
            <input type="file" id="pdf" accept=".pdf" onChange={handleFile1Change} />
        </div>
        <div>
            <div>
            <img src="https://www.svgrepo.com/show/73906/cloud-upload.svg" alt="" className='cloudlogo'/>
            <br/>
            Upload Resume Zip file to get scores 
            </div>
            <br/>
            {/* <label htmlFor="">Upload Resume Zip</label> */}
            <input type="file" id="zip" onChange={handleFile2Change} />
        </div>
        </div>
        <div>
        <button type="submit" className='btn'>Submit</button>
        </div>
        <div className='output'>
            <div classname='jd_viewer'>
            {viewPdf ? (
                <div className='pdf'>
                    <Worker workerUrl={`https://unpkg.com/pdfjs-dist@2.16.105/build/pdf.worker.min.js`}>
                        <Viewer fileUrl={viewPdf} plugins={[defaultLayoutPlugin]} />
                    </Worker>
                </div>
            ) : (
                <p></p>
            )}
            </div>
            <div className='result'>
            {responseData && responseData.length > 0 && (
                <div>
                    <b>Results !</b>
                    <br/>
                    <br/>
                    <table>
                        {/* <thead>
                            <tr>
                                <th>Filename</th>
                                <th>Score</th>
                                <th>Path</th>
                                <th>Question</th>
                            </tr>
                        </thead> */}
                        <tbody>
                            {responseData.map((row, index) => (
                                <div className='result_row'>
                                <details className='dropdown'>
                                    <summary>
                                        
                                        <tr key={index}>
                                        {/* <td className='cell'><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJQAAACUCAMAAABC4vDmAAAAJ1BMVEUBAAL///8AAAKWlpZwcHAVFBWko6TDw8T7/PuMjIyHhofq6ekJCAkEgSW/AAAA6UlEQVR4nO3cORLCMAxAUaPsy/3PC8zQBSYhhUeE53RO8/3Uq9y2Z2i7KFVOdO3wJqBsbsYpIsqjKj58313v/IiYxgNRc1RiemHFvB+1rHHu5eekHlHrshvV14V6UvW7Uc3Zl5+VKtEciap8jkWRIkWKFClSpEiRIlVHKmWU8ZEiRYoUKVKkSJEiRYrUtaVSRhkfKVKkSJEiRYoUKVKkflMqZZTxkSJFihQpUqRIkSJFitS1pVJGGR8pUqRIkSJFihQpUqRIXVsqZZTxkSJFihQpUqRIkfpXqZRrDlMuhEy5OjPnktEE61jvK+s2t5sV6HEAAAAASUVORK5CYII=" alt="" className='blackrect'/></td> */}
                                        <td className='cellname'>{row.name}</td>
                                        
                                        <td className='cellscore'>Score: {row.score}%</td>
                                        {/* <td className='cellpath'>{row.path}</td> */}
                                    {/* <td className='cellpath'> <img
                                        src="https://www.freeiconspng.com/thumbs/pdf-icon-png/pdf-icon-png-pdf-zum-download-2.png"
                                        alt="PDF Image"
                                        onClick={() => openPdfInNewTab(row.path)}
                                        style={{ cursor: 'pointer' }}
                                        className="pdf_image"
                                    /></td> */}
                                        {/* <td className='cellpath'>
                                        <a href={row.path} target="_blank">
                                        <img src="https://www.freeiconspng.com/thumbs/pdf-icon-png/pdf-icon-png-pdf-zum-download-2.png" className="pdf_image"/> 
                                        
                                        </a></td> */}

                                    {/* <td>{row.questions}</td> */}
                                </tr>
                                </summary>
                                <p>
                                    <b>Questions: </b>
                                </p>
                                    {renderQuestions(row.questions)}
                                    
                                </details>
                                </div>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
            </div>
            </div>
        </form>
        </div>
    </div>  
);
}

export default App;
