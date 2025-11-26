# Achievements Service Tests

This directory contains comprehensive test suites for the Winged Achievements Service.

## Test Structure

### Unit Tests (`tests/unit/`)
- **Domain Layer Tests**: Entity business logic, value objects, domain services
- **Application Layer Tests**: Use cases, application services
- **Infrastructure Tests**: Repository patterns, database interactions
- **Presentation Tests**: API endpoints, controllers, schemas

### Integration Tests (`tests/integration/`)
- **API Integration**: End-to-end API testing with test database
- **External Services**: Integration with ML Worker, Sightings services
- **Database Integration**: Real database operations with fixtures

## Running Tests

### Run All Tests
```bash
pytest services/achievements/tests/
```

### Run Unit Tests Only
```bash
pytest services/achievements/tests/unit/
```

### Run Integration Tests Only
```bash
pytest services/achievements/tests/integration/
```

### Run with Coverage
```bash
pytest services/achievements/tests/ --cov=services/achievements/app/ --cov-report=html
```

## Test Dependencies

- `pytest`: Testing framework
- `pytest-asyncio`: Async testing support
- `pytest-mock`: Mocking utilities
- `httpx`: HTTP testing
- `sqlalchemy`: Database testing
- `faker`: Test data generation

## Test Database

Integration tests use a separate test database to ensure isolation from development data.