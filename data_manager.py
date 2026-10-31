import json
import os

from product import Product


class DataManager:

    def __init__(self):
        self.data_folder = "data"

        os.makedirs(self.data_folder, exist_ok=True)

        self.products_file = os.path.join(
            self.data_folder, "products.json"
        )

        self.sales_file = os.path.join(
            self.data_folder, "sales.json"
        )

        self.initialize_files()

    def initialize_files(self):
        for file_path in [
            self.products_file,
            self.sales_file
        ]:
            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    json.dump([], file)

    def load_products(self):
        with open(self.products_file, "r") as file:
            data = json.load(file)

        return [
            Product.from_dict(item)
            for item in data
        ]

    def save_products(self, inventory):
        with open(self.products_file, "w") as file:
            json.dump(
                inventory.to_list(),
                file,
                indent=4
            )

    def load_sales(self):
        with open(self.sales_file, "r") as file:
            return json.load(file)

    def save_sale(self, transaction):
        sales = self.load_sales()

        sales.append(transaction.to_dict())

        with open(self.sales_file, "w") as file:
            json.dump(sales, file, indent=4)