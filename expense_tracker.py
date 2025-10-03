from expense import Expense
import calendar
import datetime
import os

# ANSI colors for styling
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{BOLD}{CYAN}===== Expense Tracker App ====={RESET}\n")
    
    expense_file_path = "expenses.csv"
    budget = 2000

    while True:
        print(f"{YELLOW}1. Add Expense\n2. View Summary\n3. View by Category\n4. Delete One Expense\n5. Delete All Expenses\n6. Exit{RESET}")
        choice = input("Choose an option: ")

        if choice == "1":
            expense = get_user_expense()
            save_expense_to_file(expense, expense_file_path)
        elif choice == "2":
            summarize_expenses(expense_file_path, budget)
        elif choice == "3":
            view_by_category(expense_file_path)
        elif choice == "4":
            delete_one_expense(expense_file_path)
        elif choice == "5":
            delete_all_expenses(expense_file_path)
        elif choice == "6":
            print(f"{GREEN}Goodbye! Stay on budget!{RESET}")
            break
        else:
            print(f"{RED}Invalid choice, please try again.{RESET}\n")


def get_user_expense():
    print(f"\n{CYAN}Getting User Expense...{RESET}")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))
    expense_categories = [
        "Foods", "Housing", "Transport", "Education", "Bills", "Entertainment", "Health"
    ]

    while True:
        print("\nSelect a category:")
        for i, category_name in enumerate(expense_categories, 1):
            print(f"  {i}. {category_name}")

        try:
            selected_index = int(input(f"Enter a category number [1-{len(expense_categories)}]: ")) - 1
            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                return Expense(name=expense_name, category=selected_category, amount=expense_amount)
            else:
                print(f"{RED}Invalid category. Try again!{RESET}")
        except ValueError:
            print(f"{RED}Please enter a number!{RESET}")


def save_expense_to_file(expense: Expense, expense_file_path):
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    print(f"{GREEN}Saved: {expense.name} | {expense.category} | ${expense.amount:.2f}{RESET}\n")


def summarize_expenses(expense_file_path, budget):
    print(f"\n{BOLD}{CYAN}=== Monthly Summary ==={RESET}")
    expenses = load_expenses(expense_file_path)

    if not expenses:
        print(f"{RED}No expenses found yet!{RESET}")
        return

    amount_by_category = {}
    for expense in expenses:
        amount_by_category[expense.category] = amount_by_category.get(expense.category, 0) + expense.amount

    # Display per category
    for key, amount in amount_by_category.items():
        print(f"{YELLOW}{key:<15}{RESET}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    remaining_budget = budget - total_spent

    print(f"\n{BOLD}Total Spent: {RESET}${total_spent:.2f}")
    print(f"{BOLD}Budget Remaining: {RESET}${remaining_budget:.2f}")

    # Daily Budget
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0

    print(f"{BOLD}Daily Allowance:{RESET} {GREEN}${daily_budget:.2f}{RESET}\n")

    # Top category
    top_category = max(amount_by_category, key=amount_by_category.get)
    print(f"{CYAN}Most spending in:{RESET} {BOLD}{top_category}{RESET} (${amount_by_category[top_category]:.2f})\n")


def view_by_category(expense_file_path):
    print(f"\n{BOLD}{CYAN}=== Expenses by Category ==={RESET}")
    expenses = load_expenses(expense_file_path)

    if not expenses:
        print(f"{RED}No expenses found!{RESET}")
        return

    categories = set([x.category for x in expenses])
    for cat in categories:
        print(f"\n{BOLD}{cat}{RESET}:")
        for e in expenses:
            if e.category == cat:
                print(f"  {e.name:<15} ${e.amount:.2f}")


def delete_one_expense(expense_file_path):
    expenses = load_expenses(expense_file_path)
    if not expenses:
        print(f"{RED}No expenses to delete.{RESET}\n")
        return

    print(f"\n{BOLD}{CYAN}=== Delete an Expense ==={RESET}")
    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp.name:<15} ${exp.amount:.2f} ({exp.category})")

    try:
        choice = int(input("\nEnter the number of the expense to delete: "))
        if 1 <= choice <= len(expenses):
            removed = expenses.pop(choice - 1)
            with open(expense_file_path, "w") as f:
                for e in expenses:
                    f.write(f"{e.name},{e.amount},{e.category}\n")
            print(f"{GREEN}Deleted: {removed.name} (${removed.amount:.2f}){RESET}\n")
        else:
            print(f"{RED}Invalid choice.{RESET}\n")
    except ValueError:
        print(f"{RED}Please enter a valid number.{RESET}\n")


def delete_all_expenses(expense_file_path):
    confirm = input(f"{RED}Are you sure you want to delete all expenses? (y/n): {RESET}")
    if confirm.lower() == "y":
        with open(expense_file_path, "w") as f:
            pass  # overwrite with nothing
        print(f"{GREEN}All expenses deleted. Starting fresh!{RESET}\n")
    else:
        print(f"{YELLOW}Delete cancelled. Your data is safe.{RESET}\n")


def load_expenses(expense_file_path):
    expenses = []
    try:
        with open(expense_file_path, "r") as f:
            for line in f:
                if line.strip():
                    expense_name, expense_amount, expense_category = line.strip().split(",")
                    expenses.append(Expense(
                        name=expense_name,
                        amount=float(expense_amount),
                        category=expense_category,
                    ))
    except FileNotFoundError:
        pass
    return expenses


if __name__ == "__main__":
    main()
