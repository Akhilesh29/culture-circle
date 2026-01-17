"""
Caching layer for recommendation results.
Uses in-memory cache for fast response times.
"""
from typing import Optional, Dict, List
from functools import lru_cache
from app.models import Outfit, RecommendationRequest
import hashlib
import json


class RecommendationCache:
    """
    Simple in-memory cache for recommendations.
    In production, this could be Redis or similar.
    """
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, List[Dict]] = {}
        self.max_size = max_size
    
    def _cache_key(self, request: RecommendationRequest) -> str:
        """Generate cache key from request."""
        key_data = {
            "base_product_id": request.base_product_id,
            "occasion": request.occasion.value if request.occasion else None,
            "season": request.season.value if request.season else None,
            "max_budget": request.max_budget,
            "style_preference": request.style_preference.value if request.style_preference else None,
            "num_recommendations": request.num_recommendations
        }
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, request: RecommendationRequest) -> Optional[List[Dict]]:
        """Get cached recommendations."""
        key = self._cache_key(request)
        return self.cache.get(key)
    
    def set(self, request: RecommendationRequest, outfits: List[Outfit]):
        """Cache recommendations."""
        key = self._cache_key(request)
        
        # Simple LRU eviction if cache is full
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            if self.cache:
                first_key = next(iter(self.cache))
                del self.cache[first_key]
        
        # Store as dictionaries for serialization
        self.cache[key] = [outfit.to_dict() for outfit in outfits]
    
    def clear(self):
        """Clear all cached entries."""
        self.cache.clear()

