# ScriptMyIdeas - Architecture Documentation

## Overview
ScriptMyIdeas is a modern script management platform that allows creation, modification, version control, and visualization of scripts and their artifacts through a futuristic web interface.

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: Back4app (Parse Server)
- **API**: RESTful API with automatic OpenAPI documentation
- **Authentication**: Parse Authentication
- **File Storage**: Back4app File Storage for artifacts

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS with custom futuristic theme
- **UI Components**: Shadcn/ui with custom AI/IT themed components
- **State Management**: React Query + Zustand
- **Code Editor**: Monaco Editor (VS Code editor)
- **Visualization**: Recharts for analytics

### Infrastructure
- **Version Control**: Git-based with metadata in Back4app
- **Search**: Back4app Query with indexed fields
- **Real-time**: WebSocket support for live updates

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface (React)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │
│  │  Script  │ │  Version │ │ Artifact │ │   Search     │   │
│  │  Editor  │ │  Control │ │  Viewer  │ │   Engine     │   │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                     REST API (HTTPS)
                            │
┌─────────────────────────────────────────────────────────────┐
│                   Backend API (FastAPI)                      │
│  ┌──────────────┐ ┌─────────────┐ ┌───────────────────┐    │
│  │   Script     │ │   Version   │ │     Artifact      │    │
│  │   Manager    │ │   Manager   │ │     Manager       │    │
│  └──────────────┘ └─────────────┘ └───────────────────┘    │
│  ┌──────────────┐ ┌─────────────┐ ┌───────────────────┐    │
│  │   Search     │ │    Auto     │ │    Integration    │    │
│  │   Service    │ │    Save     │ │      Service      │    │
│  └──────────────┘ └─────────────┘ └───────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                    Parse SDK / REST API
                            │
┌─────────────────────────────────────────────────────────────┐
│                    Back4app Database                         │
│  ┌──────────────┐ ┌─────────────┐ ┌───────────────────┐    │
│  │   Scripts    │ │  Versions   │ │    Artifacts      │    │
│  │   Table      │ │   Table     │ │      Table        │    │
│  └──────────────┘ └─────────────┘ └───────────────────┘    │
│  ┌──────────────┐ ┌─────────────┐                           │
│  │    Tags      │ │    Files    │                           │
│  │   Table      │ │   Storage   │                           │
│  └──────────────┘ └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

## Data Models

### Script
```json
{
  "objectId": "string",
  "name": "string",
  "description": "string",
  "language": "python|bash|javascript|powershell|...",
  "content": "string",
  "version": "string (semver)",
  "createdBy": "string (AI|User)",
  "createdAt": "datetime",
  "updatedAt": "datetime",
  "tags": ["string"],
  "category": "string",
  "isLatest": "boolean",
  "parentScript": "pointer to Script (for versions)",
  "metadata": {
    "size": "number",
    "lines": "number",
    "complexity": "number"
  }
}
```

### Artifact
```json
{
  "objectId": "string",
  "scriptId": "pointer to Script",
  "scriptVersion": "string",
  "name": "string",
  "type": "html|json|csv|log|image|...",
  "content": "string or File pointer",
  "size": "number",
  "createdAt": "datetime",
  "metadata": "object"
}
```

### ScriptVersion
```json
{
  "objectId": "string",
  "scriptId": "pointer to Script",
  "versionNumber": "string (semver)",
  "content": "string",
  "changelog": "string",
  "createdBy": "string",
  "createdAt": "datetime",
  "hash": "string (SHA-256)"
}
```

## Core Features

### 1. Auto-Save Integration
When Claude creates a script during conversation:
1. Parse the script content
2. Generate metadata (language, size, complexity)
3. Create Script object in Back4app
4. Save initial version
5. Return script ID and access URL

### 2. Version Control
- Automatic versioning using semantic versioning
- Full diff view between versions
- Easy rollback to previous versions
- Version comparison tool
- Change history tracking

### 3. Search Engine
- Full-text search across script content
- Filter by: language, tags, date, creator
- Search in artifact content
- Advanced query builder
- Recent searches

### 4. Artifact Management
- Store all script outputs
- HTML reports rendered in iframe with security
- JSON/CSV data visualization
- Image gallery for visual outputs
- Log file viewer with syntax highlighting

### 5. Web Interface Features
- Split-pane editor with live preview
- Syntax highlighting for multiple languages
- One-click script execution (future)
- Drag-and-drop file uploads
- Dark/light mode with futuristic themes
- Dashboard with analytics

## Security Considerations

1. **Authentication**: Parse User authentication
2. **API Keys**: Environment variables, never in code
3. **Input Validation**: Sanitize all inputs
4. **HTML Rendering**: Sandboxed iframes for artifacts
5. **Rate Limiting**: API request throttling
6. **CORS**: Configured for frontend domain only

## Deployment Strategy

### Development
```bash
# Backend: localhost:8000
uvicorn main:app --reload

# Frontend: localhost:3000
npm run dev
```

### Production
- Backend: Deploy to Railway/Render/Fly.io
- Frontend: Deploy to Vercel/Netlify
- Database: Back4app (managed)

## API Endpoints

### Scripts
- `GET /api/scripts` - List all scripts
- `GET /api/scripts/{id}` - Get script details
- `POST /api/scripts` - Create new script
- `PUT /api/scripts/{id}` - Update script
- `DELETE /api/scripts/{id}` - Delete script
- `GET /api/scripts/search` - Search scripts

### Versions
- `GET /api/scripts/{id}/versions` - List versions
- `GET /api/scripts/{id}/versions/{version}` - Get specific version
- `POST /api/scripts/{id}/versions` - Create new version
- `GET /api/scripts/{id}/versions/{v1}/diff/{v2}` - Compare versions

### Artifacts
- `GET /api/artifacts` - List artifacts
- `GET /api/artifacts/{id}` - Get artifact
- `POST /api/artifacts` - Upload artifact
- `GET /api/artifacts/{id}/render` - Render artifact

### Integration
- `POST /api/integration/auto-save` - Auto-save script from AI
- `GET /api/integration/stats` - Get platform statistics

## Future Enhancements

1. Script execution engine
2. Collaborative editing
3. Script templates library
4. AI-powered script suggestions
5. Script testing framework
6. CI/CD integration
7. Marketplace for sharing scripts
8. Mobile app (React Native)
