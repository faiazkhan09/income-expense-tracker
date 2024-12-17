from datetime import datetime
date_format = "%d/%m/%Y"
TYPE =  {
    'I': 'Income',
    'E': 'Expense'
}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format) #this converts the date entered in date_str to date object and compares it with the given date format. if correct format then stores the date object to valid_date else it gives ValueError
        return valid_date.strftime(date_format) #converts the date object to string
    except ValueError:
        print('Invalid date. Please enter date as dd/mm/yyyy ')
        return get_date(prompt, allow_default)

def get_amount():
    amount = float(input('Enter amount: '))
    try:
        if amount <= 0:
            raise ValueError('Amount must be non-zero and non-negative!')
        return amount
    except ValueError as e:
        print(e)
        return get_amount()
    
def get_type():                                                                               # example of dictionary
    type = input("Enter type of finance. Write 'I' for income and 'E' for expense: ").upper() # hello = { "one": "1", "two": "2"}
    if type in TYPE:                                                                          # print(hello["one"])
        return TYPE[type]                                                                     # >>>1
    print("Invalid input. Please enter 'I' for income and 'E' for expense: ")

def get_description():
    return input("Enter a description (optional): ")

    