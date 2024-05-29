import sqlite3

data = open("data.txt", 'r')
conn = sqlite3.connect('xpilot_data.db')
cursor = conn.cursor()
while True:
    frame = data.readline().strip()
    action = data.readline().strip()
    if not frame:
        break
    cursor.execute("INSERT INTO frames (frame,actions) values(?,?)",(frame,action))
conn.commit()
conn.close()
