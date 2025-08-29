# Non-Deterministic Website Generator

A web application that generates unique, AI-powered websites using Groq's LLM API. Each request produces a different website based on the provided prompt and style.

## Features

- 🚀 Generate unique websites with AI
- 🎨 Multiple style options
- ⚡ Fast response times with Groq Cloud
- 📦 Export websites as HTML files
- 🔒 Rate limited to 100 generations per day
- 🎯 Modern, responsive UI

## Prerequisites

- Node.js (v14 or higher)
- Python 3.8+
- Groq API key (get it from [Groq Cloud](https://console.groq.com/))

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Start the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

1. Enter a prompt describing the website you want to generate (e.g., "A portfolio for a photographer")
2. Select a style from the dropdown
3. Click "Generate Website"
4. Once generated, you can preview the website and download the HTML file

## Deployment

### Backend Deployment

You can deploy the backend to services like:
- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [Heroku](https://www.heroku.com/)

### Frontend Deployment

Build the frontend for production:
```bash
cd frontend
npm run build
```

You can deploy the `build` folder to:
- [Vercel](https://vercel.com/)
- [Netlify](https://www.netlify.com/)
- [GitHub Pages](https://pages.github.com/)

## Rate Limiting

The application is rate-limited to 100 generations per day. This limit is reset every 24 hours.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
