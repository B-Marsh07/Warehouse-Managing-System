import sqlite3 

import os 

import csv 

 

class ProductDB: 

    def __init__(self, db_name): 

        self.db_name = db_name 

 

    def connect(self): 

        if not os.path.exists(self.db_name): 

            self._create_db() 

            print(f"Database '{self.db_name}' created and connected.") 

        else: 

            print(f"Connected to existing database '{self.db_name}'.") 

        self.connection = sqlite3.connect(self.db_name) 

        self.cursor = self.connection.cursor() 

 

    def _create_db(self): 

        with sqlite3.connect(self.db_name) as conn: 

            conn.execute(''' 

            CREATE TABLE Products ( 

                ProductID INTEGER PRIMARY KEY, 

                ProductName TEXT NOT NULL, 

                Manufacturer TEXT NOT NULL, 

                QuantityInStock INTEGER NOT NULL, 

                Location TEXT NOT NULL 

            ) 

            ''') 

 

    def add_product(self, product_id, product_name, manufacturer, quantity, location): 

        if self._validate(product_id, product_name, manufacturer, quantity, location): 

            try: 

                self.cursor.execute(''' 

                INSERT INTO Products (ProductID, ProductName, Manufacturer, QuantityInStock, Location) 

                VALUES (?, ?, ?, ?, ?) 

                ''', (product_id, product_name, manufacturer, quantity, location)) 

                self.connection.commit() 

                print("Product added successfully.") 

            except sqlite3.IntegrityError as e: 

                print(f"An error occurred: {e}") 

        else: 

            print("Invalid input data.") 

 

    def search_product(self, identifier): 

        self.cursor.execute('SELECT * FROM Products WHERE ProductID = ? OR ProductName = ?', (identifier, identifier)) 

        product = self.cursor.fetchone() 

        if product: 

            print(f"Product found:\nID: {product[0]}\nName: {product[1]}\nManufacturer: {product[2]}\nQuantity in Stock: {product[3]}\nLocation: {product[4]}") 

        else: 

            print("Product not found.") 

 

    def update_product(self, product_id, product_name=None, manufacturer=None, quantity=None, location=None): 

        updates = {"ProductName": product_name, "Manufacturer": manufacturer, "QuantityInStock": quantity, "Location": location} 

        updates = {k: v for k, v in updates.items() if v is not None} 

        if updates: 

            set_clause = ', '.join([f"{k} = ?" for k in updates]) 

            params = list(updates.values()) + [product_id] 

            self.cursor.execute(f'UPDATE Products SET {set_clause} WHERE ProductID = ?', params) 

            self.connection.commit() 

            print("Product updated successfully.") 

        else: 

            print("No valid fields to update.") 

 

    def delete_product(self, product_id): 

        self.cursor.execute('DELETE FROM Products WHERE ProductID = ?', (product_id,)) 

        if self.cursor.rowcount > 0: 

            print("Product deleted successfully.") 

        else: 

            print("Product not found.") 

 

    def _validate(self, product_id, product_name, manufacturer, quantity, location): 

        return ( 

            isinstance(product_id, int) and len(str(product_id)) == 7 and 

            isinstance(product_name, str) and product_name.strip() and 

            isinstance(manufacturer, str) and manufacturer.strip() and 

            isinstance(quantity, int) and quantity >= 0 and 

            isinstance(location, str) and len(location) == 2 and location[0].isalpha() and location[1].isdigit() 

        ) 

 

    def export_to_csv(self, table_name, csv_file): 

        self.cursor.execute(f"SELECT * FROM {table_name}") 

        with open(csv_file, 'w', newline='') as f: 

            writer = csv.writer(f) 

            writer.writerow([desc[0] for desc in self.cursor.description])  # Write headers 

            writer.writerows(self.cursor.fetchall())  # Write data rows 

        print(f"Table '{table_name}' exported to '{csv_file}' successfully.") 

 

def main(): 

    db_name = input("Enter the database file name (e.g., 'products.db'): ") 

    product_db = ProductDB(db_name) 

    product_db.connect() 

     

    while True: 

        print("\nOptions:\n1. Add Product\n2. Search Product\n3. Update Product\n4. Delete Product\n5. Export to CSV\n6. Exit") 

        choice = input("Select an option: ") 

        try: 

            if choice == '1': 

                product_db.add_product( 

                    int(input("Enter Product ID (7 digits): ")), 

                    input("Enter Product Name: "), 

                    input("Enter Manufacturer: "), 

                    int(input("Enter Quantity in Stock: ")), 

                    input("Enter Location (e.g., A1): ") 

                ) 

            elif choice == '2': 

                product_db.search_product(input("Enter Product ID or Name to search: ")) 

            elif choice == '3': 

                product_db.update_product( 

                    int(input("Enter Product ID to update: ")), 

                    input("Enter new Product Name (or press Enter to skip): ") or None, 

                    input("Enter new Manufacturer (or press Enter to skip): ") or None, 

                    input("Enter new Quantity in Stock (or press Enter to skip): ") or None, 

                    input("Enter new Location (e.g., A1) (or press Enter to skip): ") or None 

                ) 

            elif choice == '4': 

                product_db.delete_product(int(input("Enter Product ID to delete: "))) 

            elif choice == '5': 

                product_db.export_to_csv("Products", input("Enter CSV file name (e.g., 'products.csv'): ")) 

            elif choice == '6': 

                print("Exiting the program.") 

                break 

            else: 

                print("Invalid option. Please try again.") 

        except ValueError as e: 

            print(f"Invalid input. Error: {e}") 

        except sqlite3.IntegrityError as e: 

            print(f"An error occurred: {e}") 

        except Exception as e: 

            print(f"An unexpected error occurred: {e}") 

 

if __name__ == "__main__": 

    main() 

 

 
