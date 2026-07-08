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
      <div className="result-block">
        <p className="result-label">Generated code</p>
        <div className="code-console">
          <div className="code-console-bar">
            <span className="code-console-dot"></span>
            <span className="code-console-dot"></span>
            <span className="code-console-dot"></span>
          </div>
          <pre>{result.generated_code}</pre>
        </div>

        <p className="result-label">Result</p>
        {result.result_type === 'chart' && (
          <div className="result-chart">
            <img src={result.result_data} alt="Query result chart" />
          </div>
        )}
        {result.result_type === 'value' && (
          <p className="result-value">{String(result.result_data)}</p>
        )}
        {result.result_type === 'table' && (
          <div className="data-table-wrap">
            <table>
              <thead>
                <tr>
                  {result.result_data.length > 0 &&
                    Object.keys(result.result_data[0]).map((col) => (
                      <th key={col}>{col}</th>
                    ))}
                </tr>
              </thead>
              <tbody>
                {result.result_data.map((row, i) => (
                  <tr key={i}>
                    {Object.values(row).map((val, j) => (
                      <td key={j}>{String(val)}</td>
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
    <div>
      <form className="query-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. What is the average sales price?"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {error && <p className="error-text">{error}</p>}
      {renderResult()}
    </div>
  );
}

export default QueryInterface;