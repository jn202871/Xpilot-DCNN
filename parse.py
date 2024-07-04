import sqlite3

data = open("data.txt", 'r')
conn = sqlite3.connect('./dcnn/match_data.db')
cursor = conn.cursor()
while True:
    frame = data.readline().strip()
    action = data.readline().strip()
    if not frame:
        break
    cursor.execute("INSERT INTO frames (frame,actions) values(?,?)",(frame,action))
conn.commit()
conn.close()

score1 = 0.0
score2 = 0.0
with open('score1.txt', 'r') as file:
    score1 = float(file.readlines()[-1].strip())
with open('score2.txt', 'r') as file:
    score2 = float(file.readlines()[-1].strip())
conn = sqlite3.connect('./score_data.db')
c = conn.cursor()
c.execute('INSERT INTO scores (Bot, DCNN) VALUES (?, ?)',
      (score1, score2))
conn.commit()
conn.close()
