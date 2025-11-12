# PR Resolution Automation System - GraphQL API

## Overview

A comprehensive GraphQL-based PR conflict resolution system with OpenAI integration, built using FastAPI, Neo4j, and Graphene. This system provides intelligent PR conflict detection, resolution suggestions, and automated processing capabilities.

## Architecture

The system follows a microservices architecture with the following components:

- **GraphQL API Layer**: FastAPI + Graphene for GraphQL schema and resolvers
- **Graph Database**: Neo4j for storing PR conflicts and relationships
- **Caching Layer**: Redis for performance optimization
- **Monitoring**: Built-in performance monitoring and health checks
- **Containerization**: Docker and Docker Compose for deployment

## Project Structure

```
src/
├── api/                  # FastAPI application
│   └── main.py          # Main application entry point
├── config/              # Configuration management
│   └── settings.py      # Application settings
├── database/            # Database layer
│   ├── connection.py    # Neo4j connection management
│   ├── data_access.py   # Data access objects
│   └── init.py         # Database initialization
├── graphql/             # GraphQL layer
│   ├── schema.py       # GraphQL schema definitions
│   └── resolvers.py    # GraphQL resolvers
├── models/              # Data models
│   └── graph_entities.py # Pydantic models for graph entities
└── utils/               # Utility modules
    ├── caching.py       # Redis caching layer
    ├── monitoring.py    # Performance monitoring
    └── rate_limit.py   # Rate limiting

tests/
└── test_graphql_api.py # Comprehensive test suite

deployment/
├── Dockerfile.pr-automation    # Container configuration
└── docker-compose.pr-automation.yml  # Multi-service deployment

requirements-graphql.txt        # Additional dependencies
```

## Key Features

### 1. GraphQL API
- **Queries**: Get PRs, conflicts, dependencies, complexity analysis
- **Mutations**: Create PRs, update status, resolve conflicts
- **Performance**: ≤100ms queries, ≤500ms mutations
- **Rate Limiting**: Configurable rate limiting per client
- **Caching**: Redis-based caching for read operations

### 2. Graph Database Integration
- **Neo4j**: Native graph database for relationship modeling
- **Entity Types**: PullRequest, Commit, File, Developer, Conflict
- **Performance**: Optimized with indexes and constraints
- **Scalability**: Supports complex graph traversal operations

### 3. Performance Optimization
- **Query Complexity Analysis**: Prevents expensive operations
- **Connection Pooling**: Efficient database connection management
- **Memory Management**: ≤2GB memory footprint target
- **Monitoring**: Real-time performance metrics

### 4. Health Monitoring
- **Health Checks**: Database, cache, and service health
- **Metrics**: Performance, system, and application metrics
- **Logging**: Structured logging with performance tracking

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements-graphql.txt
```

### 2. Environment Setup
Create a `.env` file with:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
REDIS_URL=redis://localhost:6379
DEBUG=false
```

### 3. Start with Docker Compose
```bash
cd deployment
docker-compose -f docker-compose.pr-automation.yml up -d
```

### 4. Access the API
- **GraphQL Endpoint**: http://localhost:8001/graphql
- **Health Check**: http://localhost:8001/health
- **Metrics**: http://localhost:8001/metrics

## API Usage Examples

### Get All Pull Requests
```graphql
query {
  pullRequests(limit: 10) {
    id
    title
    status
    complexity
  }
}
```

### Create a Pull Request
```graphql
mutation {
  createPR(input: {
    title: "Fix authentication bug"
    description: "Authentication fails with certain credentials"
    sourceBranch: "feature/auth-fix"
    targetBranch: "main"
    authorId: "user123"
  }) {
    id
    title
    status
  }
}
```

### Get PR Conflicts
```graphql
query {
  prConflicts(prId: "pr_123") {
    id
    type
    severity
    description
  }
}
```

### Resolve Conflict
```graphql
mutation {
  resolveConflict(input: {
    conflictId: "conflict_123"
    method: AI_RESOLVED
    description: "Auto-resolved using AI analysis"
  }) {
    id
    method
    confidence
  }
}
```

## Development

### Running Tests
```bash
pytest tests/test_graphql_api.py -v
```

### Running in Development Mode
```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

### Database Setup
The system automatically creates Neo4j constraints and indexes on startup:
- Unique constraints for entity IDs
- Performance indexes for status, dates, and relationships

## Performance Targets

- **Query Response Time**: ≤100ms (95th percentile)
- **Mutation Response Time**: ≤500ms (95th percentile)  
- **Memory Usage**: ≤2GB average
- **System Uptime**: 99.9% availability
- **Automation Rate**: 95% of PRs processed automatically

## Deployment

### Production Deployment
1. **Build Images**:
   ```bash
   docker build -f deployment/Dockerfile.pr-automation -t pr-automation-api .
   ```

2. **Deploy with Compose**:
   ```bash
   docker-compose -f deployment/docker-compose.pr-automation.yml up -d
   ```

3. **Scale Services**:
   ```bash
   docker-compose -f deployment/docker-compose.pr-automation.yml up -d --scale pr-automation-api=3
   ```

### Environment Variables
- `NEO4J_URI`: Neo4j connection URI
- `REDIS_URL`: Redis connection URL
- `GRAPHQL_PORT`: API port (default: 8001)
- `DEBUG`: Enable debug mode
- `RATE_LIMIT_REQUESTS`: Requests per minute (default: 100)

## Monitoring

### Health Endpoints
- `/health`: Overall system health
- `/metrics`: Performance and system metrics
- `/graphql`: GraphQL introspection and playground

### Performance Monitoring
- Request/response time tracking
- Query complexity analysis
- System resource monitoring
- Error rate tracking

## Security

- **Rate Limiting**: Prevents API abuse
- **Input Validation**: Pydantic models for type safety
- **CORS Configuration**: Restricted to allowed origins
- **Health Checks**: No sensitive data exposure

## Future Enhancements

1. **OpenAI Integration**: AI-powered conflict resolution
2. **Real-time Subscriptions**: WebSocket support for live updates
3. **Advanced Analytics**: Machine learning for pattern detection
4. **GitHub Integration**: Direct GitHub API integration
5. **Multi-tenant Support**: Support for multiple organizations

## Contributing

1. Follow the existing code structure and patterns
2. Add tests for new features
3. Update documentation for API changes
4. Ensure performance targets are met

## License

This project is part of the EmailIntelligence system and follows the same licensing terms.