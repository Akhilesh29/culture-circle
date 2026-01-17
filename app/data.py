"""
Mock product data for the recommendation system.
In production, this would come from a database.
"""
from app.models import Product, Category, Style, Season, Occasion, Color


def generate_mock_products() -> list[Product]:
    """Generate a diverse set of mock products for testing."""
    
    products = [
        # TOPS
        Product(
            id="top_001",
            name="Classic White T-Shirt",
            category=Category.TOP,
            style=Style.CASUAL,
            color=Color(255, 255, 255),
            price=29.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.SPORTS, Occasion.TRAVEL],
            brand="Basics Co"
        ),
        Product(
            id="top_002",
            name="Navy Blue Blazer",
            category=Category.TOP,
            style=Style.FORMAL,
            color=Color(0, 32, 96),
            price=199.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT, Occasion.DATE],
            brand="Formal Wear"
        ),
        Product(
            id="top_003",
            name="Black Leather Jacket",
            category=Category.TOP,
            style=Style.STREETWEAR,
            color=Color(20, 20, 20),
            price=299.99,
            season=Season.FALL,
            occasion=[Occasion.EVERYDAY, Occasion.PARTY, Occasion.DATE],
            brand="Urban Edge"
        ),
        Product(
            id="top_004",
            name="Floral Summer Blouse",
            category=Category.TOP,
            style=Style.BOHEMIAN,
            color=Color(255, 182, 193),
            price=49.99,
            season=Season.SPRING,
            occasion=[Occasion.EVERYDAY, Occasion.DATE, Occasion.PARTY],
            brand="Boho Chic"
        ),
        Product(
            id="top_005",
            name="Gray Hoodie",
            category=Category.TOP,
            style=Style.CASUAL,
            color=Color(128, 128, 128),
            price=59.99,
            season=Season.FALL,
            occasion=[Occasion.EVERYDAY, Occasion.SPORTS, Occasion.TRAVEL],
            brand="Comfort Wear"
        ),
        Product(
            id="top_006",
            name="White Button-Down Shirt",
            category=Category.TOP,
            style=Style.BUSINESS,
            color=Color(250, 250, 250),
            price=79.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT],
            brand="Professional"
        ),
        Product(
            id="top_007",
            name="Red Sweater",
            category=Category.TOP,
            style=Style.CASUAL,
            color=Color(220, 20, 60),
            price=69.99,
            season=Season.WINTER,
            occasion=[Occasion.EVERYDAY, Occasion.DATE],
            brand="Cozy Wear"
        ),
        Product(
            id="top_008",
            name="Denim Jacket",
            category=Category.TOP,
            style=Style.CASUAL,
            color=Color(59, 89, 152),
            price=89.99,
            season=Season.SPRING,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Classic Denim"
        ),
        
        # BOTTOMS
        Product(
            id="bottom_001",
            name="Dark Blue Jeans",
            category=Category.BOTTOM,
            style=Style.CASUAL,
            color=Color(25, 25, 112),
            price=79.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.DATE, Occasion.TRAVEL],
            brand="Denim Co"
        ),
        Product(
            id="bottom_002",
            name="Black Dress Pants",
            category=Category.BOTTOM,
            style=Style.FORMAL,
            color=Color(0, 0, 0),
            price=129.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT],
            brand="Formal Wear"
        ),
        Product(
            id="bottom_003",
            name="Khaki Chinos",
            category=Category.BOTTOM,
            style=Style.CASUAL,
            color=Color(240, 230, 140),
            price=69.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.WORK, Occasion.TRAVEL],
            brand="Casual Co"
        ),
        Product(
            id="bottom_004",
            name="Gray Sweatpants",
            category=Category.BOTTOM,
            style=Style.SPORTY,
            color=Color(105, 105, 105),
            price=49.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.SPORTS, Occasion.EVERYDAY],
            brand="Athletic"
        ),
        Product(
            id="bottom_005",
            name="White Linen Pants",
            category=Category.BOTTOM,
            style=Style.BOHEMIAN,
            color=Color(255, 255, 255),
            price=89.99,
            season=Season.SUMMER,
            occasion=[Occasion.EVERYDAY, Occasion.DATE, Occasion.PARTY],
            brand="Summer Style"
        ),
        Product(
            id="bottom_006",
            name="Navy Blue Trousers",
            category=Category.BOTTOM,
            style=Style.BUSINESS,
            color=Color(0, 0, 128),
            price=99.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT],
            brand="Professional"
        ),
        Product(
            id="bottom_007",
            name="Black Leather Pants",
            category=Category.BOTTOM,
            style=Style.STREETWEAR,
            color=Color(20, 20, 20),
            price=199.99,
            season=Season.FALL,
            occasion=[Occasion.PARTY, Occasion.DATE],
            brand="Urban Edge"
        ),
        Product(
            id="bottom_008",
            name="Beige Cargo Pants",
            category=Category.BOTTOM,
            style=Style.CASUAL,
            color=Color(245, 245, 220),
            price=79.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Adventure"
        ),
        
        # FOOTWEAR
        Product(
            id="footwear_001",
            name="White Sneakers",
            category=Category.FOOTWEAR,
            style=Style.CASUAL,
            color=Color(255, 255, 255),
            price=99.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.SPORTS, Occasion.TRAVEL],
            brand="Sport Co"
        ),
        Product(
            id="footwear_002",
            name="Black Oxford Shoes",
            category=Category.FOOTWEAR,
            style=Style.FORMAL,
            color=Color(0, 0, 0),
            price=199.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT],
            brand="Formal Wear"
        ),
        Product(
            id="footwear_003",
            name="Brown Leather Boots",
            category=Category.FOOTWEAR,
            style=Style.CASUAL,
            color=Color(139, 69, 19),
            price=249.99,
            season=Season.FALL,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Outdoor Co"
        ),
        Product(
            id="footwear_004",
            name="Black Ankle Boots",
            category=Category.FOOTWEAR,
            style=Style.STREETWEAR,
            color=Color(20, 20, 20),
            price=179.99,
            season=Season.FALL,
            occasion=[Occasion.EVERYDAY, Occasion.PARTY, Occasion.DATE],
            brand="Urban Edge"
        ),
        Product(
            id="footwear_005",
            name="Tan Loafers",
            category=Category.FOOTWEAR,
            style=Style.BUSINESS,
            color=Color(210, 180, 140),
            price=149.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.EVERYDAY],
            brand="Professional"
        ),
        Product(
            id="footwear_006",
            name="Red High-Tops",
            category=Category.FOOTWEAR,
            style=Style.SPORTY,
            color=Color(220, 20, 60),
            price=119.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.SPORTS, Occasion.EVERYDAY],
            brand="Athletic"
        ),
        Product(
            id="footwear_007",
            name="Navy Blue Boat Shoes",
            category=Category.FOOTWEAR,
            style=Style.CASUAL,
            color=Color(0, 32, 96),
            price=89.99,
            season=Season.SUMMER,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Summer Style"
        ),
        Product(
            id="footwear_008",
            name="Gray Running Shoes",
            category=Category.FOOTWEAR,
            style=Style.SPORTY,
            color=Color(128, 128, 128),
            price=129.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.SPORTS, Occasion.EVERYDAY],
            brand="Athletic"
        ),
        
        # ACCESSORIES
        Product(
            id="acc_001",
            name="Black Leather Belt",
            category=Category.ACCESSORY,
            style=Style.FORMAL,
            color=Color(0, 0, 0),
            price=49.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT, Occasion.EVERYDAY],
            brand="Accessories Co"
        ),
        Product(
            id="acc_002",
            name="Silver Watch",
            category=Category.ACCESSORY,
            style=Style.FORMAL,
            color=Color(192, 192, 192),
            price=299.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.WORK, Occasion.FORMAL_EVENT, Occasion.DATE],
            brand="Timepieces"
        ),
        Product(
            id="acc_003",
            name="Brown Leather Wallet",
            category=Category.ACCESSORY,
            style=Style.CASUAL,
            color=Color(139, 69, 19),
            price=79.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.WORK],
            brand="Leather Goods"
        ),
        Product(
            id="acc_004",
            name="Black Sunglasses",
            category=Category.ACCESSORY,
            style=Style.CASUAL,
            color=Color(20, 20, 20),
            price=89.99,
            season=Season.SUMMER,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Sun Protection"
        ),
        Product(
            id="acc_005",
            name="Navy Blue Scarf",
            category=Category.ACCESSORY,
            style=Style.CASUAL,
            color=Color(0, 32, 96),
            price=39.99,
            season=Season.WINTER,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL],
            brand="Winter Co"
        ),
        Product(
            id="acc_006",
            name="Gold Chain Necklace",
            category=Category.ACCESSORY,
            style=Style.STREETWEAR,
            color=Color(255, 215, 0),
            price=149.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.PARTY, Occasion.DATE],
            brand="Jewelry Co"
        ),
        Product(
            id="acc_007",
            name="Beige Canvas Hat",
            category=Category.ACCESSORY,
            style=Style.CASUAL,
            color=Color(245, 245, 220),
            price=29.99,
            season=Season.SUMMER,
            occasion=[Occasion.EVERYDAY, Occasion.TRAVEL, Occasion.SPORTS],
            brand="Outdoor Co"
        ),
        Product(
            id="acc_008",
            name="Red Baseball Cap",
            category=Category.ACCESSORY,
            style=Style.SPORTY,
            color=Color(220, 20, 60),
            price=24.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.SPORTS, Occasion.EVERYDAY],
            brand="Athletic"
        ),
        Product(
            id="acc_009",
            name="Black Backpack",
            category=Category.ACCESSORY,
            style=Style.CASUAL,
            color=Color(0, 0, 0),
            price=79.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.EVERYDAY, Occasion.WORK, Occasion.TRAVEL],
            brand="Travel Co"
        ),
        Product(
            id="acc_010",
            name="White Pearl Earrings",
            category=Category.ACCESSORY,
            style=Style.FORMAL,
            color=Color(255, 255, 255),
            price=199.99,
            season=Season.ALL_SEASON,
            occasion=[Occasion.FORMAL_EVENT, Occasion.DATE],
            brand="Jewelry Co"
        ),
    ]
    
    return products

