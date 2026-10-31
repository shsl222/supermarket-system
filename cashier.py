from cart import ShoppingCart
from transaction import Transaction


class CashierSystem:

    def __init__(self, inventory, data_manager):
        self.inventory = inventory
        self.data_manager = data_manager
        self.cart = ShoppingCart(inventory)

        self.tax_rate = 7.0

    def add_to_cart(self, code, quantity):
        return self.cart.add_item(code, quantity)

    def checkout(self, paid, discount_rate=0):

        if self.cart.is_empty():
            print("Cart is empty.")
            return None

        if not 0 <= discount_rate <= 100:
            print("Invalid discount.")
            return None

        subtotal = self.cart.calculate_subtotal()

        discount = round(
            subtotal * discount_rate / 100, 2
        )

        tax = round(
            (subtotal - discount) * self.tax_rate / 100, 2
        )

        total = round(
            subtotal - discount + tax, 2
        )

        if paid < total:
            print(f"Insufficient payment. Required: ${total:.2f}")
            return None

        # Create transaction using a snapshot of cart items.
        transaction = Transaction(
            items=self.cart.get_receipt_items(),
            subtotal=subtotal,
            discount_rate=discount_rate,
            tax_rate=self.tax_rate,
            paid=round(paid, 2)
        )

        # Deduct purchased quantities from inventory.
        for item in self.cart.items.values():
            item.product.update_stock(-item.quantity)

        # Save everything.
        self.data_manager.save_products(self.inventory)
        self.data_manager.save_sale(transaction)

        transaction.print_receipt()

        self.cart.clear()

        return transaction

    def search_product(self, keyword):
        results = self.inventory.search_product(keyword)

        if not results:
            print("No products found.")
            return

        print("\nSearch results:")

        for product in results:
            print(product)

    def sales_report(self):

        sales = self.data_manager.load_sales()

        if not sales:
            print("\nNo sales recorded yet.")
            return

        total_revenue = sum(
            sale["total"] for sale in sales
        )

        total_transactions = len(sales)

        total_items = sum(
            item["quantity"]
            for sale in sales
            for item in sale["items"]
        )

        print("\n========== SALES REPORT ==========")

        print(f"Total transactions: {total_transactions}")
        print(f"Items sold: {total_items}")
        print(f"Total revenue: ${total_revenue:.2f}")

        print("==================================")

    def show_sales_history(self):

        sales = self.data_manager.load_sales()

        if not sales:
            print("No sales history.")
            return

        print("\n========== SALES HISTORY ==========")

        for sale in sales:
            print(
                f"ID: {sale['transaction_id']} | "
                f"Date: {sale['date']} | "
                f"Total: ${sale['total']:.2f}"
            )