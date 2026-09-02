def read_product():
    """
    Reads product data from 'products.txt' file and returns a list of product dictionaries.
    
    Attempts to open and read the products file line by line, parsing each line into 
    a product dictionary with keys: Product, Brand, Quantity, Price, Origin.
    
    Returns:
        list: A list of dictionaries where each dictionary represents a product.
              Returns empty list if file is empty or doesn't exist.
              
    Handles:
        FileNotFoundError: If file doesn't exist, creates an empty file and returns empty list.
    """
    products = []

    try:
        with open('products.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():  # Skip empty lines
                    part = line.strip().split(', ')
                    product = {
                        "Product": part[0],
                        "Brand": part[1],
                        "Quantity": int(part[2]),
                        "Price": int(part[3]),
                        "Origin": part[4]
                    }
                    products.append(product)
    except FileNotFoundError:
        print("Products file not found. Creating a new one.")
        open('products.txt', 'w').close()
    
    return products


def display_products():
    """
    Displays all available products in a formatted table with VAT.
    
    Reads products using read_product() and displays them in a well-formatted table
    with columns: No., Product, Brand, Stock, Price, Origin.
    
    Handles empty product list by displaying appropriate message.
    
    """
    products = read_product()

    if not products:
        print("\nNo products available right now.")
        return

    print("\nAvailable Products:\n")
    
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
            f"Rs. {product['Price']}",
            product['Origin']
        ))
        print("-"* 90)
        i += 1


if __name__ == "__main__":
    """
    Direct execution entry point.
    Calls display_products() when this module is run as a standalone script.
    """
    display_products()