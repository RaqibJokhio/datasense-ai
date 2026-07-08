import { useState } from 'react';
import FileUpload from './components/FileUpload';
import DataPreview from './components/DataPreview';
import QueryInterface from './components/QueryInterface';
import './App.css';

function App() {
  const [uploadData, setUploadData] = useState(null);

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '20px' }}>
      <h1>DataSense AI</h1>
      <p>Upload a CSV or Excel file and ask questions about your data.</p>

      <FileUpload onUploadSuccess={setUploadData} />

      {uploadData && (
        <>
          <DataPreview data={uploadData} />
          <QueryInterface sessionId={uploadData.session_id} />
        </>
      )}
    </div>
  );
}

export default App;