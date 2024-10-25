import os

# 텍스트 파일이 저장된 폴더 경로
folder_path = 'C:/Users/user/Desktop/tmp_d'

# 폴더 내 모든 파일 목록을 가져옴
files = os.listdir(folder_path)

# 모든 .txt 파일에 대해 작업 수행
for file in files:
    if file.endswith('.txt'):
        # 파일 경로 설정
        file_path = os.path.join(folder_path, file)
        
        # 파일 열기
        with open(file_path, 'r+') as f:
            content = f.read()  # 파일 내용을 읽음
            
            if content:  # 내용이 있는지 확인
                # 첫 글자를 2로 바꾼 후 나머지 내용을 유지
                new_content = '2' + content[1:]
                
                # 파일을 다시 처음부터 쓰기 모드로 열고 수정된 내용을 저장
                f.seek(0)
                f.write(new_content)
                f.truncate()  # 기존 내용이 남지 않도록 파일 길이를 잘라냄
                
        print(f"{file}의 첫 글자를 0으로 바꿨습니다.")
