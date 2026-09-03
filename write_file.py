from datetime import datetime

VAT_RATE = 0.13 # 13%

def write_product():
    """
    Adds a new product to the inventory system.
    
    Guides the user through entering product details including:
    - Product name
    - Brand
    - Stock quantity
    - Price
    - Origin
    - Supplier name
    
    Validates all inputs and ensures no empty values or negative numbers are accepted.
    Appends the new product to 'products.txt' file and generates a restock invoice.
    
    Returns:
        bool: True if product was successfully added, False otherwise.
    """
    print("\n=== ADD NEW PRODUCT ===")
    while True:
        try:
            product = input("Enter product name: ").strip()
            if not product:
                raise ValueError("Product name cannot be empty.")
            
            brand = input("Enter brand: ").strip()
            if not brand:
                raise ValueError("Brand cannot be empty.")
            
            quantity = int(input("Enter quantity: "))
            if quantity < 0:
                raise ValueError("Quantity cannot be negative.")
            
            price = int(input("Enter price (Rs.): "))
            if price < 0:
                raise ValueError("Price cannot be negative")
            
            origin = input("Enter origin: ").strip()
            if not origin:
                raise ValueError("Origin cannot be empty")
            
            supplier = input("Enter supplier name: ").strip()
            if not supplier:
                raise ValueError("Supplier name cannot be empty")
            
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

    product_data = f"{product}, {brand}, {quantity}, {price}, {origin}, {supplier}\n"
    
    with open("products.txt", "a") as file:
        file.write(product_data)
        print("\nProduct added successfully!")
    
    # Generate restock invoice
    generate_restock_invoice([{
        "Product": product,
        "Brand": brand,
        "Quantity": quantity,
        "Price": price,
        "Origin": origin
    }], supplier)
    
    return True

def add_quantity():
    """
    Restocks an existing product in the inventory.
    
    Displays all available products in a formatted table and allows user to:
    1. Select a product to restock
    2. Enter additional quantity (must be positive)
    3. Optionally update the product's price
    4. Enter supplier name
    
    Updates the product file with new quantities and generates a restock invoice.
    Handles all input validation and provides appropriate error messages.
    """
    from read_file import read_product
    
    products = read_product()
    if not products:
        print("\nNo products available to restock.")
        return
    
    print("\n=== RESTOCK PRODUCT ===")
    
    # Display products in table format
    print("\n{:<5} {:<20} {:<15} {:<15} {:<15} {:<10}".format(
        "No.", "Product", "Brand", "Quantity", "Price", "Origin"))
    print("-" * 90)

    i = 1
    for product in products:
        print("{:<5} {:<20} {:<15} {:<15} {:<15} {:<10}".format(
            i,
            product['Product'],
            product['Brand'],
            product['Quantity'],
            f"Rs. {product['Price']}",
            product['Origin'],
        ))
        print("-" * 90)
        i += 1
    
    try:
        choice = int(input("\nSelect product to restock (1-{}): ".format(len(products))))
        if 1 <= choice <= len(products):
            selected_product = products[choice-1]
            
            add_qty = int(input(f"Enter quantity to add to {selected_product['Product']}: "))
            if add_qty <= 0:
                print("Quantity must be positive.")
                return
                
            new_cost = input(f"Enter new price (Rs.) or press enter to keep current ({selected_product['Price']}): ")
            
            # Update price if provided
            if new_cost:
                try:
                    new_cost = int(new_cost)
                    if new_cost <= 0:
                        print("Price must be positive. Keeping current price.")
                    else:
                        selected_product['Price'] = new_cost
                except ValueError:
                    print("Invalid price. Keeping current price.")
            
            # Get supplier name
            supplier = input("Enter supplier name: ").strip()
            if not supplier:
                print("Supplier name cannot be empty.")
            
            # Update the quantity
            selected_product['Quantity'] += add_qty
            selected_product['Supplier'] = supplier
            
            # Rewrite the entire file with updated quantities
            with open("products.txt", "w") as file:
                for product in products:
                    file.write(f"{product['Product']}, {product['Brand']}, {product['Quantity']}, {product['Price']}, {product['Origin']}\n")
            
            print(f"\nSuccessfully added {add_qty} to {selected_product['Product']}. New quantity: {selected_product['Quantity']}")
            
            # Generate restock invoice
            generate_restock_invoice([{
                "Product": selected_product['Product'],
                "Brand": selected_product['Brand'],
                "Quantity": add_qty,
                "Price": selected_product['Price'],
                "Origin": selected_product['Origin']
            }], supplier)
            
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def generate_restock_invoice(products, supplier):
    """
    Generates a restock invoice text file with transaction details.
    
    products (list): List of product dictionaries containing:
                    - Product
                    - Brand
                    - Quantity
                    - Price
                    - Origin
    supplier (str): Source of the restock
    
    Creates a timestamped text file with:
    - Header information
    - Date/time of restock
    - Supplier information
    - Detailed list of products restocked
    - Total amount for the restock
    
    File naming format: restock_invoice_YYYYMMDD_HHMMSS.txt
    """
    now = datetime.now()
    timestamp = f"{now.year}{now.month:02}{now.day:02}_{now.hour:02}{now.minute:02}{now.second:02}"
    filename = f"restock_invoice_{timestamp}.txt"
    subtotal = sum(p['Quantity'] * p['Price'] for p in products)
    vat_amount = subtotal * VAT_RATE
    total = subtotal + vat_amount
    
    with open(filename, 'w') as file:
        file.write("=== WECARE RESTOCK INVOICE ===\n")
        file.write(f"Date: {now.year}-{now.month:02}-{now.day:02} {now.hour:02}:{now.minute:02}:{now.second:02}\n")
        file.write(f"Supplier: {supplier}\n")
        file.write("-" * 90 + "\n")
        
        for product in products:
            file.write(f"Product: {product['Product']}\n")
            file.write(f"Brand: {product['Brand']}\n")
            file.write(f"Quantity: {product['Quantity']}\n")
            file.write(f"Price per item: Rs. {product['Price']}\n")
            file.write(f"Origin: {product['Origin']}\n")
            file.write("-" * 90 + "\n")
        
        file.write(f"SUB-TOTAL: Rs. {subtotal}\n")
        file.write(f"VAT ({VAT_RATE*100}%): Rs. {vat_amount}\n")
        file.write(f"TOTAL AMOUNT: Rs. {total}\n")
    
    print(f"\nRestock invoice generated: {filename}")
    print(f"Sub-total: Rs. {subtotal}")
    print(f"VAT ({VAT_RATE*100}%): Rs. {vat_amount}")
    print(f"Total Amount: Rs. {total}")

if __name__ == "__main__":
    """
    Entry point for direct script execution.
    Calls write_product() when this module is run as a standalone program.
    """
    write_product()