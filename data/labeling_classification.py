import os
import shutil

# 원본 이미지와 텍스트 파일이 저장된 폴더 경로
source_folder = 'C:/Users/user/Desktop/google_label'  # 원본 폴더 경로
destination_folder = 'C:/Users/user/Desktop/google_Image'  # 새로운 폴더 경로

# 새로운 폴더가 존재하지 않으면 생성
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 원본 폴더에서 파일 목록을 가져오기
files = os.listdir(source_folder)

# 모든 .jpg 파일에 대해 .txt 파일이 있는지 확인
for file in files:
    if file.endswith('.jpg'):
        # 이미지 파일과 같은 이름의 텍스트 파일 경로
        txt_file = file.replace('.jpg', '.txt')
        
        # .txt 파일이 존재하는지 확인
        if txt_file in files:
            # .jpg와 .txt 파일 경로 설정
            jpg_path = os.path.join(source_folder, file)
            txt_path = os.path.join(source_folder, txt_file)
            
            # 새로운 폴더에 .jpg와 .txt 파일 복사
            shutil.copy(jpg_path, os.path.join(destination_folder, file))
            shutil.copy(txt_path, os.path.join(destination_folder, txt_file))
            
            print(f"{file} 와 {txt_file} 를 {destination_folder}로 복사했습니다.")
        else:
            print(f"{file} 에 대응하는 .txt 파일이 없습니다.")
