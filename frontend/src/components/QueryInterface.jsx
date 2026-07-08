import { useState } from 'react';
import { queryData } from '../api/client';

function QueryInterface({ sessionId }) {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await queryData(sessionId, question);
      setResult(data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Query failed');
    } finally {
      setIsLoading(false);
    }
  };

  const renderResult = () => {
    if (!result) return null;

    return (
      <div style={{ marginTop: '20px' }}>
        <p><strong>Generated code:</strong></p>
        <pre style={{ background: '#f4f4f4', padding: '10px', borderRadius: '4px', overflowX: 'auto' }}>
          {result.generated_code}
        </pre>

        <p><strong>Result:</strong></p>
        {result.result_type === 'chart' && (
          <img src={result.result_data} alt="Query result chart" style={{ maxWidth: '100%' }} />
        )}
        {result.result_type === 'value' && (
          <p style={{ fontSize: '1.2em' }}>{String(result.result_data)}</p>
        )}
        {result.result_type === 'table' && (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%' }}>
              <thead>
                <tr>
                  {result.result_data.length > 0 &&
                    Object.keys(result.result_data[0]).map((col) => (
                      <th key={col} style={{ border: '1px solid #ddd', padding: '8px', background: '#f4f4f4' }}>
                        {col}
                      </th>
                    ))}
                </tr>
              </thead>
              <tbody>
                {result.result_data.map((row, i) => (
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
        )}
      </div>
    );
  };

  return (
    <div style={{ marginTop: '30px' }}>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your data..."
          style={{ width: '70%', padding: '10px' }}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading} style={{ padding: '10px 20px', marginLeft: '10px' }}>
          {isLoading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {renderResult()}
    </div>
  );
}

export default QueryInterface;