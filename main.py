from product import Product
from inventory import Inventory
from data_manager import DataManager
from cashier import CashierSystem


def initialize_system():

    data_manager = DataManager()

    products = data_manager.load_products()

    # Add default products only on first launch.
    if not products:

        products = [
            Product("001", "Apple", 0.50, 100),
            Product("002", "Banana", 0.30, 100),
            Product("003", "Orange", 0.80, 100),
            Product("004", "Milk", 1.20, 50),
            Product("005", "Bread", 1.00, 50)
        ]

        inventory = Inventory(products)
        data_manager.save_products(inventory)

    else:
        inventory = Inventory(products)

    return CashierSystem(inventory, data_manager)


def print_menu():

    print("\n")
    print("=" * 40)
    print("         SUPERMARKET POS SYSTEM")
    print("=" * 40)

    print("1.  Show Products")
    print("2.  Search Products")
    print("3.  Add Item to Cart")
    print("4.  Show Cart")
    print("5.  Remove Item from Cart")
    print("6.  Update Cart Quantity")
    print("7.  Checkout")
    print("8.  Add New Product")
    print("9.  Update Product Price")
    print("10. Update Product Stock")
    print("11. Delete Product")
    print("12. Sales Report")
    print("13. Sales History")
    print("14. Exit")

    print("=" * 40)


def get_integer(prompt):

    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return None


def get_positive_float(prompt):

    try:
        value = float(input(prompt))

        if value <= 0:
            print("Value must be positive.")
            return None

        return value

    except ValueError:
        print("Invalid number.")
        return None


def run_system():

    cashier = initialize_system()

    print("\nWelcome to Supermarket POS!")

    while True:

        print_menu()

        choice = input("Select an option: ").strip()

        if choice == "1":

            cashier.inventory.show_products()

        elif choice == "2":

            keyword = input("Search product: ").strip()
            cashier.search_product(keyword)

        elif choice == "3":

            code = input("Product code: ").strip()
            quantity = get_integer("Quantity: ")

            if quantity is not None:
                cashier.add_to_cart(code, quantity)

        elif choice == "4":

            cashier.cart.show_cart()

        elif choice == "5":

            code = input("Product code to remove: ").strip()
            cashier.cart.remove_item(code)

        elif choice == "6":

            code = input("Product code: ").strip()
            quantity = get_integer("New quantity: ")

            if quantity is not None:
                cashier.cart.update_quantity(code, quantity)

        elif choice == "7":

            cashier.cart.show_cart()

            if cashier.cart.is_empty():
                continue

            discount = get_integer(
                "Discount percentage (0-100): "
            )

            if discount is None or not 0 <= discount <= 100:
                print("Invalid discount percentage.")
                continue

            subtotal = cashier.cart.calculate_subtotal()

            discount_amount = round(
                subtotal * discount / 100, 2
            )

            tax = round(
                (subtotal - discount_amount)
                * cashier.tax_rate / 100, 2
            )

            total = round(
                subtotal - discount_amount + tax, 2
            )

            print(f"\nAmount to pay: ${total:.2f}")

            paid = get_positive_float("Payment amount: $")

            if paid is not None:
                cashier.checkout(paid, discount)

        elif choice == "8":

            code = input("Product code: ").strip()
            name = input("Product name: ").strip()

            price = get_positive_float("Price: $")
            stock = get_integer("Initial stock: ")

            if not code or not name:
                print("Code and name cannot be empty.")
                continue

            if price is None or stock is None or stock < 0:
                print("Invalid product information.")
                continue

            product = Product(code, name, price, stock)

            if cashier.inventory.add_product(product):
                cashier.data_manager.save_products(
                    cashier.inventory
                )

        elif choice == "9":

            code = input("Product code: ").strip()

            product = cashier.inventory.get_product(code)

            if product:
                price = get_positive_float("New price: $")

                if price is not None:
                    product.update_price(price)
                    cashier.data_manager.save_products(
                        cashier.inventory
                    )
                    print("Price updated successfully.")
            else:
                print("Product not found.")

        elif choice == "10":

            code = input("Product code: ").strip()
            quantity = get_integer(
                "Stock adjustment (+/-): "
            )

            if quantity is not None:
                if cashier.inventory.update_stock(code, quantity):
                    cashier.data_manager.save_products(
                        cashier.inventory
                    )

        elif choice == "11":

            code = input("Product code to delete: ").strip()

            # Prevent deletion of a product currently in the cart.
            if code in cashier.cart.items:
                print("Remove the product from your cart first.")
                continue

            if cashier.inventory.remove_product(code):
                cashier.data_manager.save_products(
                    cashier.inventory
                )

        elif choice == "12":

            cashier.sales_report()

        elif choice == "13":

            cashier.show_sales_history()

        elif choice == "14":

            print("\nThank you for using our Supermarket")
            print("Goodbye!")
            break

        else:

            print("Invalid choice. Select 1-14.")


if __name__ == "__main__":
    try:
        run_system()
    except KeyboardInterrupt:
        print("\nApplication interrupted. Goodbye!")