# Contributing to Future Artist

Thank you for your interest in contributing to Future Artist! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Google Cloud SDK
- Docker (optional)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/futureArtist.git
cd futureArtist
```

2. **Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
```

3. **Frontend setup**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local
```

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use `black` for formatting
- Use `ruff` for linting
- Type hints for all functions

```bash
# Format code
black .

# Lint code
ruff check .
```

### TypeScript (Frontend)

- Follow Airbnb style guide
- Use Prettier for formatting
- ESLint for linting

```bash
# Format and lint
npm run lint
```

## Commit Messages

Follow conventional commits:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/config changes

**Example:**
```
feat(agents): add video generation agent

Implement video generator agent with storyboard creation
and transition effects.

Closes #123
```

## Pull Request Process

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write tests for new features
- Update documentation
- Follow code style guidelines

3. **Test your changes**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

4. **Commit your changes**
```bash
git add .
git commit -m "feat: your feature description"
```

5. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

6. **Create Pull Request**
- Provide clear description
- Reference related issues
- Include screenshots if UI changes

## Testing

### Backend Testing

```bash
cd backend
pytest tests/
```

### Frontend Testing

```bash
cd frontend
npm test
```

## Documentation

Update documentation for:
- New features
- API changes
- Configuration changes
- Architecture changes

Documentation locations:
- API docs: `docs/api.md`
- Architecture: `docs/architecture.md`
- Deployment: `docs/deployment.md`

## Issue Guidelines

### Reporting Bugs

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

### Feature Requests

Include:
- Clear use case
- Proposed solution
- Alternative solutions considered
- Additional context

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
