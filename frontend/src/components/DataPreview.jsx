function DataPreview({ data }) {
  if (!data) return null;

  return (
    <div>
      <h3>{data.filename}</h3>
      <p className="meta-line">{data.rows.toLocaleString()} rows &middot; {data.columns.length} columns</p>

      <div className="data-table-wrap">
        <table>
          <thead>
            <tr>
              {data.columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.preview.map((row, i) => (
              <tr key={i}>
                {data.columns.map((col) => (
                  <td key={col}>{String(row[col])}</td>
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