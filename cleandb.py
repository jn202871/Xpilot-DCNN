import sqlite3

def remove_duplicates(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Define the queries to remove duplicates for both tables
    queries = {
        "DCNNScores": """
            DELETE FROM DCNNScores
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM DCNNScores
                GROUP BY Score, Round, Match
            );
        """,
        "ExpertScores": """
            DELETE FROM ExpertScores
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM ExpertScores
                GROUP BY Score, Round, Match
            );
        """
    }

    # Execute the queries for each table
    for table, query in queries.items():
        cursor.execute(query)
        print(f"Removed duplicates from {table}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def remove_high_rounds(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Define the queries to delete entries with Round > 10 for both tables
    queries = {
        "DCNNScores": "DELETE FROM DCNNScores WHERE Round != 100;",
        "ExpertScores": "DELETE FROM ExpertScores WHERE Round != 100;"
    }

    # Execute the deletion queries for each table
    for table, query in queries.items():
        cursor.execute(query)
        print(f"Entries with Round != 100 removed from {table}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Example usage
db_path = 'score_data.db'
#remove_duplicates(db_path)
remove_high_rounds(db_path)

