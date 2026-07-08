import { useState } from 'react';
import { uploadFile } from '../api/client';

function FileUpload({ onUploadSuccess }) {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    setError(null);

    try {
      const data = await uploadFile(file);
      onUploadSuccess(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '2px dashed #ccc', borderRadius: '8px' }}>
      <input
        type="file"
        accept=".csv,.xlsx,.xls"
        onChange={handleFileChange}
        disabled={isUploading}
      />
      {isUploading && <p>Uploading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}

export default FileUpload;