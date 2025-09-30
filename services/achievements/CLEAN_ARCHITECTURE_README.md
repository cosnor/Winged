# Clean Architecture Migration

This directory contains the new clean architecture structure for the Achievements service.

## Architecture Overview

The service is now organized into 4 main layers following clean architecture principles:

### 1. Domain Layer (`app/domain/`)
- **Entities**: Core business objects (Achievement, UserAchievement, BirdCollection, UserStats)
- **Value Objects**: Immutable objects that represent concepts (AchievementCriteria, Location, SightingEvent)
- **Domain Services**: Business logic that doesn't belong to a single entity

### 2. Application Layer (`app/application/`)
- **Use Cases**: Application-specific business rules
- **Interfaces**: Contracts for external dependencies (repositories, services)
- **Application Services**: Orchestrate use cases and manage transactions

### 3. Infrastructure Layer (`app/infrastructure/`)
- **Database**: SQLAlchemy models and repository implementations
- **External Services**: Implementations for notifications, events, etc.

### 4. Presentation Layer (`app/presentation/`)
- **API Controllers**: FastAPI route handlers
- **Schemas**: Request/response models
- **Dependencies**: Dependency injection configuration

## Key Benefits

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Testability**: Easy to unit test business logic in isolation
4. **Maintainability**: Changes in one layer don't affect others
5. **Flexibility**: Easy to swap implementations (e.g., different databases)

## Migration Steps

1. **Backup**: Old files are backed up in `backup_old_structure/`
2. **Database**: The database schema remains compatible
3. **API**: All existing endpoints are preserved with the same interface
4. **Configuration**: Update imports and dependency injection

## Running the New Structure

```bash
# Install dependencies
pip install -r requirements_clean.txt

# Run the service
python -m app.main_clean
```

## Testing

The new structure makes it much easier to write unit tests:

```python
# Test domain logic in isolation
def test_achievement_criteria():
    criteria = AchievementCriteria(category="species_count", count=5)
    assert criteria.is_met_by_count(5) == True

# Test use cases with mocked dependencies
def test_process_sighting_use_case():
    # Mock repositories
    # Test business logic
    pass
```

## Next Steps

1. Update any external services that depend on this service
2. Add comprehensive unit tests for each layer
3. Consider adding integration tests
4. Update deployment scripts if needed
