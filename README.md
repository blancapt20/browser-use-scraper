# Web Scraper API

This API allows you to scrape websites for sustainability and ESG-related information.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure your `.env` file contains the necessary OpenAI API key.

3. Run the server: (never --reload)
```bash
uvicorn app:app
```

## API Endpoints

### 1. Start a Scraping Job
```http
POST /scrape
Content-Type: application/json

{
    "url": "https://example.com"
}
```

Response:
```json
{
    "job_id": "uuid",
    "status": "started",
    "message": "Scraping job started successfully"
}
```

### 2. Check Job Status
```http
GET /status/{job_id}
```

Response:
```json
{
    "job_id": "uuid",
    "status": "pending|running|completed|failed",
    "url": "https://example.com",
    "start_time": "2023-...",
    "end_time": "2023-..."
}
```

### 3. Get Job Results
```http
GET /result/{job_id}
```

Response (when completed):
```json
{
    "findings": [
        {
            "source_url": "https://example.com/sustainability",
            "extracted_text": "...",
            "summary": "..."
        }
    ]
}
```

## Example Usage with Insomnia

1. Create a new POST request to `http://localhost:8000/scrape`
2. Set the body to JSON with the URL you want to scrape
3. Send the request and save the returned `job_id`
4. Create a GET request to `http://localhost:8000/status/{job_id}` to check progress
5. Once status shows "completed", create a GET request to `http://localhost:8000/result/{job_id}` to get the results
