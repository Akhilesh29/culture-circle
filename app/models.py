"""
Data models for the Outfit Recommendation System.
"""
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime


class Category(str, Enum):
    """Product categories."""
    TOP = "top"
    BOTTOM = "bottom"
    FOOTWEAR = "footwear"
    ACCESSORY = "accessory"


class Style(str, Enum):
    """Fashion styles."""
    CASUAL = "casual"
    FORMAL = "formal"
    SPORTY = "sporty"
    BOHEMIAN = "bohemian"
    MINIMALIST = "minimalist"
    VINTAGE = "vintage"
    STREETWEAR = "streetwear"
    BUSINESS = "business"


class Season(str, Enum):
    """Seasonal categories."""
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"
    WINTER = "winter"
    ALL_SEASON = "all_season"


class Occasion(str, Enum):
    """Occasion types."""
    EVERYDAY = "everyday"
    WORK = "work"
    PARTY = "party"
    DATE = "date"
    SPORTS = "sports"
    FORMAL_EVENT = "formal_event"
    TRAVEL = "travel"


@dataclass
class Color:
    """RGB color representation for harmony calculations."""
    r: int
    g: int
    b: int
    
    def to_hsv(self) -> tuple:
        """Convert RGB to HSV for color harmony calculations."""
        r, g, b = self.r / 255.0, self.g / 255.0, self.b / 255.0
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val
        
        # Hue calculation
        if delta == 0:
            h = 0
        elif max_val == r:
            h = 60 * (((g - b) / delta) % 6)
        elif max_val == g:
            h = 60 * (((b - r) / delta) + 2)
        else:
            h = 60 * (((r - g) / delta) + 4)
        
        # Saturation
        s = 0 if max_val == 0 else delta / max_val
        
        # Value
        v = max_val
        
        return (h, s, v)


@dataclass
class Product:
    """Product data model."""
    id: str
    name: str
    category: Category
    style: Style
    color: Color
    price: float
    season: Season
    occasion: List[Occasion]
    brand: Optional[str] = None
    description: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert product to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "style": self.style.value,
            "color": {"r": self.color.r, "g": self.color.g, "b": self.color.b},
            "price": self.price,
            "season": self.season.value,
            "occasion": [occ.value for occ in self.occasion],
            "brand": self.brand,
            "description": self.description
        }


@dataclass
class Outfit:
    """Complete outfit combination."""
    top: Product
    bottom: Product
    footwear: Product
    accessories: List[Product]
    match_score: float
    reasoning: str
    total_price: float
    
    def to_dict(self) -> dict:
        """Convert outfit to dictionary."""
        return {
            "top": self.top.to_dict(),
            "bottom": self.bottom.to_dict(),
            "footwear": self.footwear.to_dict(),
            "accessories": [acc.to_dict() for acc in self.accessories],
            "match_score": round(self.match_score, 3),
            "reasoning": self.reasoning,
            "total_price": round(self.total_price, 2)
        }


@dataclass
class RecommendationRequest:
    """Request model for outfit recommendations."""
    base_product_id: str
    occasion: Optional[Occasion] = None
    season: Optional[Season] = None
    max_budget: Optional[float] = None
    style_preference: Optional[Style] = None
    num_recommendations: int = 5

