class CartItem:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def total(self):
        return round(self.product.price * self.quantity, 2)


class ShoppingCart:

    def __init__(self, inventory):
        self.inventory = inventory
        self.items = {}

    def add_item(self, code, quantity):
        product = self.inventory.get_product(code)

        if not product:
            print("Product not found.")
            return False

        if quantity <= 0:
            print("Quantity must be positive.")
            return False

        current_quantity = (
            self.items[code].quantity
            if code in self.items else 0
        )

        if current_quantity + quantity > product.stock:
            print(f"Not enough stock! Available: {product.stock - current_quantity}")
            return False

        if code in self.items:
            self.items[code].quantity += quantity
        else:
            self.items[code] = CartItem(product, quantity)

        print(f"{quantity} x {product.name} added to cart.")
        return True

    def remove_item(self, code):
        if code not in self.items:
            print("Item not found in cart.")
            return False

        del self.items[code]
        print("Item removed from cart.")
        return True

    def update_quantity(self, code, quantity):
        if code not in self.items:
            print("Item not found.")
            return False

        if quantity <= 0:
            return self.remove_item(code)

        product = self.items[code].product

        if quantity > product.stock:
            print("Not enough stock.")
            return False

        self.items[code].quantity = quantity
        print("Quantity updated.")
        return True

    def calculate_subtotal(self):
        return round(
            sum(item.total for item in self.items.values()),
            2
        )

    def show_cart(self):
        if not self.items:
            print("\nYour cart is empty.")
            return

        print("\n============== SHOPPING CART ==============")
        print(f"{'Product':<15}{'Qty':<8}{'Price':<10}{'Total'}")
        print("-" * 50)

        for item in self.items.values():
            print(
                f"{item.product.name:<15}"
                f"{item.quantity:<8}"
                f"${item.product.price:<9.2f}"
                f"${item.total:.2f}"
            )

        print("-" * 50)
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")

    def clear(self):
        self.items.clear()

    def is_empty(self):
        return len(self.items) == 0

    def get_receipt_items(self):
        return [
            {
                "code": item.product.code,
                "name": item.product.name,
                "price": item.product.price,
                "quantity": item.quantity,
                "total": item.total
            }
            for item in self.items.values()
        ]