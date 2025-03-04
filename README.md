# AI Regex Generator

An AI-powered regular expression generator built with FastAPI that helps you create, test, and manage complex regex patterns with ease.

## Features

- **AI-Powered Generation**: Describe what you need and let AI create the perfect regex pattern
- **Interactive Testing**: Test your regex against sample text with visual match highlighting
- **Pattern Library**: Save and reuse your regex patterns
- **Detailed Explanations**: Get step-by-step explanations of how each regex works
- **Test Cases**: Create and run test cases to validate your patterns
- **Multiple Regex Flavors**: Support for different regex flags and options

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: HTML/CSS/JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL (optional)
- **AI Integration**: OpenAI API

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/sylvester-francis/ai-regex-generator.git
   cd ai-regex-generator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the example:
   ```bash
   cp .env.example .env
   ```

5. Configure your `.env` file (see [Environment Configuration](#environment-configuration) section below)

### Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

### Using Docker

1. Make sure you have Docker and Docker Compose installed.

2. Create a `.env` file with your configuration as described in the [Environment Configuration](#environment-configuration) section.

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. The application will be available at [http://localhost:8000](http://localhost:8000)

## Environment Configuration

The application uses a `.env` file for configuration, which should be placed in the project root directory.

### Required Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key for AI generation capability | None (must be provided) |

### Database Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./regex_generator.db` |

Database URL format examples:
- SQLite: `sqlite+aiosqlite:///./regex_generator.db`
- PostgreSQL: `postgresql+asyncpg://user:password@localhost:5432/regex_generator`
- MySQL: `mysql+aiomysql://user:password@localhost:3306/regex_generator`

### Application Settings

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `HOST` | Host to bind the server | `0.0.0.0` |
| `PORT` | Port to bind the server | `8000` |
| `SECRET_KEY` | Secret key for security | `change-this-to-a-secure-random-key-in-production` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | `INFO` |
| `MAX_REQUESTS_PER_MINUTE` | Rate limiting for API requests | `60` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `API_TIMEOUT` | Timeout for API requests (seconds) | `30` |

### Sample `.env` File

```bash
# Required: Your OpenAI API key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Database connection (SQLite by default)
DATABASE_URL=sqlite+aiosqlite:///./regex_generator.db

# Application settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Security settings
SECRET_KEY=change-this-to-a-secure-random-key-in-production
```

### Production Recommendations

For production deployments:

1. Set `DEBUG=False` to disable debug mode
2. Generate a secure random key for `SECRET_KEY`:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
3. Use a production-ready database like PostgreSQL
4. Configure appropriate rate limiting
5. Never commit your `.env` file to version control (it's already in `.gitignore`)

## Usage Guide

### Generating a Regex Pattern

1. Go to the home page and fill out the generator form:
   - Describe what you want the regex to match or extract
   - Provide sample text containing examples
   - Optionally specify exactly what parts should be matched

2. Click "Generate Regex" and wait for the AI to create your pattern

3. Review the generated pattern, explanation, and test results

4. Use the "View Pattern Details" button to save the pattern to your library

### Testing a Regex Pattern

1. On a pattern's detail page, use the testing form to try different inputs

2. Add test cases to validate your pattern against specific inputs

3. Use the flags checkboxes to modify the behavior of the regex:
   - `i`: Case insensitive matching
   - `m`: Multi-line mode
   - `s`: Dot matches newline
   - `x`: Verbose mode

### Managing Your Pattern Library

1. Browse all your saved patterns in the Pattern Library

2. Create new patterns manually or via the AI generator

3. View detailed information about each pattern

4. Test and refine your patterns

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
ai-regex-generator/
├── app/
│   ├── routes/              # API and view routes
│   │   ├── api/             # API endpoints
│   │   └── views.py         # Template-based views
│   ├── services/            # Business logic
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # Jinja2 templates
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   └── schemas.py           # Pydantic schemas
├── .env.example             # Example environment variables
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── main.py                  # Application entry point
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/) - Modern, fast web framework for building APIs
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQL toolkit and ORM
- [OpenAI](https://openai.com/) - AI language models
- [Bootstrap](https://getbootstrap.com/) - Frontend framework