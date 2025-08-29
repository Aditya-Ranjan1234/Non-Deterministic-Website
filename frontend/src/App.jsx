import { useState, useEffect, useCallback } from 'react';
import './styles.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [style, setStyle] = useState('modern');
  const [html, setHtml] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [remaining, setRemaining] = useState(100);
  const [resetTime, setResetTime] = useState('');
  const [currentId, setCurrentId] = useState(Date.now());

  const styles = [
    { value: 'modern', label: 'Modern' },
    { value: 'minimal', label: 'Minimal' },
    { value: 'corporate', label: 'Corporate' },
    { value: 'creative', label: 'Creative' },
    { value: 'elegant', label: 'Elegant' },
  ];

  const generateRandomWebsite = useCallback(async () => {
    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('https://non-deterministic-website.onrender.com/random', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate website');
      }

      const data = await response.json();
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    }
  }, []);

  const generateCustomWebsite = async (e) => {
    if (e) e.preventDefault();
    if (e && !prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setIsLoading(true);
    setError('');
    
    try {
      const response = await fetch('https://non-deterministic-website.onrender.com/generate', {
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

  // Handle browser navigation (back/forward buttons)
  useEffect(() => {
    const handlePopState = async () => {
      const data = await generateRandomWebsite();
      if (data) {
        setHtml(data.html);
        setRemaining(data.remaining);
        if (data.reset_time) {
          const resetDate = new Date(data.reset_time * 1000);
          setResetTime(resetDate.toLocaleString());
        }
      }
      // Update the URL with a new unique ID
      const newId = Date.now();
      setCurrentId(newId);
      window.history.pushState({ id: newId }, '', `/${newId}`);
    };

    // Initial load
    const loadInitialWebsite = async () => {
      const data = await generateRandomWebsite();
      if (data) {
        setHtml(data.html);
        setRemaining(data.remaining);
        if (data.reset_time) {
          const resetDate = new Date(data.reset_time * 1000);
          setResetTime(resetDate.toLocaleString());
        }
        // Set initial history state
        const newId = Date.now();
        setCurrentId(newId);
        window.history.replaceState({ id: newId }, '', `/${newId}`);
      }
      setIsLoading(false);
    };

    loadInitialWebsite();
    window.addEventListener('popstate', handlePopState);
    
    return () => {
      window.removeEventListener('popstate', handlePopState);
    };
  }, [generateRandomWebsite]);

  // Function to manually generate a new random website
  const generateNewWebsite = () => {
    const newId = Date.now();
    setCurrentId(newId);
    window.history.pushState({ id: newId }, '', `/${newId}`);
    generateRandomWebsite().then(data => {
      if (data) {
        setHtml(data.html);
        setRemaining(data.remaining);
        if (data.reset_time) {
          const resetDate = new Date(data.reset_time * 1000);
          setResetTime(resetDate.toLocaleString());
        }
      }
    });
  };

  return (
    <div className="app">
      <header className="header">
        <h1>AI Website Generator</h1>
        <p>Discover unique, AI-created websites</p>
        {resetTime && <p className="reset-info">Daily limit resets at: {resetTime}</p>}
      </header>

      <main className="main-content">
        <div className="navigation-buttons">
          <button 
            onClick={generateNewWebsite}
            disabled={isLoading}
            className="nav-button"
          >
            {isLoading ? 'Creating...' : 'Generate Random Website'}
          </button>
        </div>
        
        {error && <div className="error-message">{error}</div>}

        <div className="preview-section">
          <div className="preview-header">
            <h2>{isLoading ? 'Creating Something Amazing...' : 'Your Website'}</h2>
          </div>
          <div className="preview-container">
            {isLoading ? (
              <div className="loading-state">
                <div className="spinner"></div>
                <p>Creating a unique website for you...</p>
              </div>
            ) : html ? (
              <iframe
                title="Generated Website Preview"
                srcDoc={html}
                className="preview-iframe"
                onLoad={() => setIsLoading(false)}
              />
            ) : (
              <div className="empty-state">
                <p>Click "Generate New Website" to create your first website!</p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Powered by Groq AI • {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;
