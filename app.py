import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Silk Road Trade Optimizer", layout="wide")

# Map of cities based on the sequence in the PDF, now including Pelpolis for accurate distance!
cities_sequence = ["Tyre", "Antioch", "Damascus", "Palmyra", "Ctesiphon", "Ecbatana", "Susa", "Pelpolis", "Isfahan"]

# Define categories for bonus matching
item_categories = {
    "Olive Oil": "Food", "Dried Fish": "Food", "Sea Salt": "Food", "Wheat": "Food", "Barley": "Food", "Sesame": "Food", "Coriander": "Food",
    "Books": "Luxury", "Glassware": "Luxury", "Persian Carpets": "Luxury", "Minanakari Ware": "Luxury", "Saffron": "Luxury",
    "Tools": "Tools", "Weapons": "Weapons", "Weapon": "Weapons",
    "Linen": "Textile", "Wool": "Textile", "Wools": "Textile", "Cotton Yarn": "Textile", "Leather": "Textile", "Leathers": "Textile", "Hides": "Textile"
}

# Trade Data Dictionary built from your PDF
trade_data = {
    "Tyre": {
        "culture": "Greek", "hasGlobalBonus": True, "foreignBonus": False, "foreignPenalty": False, "bonusCategories": [],
        "local": {"Olive Oil": 58, "Dried Fish": 21, "Sea Salt": 66, "Clay": 9, "Glassware": 164, "Linen": 9},
        "imports": {"Wheat": 24, "Barley": 24, "Copper Ingot": 37, "Iron Ingot": 49, "Sesame": 91, "Coriander": 118, "Saffron": 272, "Books": 430, "Earthenware": 23, "Paper": 49, "Tools": 91, "Weapons": 118, "Wool": 14, "Hides": 23, "Cotton Yarn": 31, "Leather": 20}
    },
    "Antioch": {
        "culture": "Greek", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": False, "bonusCategories": ["Luxury", "Tools"],
        "local": {"Books": 335, "Wools": 7, "Hides": 14, "Weapon": 98, "Copper Ingot": 32, "Iron Ingot": 41, "Linen": 12, "Cotton Yarn": 28, "Leathers": 18},
        "imports": {"Earthenware": 20, "Clay": 12, "Glassware": 148, "Paper": 41, "Wheat": 18, "Barley": 18, "Olive Oil": 41, "Dried Fish": 20, "Tools": 76}
    },
    "Damascus": {
        "culture": "Greek", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": False, "bonusCategories": ["Food"],
        "local": {"Earthenware": 18, "Paper": 44, "Copper Ingot": 31, "Iron Ingot": 44, "Tools": 87, "Weapons": 114, "Sesame": 87},
        "imports": {"Books": 455, "Clay": 14, "Glassware": 188, "Wheat": 14, "Barley": 14, "Olive Oil": 51, "Dried Fish": 24, "Sea Salt": 78, "Coriander": 124, "Saffron": 266}
    },
    "Palmyra": {
        "culture": "Greek", "hasGlobalBonus": False, "foreignBonus": True, "foreignPenalty": False, "bonusCategories": ["Tools", "Weapons"],
        "local": {"Wool": 7, "Linen": 7, "Cotton Yarn": 14, "Leather": 7, "Wheat": 7, "Barley": 7},
        "imports": {"Sea Salt": 71, "Sesame": 76, "Coriander": 98, "Saffron": 199, "Tools": 66, "Weapons": 85, "Copper Ingot": 32, "Books": 376}
    },
    "Ctesiphon": {
        "culture": "Persian", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": False, "bonusCategories": ["Luxury"],
        "local": {"Tools": 87, "Sesame": 87, "Coriander": 114, "Earthenware": 18, "Glassware": 174, "Paper": 44, "Cotton Yarn": 18, "Wheat": 9, "Olive Oil": 44},
        "imports": {"Weapon": 142, "Sea Salt": 96, "Saffron": 233, "Books": 476, "Clay": 20, "Wool": 14, "Linen": 14, "Hides": 24, "Leather": 14, "Barley": 14, "Dried Fish": 42}
    },
    "Ecbatana": {
        "culture": "Persian", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": True, "bonusCategories": [],
        "local": {"Weapon": 134, "Wool": 11, "Hides": 21, "Leather": 11, "Linen": 16, "Cotton Yarn": 27, "Barley": 11, "Saffron": 256, "Sea Salt": 108, "Sesame": 111, "Coriander": 144, "Copper ingot": 36},
        "imports": {"Tools": 111, "Books": 530, "Earthenware": 27, "Clay": 16, "Glassware": 218, "Paper": 59, "Wheat": 16, "Olive Oil": 59, "Dried Fish": 45, "Iron ingot": 59}
    },
    "Susa": {
        "culture": "Persian", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": True, "bonusCategories": ["Textile"],
        "local": {"Sesame": 102, "Saffron": 256, "Books": 510, "Clay": 11, "Wool": 10, "Linen": 10},
        "imports": {"Sea Salt": 99, "Coriander": 156, "Earthenware": 35, "Glassware": 233, "Paper": 68, "Tools": 121, "Weapons": 144, "Wheat": 22, "Barley": 16, "Olive Oil": 68, "Dried Fish": 35, "Hides": 25, "Cotton Yarn": 33, "Leather": 15, "Copper Ingot": 43, "Iron Ingot": 68}
    },
    "Pelpolis": {
        "culture": "Persian", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": False, "bonusCategories": [],
        "local": {}, # Goods are no longer traded here
        "imports": {} # Goods are no longer traded here
    },
    "Isfahan": {
        "culture": "Persian", "hasGlobalBonus": False, "foreignBonus": False, "foreignPenalty": True, "bonusCategories": ["Tools", "Textile"],
        "local": {"Minanakari Ware": 306, "Glassware": 204, "Paper": 52, "Tools": 102, "Olive Oil": 52, "Coriander": 134},
        "imports": {"Books": 551, "Earthenware": 58, "Clay": 22, "Wool": 21, "Linen": 21, "Hides": 43, "Cotton Yarn": 56, "Leather": 30, "Copper Ingot": 61, "Iron Ingot": 89, "Weapons": 168, "Wheat": 45, "Barley": 31, "Dried Fish": 58, "Sea Salt": 119, "Sesame": 121, "Saffron": 287}
    }
}

# --- UI Header ---
st.title("🐪 Silk Road Trade Optimizer")
st.markdown("Calculate the best routes, nearest drops, and optimal profit margins based on the game's actual math.")

# --- Setup Selection UI ---
col1, col2, col3 = st.columns(3)
with col1:
    current_city = st.selectbox("Your Current Location:", cities_sequence)
with col2:
    player_culture = st.selectbox("Your Character Culture:", ["Greek", "Persian"])
with col3:
    sort_option = st.selectbox("Sort Routes By:", ["Highest Base Profit", "Nearest Distance", "Bonuses First"])

st.divider()

if current_city == "Pelpolis":
    st.warning("Goods are no longer traded in Pelpolis. Please select another city to begin trading.")
else:
    st.subheader(f"Best export options from {current_city}")

    # --- Route Calculation Logic ---
    current_city_data = trade_data[current_city]
    source_index = cities_sequence.index(current_city)

    valid_routes = []

    for product, buy_price in current_city_data["local"].items():
        category = item_categories.get(product, "General")
        
        for target_city, target_data in trade_data.items():
            # Skip checking the city you are currently in, and skip Pelpolis as a destination
            if target_city == current_city or target_city == "Pelpolis":
                continue
                
            if product in target_data["imports"]:
                sell_price = target_data["imports"][product]
                base_profit = sell_price - buy_price
                target_index = cities_sequence.index(target_city)
                distance = abs(source_index - target_index)
                
                # Flags
                bonuses = []
                penalties = []
                has_bonus = False
                
                if category in target_data["bonusCategories"]:
                    bonuses.append(f"🌟 Category Bonus ({category})")
                    has_bonus = True
                if target_data["hasGlobalBonus"]:
                    bonuses.append("🌟 Global City Bonus (+5%)")
                    has_bonus = True
                    
                is_foreign = current_city_data["culture"] != target_data["culture"]
                if is_foreign and target_data["foreignBonus"]:
                    bonuses.append("🌟 Foreign Trader Bonus (+10%)")
                    has_bonus = True
                if is_foreign and target_data["foreignPenalty"]:
                    penalties.append("❌ Foreign Penalty (-10%)")
                    
                valid_routes.append({
                    "product": product, "category": category, "destination": target_city,
                    "buy_price": buy_price, "sell_price": sell_price, "base_profit": base_profit,
                    "distance": distance, "bonuses": bonuses, "penalties": penalties, "has_bonus": has_bonus
                })

    # --- Sorting Logic ---
    if sort_option == "Highest Base Profit":
        valid_routes.sort(key=lambda x: x["base_profit"], reverse=True)
    elif sort_option == "Nearest Distance":
        valid_routes.sort(key=lambda x: (x["distance"], -x["base_profit"]))
    elif sort_option == "Bonuses First":
        valid_routes.sort(key=lambda x: (not x["has_bonus"], -x["base_profit"]))

    # --- Rendering the Output ---
    if not valid_routes:
        st.info("No profitable export routes found from this city.")
    else:
        for route in valid_routes:
            with st.container(border=True):
                r_col1, r_col2, r_col3 = st.columns([3, 2, 2])
                
                with r_col1:
                    st.markdown(f"### 📦 {route['product']}")
                    st.caption(f"Category: {route['category']}")
                    
                    if route['distance'] == 1:
                        st.markdown("`⚠️ Nearest Neighbor`")
                        
                    for b in route['bonuses']:
                        st.markdown(f"`{b}`")
                    for p in route['penalties']:
                        st.markdown(f"`{p}`")
                        
                with r_col2:
                    st.markdown(f"**➡️ Destination:** {route['destination']}")
                    st.caption(f"Distance: {route['distance']} stops")
                    st.markdown(f"**Buy:** ${route['buy_price']} | **Sell:** ${route['sell_price']}")
                    
                with r_col3:
                    st.metric("Base Profit / Item", f"+${route['base_profit']}")
