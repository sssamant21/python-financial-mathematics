from reference import present_value, discount_amount, basis_points, money
from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_HALF_UP,
)

MONEY_QUANTUM = Decimal("0.01")
ROUNDING_MODE = ROUND_HALF_UP


def round_money(value):
    return value.quantize(
        MONEY_QUANTUM,
        rounding=ROUNDING_MODE,
    )


def read_decimal(prompt):
    value = Decimal(input(prompt).strip())
    if not value.is_finite():
        raise ValueError(
            "Financial input must be finite."
        )
    return value


print("=" * 50)
print("BASIC FINANCIAL CALCULATOR")
print("=" * 50)
print("1. Simple Interest")
print("2. Compound Interest / Future Value")
print("3. Percentage Change")
print("4. Investment Profit or Loss")
print("5. Transaction Fee")
print("6. Financial Reconciliation")
print("=" * 50)

print("7. Present Value")
print("8. Discount Amount")
print("9. Basis-Point Conversion")
choice = input("Select calculation: ").strip()

try:
    if choice == "1":
        principal = read_decimal("Principal amount: ")
        rate_percent = read_decimal(
            "Annual interest rate (%): "
        )
        years = read_decimal("Number of years: ")
        rate = rate_percent / Decimal("100")
        interest = principal * rate * years
        ending_balance = principal + interest
        interest = round_money(interest)
        ending_balance = round_money(ending_balance)

        print()
        print("SIMPLE INTEREST RESULTS")
        print("-" * 30)
        print(f"Principal:      ${principal:,.2f}")
        print(f"Interest:       ${interest:,.2f}")
        print(f"Ending Balance: ${ending_balance:,.2f}")

    elif choice == "2":
        present_value = read_decimal("Present value: ")
        rate_percent = read_decimal(
            "Annual interest rate (%): "
        )
        years = int(input("Number of years: ").strip())
        periods_per_year = int(
            input("Compounding periods per year: ").strip()
        )

        if years < 0:
            print(
                "Number of years cannot be negative "
                "for this calculator model."
            )
        elif periods_per_year <= 0:
            print(
                "Compounding periods must be greater "
                "than zero."
            )
        else:
            annual_rate = rate_percent / Decimal("100")
            periodic_rate = (
                annual_rate / Decimal(periods_per_year)
            )
            number_of_periods = periods_per_year * years
            future_value = (
                present_value
                * (Decimal("1") + periodic_rate)
                ** number_of_periods
            )
            future_value = round_money(future_value)

            print()
            print("FUTURE VALUE RESULTS")
            print("-" * 30)
            print(f"Present Value: ${present_value:,.2f}")
            print(f"Future Value:  ${future_value:,.2f}")

    elif choice == "3":
        old_value = read_decimal("Original value: ")
        new_value = read_decimal("New value: ")

        if old_value == Decimal("0"):
            print(
                "Percentage change cannot be calculated "
                "when the original value is zero."
            )
        else:
            percentage_change = (
                (new_value - old_value)
                / old_value
                * Decimal("100")
            )
            print(
                "Percentage Change: "
                f"{percentage_change:.2f}%"
            )

    elif choice == "4":
        purchase_price = read_decimal(
            "Purchase price per unit: "
        )
        selling_price = read_decimal(
            "Selling price per unit: "
        )
        quantity = read_decimal("Quantity: ")

        raw_profit_loss = (
            selling_price - purchase_price
        ) * quantity
        profit_loss = round_money(raw_profit_loss)
        initial_investment = purchase_price * quantity

        if raw_profit_loss > Decimal("0"):
            status = "PROFIT"
        elif raw_profit_loss < Decimal("0"):
            status = "LOSS"
        else:
            status = "BREAK-EVEN"

        print()
        print(f"Status: {status}")
        print(f"Profit/Loss: ${profit_loss:,.2f}")

        if initial_investment != Decimal("0"):
            return_percent = (
                raw_profit_loss
                / initial_investment
                * Decimal("100")
            )
            print(f"Return: {return_percent:.2f}%")

    elif choice == "5":
        transaction_amount = read_decimal(
            "Transaction amount: "
        )
        fee_percent = read_decimal("Fee rate (%): ")
        fee_rate = fee_percent / Decimal("100")
        fee = round_money(
            transaction_amount * fee_rate
        )
        total_paid = round_money(
            transaction_amount + fee
        )

        print()
        print("TRANSACTION FEE RESULTS")
        print("-" * 30)
        print(
            "Transaction Amount: "
            f"${transaction_amount:,.2f}"
        )
        print(f"Fee:                ${fee:,.2f}")
        print(f"Total Paid:         ${total_paid:,.2f}")

    elif choice == "6":
        system_a = read_decimal("System A amount: ")
        system_b = read_decimal("System B amount: ")
        tolerance = read_decimal(
            "Allowed reconciliation tolerance: "
        )

        if tolerance < Decimal("0"):
            print("Tolerance cannot be negative.")
        else:
            difference = abs(system_a - system_b)

            print()
            print("RECONCILIATION RESULTS")
            print("-" * 30)
            print(f"System A:   ${system_a:,.2f}")
            print(f"System B:   ${system_b:,.2f}")
            print(f"Difference: ${difference:,.2f}")
            print(f"Tolerance:  ${tolerance:,.2f}")

            if difference <= tolerance:
                print("Status: WITHIN TOLERANCE")
            else:
                print("Status: RECONCILIATION EXCEPTION")

    elif choice == "7":
        result = present_value(input("Future receipt (USD): "), input("Effective rate per period (%): "), input("Whole periods: "))
        print(f"Present Value: USD {money(result):,.2f}")
    elif choice == "8":
        result = discount_amount(input("Original price (USD): "), input("Final price (USD): "))
        print(f"Discount Amount: USD {money(result):,.2f}")
    elif choice == "9":
        rate, points = basis_points(input("Basis points (signed): "))
        print(f"Decimal rate: {rate:f}")
        print(f"Percentage points: {points:f}")
    else:
        print("Invalid calculator selection.")

except InvalidOperation:
    print(
        "Invalid numeric input. Please enter valid numbers."
    )
except ValueError as error:
    print(f"Invalid input: {error}")
