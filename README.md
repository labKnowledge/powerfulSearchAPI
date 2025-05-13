# [Verboai](https://verboai.app/) Search Engine API

A FastAPI-based search engine that uses DuckDuckGo's lite search interface.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /search

Search for content using a search phrase.

Request body:
```json
{
    "search_phrase": "your search query"
}
```

Response:
```json
{
    "results": {
        "Item_1": {
            "title": "Result title",
            "snippet": "Result snippet",
            "linkText": "Link text"
        },
        // ... more items
    }
}
```

### POST /websiteView

View and browse a website's content in Markdown format.

Request body:
```json
{
    "url": "https://example.com"
}
```

Response:
```json
{
    "title": "Website Title",
    "markdown": "# Website Title\n\nMain content in Markdown format...\n\n## Links\n\n- [Link text](https://example.com/link)\n\n## Images\n\n![Image description](https://example.com/image.jpg)",
    "links": [
        {
            "text": "Link text",
            "url": "https://example.com/link",
            "markdown": "[Link text](https://example.com/link)"
        }
    ],
    "images": [
        {
            "src": "https://example.com/image.jpg",
            "alt": "Image description",
            "markdown": "![Image description](https://example.com/image.jpg)"
        }
    ],
    "url": "https://example.com"
}
```

### POST /searchWithContent

Search for content and retrieve the full content of the top N results.

Request body:
```json
{
    "search_phrase": "your search query",
    "top_n": 5
}
```

Response:
```json
{
    "results": {
        "Item_1": {
            "title": "Result title",
            "snippet": "Result snippet",
            "linkText": "https://example.com",
            "content": {
                "title": "Website Title",
                "markdown": "# Website Title\n\nMain content in Markdown format...",
                "links": [...],
                "images": [...],
                "url": "https://example.com"
            }
        },
        // ... more items up to top_n
    }
}
```

The `content` field for each result contains the full website content in Markdown format, including:
- Title as a level 1 heading
- Main content
- Links section with Markdown-formatted links
- Images section with Markdown-formatted images

## Error Handling

The API will return appropriate HTTP status codes and error messages in case of failures:
- 500: Internal server error
- 422: Validation error (invalid request body) 