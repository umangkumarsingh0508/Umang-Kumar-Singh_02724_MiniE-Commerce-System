import os

FILE_NAME = "products.txt"

products = {}
cart = {}

# Load products from file
def load_products():
    global products
    products = {}

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) == 4:
                    pid, name, price, stock = data
                    products[pid] = {
                        "name": name,
                        "price": float(price),
                        "stock": int(stock)
                    }

# Save products to file
def save_products():
    with open(FILE_NAME, "w") as file:
        for pid, p in products.items():
            file.write(
                f"{pid},{p['name']},{p['price']},{p['stock']}\n"
            )

# Generate product ID
def generate_id():
    if not products:
        return "P101"

    numbers = [
        int(pid[1:]) for pid in products
        if pid.startswith("P") and pid[1:].isdigit()
    ]

    return "P" + str(max(numbers, default=100) + 1)

# Add product
def add_product(name, price, stock):
    if price <= 0:
        print("Invalid price. Price must be a positive number.")
        return

    if stock < 0:
        print("Invalid stock.")
        return

    pid = generate_id()

    products[pid] = {
        "name": name,
        "price": price,
        "stock": stock
    }

    save_products()

    print(
        f"Product added. ID:{pid} | {name} | "
        f"Price:{price:g} | Stock:{stock}"
    )

    if stock == 0:
        print(f"Warning: {name} is out of stock.")

# Update product
def update_product(pid, name, price, stock):
    if pid not in products:
        print(f"Product {pid} not found.")
        return

    if price <= 0 or stock < 0:
        print("Invalid product details.")
        return

    products[pid] = {
        "name": name,
        "price": price,
        "stock": stock
    }

    save_products()
    print("Product updated successfully.")

# View products
def view_products():
    if not products:
        print("No products available.")
        return

    for pid, p in products.items():
        print(
            f"ID:{pid} | {p['name']} | "
            f"Price:{p['price']:g} | Stock:{p['stock']}"
        )

# Delete product
def delete_product(pid):
    if pid not in products:
        print(f"Product {pid} not found.")
        return

    name = products[pid]["name"]
    del products[pid]

    cart.pop(pid, None)

    save_products()

    print(f"Product {name} deleted. Products left:{len(products)}")

# Add product to cart
def add_to_cart(pid, quantity):
    if pid not in products:
        print(f"Product {pid} not found.")
        return

    if quantity <= 0:
        print("Invalid quantity.")
        return

    p = products[pid]

    if quantity > p["stock"]:
        print("Not enough stock available.")
        return

    cart[pid] = cart.get(pid, 0) + quantity

    amount = p["price"] * quantity

    print(
        f"{p['name']} x{quantity} added | "
        f"Amount: {amount:g}"
    )

# Checkout
def checkout():
    if not cart:
        print("Cart is empty.")
        return

    total = 0

    for pid, quantity in cart.items():
        if pid not in products:
            continue

        p = products[pid]

        if quantity > p["stock"]:
            print("Insufficient stock.")
            return

        total += p["price"] * quantity

    print(f"Order total:{total:g}")

    for pid, quantity in cart.items():
        if pid in products:
            products[pid]["stock"] -= quantity
            print(
                f"{products[pid]['name']} stock left:"
                f"{products[pid]['stock']}"
            )

    cart.clear()
    save_products()

# Main menu
def main():
    load_products()

    while True:
        print("\n----- MINI E-COMMERCE SYSTEM -----")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Add to Cart")
        print("6. Checkout")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                name = input("Enter product name: ")
                price = float(input("Enter price: "))
                stock = int(input("Enter stock: "))
                add_product(name, price, stock)

            elif choice == 2:
                pid = input("Enter product ID: ")
                name = input("Enter new name: ")
                price = float(input("Enter new price: "))
                stock = int(input("Enter new stock: "))
                update_product(pid, name, price, stock)

            elif choice == 3:
                pid = input("Enter product ID: ")
                delete_product(pid)

            elif choice == 4:
                view_products()

            elif choice == 5:
                pid = input("Enter product ID: ")
                quantity = int(input("Enter quantity: "))
                add_to_cart(pid, quantity)

            elif choice == 6:
                checkout()

            elif choice == 7:
                save_products()
                print("Thank you for shopping!")
                break

            else:
                print("Invalid menu option.")

        except ValueError:
            print("Invalid input. Please enter valid values.")

if __name__ == "__main__":
    main()
