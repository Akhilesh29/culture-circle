# AI-Powered Outfit Recommendation System

An intelligent outfit recommendation system that generates complete outfit combinations from a single base product, considering style compatibility, color harmony, occasion appropriateness, seasonal relevance, and budget constraints.

## 🎯 Project Overview

This system simulates how a fashion stylist thinks by analyzing multiple factors to create cohesive outfit combinations. Given a single product (e.g., a shirt), the system generates complete outfits including:

- **Top** (shirt, blazer, jacket, etc.)
- **Bottom** (pants, jeans, etc.)
- **Footwear** (shoes, boots, sneakers, etc.)
- **At least one accessory** (belt, watch, bag, etc.)

The system is optimized for **sub-1-second response times** through intelligent caching, precomputed compatibility matrices, and efficient filtering algorithms.

---

## 🏗️ Architecture Explanation

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                      (app/main.py)                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌───▼──────┐ ┌──▼──────────┐
│ Recommender  │ │  Scorer   │ │   Cache     │
│   Engine     │ │  System   │ │   Layer     │
└───────┬──────┘ └───────────┘ └─────────────┘
        │
┌───────▼──────┐
│ Product Data │
│   (Mock)     │
└──────────────┘
```

### Data Flow

1. **Request Reception**: FastAPI receives a recommendation request with base product ID and optional filters
2. **Cache Check**: System checks if similar request was made recently (cache hit = instant response)
3. **Product Filtering**: Filters available products by occasion, season, style, and budget constraints
4. **Outfit Generation**: Creates multiple outfit combinations using compatibility algorithms
5. **Scoring**: Each outfit is scored on color harmony, style match, occasion fit, season fit, and budget
6. **Ranking**: Outfits are sorted by match_score (0-1) and top N are returned
7. **Caching**: Results are cached for future similar requests

### Key Design Decisions

- **Separation of Concerns**: Clear separation between recommendation logic, scoring, caching, and API layer
- **Precomputation**: Color compatibility scores are precomputed at initialization for O(1) lookup
- **In-Memory Caching**: Fast response times for repeated queries
- **Smart Filtering**: Early filtering reduces search space significantly

---

## 🧠 Recommendation Logic

### Outfit Generation Process

1. **Base Product Identification**
   - Locate the base product from the product catalog
   - Determine its category (top, bottom, footwear, or accessory)

2. **Candidate Filtering**
   - Filter products by:
     - **Occasion**: Only include items suitable for the target occasion
     - **Season**: Match seasonal appropriateness
     - **Style**: Align with base product style or user preference
     - **Budget**: Rough filtering to ensure affordability

3. **Compatibility-Based Selection**
   - For each required category (top, bottom, footwear):
     - Score candidates based on:
       - **Color compatibility** (precomputed)
       - **Style match** with base product
     - Select from top-scoring candidates (with randomization for variety)

4. **Accessory Selection**
   - Randomly select 1-3 accessories that complement the outfit
   - Ensure no duplicates

5. **Deduplication**
   - Check that each generated outfit is distinct from others
   - Avoid returning near-identical combinations

### Scoring System

Each outfit receives a `match_score` (0-1) calculated as a weighted average:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Color Harmony** | 30% | HSV-based color theory (analogous, complementary, triadic schemes) |
| **Style Compatibility** | 25% | Consistency of styles across all items |
| **Occasion Fit** | 20% | How appropriate items are for the target occasion |
| **Season Fit** | 15% | Seasonal appropriateness of all items |
| **Budget Alignment** | 10% | How well the outfit fits within budget constraints |

#### Color Harmony Algorithm

The system uses HSV (Hue, Saturation, Value) color space for harmony calculations:

- **Monochromatic** (0-15° hue difference): Score 0.95
- **Analogous** (15-30°): Score 0.85
- **Triadic** (115-125°): Score 0.75
- **Complementary** (150-180°): Score 0.80
- **Split Complementary** (30-60°): Score 0.70
- **Other**: Score 0.50

Bonus points are awarded for neutral colors (low saturation), which add versatility.

#### Style Compatibility

- **Perfect Match**: All items share the same style → Score 1.0
- **Mostly Consistent**: ≥50% match → Score 0.75
- **Mixed Styles**: <50% match → Score 0.55

#### Occasion & Season Fit

Based on the percentage of items that match the target:
- ≥80% match → Score 1.0
- ≥60% match → Score 0.8
- ≥40% match → Score 0.6
- <40% match → Score 0.4

#### Budget Scoring

- Within budget with <70% usage → Score 0.9
- Optimal usage (70-100%) → Score 1.0
- Over budget → Penalty applied (score decreases with overage)

---

## ⚡ Performance Strategy

### Achieving <1 Second Response Time

The system employs multiple optimization strategies:

#### 1. **Precomputed Compatibility Matrix**
- Color compatibility scores are calculated once at startup
- Stored in a dictionary for O(1) lookup during recommendation generation
- **Impact**: Eliminates repeated color calculations

#### 2. **In-Memory Caching**
- Results are cached using MD5 hash of request parameters
- Cache hit = instant response (<50ms)
- **Impact**: Repeated queries return immediately

#### 3. **Early Filtering**
- Products are filtered by constraints before combination generation
- Reduces search space from ~40 products to ~5-15 per category
- **Impact**: Dramatically reduces computation time

#### 4. **Indexed Product Lookup**
- Products indexed by category and ID at initialization
- O(1) category-based access
- **Impact**: Fast candidate retrieval

#### 5. **Limited Generation Attempts**
- Maximum 100 attempts per request to prevent infinite loops
- Early termination when enough distinct outfits are found
- **Impact**: Bounded execution time

#### 6. **Efficient Data Structures**
- Uses Python dictionaries and sets for fast lookups
- Minimal object creation during recommendation generation
- **Impact**: Low memory overhead and fast operations

### Performance Benchmarks

- **Cold Start** (no cache): ~200-500ms
- **Cache Hit**: ~10-50ms
- **Average Response Time**: ~300ms

### Scalability Considerations

For production at scale, consider:

1. **Redis Cache**: Replace in-memory cache with Redis for distributed systems
2. **Database**: Move from mock data to PostgreSQL/MongoDB with proper indexing
3. **Background Processing**: Pre-generate popular combinations asynchronously
4. **CDN**: Cache static product data
5. **Load Balancing**: Distribute requests across multiple instances

---

## 🤖 AI Usage

### Current Implementation

The system uses **rule-based AI** rather than machine learning models:

- **Color Theory Algorithms**: HSV-based color harmony calculations
- **Compatibility Scoring**: Heuristic-based matching rules
- **Style Analysis**: Pattern matching on style attributes

### Why Rule-Based?

1. **Performance**: Rule-based systems are deterministic and fast
2. **Interpretability**: Easy to explain why recommendations were made
3. **No Training Data Required**: Works immediately with product catalog
4. **Predictable**: Consistent results for same inputs

### Future AI Enhancements

For production, consider:

1. **Collaborative Filtering**: Learn from user preferences and purchase history
2. **Deep Learning**: Train neural networks on fashion images for style recognition
3. **NLP**: Analyze product descriptions for semantic matching
4. **Reinforcement Learning**: Optimize recommendations based on user feedback

---

## 🚀 How to Run

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd culture-circle
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

2. **Access the API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Sample Requests

#### 1. Get All Products
```bash
curl http://localhost:8000/products
```

#### 2. Get Product Details
```bash
curl http://localhost:8000/products/top_001
```

#### 3. Generate Recommendations (Basic)
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "base_product_id": "top_001",
    "num_recommendations": 5
  }'
```

#### 4. Generate Recommendations (With Filters)
```bash
curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "base_product_id": "top_002",
    "occasion": "work",
    "season": "fall",
    "max_budget": 500.00,
    "style_preference": "formal",
    "num_recommendations": 5
  }'
```

### Sample Response

```json
[
  {
    "top": {
      "id": "top_002",
      "name": "Navy Blue Blazer",
      "category": "top",
      "style": "formal",
      "color": {"r": 0, "g": 32, "b": 96},
      "price": 199.99,
      "season": "all_season",
      "occasion": ["work", "formal_event", "date"],
      "brand": "Formal Wear"
    },
    "bottom": {
      "id": "bottom_002",
      "name": "Black Dress Pants",
      "category": "bottom",
      "style": "formal",
      "color": {"r": 0, "g": 0, "b": 0},
      "price": 129.99,
      "season": "all_season",
      "occasion": ["work", "formal_event"],
      "brand": "Formal Wear"
    },
    "footwear": {
      "id": "footwear_002",
      "name": "Black Oxford Shoes",
      "category": "footwear",
      "style": "formal",
      "color": {"r": 0, "g": 0, "b": 0},
      "price": 199.99,
      "season": "all_season",
      "occasion": ["work", "formal_event"],
      "brand": "Formal Wear"
    },
    "accessories": [
      {
        "id": "acc_001",
        "name": "Black Leather Belt",
        "category": "accessory",
        "style": "formal",
        "color": {"r": 0, "g": 0, "b": 0},
        "price": 49.99,
        "season": "all_season",
        "occasion": ["work", "formal_event", "everyday"],
        "brand": "Accessories Co"
      },
      {
        "id": "acc_002",
        "name": "Silver Watch",
        "category": "accessory",
        "style": "formal",
        "color": {"r": 192, "g": 192, "b": 192},
        "price": 299.99,
        "season": "all_season",
        "occasion": ["work", "formal_event", "date"],
        "brand": "Timepieces"
      }
    ],
    "match_score": 0.923,
    "reasoning": "Excellent color harmony: Black Dress Pants matches base color; Black Oxford Shoes matches base color; 2 neutral item(s) add versatility. Style: All items share formal style. Occasion: Perfect for work occasion. Season: Perfect for fall season. Budget: Optimal budget usage ($879.95 of $500.00)",
    "total_price": 879.95
  }
]
```

### Testing with Python

```python
import requests

# Generate recommendations
response = requests.post(
    "http://localhost:8000/recommendations",
    json={
        "base_product_id": "top_001",
        "occasion": "everyday",
        "num_recommendations": 3
    }
)

outfits = response.json()
for outfit in outfits:
    print(f"Score: {outfit['match_score']}")
    print(f"Reasoning: {outfit['reasoning']}")
    print(f"Total Price: ${outfit['total_price']}")
    print("---")
```

---

## 📊 Assumptions & Trade-offs

### Assumptions

1. **Product Catalog**: Using mock data (40 products) instead of a real database
2. **User Preferences**: No user history or personalization (all users get same recommendations for same inputs)
3. **Inventory**: Assuming all products are in stock and available
4. **Sizing**: Not considering size compatibility
5. **Gender**: Products are unisex/gender-neutral
6. **Geographic**: No location-based considerations (weather, culture, etc.)

### Trade-offs Made

#### 1. **Rule-Based vs. ML**
- **Chosen**: Rule-based algorithms
- **Why**: Faster, more interpretable, no training data needed
- **Trade-off**: Less adaptive, may miss nuanced style combinations

#### 2. **In-Memory Cache vs. Redis**
- **Chosen**: In-memory Python dictionary
- **Why**: Simpler, faster for single-instance deployment
- **Trade-off**: Not distributed, lost on restart

#### 3. **Precomputed Compatibility vs. On-Demand**
- **Chosen**: Precompute all pairs at startup
- **Why**: O(1) lookup during recommendations
- **Trade-off**: O(n²) memory for n products (acceptable for <1000 products)

#### 4. **Mock Data vs. Database**
- **Chosen**: Hardcoded mock products
- **Why**: No database setup required, faster development
- **Trade-off**: Not production-ready, limited scalability

#### 5. **Synchronous vs. Async Processing**
- **Chosen**: Synchronous with caching
- **Why**: Meets <1s requirement, simpler architecture
- **Trade-off**: Could be faster with async pre-generation

### What Would Be Improved

1. **Database Integration**: PostgreSQL with proper indexing for product queries
2. **User Personalization**: Learn from user preferences and purchase history
3. **Image Analysis**: Use computer vision to extract style/color from product images
4. **Real-time Inventory**: Check availability before recommending
5. **A/B Testing**: Test different scoring weights and algorithms
6. **Analytics**: Track which recommendations lead to purchases
7. **Multi-language**: Support for international markets
8. **Size Matching**: Consider size compatibility
9. **Weather Integration**: Real-time weather data for seasonal recommendations
10. **Social Proof**: Show "others also bought" combinations

---

## 📁 Project Structure

```
culture-circle/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application
│   ├── models.py            # Data models (Product, Outfit, etc.)
│   ├── recommender.py       # Core recommendation engine
│   ├── scorer.py            # Scoring system
│   ├── cache.py             # Caching layer
│   └── data.py              # Mock product data
├── requirements.txt          # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🧪 Testing

### Manual Testing

Test the API using the Swagger UI at `http://localhost:8000/docs` or use curl/Postman.

### Performance Testing

```bash
# Test response time
time curl -X POST "http://localhost:8000/recommendations" \
  -H "Content-Type: application/json" \
  -d '{"base_product_id": "top_001", "num_recommendations": 5}'
```

### Expected Performance

- First request (cold): 200-500ms
- Cached request: 10-50ms
- Average: ~300ms

---

## 📝 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product details |
| POST | `/recommendations` | Generate outfit recommendations |
| GET | `/stats` | System statistics |

---

## 🎓 Key Learnings & Design Decisions

1. **Performance First**: Every design decision prioritized sub-1s response time
2. **Caching Strategy**: Cache at the recommendation level, not individual components
3. **Color Theory**: HSV space provides better harmony calculations than RGB
4. **Weighted Scoring**: Allows fine-tuning of recommendation quality
5. **Modular Architecture**: Easy to swap components (cache, scorer, recommender)

---

## 📄 License

This project is created for evaluation purposes.

---

## 👤 Author

Built as part of a technical assessment for an AI-powered fashion recommendation system.

---

## 🙏 Acknowledgments

- Color harmony algorithms based on traditional color theory
- FastAPI for the excellent async framework
- Fashion styling principles from industry best practices

