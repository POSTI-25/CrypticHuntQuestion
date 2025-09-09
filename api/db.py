import sqlite3

def create_database_and_table():
    """
    Connects to an SQLite database (or creates it if it doesn't exist),
    creates a table named 'points' with specified columns,
    and then closes the connection.
    """
    try:
        # Connect to the SQLite database.
        # If the file doesn't exist, it will be created.
        conn = sqlite3.connect('coordinates.db')

        # Create a cursor object to execute SQL commands
        cursor = conn.cursor()

        # SQL statement to create a table.
        # Note: Using underscores in column names is standard practice.
        # x_coordinate and y_coordinate are of type REAL (for floating-point numbers)
        # flag is of type INTEGER (can be used as a boolean, 0=False, 1=True)
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS points (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            x_coordinate REAL NOT NULL,
            y_coordinate REAL NOT NULL,
            flag INTEGER NOT NULL
        );
        '''

        # Execute the query to create the table
        cursor.execute(create_table_query)
        print("Table 'points' created successfully or already exists.")

        # Commit the changes
        conn.commit()
        print("Changes have been committed.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if conn:
            conn.close()
            print("Database connection closed.")

def insert_sample_row():
    try:
        conn = sqlite3.connect('coordinates.db')
        cursor = conn.cursor()

        insert_query = '''
        INSERT INTO points (x_coordinate, y_coordinate, flag)
        VALUES (?, ?, ?);
        '''
        cursor.execute(insert_query, (-153, -50, 180725))  # Example values
        conn.commit()
        print("Sample row inserted successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred while inserting: {e}")

    finally:
        if conn:
            conn.close()
            print("Database connection closed after insert.")

if __name__ == '__main__':
    create_database_and_table()
    insert_sample_row()
