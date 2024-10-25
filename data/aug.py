import albumentations as A

# 데이터 증강 기법 정의
augmentation_small_class = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.Rotate(limit=10, p=0.7)
])

augmentation_large_class = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.1)
])

import cv2
import os

def augment_images(input_dir, output_dir, label_dir, augmentation, num_augmentations=3):
    # 입력 디렉토리의 이미지 파일을 읽어옴
    image_files = [f for f in os.listdir(input_dir) if f.endswith('.jpg')]

    for image_file in image_files:
        img = cv2.imread(os.path.join(input_dir, image_file))
        
        # 라벨 파일 이름 설정
        label_file = os.path.splitext(image_file)[0] + '.txt'
        label_path = os.path.join(label_dir, label_file)
        
        # 라벨 읽기
        with open(label_path, 'r') as f:
            labels = f.readlines()

        for i in range(num_augmentations):
            augmented_img = augmentation(image=img)['image']
            new_filename = f"{os.path.splitext(image_file)[0]}_aug_{i}.jpg"
            cv2.imwrite(os.path.join(output_dir, new_filename), augmented_img)

            # 새로운 라벨 파일 생성
            new_label_path = os.path.join(output_dir, os.path.splitext(new_filename)[0] + '.txt')

            with open(new_label_path, 'w') as f:
                for label in labels:
                    # 여기서 라벨 수정 로직 추가
                    f.write(label)  # 수정된 라벨을 저장

# 클래스별로 이미지 증강
input_small_class_dir = 'C:/Users/user/Desktop/1023/3'
output_small_class_dir = 'C:/Users/user/Desktop/1023/a3'
input_small_class_labels_dir = 'C:/Users/user/Desktop/1023/3_label' # 라벨 디렉토리
augment_images(input_small_class_dir, output_small_class_dir, input_small_class_labels_dir, augmentation_small_class)

# input_large_class_dir = 'C:/Users/user/Desktop/1023_증강위해 데이터 수정/1'
# output_large_class_dir = 'C:/Users/user/Desktop/1023_증강위해 데이터 수정/a1'
# input_large_class_labels_dir = 'C:/Users/user/Desktop/1023_증강위해 데이터 수정/1_label' # 라벨 디렉토리
# augment_images(input_large_class_dir, output_large_class_dir, input_large_class_labels_dir, augmentation_large_class)

