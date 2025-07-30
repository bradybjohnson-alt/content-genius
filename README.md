# ContentGenius AI - AI-Powered Content Creation Platform

A full-stack web application that combines AI-powered content generation with human oversight to deliver high-quality content for businesses.

## 🚀 Features

- **AI-Powered Content Generation**: Leverages OpenAI GPT-4 for intelligent content creation
- **Human Oversight**: Every piece of content is reviewed and refined by experts
- **Professional Landing Page**: Modern, responsive design with pricing tiers
- **Content Request System**: Easy-to-use form for submitting content requirements
- **Database Management**: SQLite database for storing content requests and client information
- **RESTful API**: Complete backend API for content and client management

## 🛠 Tech Stack

### Frontend
- **React 19** with Vite
- **Tailwind CSS** for styling
- **shadcn/ui** components
- **Lucide React** icons
- **Framer Motion** for animations

### Backend
- **Flask** web framework
- **SQLAlchemy** ORM
- **SQLite** database
- **OpenAI API** integration
- **Flask-CORS** for cross-origin requests

## 📁 Project Structure

```
content-genius-complete/
├── contentgenius-ai/          # React frontend source
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── ...
│   ├── package.json
│   ├── vite.config.js         # ✅ Fixed with proper path aliases
│   └── ...
├── src/                       # Flask backend source
│   ├── models/
│   │   ├── content.py         # Content and Client models
│   │   └── user.py
│   ├── routes/
│   │   ├── content.py         # Content API endpoints
│   │   └── user.py
│   ├── static/               # Built React app (for deployment)
│   ├── database/
│   └── main.py               # Flask application
├── main.py                   # Entry point for deployment
├── requirements.txt          # Python dependencies
└── README.md
```

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- Node.js 20+
- pnpm

### Backend Setup
1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

4. Run the Flask server:
   ```bash
   python src/main.py
   ```

### Frontend Development
1. Navigate to frontend directory:
   ```bash
   cd contentgenius-ai
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start development server:
   ```bash
   pnpm run dev
   ```

4. Build for production:
   ```bash
   pnpm run build
   ```

## 🚀 Deployment on Render

### Build Configuration
- **Build Command**: `cd contentgenius-ai && pnpm install && pnpm run build && cd .. && pip install -r requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Python 3

### Environment Variables
Set these in your Render dashboard:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PORT`: (Render sets this automatically)

### Deployment Steps
1. Push this repository to GitHub
2. Connect your GitHub repository to Render
3. Set the build and start commands above
4. Add environment variables
5. Deploy!

## 🔑 API Endpoints

### Content Requests
- `POST /api/content-requests` - Create new content request
- `GET /api/content-requests` - Get all content requests
- `GET /api/content-requests/<id>` - Get specific content request
- `PUT /api/content-requests/<id>` - Update content request

### Clients
- `POST /api/clients` - Create new client
- `GET /api/clients` - Get all clients

## 💰 Pricing Tiers

- **Starter**: $299/month - Up to 20 pieces of content
- **Professional**: $799/month - Up to 50 pieces of content (Most Popular)
- **Enterprise**: Custom pricing - Unlimited content

## 🔒 Security Features

- CORS enabled for secure cross-origin requests
- Environment variable protection for API keys
- Input validation on all API endpoints
- SQLAlchemy ORM for SQL injection protection

## 📝 Content Types Supported

- Blog Posts & Articles
- Social Media Content
- Email Campaigns
- Product Descriptions
- Website Copy
- Press Releases
- Video Scripts
- Ad Copy

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the Apache-2.0 License.

## 🆘 Troubleshooting

### Common Issues

1. **Vite Build Error**: Ensure `vite.config.js` has proper path aliases configured
2. **OpenAI API Error**: Check that `OPENAI_API_KEY` environment variable is set
3. **CORS Issues**: Verify Flask-CORS is installed and configured
4. **Database Issues**: Ensure SQLite database directory exists and is writable

### Support

For support, please open an issue on GitHub or contact the development team.

---

Built with ❤️ using React, Flask, and OpenAI

