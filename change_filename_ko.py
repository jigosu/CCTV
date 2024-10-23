import os

def rename_files_in_directory(directory, target_char):
    # 지정된 디렉토리의 모든 파일을 반복
    for filename in os.listdir(directory):
        # .jpg 및 .txt 파일만 필터링
        if filename.endswith('.jpg') or filename.endswith('.txt'):
            # 특정 문자를 제거
            new_filename = filename.replace(target_char, '')
            # 파일 경로 구성
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            # 파일 이름 변경
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {old_file_path} -> {new_file_path}')

# 사용 예
directory_path = 'C:/Users/user/Desktop/1023/3'  # 경로를 원하는 폴더로 수정하세요
target_character = '아이유'  # 제거하고 싶은 특정 문자
rename_files_in_directory(directory_path, target_character)
