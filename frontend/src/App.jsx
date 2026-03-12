import { useEffect, useRef, useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [parsedData, setParsedData] = useState(null);
  const [parsing, setParsing] = useState(false);
  const [dots, setDots] = useState("");
  const fileInputRef = useRef(null);


  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];

    if(droppedFile && droppedFile.type === "application/pdf"){
      setFile(droppedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  }

  useEffect(() => {
    if (!parsing) return;
  
    const interval = setInterval(() => {
      setDots(prev => {
        if (prev.length >= 3) return "";
        return prev + ".";
      });
    }, 500);
  
    return () => clearInterval(interval);
  }, [parsing]);

  const handleUpload = async () => {
    if (!file) return;
    
    setParsing(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/resume/extract-text", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      const parsedObject = JSON.parse(data.parsed);
      setParsedData(parsedObject)
    } catch (err) {
      console.error("Upload failed", err);
    }

    setParsing(false);
  };

  return (
    <div>
      <h1>AI-Resume-Extractor</h1>

      <h2>Please put up your file:</h2>

      <div className='dropzone' onDrop={handleDrop} onDragOver={handleDragOver} onClick={() => fileInputRef.current.click()}>
        {file ? (
          <p>{file.name}</p>
        ) : (
          <p>Drag & Drop your PDF in here or click to Upload</p>
        )}
        <input type="file" accept='application/pdf' ref={fileInputRef} onChange={handleFileChange} />
      </div>
    
      <br/>
      <button style={{marginTop: "20px", marginBottom: "30px"}} onClick={handleUpload}>Upload PDF</button>
      <br/>

      {parsing && <h2>Parsing data{dots}</h2>}

      {!parsing && parsedData && (
        <div>
        <p><b>Name:</b> {parsedData.name}</p>
        <p><b>Email:</b> {parsedData.email}</p>
        <p><b>Skills:</b> {parsedData.skills.join(", ")}</p>
        <p><b>Experience:</b></p>
        {parsedData.experience.map((exp, index) => (
          <li key={index}>{exp.company}, {exp.role}, {exp.details}</li>
        ))}
        <p><b>Degrees:</b></p>
        {parsedData.degrees.map((degree, index) => (
        <li key={index}>{degree.institution}, {degree.degree}, {degree.start_year}-{degree.end_year}</li>
        ))}
        </div>
      )}
    </div>
  );
}

export default App;
