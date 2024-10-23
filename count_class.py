import os

def count_first_char_in_files(folder_path):
    # 결과를 저장할 딕셔너리
    counts = {'0': 0, '1': 0, '2': 0}
    
    # 폴더 내의 파일 목록을 가져옴
    for file_name in os.listdir(folder_path):
        # .txt 파일만 처리
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                # 파일의 각 행을 읽음
                for line in file:
                    # 첫 문자가 '0', '1', '2' 중 하나인 경우 count 증가
                    if line and line[0] in counts:
                        counts[line[0]] += 1

    # 결과 출력
    print(f"Counts: {counts}")
    
    # 결과를 파일에 저장
    with open(os.path.join(folder_path, 'result.txt'), 'w') as result_file:
        result_file.write(f"Counts of lines starting with 0, 1, 2:\n")
        result_file.write(f"0: {counts['0']}\n")
        result_file.write(f"1: {counts['1']}\n")
        result_file.write(f"2: {counts['2']}\n")

# 현재 스크립트 위치를 기준으로 m_labels 폴더 경로 설정
current_dir = os.path.dirname(__file__)
folder_path = os.path.join(current_dir, 'labels')  # 'm_labels' 폴더 경로 설정
count_first_char_in_files(folder_path)
