import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('image_data.db')
cursor = conn.cursor()

# 데이터 조회
cursor.execute('SELECT * FROM images')
rows = cursor.fetchall()

# 결과 출력
for row in rows:
    print(row)

# 연결 종료
conn.close()
