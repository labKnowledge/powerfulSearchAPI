from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from search import search_n_browse, search_with_content
from website_viewer import fetch_website_content
from typing import Dict, List


app = FastAPI(title="VerboAI Search Engine API", description="""
VerboAI Search Engine API provides three core functionalities:
1. Web search with browsing capabilities
2. Website content extraction with structured data (title, markdown, links, and images)
3. Content-based search that returns the top N most relevant results from websites

The API is built with FastAPI, supports CORS, and is ready for cloud deployment. Powered by VerboAI.
""", version="1.0.0", docs_url="/", redoc_url="/redoc")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    search_phrase: str

class SearchResponse(BaseModel):
    results: dict

class WebsiteViewRequest(BaseModel):
    url: str




class WebsiteViewResponse(BaseModel):
    title: str
    markdown: str
    links: Dict[str, List[Dict]] = {}    
    images: Dict[str, List[Dict]] = {}
    url: str

class SearchWithContentRequest(BaseModel):
    search_phrase: str
    top_n: int = 5

class SearchWithContentResponse(BaseModel):
    results: dict

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        results = await search_n_browse(request.search_phrase)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/websiteView", response_model=WebsiteViewResponse)
async def view_website(request: WebsiteViewRequest):
    try:
        
        website_content = await fetch_website_content(request.url)
        return WebsiteViewResponse(**website_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/searchWithContent", response_model=SearchWithContentResponse)
async def search_with_content_endpoint(request: SearchWithContentRequest):
    try:
        results = await search_with_content(request.search_phrase, request.top_n)
        return SearchWithContentResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860) 