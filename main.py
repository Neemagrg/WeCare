from read_file import read_product, display_products 
from write_file import write_product, add_quantity
from transaction import buy_products
from datetime import datetime

def main():
    """
    Main function for the WECARE MANAGEMENT SYSTEM.

    It displays a menu of options and calls the appropriate functions based on user input.

    The menu options include:
    1. View Products - Displays all available products
    2. Add New Product - Allows adding a new product 
    3. Restock Product - Allows increasing the quantity of an existing product
    4. BUY Products - Handles the product purchasing process
    5. Exit - Terminates the program
    
    The function runs in a continuous loop until the user chooses to exit.
    """
    while True:
        print("\n=== WECARE MANAGEMENT SYSTEM ===")
        print("1. View Products")
        print("2. Add New Product")
        print("3. Restock Product")
        print("4. Buy Products")
        print("5. Exit")
        
        option = input("Enter your choice (1-5): ")
        
        if option == "1":
            display_products() 
        elif option == "2":
            write_product()
        elif option == "3":
            add_quantity()
        elif option == "4":
            buy_products()
        elif option == "5":
            print("\nExiting")
            break
        else:
            print("\nInvalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    """
    Entry point of the program.
    Executes the main function when the script is run directly.
    """
    main()