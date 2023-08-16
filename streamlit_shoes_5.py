import streamlit as st
from PIL import Image
import numpy as np
import subprocess
import re
import torch

def extract_labels(output):
    pattern = r'\b(\d+)\s+(\w+)\b'
    matches = re.findall(pattern, output)
    detected_labels = []

    for num_labels, label_name in matches:
        detected_labels.extend([label_name] * int(num_labels))

    return detected_labels

# 등급을 결정하기 위한 로직
def determine_grade(labels):
    num_pollution = labels.count('pollutions')
    num_wrinkle = labels.count('wrinkle')
    num_damaged = labels.count('damageds')

    if num_pollution + num_wrinkle + num_damaged == 0:
        return 'A'
    elif num_pollution + num_wrinkle + num_damaged <= 2:
        return 'B'
    else:
        return 'C'

def main():
    st.title("Object Detection using YOLOv5")

    # 이미지 업로드
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "png"])
    

    if uploaded_image is not None:
        image_filename = uploaded_image.name
        image_path = f"/content/{image_filename}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())
        
        command = [
            "python", "/content/drive/MyDrive/shoes/yolov5/detect.py",  # Update this path
            "--weights", "/content/drive/MyDrive/shoes/yolov5/runs/train/shoes2/weights/best.pt",  # Update this path
            "--source", image_path
        ]

        # subprocess를 사용하여 명령 실행
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()

        # 결과 출력
        result_output = stdout.decode("utf-8")

        labels = extract_labels(result_output)

        # 등급 출력
        predicted_grade = determine_grade(labels)

        # 결과 및 등급 출력
        # st.text("결과 출력:")
        # st.text(result_output)

        st.text("감지된 레이블:")
        st.text(labels)

        # st.text(f"예측 등급: {predicted_grade}")

        if predicted_grade == 'A':
            st.success(f"예측 등급: {predicted_grade} 😎")
        elif predicted_grade == 'B':
            st.warning(f"예측 등급: {predicted_grade} 😢")
        else:
            st.error(f"예측 등급: {predicted_grade} 😠")

        

        
        # 경로 추출을 위한 정규표현식
        pattern = r"Results saved to (.*?)$"
        match = re.search(pattern, result_output, re.MULTILINE)

        if match:
            saved_path = match.group(1)
            # st.text(f"Saved path: {saved_path}")
        else:
            st.text("Saved path not found in the output.")




        pattern = r'\x1b\[1m(.+?)\x1b\[0m'
        match = re.findall(pattern, saved_path)
        # st.text(match)
        image_filename = uploaded_image.name
        image_path = match[0] + '/' + image_filename
        
        # detect 이미지 표시
        st.image(image_path, caption="detect predict", use_column_width=True)


if __name__ == "__main__":
    main()