from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('cred.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# check if our APIs are connected and retrive the data
# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

def get_sales_data():
    """
    Get sales figures from user.
    run a while loop to collect a valid string of data from the user via terminal, which must be a string of six numbers separated by commas.The loop will repeatedly request data untill it is valid.
    """
    while True:
        print("Please enter sales data from last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str  = input("Enter your data here: ")
        # print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")

        if (validate_data(sales_data)):
            print("Data is valid!")
            break
    return sales_data

    

def validate_data(values):
    """
    Inside the try, convert all the string values into integer.
    Raise ValueError if string cannot be converted into int or if there aren't excatly 6 values
    """
    # print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"invalid data {e}, please try again\n")
        return False
    
    return True

# update_sales_worksheet(data) and update_surplus_worksheet(data) have been refactoring with update_worksheet(data,worksheet)

# def update_sales_worksheet(data):
#     """
#     Update sales worksheet with a new row the user provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet('sales')
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully!\n")

# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet with a new row coming from the subtraction between stock and sales 
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet('surplus')
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully!\n")

def update_worksheet(data,worksheet):
    """
    Update surplus worksheet with a new row coming from the subtraction between stock and sales 
    """
    print(f"Updating {worksheet} worksheet...\n")
    get_worksheet = SHEET.worksheet(f'{worksheet}')
    get_worksheet.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calcutale surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock;
    - Posive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(f"from pprint:\n {stock}")
    stock_row = stock[-1]
    print(f"stock row: {stock_row}")
    print(f"sales row: {sales_row}")
    surplus_data = []
    for stock,sales in zip(stock_row,sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data




def get_the_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,collecting the last 5 entries from each sandwich and returns the data as a list of list
    """
    sales = SHEET.worksheet("sales")
    # columns  = sales.col_values(3)
    # print(column)
    columns_list = []
    for index in range(1,7):
        column  = sales.col_values(index)
        # columns_list.append(column[0])
        columns_list.append(column[-5:])
    
    # pprint(columns_list)
    return columns_list



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    print(data)
    sales_data = [int(num) for num in data]
    # update_sales_worksheet(sales_data)
    update_worksheet(sales_data,"sales")
    surplus_d = calculate_surplus_data(sales_data)
    print(surplus_d)
    # update_surplus_worksheet(surplus_d)
    update_worksheet(surplus_d,"surplus")

print("Welcome to Love Sandwiches Data Automation")
# main()
sales_columns = get_the_last_5_entries_sales()




