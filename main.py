import pandas as pd
from datetime import datetime 
import csv
from enter_data import get_amount, get_date, get_description, get_type
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["Date", "Amount", "Type", "Description"]
    D_FORMAT = "%d/%m/%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns= cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_data(cls, date, amount, type, description):
        new_data = {
            "Date": date,
            "Amount": amount,
            "Type": type,
            "Description": description
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_data)
        print('Entry added successfully!')

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.D_FORMAT)
        start_date = datetime.strptime(start_date, CSV.D_FORMAT)
        end_date = datetime.strptime(end_date, CSV.D_FORMAT)

        mask = (df["Date"]>= start_date) & (df["Date"]<= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print('There are no transactions within these dates!')

        else:
            print(f"Transactions between {start_date.strftime(cls.D_FORMAT)} and {end_date.strftime(cls.D_FORMAT)} are-\n")
            print(filtered_df.to_string(index=False, formatters={"Date": lambda x: x.strftime(CSV.D_FORMAT)}))

            total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()

            print(f"\nTotal Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Saving: {(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter date (dd/mm/yyyy) or press enter to record today's date: ", allow_default=True)
    ammount = get_amount()
    type = get_type()
    description = get_description()
    CSV.add_data(date, ammount, type, description)

def plot_transaction(df):
    df.set_index("Date", inplace=True) 

    income_df = df[df["Type"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["Type"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="green")
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print(f"\nWelcome to Finance App")
        print(f"\n1. Enter Income/Expense")
        print("2. View Income/Expense")
        print("3. Exit")

        choice = input(f"Enter your choice: ")

        if choice == '1':
            add()
        elif choice == '2':
            start_date = get_date(f"\nEnter start date (dd/mm/yyyy): ")
            end_date = get_date("Enter end date (dd/mm/yyyy): ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want to see Income/Expense graph? (y/n): ").lower() == 'y':
                plot_transaction(df)
        elif choice == '3':
            print('Exitting...')
            break
        else:
            print('Invalid input. Enter values between 1-3: ')

if __name__ == "__main__":
    main()


