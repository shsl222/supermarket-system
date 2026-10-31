from product import Product


class Inventory:

    def __init__(self, products=None):
        self.products = {
            product.code: product
            for product in (products or [])
        }

    def add_product(self, product):
        if product.code in self.products:
            print("Product already exists.")
            return False

        self.products[product.code] = product
        print("Product added successfully!")
        return True

    def remove_product(self, code):
        if code not in self.products:
            print("Product not found.")
            return False

        del self.products[code]
        print("Product removed successfully!")
        return True

    def get_product(self, code):
        return self.products.get(code)

    def search_product(self, keyword):
        keyword = keyword.lower()

        return [
            product for product in self.products.values()
            if keyword in product.name.lower()
            or keyword in product.code.lower()
        ]

    def show_products(self):
        print("\n========== INVENTORY ==========")
        print(f"{'Code':<8}{'Name':<15}{'Price':<12}{'Stock'}")
        print("-" * 45)

        for product in self.products.values():
            print(product)

        print("-" * 45)

    def update_stock(self, code, quantity):
        product = self.get_product(code)

        if not product:
            print("Product not found.")
            return False

        try:
            product.update_stock(quantity)
            print("Stock updated successfully!")
            return True
        except ValueError as error:
            print(error)
            return False

    def to_list(self):
        return [
            product.to_dict()
            for product in self.products.values()
        ]