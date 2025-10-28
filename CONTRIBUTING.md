# Contributing to ScriptMyIdeas

Thank you for considering contributing to ScriptMyIdeas! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to maintain a welcoming community.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Nish-H/ScriptMyIdeas/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check [Issues](https://github.com/Nish-H/ScriptMyIdeas/issues) for similar suggestions
2. Create a new issue with:
   - Clear use case description
   - Expected behavior
   - Why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Follow the coding standards below
5. Test your changes thoroughly
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes

## Development Setup

See [README.md](README.md) for setup instructions.

## Coding Standards

### Python (Backend)

- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Maximum line length: 100 characters
- Use async/await for IO operations

### TypeScript (Frontend)

- Use TypeScript strict mode
- Follow React best practices
- Use functional components with hooks
- Write meaningful component names
- Keep components small and focused

### Commit Messages

Format: `type: description`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example: `feat: add script export functionality`

## Testing

- Backend: `pytest` in backend directory
- Frontend: `npm test` in frontend directory
- Ensure all tests pass before submitting PR

## Questions?

Feel free to open an issue for questions or reach out to maintainers.
