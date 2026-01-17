"""
Recommendation engine for generating outfit combinations.
Uses intelligent matching and caching for performance.
"""
import random
from typing import List, Optional, Dict
from collections import defaultdict
from app.models import (
    Product, Outfit, Category, Style, Season, Occasion,
    RecommendationRequest
)
from app.scorer import OutfitScorer


class OutfitRecommender:
    """
    Core recommendation engine.
    Uses precomputed compatibility matrices and smart filtering for <1s response.
    """
    
    def __init__(self, products: List[Product]):
        self.products = products
        self._index_products()
        self._precompute_compatibility()
    
    def _index_products(self):
        """Index products by category for fast lookup."""
        self.by_category: Dict[Category, List[Product]] = defaultdict(list)
        self.by_id: Dict[str, Product] = {}
        
        for product in self.products:
            self.by_category[product.category].append(product)
            self.by_id[product.id] = product
    
    def _precompute_compatibility(self):
        """
        Precompute compatibility scores between products.
        This is done once at initialization for performance.
        """
        self.compatibility_cache: Dict[tuple, float] = {}
        
        # Precompute color compatibility for all pairs
        for i, p1 in enumerate(self.products):
            for p2 in self.products[i+1:]:
                key = tuple(sorted([p1.id, p2.id]))
                score = self._calculate_color_compatibility(p1.color, p2.color)
                self.compatibility_cache[key] = score
    
    def _calculate_color_compatibility(self, color1, color2) -> float:
        """Quick color compatibility check."""
        hsv1 = color1.to_hsv()
        hsv2 = color2.to_hsv()
        
        hue_diff = abs(hsv1[0] - hsv2[0])
        if hue_diff > 180:
            hue_diff = 360 - hue_diff
        
        # Quick compatibility score
        if hue_diff < 30:
            return 0.9  # Analogous
        elif 150 < hue_diff < 180:
            return 0.85  # Complementary
        elif 115 < hue_diff < 125:
            return 0.75  # Triadic
        else:
            return 0.6  # Less compatible
    
    def generate_recommendations(
        self, 
        request: RecommendationRequest
    ) -> List[Outfit]:
        """
        Generate outfit recommendations from a base product.
        Optimized for <1s response time.
        """
        base_product = self.by_id.get(request.base_product_id)
        if not base_product:
            raise ValueError(f"Product {request.base_product_id} not found")
        
        # Filter products by constraints
        candidates = self._filter_candidates(
            base_product, 
            request.occasion,
            request.season,
            request.max_budget,
            request.style_preference
        )
        
        # Generate outfit combinations
        outfits = []
        max_attempts = 100  # Limit to prevent infinite loops
        attempts = 0
        
        while len(outfits) < request.num_recommendations and attempts < max_attempts:
            attempts += 1
            
            try:
                outfit = self._generate_single_outfit(
                    base_product,
                    candidates,
                    request
                )
                
                # Check for duplicates
                if not self._is_duplicate(outfit, outfits):
                    outfits.append(outfit)
            except Exception:
                # Skip invalid combinations
                continue
        
        # Score and rank all outfits
        scorer = OutfitScorer(
            target_occasion=request.occasion,
            target_season=request.season,
            max_budget=request.max_budget
        )
        
        scored_outfits = []
        for outfit in outfits:
            score, reasoning = scorer.score_outfit(outfit)
            outfit.match_score = score
            outfit.reasoning = reasoning
            scored_outfits.append(outfit)
        
        # Sort by score (descending)
        scored_outfits.sort(key=lambda x: x.match_score, reverse=True)
        
        return scored_outfits[:request.num_recommendations]
    
    def _filter_candidates(
        self,
        base_product: Product,
        occasion: Optional[Occasion],
        season: Optional[Season],
        max_budget: Optional[float],
        style_preference: Optional[Style]
    ) -> Dict[Category, List[Product]]:
        """Filter products by constraints for fast candidate selection."""
        filtered = defaultdict(list)
        
        for category in [Category.TOP, Category.BOTTOM, Category.FOOTWEAR, Category.ACCESSORY]:
            candidates = self.by_category[category].copy()
            
            # Filter by occasion
            if occasion:
                candidates = [p for p in candidates if occasion in p.occasion]
            
            # Filter by season
            if season:
                candidates = [
                    p for p in candidates 
                    if p.season == season or p.season == Season.ALL_SEASON
                ]
            
            # Filter by style preference (if specified)
            if style_preference:
                # Allow base style or preferred style
                candidates = [
                    p for p in candidates 
                    if p.style == style_preference or p.style == base_product.style
                ]
            
            # Filter by budget (rough estimate - assume base product is already included)
            if max_budget:
                base_price = base_product.price
                remaining_budget = max_budget - base_price
                # Rough filtering - allow items that could fit
                candidates = [
                    p for p in candidates 
                    if p.price <= remaining_budget * 1.5  # Allow some flexibility
                ]
            
            filtered[category] = candidates
        
        return filtered
    
    def _generate_single_outfit(
        self,
        base_product: Product,
        candidates: Dict[Category, List[Product]],
        request: RecommendationRequest
    ) -> Outfit:
        """Generate a single outfit combination."""
        # Determine which category the base product is in
        base_category = base_product.category
        
        # Select items for each required category
        top = base_product if base_category == Category.TOP else self._select_item(
            candidates[Category.TOP], base_product
        )
        
        bottom = base_product if base_category == Category.BOTTOM else self._select_item(
            candidates[Category.BOTTOM], base_product
        )
        
        footwear = base_product if base_category == Category.FOOTWEAR else self._select_item(
            candidates[Category.FOOTWEAR], base_product
        )
        
        # Select at least one accessory
        num_accessories = random.randint(1, 3)  # 1-3 accessories
        accessories = []
        for _ in range(num_accessories):
            if candidates[Category.ACCESSORY]:
                acc = self._select_item(candidates[Category.ACCESSORY], base_product)
                if acc and acc not in accessories:
                    accessories.append(acc)
        
        if not accessories and candidates[Category.ACCESSORY]:
            accessories.append(self._select_item(candidates[Category.ACCESSORY], base_product))
        
        # Calculate total price
        total_price = (
            top.price + bottom.price + footwear.price + 
            sum(acc.price for acc in accessories)
        )
        
        return Outfit(
            top=top,
            bottom=bottom,
            footwear=footwear,
            accessories=accessories,
            match_score=0.0,  # Will be scored later
            reasoning="",
            total_price=total_price
        )
    
    def _select_item(self, candidates: List[Product], base_product: Product) -> Product:
        """Select an item that's compatible with the base product."""
        if not candidates:
            raise ValueError("No candidates available")
        
        # Score candidates by compatibility with base
        scored = []
        for candidate in candidates:
            if candidate.id == base_product.id:
                continue
            
            # Quick compatibility check
            compatibility = self._get_compatibility(base_product, candidate)
            
            # Bonus for style match
            style_bonus = 0.2 if candidate.style == base_product.style else 0.0
            
            score = compatibility + style_bonus
            scored.append((score, candidate))
        
        # Sort by score and pick from top candidates
        scored.sort(key=lambda x: x[0], reverse=True)
        top_candidates = scored[:max(3, len(scored) // 3)]
        
        # Random selection from top candidates for variety
        if top_candidates:
            return random.choice(top_candidates)[1]
        else:
            return random.choice(candidates)
    
    def _get_compatibility(self, p1: Product, p2: Product) -> float:
        """Get precomputed compatibility score."""
        key = tuple(sorted([p1.id, p2.id]))
        return self.compatibility_cache.get(key, 0.5)
    
    def _is_duplicate(self, outfit: Outfit, existing: List[Outfit]) -> bool:
        """Check if outfit is too similar to existing ones."""
        for existing_outfit in existing:
            if (outfit.top.id == existing_outfit.top.id and
                outfit.bottom.id == existing_outfit.bottom.id and
                outfit.footwear.id == existing_outfit.footwear.id):
                return True
        return False

