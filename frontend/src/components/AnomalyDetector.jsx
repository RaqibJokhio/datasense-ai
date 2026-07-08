import { useState } from 'react';
import { getAnomalies } from '../api/client';

function AnomalyDetector({ sessionId }) {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleDetect = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await getAnomalies(sessionId);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Anomaly detection failed');
    } finally {
      setIsLoading(false);
    }
  };

  const hasAnomalies = result && Object.keys(result.anomalies).length > 0;

  return (
    <div style={{ marginTop: '30px' }}>
      <button onClick={handleDetect} disabled={isLoading} style={{ padding: '10px 20px' }}>
        {isLoading ? 'Analyzing...' : 'Detect Anomalies'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {result && !hasAnomalies && (
        <p style={{ marginTop: '10px' }}>No anomalies detected in numeric columns.</p>
      )}

      {hasAnomalies && (
        <div style={{ marginTop: '20px' }}>
          {Object.entries(result.anomalies).map(([column, data]) => (
            <div key={column} style={{ marginBottom: '20px' }}>
              <h4>{column}</h4>
              <p>
                {data.count} outlier(s) found — normal range: {data.lower_bound} to {data.upper_bound}
              </p>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ borderCollapse: 'collapse', width: '100%' }}>
                  <thead>
                    <tr>
                      {Object.keys(data.outliers[0]).map((col) => (
                        <th key={col} style={{ border: '1px solid #ddd', padding: '8px', background: '#f4f4f4' }}>
                          {col}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.outliers.map((row, i) => (
                      <tr key={i}>
                        {Object.values(row).map((val, j) => (
                          <td key={j} style={{ border: '1px solid #ddd', padding: '8px' }}>
                            {String(val)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default AnomalyDetector;