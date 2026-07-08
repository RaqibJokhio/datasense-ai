function DataPreview({ data }) {
  if (!data) return null;

  return (
    <div style={{ marginTop: '20px' }}>
      <h3>{data.filename}</h3>
      <p>{data.rows} rows, {data.columns.length} columns</p>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              {data.columns.map((col) => (
                <th key={col} style={{ border: '1px solid #ddd', padding: '8px', background: '#f4f4f4' }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.preview.map((row, i) => (
              <tr key={i}>
                {data.columns.map((col) => (
                  <td key={col} style={{ border: '1px solid #ddd', padding: '8px' }}>
                    {String(row[col])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DataPreview;