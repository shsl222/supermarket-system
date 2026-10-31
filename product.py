class Product:
    def __init__(self, code, name, price, stock):
        self.code = code
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def update_price(self, new_price):
        if new_price <= 0:
            raise ValueError("Price must be positive.")

        self.price = float(new_price)

    def update_stock(self, quantity):
        if self.stock + quantity < 0:
            raise ValueError("Insufficient stock.")

        self.stock += quantity

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["code"],
            data["name"],
            data["price"],
            data["stock"]
        )

    def __str__(self):
        return (
            f"{self.code:<8}"
            f"{self.name:<15}"
            f"${self.price:<12.2f}"
            f"{self.stock}"
        )