import React, { useState } from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [zipFile, setZipFile] = useState(null);
  const [pdfUrl, setPdfUrl] = useState(null);
  const [zipUrl, setZipUrl] = useState(null);

  const handlePdfChange = (event) => {
    setPdfFile(event.target.files[0]);
  };

  const handleZipChange = (event) => {
    setZipFile(event.target.files[0]);
  };

  const uploadFiles = async () => {
    try {
      const formData = new FormData();
      if (pdfFile) formData.append('pdf', pdfFile);
      if (zipFile) formData.append('zip', zipFile);

      const response = await axios.post('http://your-backend-url.com/upload_files', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      setPdfUrl(response.data.pdfUrl);
      setZipUrl(response.data.zipUrl);
    } catch (error) {
      console.error('Error uploading files:', error);
    }
  };

  const openPdf = () => {
    window.open(pdfUrl, '_blank');
  };

  const openZip = () => {
    window.open(zipUrl, '_blank');
  };

  return (
    <div>
      <div>
        <label>Upload PDF:</label>
        <input type="file" onChange={handlePdfChange} accept="application/pdf" />
      </div>
      <div>
        <label>Upload ZIP:</label>
        <input type="file" onChange={handleZipChange} accept=".zip" />
      </div>
      <button onClick={uploadFiles}>Submit</button>
      {pdfUrl && <button onClick={openPdf}>Open PDF</button>}
      {zipUrl && <button onClick={openZip}>Open ZIP</button>}
    </div>
  );
};

export default FileUploader;
