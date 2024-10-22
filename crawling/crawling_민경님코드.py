
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 창을 표시하지 않고 실행
options.add_argument('--disable-gpu')  # GPU 비활성화
options.add_argument('--window-size=1920,1080')  # 창 크기 설정
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ChromeDriver 자동 설치 및 실행
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)

# 구글 이미지 검색 페이지 열기
driver.get("https://images.google.com/?hl=ko")


# 검색창 요소 찾기 및 검색어 입력
# 검색창 요소 찾기 및 검색어 입력
input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))  # 이름으로 찾기
input_element.send_keys("고화질 남자 연예인" + Keys.ENTER)


# 스크롤 다운
elem = driver.find_element(By.TAG_NAME, 'body')
for i in range(60):
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)

# "더 보기" 버튼 클릭
try:
    view_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'mye4qd')))
    view_more_button.click()
    for i in range(80):
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
except Exception as e:
    print(f"더 보기 버튼 클릭 중 오류 발생: {e}")

# img 태그를 사용하여 이미지 URL 수집 (최대 100개)
image_elements = driver.find_elements(By.CSS_SELECTOR, "img")

# 이미지 URL 수집
image_links = []
for image in image_elements:
    src = image.get_attribute('src')
    if src is None:  # 만약 src 속성이 없으면 data-src 속성을 가져옴
        src = image.get_attribute('data-src')
    if src and 'http' in src:  # 유효한 URL만 수집
        image_links.append(src)
    if len(image_links) >= 100:  # 최대 100개의 이미지만 수집
        break

# 찾은 이미지 개수 출력
print('찾은 이미지의 개수:', len(image_links))

# 이미지 URL 출력
for link in image_links:
    print(link)

# 드라이버 종료
driver.quit()

import urllib.request
import os

# 이미지 저장 폴더 경로 설정 (예: 'Desktop/google' 폴더)
save_dir = os.path.join(os.path.expanduser('~'), 'Desktop/google')

# 폴더가 존재하지 않으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 이미지 다운로드
for k, url in enumerate(image_links):
    file_path = os.path.join(save_dir, f'google_{369+k}.jpg')  # 파일명 설정
    urllib.request.urlretrieve(url, file_path)  # 이미지 다운로드
    print(f'{k + 1}번째 이미지를 다운로드했습니다: {file_path}')

print('모든 이미지 다운로드가 완료되었습니다.')