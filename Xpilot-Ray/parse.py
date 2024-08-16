import sqlite3
def parse_data(data_path, db_path):
    data = open(data_path, 'r')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frames (
            frame TEXT,
            actions TEXT
        )
    ''')
    while True:
        frame = data.readline().strip()
        action = data.readline().strip()
        if not frame:
            break
        cursor.execute("INSERT INTO frames (frame,actions) values(?,?)",(frame,action))
    conn.commit()
    conn.close()
