import React, { useState } from 'react';
import { Form, Button, ProgressBar } from 'react-bootstrap';
import axios from 'axios';  // No need to import AxiosRequestConfig separately

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    // Use inline typing for Axios config
    const config: any = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent: ProgressEvent) => {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setProgress(percentCompleted);
      },
    };

    try {
      await axios.post('/api/upload', formData, config);
    } catch (err) {
      console.error('Upload failed', err);
    }
  };

  return (
    <div className="p-3">
      <Form.Group controlId="formFile" className="mb-3">
        <Form.Label>Upload your notes</Form.Label>
        <Form.Control
          type="file"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setFile(e.target.files?.[0] || null)
          }
        />
      </Form.Group>

      <Button onClick={handleUpload}>Upload</Button>

      {progress > 0 && (
        <ProgressBar now={progress} label={`${progress}%`} className="mt-3" />
      )}
    </div>
  );
};

export default UploadPage;

