"""Curated starter stock for a small Indian neighbourhood store.

Each product is deliberately named as a real shelf label rather than a random
brand/size combination. Prices are demo prices in INR and can be edited in the
Inventory screen after seeding.
"""

from __future__ import annotations


CURATED_CATALOG = [
    ("Grocery & Staples", "India Gate Basmati Rice 5 kg", 690, 36), ("Grocery & Staples", "Aashirvaad Whole Wheat Atta 5 kg", 295, 42), ("Grocery & Staples", "Fortune Sunflower Oil 1 L", 158, 48), ("Grocery & Staples", "Tata Salt 1 kg", 30, 64), ("Grocery & Staples", "Tata Sampann Toor Dal 1 kg", 186, 34),
    ("Dairy, Milk & Paneer", "Amul Taaza Toned Milk 1 L", 58, 45), ("Dairy, Milk & Paneer", "Mother Dairy Classic Dahi 400 g", 48, 28), ("Dairy, Milk & Paneer", "Amul Butter 500 g", 285, 23), ("Dairy, Milk & Paneer", "Amul Fresh Paneer 200 g", 95, 20), ("Dairy, Milk & Paneer", "Amul Cheese Slices 200 g", 148, 17),
    ("Fresh Vegetables & Greens", "Farm Fresh Potato 1 kg", 35, 55), ("Fresh Vegetables & Greens", "Farm Fresh Onion 1 kg", 42, 50), ("Fresh Vegetables & Greens", "Farm Fresh Tomato 500 g", 28, 38), ("Fresh Vegetables & Greens", "Fresh Spinach Bunch", 25, 26), ("Fresh Vegetables & Greens", "Button Mushroom 200 g", 68, 18),
    ("Fresh Fruits & Berries", "Royal Gala Apple 1 kg", 220, 30), ("Fresh Fruits & Berries", "Robusta Banana 1 kg", 55, 38), ("Fresh Fruits & Berries", "Nagpur Orange 1 kg", 95, 27), ("Fresh Fruits & Berries", "Pomegranate 1 kg", 180, 19), ("Fresh Fruits & Berries", "Green Kiwi Pack of 3", 125, 14),
    ("Bakery & Breakfast", "Britannia Brown Bread 400 g", 52, 29), ("Bakery & Breakfast", "Kellogg's Corn Flakes 475 g", 205, 18), ("Bakery & Breakfast", "Quaker Oats 1 kg", 210, 21), ("Bakery & Breakfast", "Pintola Peanut Butter 510 g", 315, 16), ("Bakery & Breakfast", "Kissan Mixed Fruit Jam 500 g", 165, 20),
    ("Snacks, Chips & Namkeen", "Lay's Classic Salted Chips 52 g", 20, 52), ("Snacks, Chips & Namkeen", "Haldiram's Aloo Bhujia 200 g", 68, 25), ("Snacks, Chips & Namkeen", "Bikaji All in One 200 g", 72, 23), ("Snacks, Chips & Namkeen", "Act II Butter Popcorn 40 g", 30, 36), ("Snacks, Chips & Namkeen", "Farmley Roasted Makhana 100 g", 145, 15),
    ("Chocolates, Sweets & Biscuits", "Cadbury Dairy Milk Silk 60 g", 95, 24), ("Chocolates, Sweets & Biscuits", "Nestle KitKat 4 Finger 37 g", 35, 34), ("Chocolates, Sweets & Biscuits", "Parle-G Gold Biscuits 1 kg", 120, 22), ("Chocolates, Sweets & Biscuits", "Britannia NutriChoice Digestive 400 g", 95, 18), ("Chocolates, Sweets & Biscuits", "Haldiram's Soan Papdi 500 g", 180, 12),
    ("Tea, Coffee & Beverages", "Tata Tea Premium 1 kg", 560, 20), ("Tea, Coffee & Beverages", "Nescafe Classic Coffee 100 g", 385, 14), ("Tea, Coffee & Beverages", "Bisleri Mineral Water 1 L", 20, 60), ("Tea, Coffee & Beverages", "Real Mixed Fruit Juice 1 L", 125, 25), ("Tea, Coffee & Beverages", "Thums Up 750 ml", 45, 32),
    ("Personal Care & Grooming", "Dove Cream Beauty Bar Pack of 3", 185, 19), ("Personal Care & Grooming", "Head & Shoulders Shampoo 340 ml", 285, 18), ("Personal Care & Grooming", "Colgate Strong Teeth 200 g", 110, 23), ("Personal Care & Grooming", "Parachute Coconut Oil 300 ml", 145, 21), ("Personal Care & Grooming", "Nivea Men Face Wash 100 ml", 180, 14),
    ("Health, Wellness & Supplements", "Horlicks Classic Malt 500 g", 285, 16), ("Health, Wellness & Supplements", "Bournvita Chocolate 500 g", 275, 18), ("Health, Wellness & Supplements", "Ensure Vanilla Nutrition 400 g", 720, 10), ("Health, Wellness & Supplements", "Dabur Chyawanprash 500 g", 195, 14), ("Health, Wellness & Supplements", "Organic India Tulsi Tea 25 Bags", 165, 12),
    ("All Medicines & First Aid", "Dettol Antiseptic Liquid 500 ml", 160, 16), ("All Medicines & First Aid", "Band-Aid Washproof Strips Pack", 80, 20), ("All Medicines & First Aid", "Dr. Morepen Digital Thermometer", 250, 11), ("All Medicines & First Aid", "Electral ORS Sachet 21.8 g", 22, 34), ("All Medicines & First Aid", "Savlon Hand Sanitizer 200 ml", 72, 20),
    ("Household & Cleaning", "Surf Excel Easy Wash 1 kg", 150, 28), ("Household & Cleaning", "Vim Dishwash Bar Pack of 3", 45, 32), ("Household & Cleaning", "Lizol Citrus Floor Cleaner 975 ml", 180, 18), ("Household & Cleaning", "Harpic Toilet Cleaner 1 L", 165, 16), ("Household & Cleaning", "Scotch-Brite Scrub Pad Pack of 3", 55, 23),
    ("Home & Kitchenware", "Milton Thermosteel Bottle 750 ml", 720, 10), ("Home & Kitchenware", "Prestige Non Stick Fry Pan 24 cm", 850, 8), ("Home & Kitchenware", "Pigeon Pressure Cooker 3 L", 1450, 6), ("Home & Kitchenware", "Borosil Glass Bowl Set", 620, 9), ("Home & Kitchenware", "Cello Lunch Box Set", 470, 12),
    ("Stationery & Office Supplies", "Classmate Notebook 172 Pages", 75, 30), ("Stationery & Office Supplies", "Cello Butterflow Pen Pack of 5", 65, 28), ("Stationery & Office Supplies", "Apsara Platinum Pencil Pack", 55, 30), ("Stationery & Office Supplies", "Fevicol MR 100 g", 45, 20), ("Stationery & Office Supplies", "Kangaro Stapler with Pins", 120, 15),
    ("Clothing & Fashion", "Jockey Men's Cotton Socks Pack of 3", 280, 14), ("Clothing & Fashion", "Rupa Women's Leggings Black", 340, 12), ("Clothing & Fashion", "Dollar Kids Cotton T-Shirt", 250, 13), ("Clothing & Fashion", "Rain & Rainbow Cotton Handkerchiefs", 110, 16), ("Clothing & Fashion", "Wildcraft Reusable Face Mask", 160, 10),
    ("Girls Accessories & Makeup", "Lakme Kajal 2.2 g", 190, 15), ("Girls Accessories & Makeup", "Maybelline Baby Lips Balm", 175, 14), ("Girls Accessories & Makeup", "Nivea Soft Cream 100 ml", 165, 18), ("Girls Accessories & Makeup", "Vega Hair Brush", 220, 12), ("Girls Accessories & Makeup", "Claw Clip Set of 3", 95, 20),
    ("Tech & Mobile Accessories", "boAt Bassheads Earphones", 599, 13), ("Tech & Mobile Accessories", "Ambrane 20 W USB-C Charger", 899, 9), ("Tech & Mobile Accessories", "SanDisk Ultra 64 GB Memory Card", 540, 12), ("Tech & Mobile Accessories", "Portronics USB-A Cable 1 m", 180, 18), ("Tech & Mobile Accessories", "Philips LED Bulb 9 W", 120, 24),
    ("Seasonal, Pooja & Festival", "Cycle Three in One Agarbatti", 75, 20), ("Seasonal, Pooja & Festival", "Phool Incense Cones", 120, 16), ("Seasonal, Pooja & Festival", "Brass Diya Set of 2", 280, 10), ("Seasonal, Pooja & Festival", "LED String Lights 10 m", 350, 12), ("Seasonal, Pooja & Festival", "Rangoli Colour Pack", 90, 18),
    ("Ready to Eat", "MTR Ready to Eat Dal Makhani 300 g", 110, 17), ("Ready to Eat", "Maggi 2-Minute Noodles Pack of 12", 170, 22), ("Ready to Eat", "iD Fresh Idli Dosa Batter 1 kg", 95, 15), ("Ready to Eat", "McCain French Fries 750 g", 195, 16), ("Ready to Eat", "Kissan Tomato Ketchup 950 g", 145, 20),
    ("Sports & Fitness", "Nivia Storm Football Size 5", 650, 8), ("Sports & Fitness", "Yonex Badminton Racquet Pair", 1280, 6), ("Sports & Fitness", "Boldfit Yoga Mat 6 mm", 650, 10), ("Sports & Fitness", "Strauss Skipping Rope", 240, 14), ("Sports & Fitness", "SG Kashmir Willow Cricket Bat", 1650, 5),
]


def starter_products() -> list[tuple[str, str, float, int]]:
    """Return seed rows in the inventory table column order."""
    return [(name, category, price, stock) for category, name, price, stock in CURATED_CATALOG]


def validate_catalog(rows=CURATED_CATALOG) -> list[str]:
    """Return readable catalog problems so a bad seed cannot silently ship."""
    issues, names = [], set()
    for category, name, price, stock in rows:
        if not category or not name:
            issues.append("Every product needs a category and name.")
        if name in names:
            issues.append(f"Duplicate product name: {name}")
        names.add(name)
        if price <= 0:
            issues.append(f"Product price must be positive: {name}")
        if stock < 0:
            issues.append(f"Product stock cannot be negative: {name}")
    return issues
