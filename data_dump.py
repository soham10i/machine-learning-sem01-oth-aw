import pandas as pd
import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    """Create a database connection."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def import_csv_to_mysql(connection, csv_file_path, table_name):
    """Import CSV data into MySQL table."""
    try:
        # Read the CSV file
        data = pd.read_csv(csv_file_path)

        # Insert data into the MySQL table
        for i, row in data.iterrows():
            sql = f"INSERT INTO {table_name} ({', '.join(data.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
            cursor = connection.cursor()
            cursor.execute(sql, tuple(row))
        connection.commit()
        print(f"Data from {csv_file_path} imported successfully into {table_name}")
    except Error as e:
        print(f"The error '{e}' occurred")

def main():
    # Database connection parameters
    host = "your_host"
    user = "your_username"
    password = "your_password"
    database = "your_database"
    
    # Create a connection to the database
    connection = create_connection(host, user, password, database)

    # Path to your CSV file and the target table name
    csv_file_path = "path/to/your/file.csv"
    table_name = "your_table_name"

    # Import CSV data into MySQL
    import_csv_to_mysql(connection, csv_file_path, table_name)

    # Close the connection
    if connection:
        connection.close()

if __name__ == "__main__":
    main()