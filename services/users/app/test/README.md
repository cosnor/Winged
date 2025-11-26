# Unit Tests for Users Service

This directory contains comprehensive unit tests for the users service endpoints.

## Test Structure

### Test Files

- `conftest.py` - Test configuration and shared fixtures
- `test_register_endpoint.py` - Tests for user registration endpoint
- `test_login_endpoint.py` - Tests for user login endpoint  
- `test_validate_token_endpoint.py` - Tests for JWT token validation endpoint
- `test_profile_endpoints.py` - Tests for user profile and get user by ID endpoints
- `test_update_xp_endpoint.py` - Tests for user XP update endpoint
- `test_runner.py` - Test runner utilities and configuration

### Test Coverage

#### Registration Endpoint (`/register`)
- ✅ Successful user registration
- ✅ Email already exists validation
- ✅ Missing required fields validation
- ✅ Invalid email format validation
- ✅ Password too short validation
- ✅ Invalid request body format
- ✅ Internal server error handling

#### Login Endpoint (`/login`)
- ✅ Successful login with valid credentials
- ✅ Invalid email format validation
- ✅ User not found handling
- ✅ Incorrect password handling
- ✅ Missing credentials validation
- ✅ Inactive user handling
- ✅ Empty credentials handling
- ✅ Internal server error handling

#### Token Validation Endpoint (`/validate-token`)
- ✅ Valid token validation
- ✅ Invalid token handling
- ✅ Malformed token handling
- ✅ Expired token handling
- ✅ Missing token validation
- ✅ Empty token validation
- ✅ Token with invalid payload
- ✅ Internal server error handling

#### Profile Endpoints
- ✅ Get user profile (`/profile`) - **Requires Authorization header**
- ✅ Get user by ID (`/users/{user_id}`) - **Service-to-service communication**
- ✅ User not found handling
- ✅ Invalid ID format validation
- ✅ Authentication errors (missing/invalid token)
- ✅ Internal server error handling

#### XP Update Endpoint (`PATCH /users/{user_id}/xp?xp_to_add={value}`)
- ✅ Successful XP update - **Service-to-service communication**
- ✅ User not found handling
- ✅ Invalid user ID validation
- ✅ Missing xp_to_add parameter validation
- ✅ Invalid xp_to_add type validation
- ✅ Negative XP value handling
- ✅ Zero XP value handling
- ✅ Internal server error handling

## Running Tests

### Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install pytest pytest-asyncio pytest-cov
```

### Running All Tests

From the users service root directory:

```bash
# Using pytest directly
pytest app/test/ -v

# Using the test runner
python app/test/test_runner.py
```

### Running Specific Test Files

```bash
# Register endpoint tests
pytest app/test/test_register_endpoint.py -v

# Login endpoint tests
pytest app/test/test_login_endpoint.py -v

# Token validation tests
pytest app/test/test_validate_token_endpoint.py -v

# Profile endpoint tests
pytest app/test/test_profile_endpoints.py -v

# XP update endpoint tests
pytest app/test/test_update_xp_endpoint.py -v
```

### Running with Coverage

```bash
# Generate coverage report
pytest app/test/ --cov=app/ --cov-report=term-missing --cov-report=html

# Using test runner with coverage
python -c "from app.test.test_runner import run_with_coverage; run_with_coverage()"
```

## Test Architecture

### Mocking Strategy

Tests use `unittest.mock` to mock external dependencies:

- **Repository Layer**: Mocked to isolate endpoint logic from database operations
- **Use Cases**: Mocked to test controller behavior independently
- **Authentication Service**: Mocked for JWT operations
- **Database Connections**: Completely mocked out

### Fixture Design

The `conftest.py` provides reusable fixtures:

- `client`: FastAPI test client
- `mock_user_repository`: Mocked user repository
- `mock_auth_service`: Mocked authentication service
- `sample_user_dict`: Sample user data for testing
- `sample_user_entity`: Sample user entity object

### Test Patterns

Each test file follows consistent patterns:

1. **Class-based organization**: Tests grouped by endpoint functionality
2. **Descriptive naming**: Test names clearly indicate the scenario being tested
3. **Arrange-Act-Assert**: Clear separation of test setup, execution, and verification
4. **Comprehensive scenarios**: Happy path, validation errors, edge cases, and error conditions

## Notes

- Tests are designed to run independently and in parallel
- No external dependencies (database, network) required
- All tests use mocking to ensure fast execution
- Test data is generated within fixtures for consistency
- Error scenarios are thoroughly tested for proper HTTP status codes and error messages

## Integration with CI/CD

These tests can be easily integrated into continuous integration pipelines:

```yaml
# Example GitHub Actions step
- name: Run Users Service Tests
  run: |
    cd services/users
    pytest app/test/ -v --cov=app/ --cov-report=xml
```