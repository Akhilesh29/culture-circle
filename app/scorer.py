"""
Scoring system for outfit recommendations.
Calculates match_score (0-1) based on multiple factors.
"""
from typing import List, Tuple
from app.models import Outfit, Product, Color, Occasion, Season, Style


class OutfitScorer:
    """Scores outfit combinations based on multiple criteria."""
    
    # Weight factors for different scoring components
    COLOR_WEIGHT = 0.30
    STYLE_WEIGHT = 0.25
    OCCASION_WEIGHT = 0.20
    SEASON_WEIGHT = 0.15
    BUDGET_WEIGHT = 0.10
    
    def __init__(self, target_occasion: Occasion = None, target_season: Season = None, max_budget: float = None):
        self.target_occasion = target_occasion
        self.target_season = target_season
        self.max_budget = max_budget
    
    def score_outfit(self, outfit: Outfit) -> Tuple[float, str]:
        """
        Calculate overall match score and generate reasoning.
        Returns (score, reasoning_string)
        """
        color_score, color_reason = self._score_color_harmony(outfit)
        style_score, style_reason = self._score_style_compatibility(outfit)
        occasion_score, occasion_reason = self._score_occasion_fit(outfit)
        season_score, season_reason = self._score_season_fit(outfit)
        budget_score, budget_reason = self._score_budget(outfit)
        
        # Weighted average
        total_score = (
            color_score * self.COLOR_WEIGHT +
            style_score * self.STYLE_WEIGHT +
            occasion_score * self.OCCASION_WEIGHT +
            season_score * self.SEASON_WEIGHT +
            budget_score * self.BUDGET_WEIGHT
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            color_score, color_reason,
            style_score, style_reason,
            occasion_score, occasion_reason,
            season_score, season_reason,
            budget_score, budget_reason
        )
        
        return total_score, reasoning
    
    def _score_color_harmony(self, outfit: Outfit) -> Tuple[float, str]:
        """
        Score color harmony using HSV color theory.
        Returns (score, reason)
        """
        items = [outfit.top, outfit.bottom, outfit.footwear] + outfit.accessories
        colors = [item.color for item in items]
        
        # Calculate color harmony using complementary, analogous, and triadic schemes
        harmony_score = 0.0
        reasons = []
        
        # Get base color (top)
        base_hsv = colors[0].to_hsv()
        base_hue = base_hsv[0]
        
        # Check each item against base
        for i, color in enumerate(colors[1:], 1):
            hsv = color.to_hsv()
            hue_diff = abs(hsv[0] - base_hue)
            
            # Normalize hue difference (0-180 degrees)
            if hue_diff > 180:
                hue_diff = 360 - hue_diff
            
            # Score based on color harmony rules:
            # - Analogous (0-30°): High score
            # - Complementary (150-180°): High score
            # - Triadic (120°): Medium-high score
            # - Monochromatic (same hue): High score
            
            if hue_diff < 15:  # Monochromatic/very similar
                item_score = 0.95
                reasons.append(f"{items[i].name} matches base color")
            elif hue_diff < 30:  # Analogous
                item_score = 0.85
                reasons.append(f"{items[i].name} is analogous to base")
            elif 115 < hue_diff < 125:  # Triadic
                item_score = 0.75
                reasons.append(f"{items[i].name} creates triadic harmony")
            elif 150 < hue_diff < 180:  # Complementary
                item_score = 0.80
                reasons.append(f"{items[i].name} complements base color")
            elif 30 < hue_diff < 60:  # Split complementary
                item_score = 0.70
                reasons.append(f"{items[i].name} creates split complementary harmony")
            else:
                item_score = 0.50  # Less harmonious
                reasons.append(f"{items[i].name} has moderate color harmony")
            
            harmony_score += item_score
        
        # Average harmony score
        avg_score = harmony_score / len(colors[1:]) if len(colors) > 1 else 0.5
        
        # Bonus for neutral colors (low saturation)
        neutral_bonus = 0.0
        neutral_count = sum(1 for c in colors if c.to_hsv()[1] < 0.2)
        if neutral_count > 0:
            neutral_bonus = min(0.1, neutral_count * 0.03)
            reasons.append(f"{neutral_count} neutral item(s) add versatility")
        
        final_score = min(1.0, avg_score + neutral_bonus)
        reason = "; ".join(reasons[:3])  # Limit to 3 reasons
        
        return final_score, reason or "Color harmony evaluated"
    
    def _score_style_compatibility(self, outfit: Outfit) -> Tuple[float, str]:
        """Score how well styles match across items."""
        items = [outfit.top, outfit.bottom, outfit.footwear] + outfit.accessories
        styles = [item.style for item in items]
        
        # Count style matches
        base_style = styles[0]
        matches = sum(1 for style in styles[1:] if style == base_style)
        total = len(styles) - 1
        
        if total == 0:
            return 1.0, "Single item"
        
        match_ratio = matches / total
        
        # Score: Perfect match = 1.0, partial = 0.7, mixed = 0.5
        if match_ratio == 1.0:
            score = 1.0
            reason = f"All items share {base_style.value} style"
        elif match_ratio >= 0.5:
            score = 0.75
            reason = f"Mostly {base_style.value} style with some variation"
        else:
            score = 0.55
            reason = "Mixed styles create eclectic look"
        
        return score, reason
    
    def _score_occasion_fit(self, outfit: Outfit) -> Tuple[float, str]:
        """Score how appropriate the outfit is for target occasion."""
        if not self.target_occasion:
            return 0.7, "No specific occasion specified"
        
        items = [outfit.top, outfit.bottom, outfit.footwear] + outfit.accessories
        matching_items = sum(1 for item in items if self.target_occasion in item.occasion)
        total = len(items)
        
        match_ratio = matching_items / total
        
        if match_ratio >= 0.8:
            score = 1.0
            reason = f"Perfect for {self.target_occasion.value} occasion"
        elif match_ratio >= 0.6:
            score = 0.8
            reason = f"Good fit for {self.target_occasion.value}"
        elif match_ratio >= 0.4:
            score = 0.6
            reason = f"Moderately suitable for {self.target_occasion.value}"
        else:
            score = 0.4
            reason = f"May not be ideal for {self.target_occasion.value}"
        
        return score, reason
    
    def _score_season_fit(self, outfit: Outfit) -> Tuple[float, str]:
        """Score seasonal appropriateness."""
        if not self.target_season:
            return 0.7, "No specific season specified"
        
        items = [outfit.top, outfit.bottom, outfit.footwear] + outfit.accessories
        matching_items = sum(
            1 for item in items 
            if item.season == self.target_season or item.season == Season.ALL_SEASON
        )
        total = len(items)
        
        match_ratio = matching_items / total
        
        if match_ratio >= 0.8:
            score = 1.0
            reason = f"Perfect for {self.target_season.value} season"
        elif match_ratio >= 0.6:
            score = 0.8
            reason = f"Good for {self.target_season.value} season"
        elif match_ratio >= 0.4:
            score = 0.6
            reason = f"Moderately suitable for {self.target_season.value}"
        else:
            score = 0.4
            reason = f"May not be ideal for {self.target_season.value}"
        
        return score, reason
    
    def _score_budget(self, outfit: Outfit) -> Tuple[float, str]:
        """Score based on budget constraints."""
        if not self.max_budget:
            return 0.7, "No budget constraint"
        
        total_price = outfit.total_price
        
        if total_price <= self.max_budget:
            ratio = total_price / self.max_budget
            if ratio < 0.7:
                score = 0.9
                reason = f"Within budget (${total_price:.2f} of ${self.max_budget:.2f})"
            else:
                score = 1.0
                reason = f"Optimal budget usage (${total_price:.2f} of ${self.max_budget:.2f})"
        else:
            # Penalize going over budget
            overage = total_price - self.max_budget
            penalty = min(0.5, overage / self.max_budget)
            score = max(0.1, 0.5 - penalty)
            reason = f"Exceeds budget by ${overage:.2f}"
        
        return score, reason
    
    def _generate_reasoning(self, color_score, color_reason, style_score, style_reason,
                          occasion_score, occasion_reason, season_score, season_reason,
                          budget_score, budget_reason) -> str:
        """Generate comprehensive reasoning string."""
        parts = []
        
        if color_score >= 0.8:
            parts.append(f"Excellent color harmony: {color_reason}")
        elif color_score >= 0.6:
            parts.append(f"Good color coordination: {color_reason}")
        else:
            parts.append(f"Color harmony: {color_reason}")
        
        if style_score >= 0.8:
            parts.append(f"Style: {style_reason}")
        
        if self.target_occasion and occasion_score >= 0.7:
            parts.append(f"Occasion: {occasion_reason}")
        
        if self.target_season and season_score >= 0.7:
            parts.append(f"Season: {season_reason}")
        
        if self.max_budget:
            parts.append(f"Budget: {budget_reason}")
        
        return ". ".join(parts) if parts else "Well-coordinated outfit"

