from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict
import asyncio
from scraper_module import ScraperJob
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Web Scraper API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active jobs and their tasks
jobs: Dict[str, ScraperJob] = {}
tasks: Dict[str, asyncio.Task] = {}

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def start_scrape(request: ScrapeRequest):
    job_id = str(uuid.uuid4())
    job = ScraperJob(job_id=job_id, url=request.url)
    jobs[job_id] = job
    
    # Start the scraping task in the background and store the task
    task = asyncio.create_task(job.run())
    tasks[job_id] = task
    
    # Add callback to clean up task when done
    def cleanup_task(t):
        if job_id in tasks:
            del tasks[job_id]
    
    task.add_done_callback(cleanup_task)
    
    return {
        "job_id": job_id,
        "status": "started",
        "message": "Scraping job started successfully"
    }

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job.get_status()

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # If the job has a task and it's not done, wait for it
    task = tasks.get(job_id)
    if task and not task.done():
        try:
            await asyncio.wait_for(asyncio.shield(task), timeout=1.0)
        except asyncio.TimeoutError:
            pass  # We'll return the current state even if not complete
    
    return job.get_result()
