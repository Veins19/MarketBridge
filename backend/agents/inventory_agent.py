def inventory_agent(product, inventory_data):
    for item in inventory_data:
        if item["product"] == product and item["stock"] > 0:
            return f"Inventory Agent: Stock available for {product} in {item['region']} region."
    return f"Inventory Agent: Stock unavailable for {product}."
