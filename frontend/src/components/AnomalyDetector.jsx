import { useState } from 'react';
import { getAnomalies, downloadAnomaliesCsv } from '../api/client';

function AnomalyDetector({ sessionId }) {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [downloadingColumn, setDownloadingColumn] = useState(null);

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

  const handleDownload = async (column) => {
    setDownloadingColumn(column);
    try {
      await downloadAnomaliesCsv(sessionId, column);
    } catch (err) {
      setError(`Failed to download CSV for ${column}`);
    } finally {
      setDownloadingColumn(null);
    }
  };

  const hasAnomalies = result && Object.keys(result.anomalies).length > 0;

  return (
    <div>
      <button onClick={handleDetect} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Detect anomalies'}
      </button>

      {error && <p className="error-text">{error}</p>}

      {result && !hasAnomalies && (
        <p className="anomaly-empty">No anomalies detected in numeric columns.</p>
      )}

      {hasAnomalies && (
        <div style={{ marginTop: '20px' }}>
          {Object.entries(result.anomalies).map(([column, data]) => (
            <div key={column} className="anomaly-column-block">
              <h4>{column}</h4>
              <p className="anomaly-meta">
                <span className="anomaly-count">{data.count} outlier{data.count !== 1 ? 's' : ''}</span> found &middot; normal range {data.lower_bound} to {data.upper_bound}
                {' · '}
                <span
                  onClick={() => handleDownload(column)}
                  style={{ color: 'var(--accent)', cursor: 'pointer', textDecoration: 'underline' }}
                >
                  {downloadingColumn === column ? 'Downloading...' : `Download all ${data.count} as CSV`}
                </span>
              </p>
              <div className="data-table-wrap">
                <table>
                  <thead>
                    <tr>
                      {Object.keys(data.outliers[0]).map((col) => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {data.outliers.map((row, i) => (
                      <tr key={i}>
                        {Object.values(row).map((val, j) => (
                          <td key={j}>{String(val)}</td>
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