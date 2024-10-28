from sqlalchemy.orm import Session
from mymodels import User, Product, Order, OrderItem  # Assuming these models are defined as you provided

# Assuming we already have a session
session = Session()

# Step 1: Create a User
new_user = User(email="user@example.com", hashed_password="hashedpassword123")
session.add(new_user)
session.commit()  # Saving the user to the database

# Step 2: Create Products
product1 = Product(name="Laptop", description="15-inch laptop", price=1200.00, image_url="http://image1.jpg", category="Electronics")
product2 = Product(name="Headphones", description="Noise-canceling", price=200.00, image_url="http://image2.jpg", category="Electronics")
session.add_all([product1, product2])
session.commit()  # Save the products

# Step 3: Create an Order
order = Order(total_price=1400.00, address="123 Main St", status="Processing")
session.add(order)
session.commit()

# Step 4: Add OrderItems to the Order
order_item1 = OrderItem(order_id=order.id, product_id=product1.id, quantity=1)  # 1 Laptop
order_item2 = OrderItem(order_id=order.id, product_id=product2.id, quantity=2)  # 2 Headphones

# Link OrderItems to the Order
order.items.extend([order_item1, order_item2])

# Save OrderItems
session.add_all([order_item1, order_item2])
session.commit()

print(f"Order {order.id} has {len(order.items)} items")
