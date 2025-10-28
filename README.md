# ScriptMyIdeas

> **Modern AI-Powered Script Management Platform**

A comprehensive platform for managing, versioning, and organizing scripts with automatic storage, artifact management, and seamless Claude AI integration.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18+-61dafb.svg)

## Features

- **Automatic Script Storage**: Scripts created in Claude AI conversations are automatically saved
- **Version Control**: Full version history with diff comparison and easy rollback
- **Artifact Management**: Store and view HTML reports, logs, and other script outputs
- **Advanced Search**: Search across script names, content, descriptions, and tags
- **Modern UI**: Futuristic dark theme optimized for developers
- **Multi-Language Support**: Python, JavaScript, Bash, PowerShell, Go, Rust, and more
- **Monaco Editor**: VS Code-like editing experience in the browser
- **Back4app Integration**: Cloud database with automatic backups

## Architecture

```
┌─────────────────────────────────────────────────────┐
│          React Frontend (Vite + TypeScript)         │
│  • Dashboard  • Script Editor  • Version Control    │
│  • Artifact Viewer  • Search Engine                 │
└────────────────────┬────────────────────────────────┘
                     │ REST API (HTTP/JSON)
┌────────────────────┴────────────────────────────────┐
│         FastAPI Backend (Python 3.10+)              │
│  • Script Management  • Version Control             │
│  • Auto-Save Integration  • Search Service          │
└────────────────────┬────────────────────────────────┘
                     │ Parse REST API
┌────────────────────┴────────────────────────────────┐
│              Back4app Database                       │
│  • Scripts  • Versions  • Artifacts  • Files        │
└──────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **Back4app Account** (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/Nish-H/ScriptMyIdeas.git
cd ScriptMyIdeas
```

### 2. Set Up Back4app

Follow the [Back4app Setup Guide](docs/BACK4APP_SETUP.md) to:
1. Create a Back4app account
2. Create a new app
3. Get your API credentials

### 3. Configure Backend

```bash
cd backend
cp .env.example .env
# Edit .env with your Back4app credentials
```

Required environment variables:
```env
BACK4APP_APPLICATION_ID=your_application_id
BACK4APP_REST_API_KEY=your_rest_api_key
BACK4APP_JAVASCRIPT_KEY=your_javascript_key
BACK4APP_SERVER_URL=https://parseapi.back4app.com
```

### 4. Install Backend Dependencies

```bash
# From backend directory
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Install Frontend Dependencies

```bash
# From frontend directory
cd ../frontend
npm install
```

### 6. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn app.main:app --reload
# Backend runs on http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:3000
```

### 7. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/api/docs
- **Backend ReDoc**: http://localhost:8000/api/redoc

## Usage

### Creating Scripts Manually

1. Navigate to "Scripts" → "New Script"
2. Fill in script details (name, description, language, category)
3. Write or paste your script code
4. Add tags for easy searching
5. Click "Create Script"

### Auto-Save from Claude AI

When Claude creates a script during a conversation, you can use the Integration API to automatically save it:

```bash
curl -X POST "http://localhost:8000/api/integration/auto-save" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "data_processor.py",
    "content": "import pandas as pd\n...",
    "description": "Process CSV data and generate reports",
    "language": "python",
    "category": "data_processing",
    "tags": ["csv", "reports", "pandas"],
    "artifacts": [
      {
        "name": "output.html",
        "type": "html",
        "content": "<html>...</html>"
      }
    ]
  }'
```

### Version Management

1. Open any script
2. Click "Edit" to modify
3. Save creates a new version automatically
4. View version history in the script detail page
5. Compare versions to see changes

### Searching Scripts

1. Go to "Search" page
2. Enter keywords (searches name, description, content, tags)
3. Click on results to view script details

## API Endpoints

### Scripts
- `GET /api/scripts` - List all scripts
- `GET /api/scripts/{id}` - Get script by ID
- `POST /api/scripts` - Create new script
- `PUT /api/scripts/{id}` - Update script
- `DELETE /api/scripts/{id}` - Delete script

### Versions
- `GET /api/versions/script/{script_id}` - List versions
- `GET /api/versions/{version_id}` - Get specific version
- `GET /api/versions/diff/{v1}/{v2}` - Compare versions

### Artifacts
- `GET /api/artifacts` - List artifacts
- `GET /api/artifacts/{id}` - Get artifact
- `POST /api/artifacts/upload` - Upload artifact file

### Search
- `GET /api/search?q={query}` - Search scripts

### Integration
- `POST /api/integration/auto-save` - Auto-save from Claude
- `GET /api/integration/stats` - Platform statistics

Full API documentation available at: http://localhost:8000/api/docs

## Project Structure

```
ScriptMyIdeas/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   │   └── routes/     # Endpoint handlers
│   │   ├── core/           # Configuration
│   │   ├── models/         # Pydantic models
│   │   ├── services/       # Business logic
│   │   ├── utils/          # Helper functions
│   │   └── main.py         # FastAPI app
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment template
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API client
│   │   ├── styles/         # Global styles
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main app component
│   │   └── main.tsx        # Entry point
│   ├── public/             # Static assets
│   ├── package.json        # npm dependencies
│   └── vite.config.ts      # Vite configuration
│
├── scripts/                # Stored scripts (gitignored)
├── artifacts/              # Stored artifacts (gitignored)
├── docs/                   # Documentation
│   ├── ARCHITECTURE.md     # System architecture
│   └── BACK4APP_SETUP.md   # Database setup guide
│
├── .github/                # GitHub workflows
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **httpx**: Async HTTP client
- **python-dotenv**: Environment management
- **Back4app/Parse**: Database backend

### Frontend
- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool
- **TanStack Query**: Data fetching
- **Monaco Editor**: Code editor
- **Tailwind CSS**: Styling
- **Lucide React**: Icons

### Database
- **Back4app**: Parse Server cloud database
- **File Storage**: Back4app file storage

## Development

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
```

### Linting
```bash
# Backend
cd backend
flake8 app/

# Frontend
cd frontend
npm run lint
```

### Building for Production

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

## Deployment

### Backend Deployment (Railway/Render/Fly.io)

1. Set environment variables in hosting platform
2. Use Python 3.10+ runtime
3. Install command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel/Netlify)

1. Build command: `npm run build`
2. Output directory: `dist`
3. Environment variables: `VITE_API_URL=your_backend_url`

## Configuration

### Backend Environment Variables

See `backend/.env.example` for all available options:
- Back4app credentials
- CORS origins
- File upload limits
- Security settings

### Frontend Environment Variables

Create `frontend/.env`:
```env
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Script execution engine
- [ ] Collaborative editing
- [ ] Script templates library
- [ ] AI-powered script suggestions
- [ ] Testing framework integration
- [ ] CI/CD pipeline integration
- [ ] Mobile app (React Native)
- [ ] Script marketplace

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/Nish-H/ScriptMyIdeas/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Nish-H/ScriptMyIdeas/discussions)

## Acknowledgments

- Built with [Claude AI](https://claude.ai)
- Powered by [Back4app](https://www.back4app.com/)
- Icons by [Lucide](https://lucide.dev/)
- Editor by [Monaco Editor](https://microsoft.github.io/monaco-editor/)

---

**Made with ❤️ by Claude AI & Nish-H**
