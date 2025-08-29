import { useState, useEffect } from 'react';
import './styles.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [style, setStyle] = useState('modern');
  const [html, setHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [remaining, setRemaining] = useState(100);
  const [resetTime, setResetTime] = useState('');

  const styles = [
    { value: 'modern', label: 'Modern' },
    { value: 'minimal', label: 'Minimal' },
    { value: 'corporate', label: 'Corporate' },
    { value: 'creative', label: 'Creative' },
    { value: 'elegant', label: 'Elegant' },
  ];

  const generateWebsite = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt, style }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate website');
      }

      const data = await response.json();
      setHtml(data.html);
      setRemaining(data.remaining);
      
      if (data.reset_time) {
        const resetDate = new Date(data.reset_time * 1000);
        setResetTime(resetDate.toLocaleString());
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const downloadWebsite = () => {
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'website.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Non-Deterministic Website Generator</h1>
        <p className="subtitle">Create unique websites with AI - {remaining} generations remaining today</p>
        {resetTime && <p className="reset-info">Daily limit resets at: {resetTime}</p>}
      </header>

      <main className="main-content">
        <form onSubmit={generateWebsite} className="generator-form">
          <div className="form-group">
            <label htmlFor="prompt">What kind of website do you want to create?</label>
            <input
              id="prompt"
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g., A portfolio for a photographer, A restaurant website, etc."
              className="input-field"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="style">Style:</label>
            <select
              id="style"
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              className="select-field"
            >
              {styles.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>

          <button 
            type="submit" 
            disabled={isLoading}
            className="generate-button"
          >
            {isLoading ? 'Generating...' : 'Generate Website'}
          </button>
          
          {error && <div className="error-message">{error}</div>}
        </form>

        {html && (
          <div className="preview-section">
            <div className="preview-header">
              <h2>Preview</h2>
              <button onClick={downloadWebsite} className="download-button">
                Download HTML
              </button>
            </div>
            <div className="preview-container">
              <iframe
                title="Generated Website Preview"
                srcDoc={html}
                className="preview-iframe"
              />
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by Groq AI • {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
