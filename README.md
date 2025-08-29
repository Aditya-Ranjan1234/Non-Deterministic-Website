# Non-Deterministic Website Generator

A web application that generates unique, AI-powered websites using Groq's LLM API. Each request produces a different website based on the provided prompt and style, making it perfect for rapid prototyping, inspiration, or quick website generation.

## 🌟 Key Features

### AI-Powered Generation
- **Smart Content Creation**: Generates complete HTML, CSS, and JavaScript based on your description
- **Multiple Style Options**: Choose from various design styles including Modern, Minimal, Corporate, Creative, and Elegant
- **Dynamic Content**: Each generation creates unique layouts, color schemes, and content structures

### User Experience
- **Real-time Preview**: See your generated website instantly
- **One-Click Download**: Export the complete website as a single HTML file
- **Responsive Design**: Websites automatically adapt to different screen sizes
- **Interactive Elements**: Generated sites include interactive components like navigation, forms, and animations

### Technical Features
- **Lightning Fast**: Powered by Groq's high-performance LLM API
- **Rate Limited**: Fair usage policy of 100 generations per day
- **Modern Stack**: Built with React and FastAPI for optimal performance
- **Easy Deployment**: Ready to deploy on platforms like Render and Vercel

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

## 🛠️ Usage Guide

### Basic Usage
1. **Enter Your Vision**: Describe the website you want in the input field (e.g., "A portfolio for a photographer with dark theme and modern animations")
2. **Choose a Style**: Select from our curated style options:
   - **Modern**: Clean layouts with contemporary design elements
   - **Minimal**: Simple, content-focused designs with ample white space
   - **Corporate**: Professional layouts suitable for businesses
   - **Creative**: Bold, artistic designs with unique layouts
   - **Elegant**: Sophisticated designs with refined typography
3. **Generate**: Click "Generate Website" and watch as AI creates your custom site
4. **Preview & Download**: View the result and download the complete HTML file with one click

### Advanced Tips
- **Be Specific**: The more details you provide, better the results (e.g., "A bakery website with a warm color scheme, product gallery, and online ordering section")
- **Combine Styles**: Some style combinations work exceptionally well together
- **Iterate**: Generate multiple versions to explore different design directions
- **Customize**: The downloaded HTML can be easily modified in any code editor

## 🚀 Deployment

### Backend Deployment
Deploy the FastAPI backend to any cloud provider:

#### Render (Recommended)
1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set the following environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `PYTHON_VERSION`: 3.10.8
   - `PORT`: 10000
4. Deploy!

#### Other Options
- [Railway](https://railway.app/)
- [Heroku](https://www.heroku.com/)
- [PythonAnywhere](https://www.pythonanywhere.com/)

### Frontend Deployment

1. Build the production version:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy the `build` folder to:
   - [Vercel](https://vercel.com/) (Recommended)
   - [Netlify](https://www.netlify.com/)
   - [GitHub Pages](https://pages.github.com/)

### Environment Variables
For local development, create a `.env` file in the backend directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

## 🌐 Live Demo
Check out the live demo at:
- Frontend: [GitHub Pages](https://aditya-ranjan1234.github.io/Non-Deterministic-Website/)
- Backend API: [Render](https://non-deterministic-website.onrender.com)

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
- [GitHub Pages](https://pages.github.com/)

## Rate Limiting

The application is rate-limited to 100 generations per day. This limit is reset every 24 hours.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
