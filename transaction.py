from read_file import read_product
from write_file import generate_restock_invoice
from datetime import datetime

VAT_RATE = 0.13 # 13% 

def buy_products():
    """
    Handles the product purchasing process for customers.
    Now includes VAT in the final invoice.
    
    Main workflow:
    1. Displays available products in a formatted table
    2. Allows customer to select products and quantities
    3. Applies promotional offer (buy 3 get 1 free)
    4. Updates product quantities 
    5. Generates sales invoice
    
    Features:
    - Validates all user inputs
    - Tracks free items (promotional offer)
    - Maintains real-time stock levels
    - Handles empty cart case
    - Generates detailed invoice
    
    """
    products = read_product()
    if not products:
        print("\nNo products available for sale.")
        return
    
    print("\n=== BUY PRODUCTS ===")
    display_products_for_sale(products)
    
    cart = []
    while True:
        try:
            choice = input("\nEnter product number to add to cart or 0 to proccessed: ")
            if choice == '0':
                break
                
            choice = int(choice)
            if 1 <= choice <= len(products):
                selected_product = products[choice-1]
                max_qty = selected_product['Quantity']
                
                qty = int(input(f"Enter quantity of {selected_product['Product']} to sell (max {max_qty}): "))
                if qty <= 0:
                    print("Quantity must be positive.")
                    continue
                    
                if qty > max_qty:
                    print(f"Not enough stock. Only {max_qty} available.")
                    continue
                
                # Calculate free items (buy 3 get 1 free)
                free_items = qty // 3
                total_items = qty + free_items
                
                if total_items > max_qty:
                    print(f"Cannot provide {free_items} free items. Not enough stock.")
                    continue
                
                # Add to cart
                cart.append({
                    "Product": selected_product['Product'],
                    "Brand": selected_product['Brand'],
                    "Quantity": qty,
                    "Free Items": free_items,
                    "Price": selected_product['Price'],
                    "Origin": selected_product['Origin'],
                    "Total": qty * selected_product['Price']
                })
                
                # Update product quantity 
                selected_product['Quantity'] -= total_items
                
                print(f"Added {qty} {selected_product['Product']} (+{free_items} free) to cart.")
                print(f"Remaining stock: {selected_product['Quantity']}")
                
            else:
                print("Invalid product number.")
                
        except ValueError:
            print("Please enter a valid number.")
    
    if not cart:
        print("\nNo products were sold.")
        return
    
    # Update stock 
    update_product_stock(products)
    
    # Generate sales invoice
    generate_sales_invoice(cart)

def display_products_for_sale(products):
    """
    Displays available products in a formatted table for customer selection.
    
    products (list): List of product dictionaries containing:
                    - Product
                    - Brand
                    - Quantity
                    - Price
                    - Origin
    
    Output:
        Prints a well-formatted table showing:
        - Product number
        - Product details
        - Current stock levels
        - Pricing information
    """
    print("\nAvailable Products for Sale:\n")
    
    print("{:<5} {:<20} {:<15} {:<15} {:<15} {:<10}".format(
        "No.", "Product", "Brand", "Quantity", "Price", "Origin"))
    print("-" * 90)
    
    i = 1
    for product in products:
        print("{:<5} {:<20} {:<15} {:<15} {:<15} {:<10}".format(
            i,
            product['Product'],
            product['Brand'],
            product['Quantity'],
            product['Price'],
            product['Origin']
        ))
        print("-" * 90)
        i += 1

def update_product_stock(products):
    """
    Updates the product quantity file with current stock levels.
    
    products (list): List of product dictionaries with updated quantities
    
    Writes:
        Updates 'products.txt' with current inventory levels
        Overwrites existing file with new quantities
    """
    with open("products.txt", "w") as file:
        for product in products:
            file.write(f"{product['Product']}, {product['Brand']}, {product['Quantity']}, {product['Price']}, {product['Origin']}\n")

def generate_sales_invoice(cart):
    """
    Generates a detailed sales invoice for the customer purchase with VAT.
    
    cart (list): List of purchased items with details:
                - Product
                - Brand
                - Quantity
                - Free Items
                - Price
                - Origin
                - Total
    
    Creates:
        A timestamped text file containing:
        - Store header
        - Date/time of purchase
        - Customer information
        - Detailed list of purchased items
        - Free items (promotional)
        - Total amount due
    
    File naming format: sales_invoice_YYYYMMDD_HHMMSS.txt
    """
    customer_name = input("\nEnter customer name: ").strip() 
    now = datetime.now()
    timestamp = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"
    filename = f"sales_invoice_{timestamp}.txt"
    subtotal = sum(item['Total'] for item in cart)
    vat_amount = subtotal * VAT_RATE
    total = subtotal + vat_amount
    
    with open(filename, 'w') as file:
        file.write("=== WECARE SALES INVOICE ===\n")
        file.write(f"Date: {now.year}-{now.month:02}-{now.day:02} {now.hour:02}:{now.minute:02}:{now.second:02}\n")
        file.write(f"Customer: {customer_name}\n")
        file.write("----------------------------------------------------------------------------\n")
        
        for item in cart:
            file.write(f"Product: {item['Product']}\n")
            file.write(f"Brand: {item['Brand']}\n")
            file.write(f"Quantity Paid: {item['Quantity']}\n")
            file.write(f"Free Items: {item['Free Items']}\n")
            file.write(f"Price per item: Rs. {item['Price']}\n")
            file.write(f"Origin: {item['Origin']}\n")
            file.write("-------------------------------------------------------------------------------\n")
        
        file.write(f"SUB-TOTAL: Rs. {subtotal}\n")
        file.write(f"VAT ({VAT_RATE*100}%): Rs. {vat_amount}\n")
        file.write(f"TOTAL AMOUNT: Rs. {total}\n")
        file.write("\nThank you for shopping with WeCare!\n")
    
    print(f"\nSales invoice generated: {filename}")
    print(f"Sub-total: Rs. {subtotal}")
    print(f"VAT ({VAT_RATE*100}%): Rs. {vat_amount}")
    print(f"Total Amount: Rs. {total}")

if __name__ == "__main__":
    """
    Entry point for direct script execution.
    Calls buy_products() when this module is run as a standalone program.
    """
    buy_products()