import os
import cv2
import smtplib
import threading
import time
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from ultralytics import YOLO
from flask import Flask, render_template, Response, request
from datetime import datetime
import numpy as np

app = Flask(__name__)

# YOLOv8 모델 로드
model = YOLO('best_증강전_l모델.pt')

# 비디오 스트림 설정
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 이미지 저장 경로
save_dir = os.path.join('static', 'save_img')  # 상대 경로 사용
os.makedirs(save_dir, exist_ok=True)


# SQLite 데이터베이스 설정
db_file = 'image_data.db'
conn = sqlite3.connect(db_file, check_same_thread=False)
cursor = conn.cursor()

# 이미지 정보를 저장할 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT NOT NULL,
    save_date TEXT NOT NULL,
    labels TEXT NOT NULL
)
''')
conn.commit()

# 이메일 설정
email_interval = 5
last_email_time = 0

def send_email(image_name, class_name):
    sender_email = ""  # 발신자 이메일
    password = ""  # 비밀번호 또는 앱 비밀번호
    receiver_email = ""  # 수신자 이메일

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "실시간 CCTV 감지 - " + str(class_name)
    
    body = "얼굴이 감지되었습니다."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(image_name, 'rb') as img_file:
            img = MIMEImage(img_file.read(), name=os.path.basename(image_name))  # 파일 이름 수정
            msg.attach(img)
    except FileNotFoundError:
        print(f"이미지를 찾을 수 없습니다: {image_name}")

    with smtplib.SMTP('smtp.naver.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)

def detect_faces():
    global last_email_time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        image_labels = []
        boxes = []

        for result in results:
            for box in result.boxes:
                confidence = box.conf[0]
                boxes.append((box.xyxy[0].cpu().numpy(), confidence, box.cls[0]))

        # NMS를 적용하기 위해 박스를 numpy 배열로 변환
        if boxes:
            boxes_array = np.array([b[0] for b in boxes])  # 좌표
            confidences = np.array([b[1] for b in boxes])  # 신뢰도
            indices = cv2.dnn.NMSBoxes(boxes_array.tolist(), confidences.tolist(), score_threshold=0.5, nms_threshold=0.4)

            # 인덱스가 비어있지 않은 경우에만 처리
            if indices is not None and len(indices) > 0:
                for i in indices.flatten():  # 인덱스를 1D 배열로 변환
                    box = boxes[i][0]
                    label_id = int(boxes[i][2])
                    label = model.names[label_id]
                    image_labels.append(label)

                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        if image_labels:
            current_time = time.time()
            if current_time - last_email_time >= email_interval:
                image_name = os.path.join(save_dir, f"{','.join(image_labels)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")

                if cv2.imwrite(image_name, frame):  # 성공적으로 저장되면 True를 반환
                    print(f"이미지 저장 성공: {image_name}")
                else:
                    print(f"이미지 저장 실패: {image_name}")

                save_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                labels_str = ', '.join(image_labels)

                # 경로를 슬래시('/')로 변경하여 저장
                image_name_normalized = image_name.replace(os.sep, '/')
                
                cursor.execute('INSERT INTO images (image_name, save_date, labels) VALUES (?, ?, ?)', (image_name_normalized, save_date, labels_str))
                conn.commit()

                email_thread = threading.Thread(target=send_email, args=(image_name,image_labels))  # 기존의 절대 경로를 사용
                email_thread.start()
                last_email_time = current_time

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(detect_faces(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    conn = get_db_connection()
    images = conn.execute('SELECT * FROM images ORDER BY save_date DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('index.html', images=images)

def get_db_connection():
    conn = sqlite3.connect('image_data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    conn = get_db_connection()
    
    # 기본 쿼리
    query = "SELECT * FROM images WHERE 1=1"
    parameters = []

    if search_query:
        query += " AND labels LIKE ?"
        parameters.append('%' + search_query + '%')
    
    if start_date:
        query += " AND save_date >= ?"
        parameters.append(start_date)
    
    if end_date:
        query += " AND save_date <= ?"
        parameters.append(end_date)

    query += " ORDER BY save_date DESC LIMIT 10"
    
    results = conn.execute(query, parameters).fetchall()
    conn.close()

    # 결과를 HTML 형식으로 변환
    results_html = ''
    for image in results:
        results_html += f'''
            <li class="image-item" data-image="{ image[1] }">
                <strong>방문 날짜:</strong> {image[2]} <br>
                <strong>방문자:</strong> {image[3]}
                <img src="../{ image[1] }" alt="Image" class="hidden-image" style="display: none; width: 50%; height: auto; border-radius: 10px; margin-top: 5px;"/>
            </li>
        '''  

    return results_html  # HTML 결과 반환

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
