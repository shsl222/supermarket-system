from datetime import datetime
import uuid


class Transaction:

    def __init__(
        self,
        items,
        subtotal,
        discount_rate,
        tax_rate,
        paid
    ):
        self.transaction_id = str(uuid.uuid4())[:8].upper()

        self.date = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self.items = items
        self.subtotal = subtotal

        self.discount_rate = discount_rate
        self.discount = round(
            subtotal * discount_rate / 100, 2
        )

        self.tax_rate = tax_rate
        self.tax = round(
            (subtotal - self.discount) * tax_rate / 100, 2
        )

        self.total = round(
            subtotal - self.discount + self.tax, 2
        )

        self.paid = paid
        self.change = round(paid - self.total, 2)

    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "date": self.date,
            "items": self.items,
            "subtotal": self.subtotal,
            "discount_rate": self.discount_rate,
            "discount": self.discount,
            "tax_rate": self.tax_rate,
            "tax": self.tax,
            "total": self.total,
            "paid": self.paid,
            "change": self.change
        }

    def print_receipt(self):

        print("\n")
        print("=" * 45)
        print("             SUPERMARKET")
        print("              RECEIPT")
        print("=" * 45)

        print(f"Transaction: {self.transaction_id}")
        print(f"Date: {self.date}")

        print("-" * 45)

        for item in self.items:
            print(
                f"{item['name']} x {item['quantity']}"
            )
            print(f"  ${item['price']:.2f} each = ${item['total']:.2f}")

        print("-" * 45)

        print(f"Subtotal:       ${self.subtotal:.2f}")
        print(f"Discount:       -${self.discount:.2f}")
        print(f"Tax:            ${self.tax:.2f}")
        print(f"TOTAL:          ${self.total:.2f}")

        print("-" * 45)

        print(f"Paid:           ${self.paid:.2f}")
        print(f"Change:         ${self.change:.2f}")

        print("=" * 45)
        print("       THANK YOU FOR SHOPPING!")
        print("=" * 45)

        print()