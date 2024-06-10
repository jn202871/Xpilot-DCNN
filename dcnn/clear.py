import sqlite3

def delete_data():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('./dcnn/match_data.db')
        cursor = conn.cursor()

        # Delete all data from the specified table
        cursor.execute(f'DELETE FROM frames')

        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print("Error occurred:", e)

    finally:
        # Close the connection
        if conn:
            conn.close()

delete_data()

