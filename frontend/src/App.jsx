import { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataPreview from './components/DataPreview';
import QueryInterface from './components/QueryInterface';
import AnomalyDetector from './components/AnomalyDetector';
import './App.css';

function App() {
  const [uploadData, setUploadData] = useState(null);

  return (
    <div className="app-shell">
      <header className="app-header">
        <p className="eyebrow">DataSense AI</p>
        <h1>Ask your data anything</h1>
        <p>Upload a CSV or Excel file, ask plain-English questions, and get pandas-generated answers, charts, and outlier detection.</p>
      </header>

      <div className="card">
        <h3>Upload dataset</h3>
        <FileUpload onUploadSuccess={setUploadData} />
      </div>

      {uploadData && (
        <>
          <div className="card">
            <DataPreview data={uploadData} />
          </div>

          <div className="card">
            <h3>Ask a question</h3>
            <QueryInterface sessionId={uploadData.session_id} />
          </div>

          <div className="card">
            <h3>Anomaly detection</h3>
            <AnomalyDetector sessionId={uploadData.session_id} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;