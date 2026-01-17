"""
FastAPI application for the Outfit Recommendation System.
Optimized for <1s response time with caching and efficient algorithms.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import time

from app.models import Product, RecommendationRequest, Occasion, Season, Style
from app.recommender import OutfitRecommender
from app.cache import RecommendationCache
from app.data import generate_mock_products


# Initialize FastAPI app
app = FastAPI(
    title="Outfit Recommendation API",
    description="AI-powered outfit recommendation system with <1s response time",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global components
products = generate_mock_products()
recommender = OutfitRecommender(products)
cache = RecommendationCache()


# Request/Response models
class RecommendationRequestModel(BaseModel):
    base_product_id: str
    occasion: Optional[str] = None
    season: Optional[str] = None
    max_budget: Optional[float] = None
    style_preference: Optional[str] = None
    num_recommendations: int = 5


class ProductResponse(BaseModel):
    id: str
    name: str
    category: str
    style: str
    color: dict
    price: float
    season: str
    occasion: List[str]
    brand: Optional[str] = None
    description: Optional[str] = None


class OutfitResponse(BaseModel):
    top: ProductResponse
    bottom: ProductResponse
    footwear: ProductResponse
    accessories: List[ProductResponse]
    match_score: float
    reasoning: str
    total_price: float


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Outfit Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /products": "List all available products",
            "GET /products/{product_id}": "Get product details",
            "POST /recommendations": "Generate outfit recommendations",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "products_count": len(products)}


@app.get("/products", response_model=List[ProductResponse])
async def get_products():
    """Get all available products."""
    return [ProductResponse(**product.to_dict()) for product in products]


@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get a specific product by ID."""
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product.to_dict())


@app.post("/recommendations", response_model=List[OutfitResponse])
async def get_recommendations(request: RecommendationRequestModel):
    """
    Generate outfit recommendations from a base product.
    Optimized for <1s response time using caching and precomputed compatibility.
    """
    start_time = time.time()
    
    # Check cache first
    cache_request = RecommendationRequest(
        base_product_id=request.base_product_id,
        occasion=Occasion(request.occasion) if request.occasion else None,
        season=Season(request.season) if request.season else None,
        max_budget=request.max_budget,
        style_preference=Style(request.style_preference) if request.style_preference else None,
        num_recommendations=request.num_recommendations
    )
    
    cached_result = cache.get(cache_request)
    if cached_result:
        # Return cached results directly (already in dict format)
        return [OutfitResponse(**outfit_dict) for outfit_dict in cached_result]
    
    # Generate recommendations
    try:
        outfits = recommender.generate_recommendations(cache_request)
        
        # Cache the results
        cache.set(cache_request, outfits)
        
        elapsed = time.time() - start_time
        
        # Log performance (in production, use proper logging)
        if elapsed > 1.0:
            print(f"WARNING: Response time {elapsed:.3f}s exceeds 1s target")
        
        return [OutfitResponse(**outfit.to_dict()) for outfit in outfits]
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get system statistics."""
    return {
        "total_products": len(products),
        "products_by_category": {
            category.value: len([p for p in products if p.category == category])
            for category in ["top", "bottom", "footwear", "accessory"]
        },
        "cache_size": len(cache.cache),
        "cache_max_size": cache.max_size
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

