# EmailIntelligence Project Knowledge

## Mission
Email Intelligence is an AI-powered email management application that provides intelligent analysis, categorization, and filtering for Gmail emails. The project combines Python NLP models with a modern React frontend.

## Architecture
- **Frontend**: React (client/) with TypeScript, TailwindCSS, and Radix UI components
- **Backend**: Python FastAPI (backend/) with AI/ML integration
- **AI Engine**: Python-based NLP models for sentiment, intent, topic, and urgency analysis
- **Database**: SQLite for local storage and caching

## Development Setup
- Run `npm run dev` to start the Node.js server in development mode
- Run `npm run test:py` for Python tests
- Run `npm run test:ts` for TypeScript tests
- Client development server runs on separate port via Vite

## Project Structure
- `/client/` - React frontend application
- `/backend/` - Python FastAPI backend and API routes
- `/backend/python_nlp/` - Python NLP models and analysis components
- `/backend/python_backend/` - Python backend services
- `/extensions/` - Extensible plugin system
- `/shared/` - Shared TypeScript schemas

## Key Features
- Gmail integration with OAuth
- AI-powered email analysis (sentiment, intent, topic, urgency)
- Smart filtering and categorization
- Performance metrics and analytics
- Dashboard with email insights

## Technology Stack
- **Frontend**: React 18, TypeScript, TailwindCSS, Radix UI, Wouter (routing), React Query
- **Backend**: Python (FastAPI/Flask)
- **AI/ML**: Python NLP models, scikit-learn
- **Database**: SQLite, Drizzle ORM
- **Build Tools**: Vite, esbuild

## Development Notes
- Use TypeScript for all new code
- Follow existing component patterns in `/client/src/components/`
- Python code should follow PEP 8 style guidelines
- Tests are required for both TypeScript and Python components