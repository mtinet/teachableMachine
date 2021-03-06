# python 홈페이지로 가서 python 3.7버전을 설치함, 최신버전을 설치하면 tensorflow 라이브러리가 설치가 되지 않으니 주의할 것
# python의 pip로 tensorflow, PIL, numpy, cv2, serial을 설치함
# windows의 cmd 창을 열어 설치하면 되며, 순서대로 설치하는 명령어는 다음과 같음
# pip install tensorflow
# pip install pillow
# pip install numpy
# pip install opencv-python
# OpenCV의 확장 모듈을 설치하려면 pip install opencv-contrib-python
# pip install pyserial

# 모두 설치가 되면 아래 import가 정상적으로 동작할 것임

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import serial

# 시리얼 통신 설정
# 파이썬의 시리얼 통신 라이브러리를 이용해 시리얼 통신을 연결하고 이를 사용할 때 ser로 사용할 수 있도록 변수를 지정함
ser = serial.Serial(
    # 시리얼 포트 체크
    # 아래는 맥에서의 시리얼 포트 설정방법임, 사용하려면 주석을 해제함
    # port='/dev/cu.usbmodem141201',

    # 아래는 윈도우에서의 시리얼 포트 설정방법임, 포트번호는 사용자의 아두이노나 마이크로비트가 연결된 포트번호로 수정해줘야 함
    port='COM17',
    # 통신속도는 9600bps, 이게 디폴트임.
    baudrate=9600,
)

# e-04와 같은 scientific notation을 제거하고 싶을 때 사용하는 옵션
np.set_printoptions(suppress=True)

# Teachable Machine에서 학습시킨 모델 파일을 모델 파일을 model 변수에 넣음
model = tensorflow.keras.models.load_model('keras_model.h5')

# numpy를 이용해 이미지를 1차원, 높이 224pixel, 폭 224pixel, 색상 3채널(RGB)로 변환해서 data 변수에 넣음, 형식은 float32, 여기서는 data 변수를 만드는 의미로 쓰임
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# OpenCV를 이용해 캠으로 들어오는 영상을 cap 변수에 넣음, '0'은 컴퓨터가 인식한 첫번째 카메라를 의미함
cap = cv2.VideoCapture(0)


# while문 안의 내용을 계속 반복시킴. 캠에서 영상 프레임이 들어올 때마다 아래 프로그램을 실행함
while(True):
    # cap 변수에 비디오 프레임이 들어올 때마다 읽어서 frame 변수에 넣음, 제대로 프레임이 읽어지면 ret값이 True, 실패하면 False가 나타남
    ret, frame = cap.read()

    # frame 변수에 들어있는 비디오 프레임을 'frame'라는 이름의 창을 만들고 보여줌
    cv2.imshow('frame',frame)

    # 바이큐빅보간법(cv2.INTER_CUBIC, 이미지를 확대할 때 주로 사용)을 이용해 frame변수에 들어온 비디오 프레임의 사이즈를 224, 224로 변경하여 image 변수에 넣음
    image = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    # asarray메소드를 이용해 image에 들어있는 크기가 변형된 이미지를 numpy가 처리할 수 있는 배열로 만들어서 image_array 변수에 넣음
    image_array = np.asarray(image)

    # image_array에 들어있는 image의 변형된 배열을 정규화(normalized)하기 위해 수식을 적용함
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # 정규화된 배열을 data[0]에 넣음
    data[0] = normalized_image_array

    # 정규화된 배열값으로 정돈된 data를 Teachable Machine으로 학습시켜서 얻은 모델을 이용해 추론하고, 그 결과를 prediction 변수에 넣음
    prediction = model.predict(data)

    # prediction 변수에 들어 있는 값을 화면에 띄움, 만들어진 모델의 label 갯수 만큼의 리스트로 출력됨, 학습시킬 때 Class를 많이 나눌 수록 label이 많아짐
    # print(type(prediction))
    print(prediction)

    # numpy.ndarray로 되어 있는 prediction을 분해하는 방법
    # print(prediction[:, 0])
    # print(prediction[:, 1])
    # print(prediction[:, 2])

    # prediction의 첫번째 리스트값이 0.7을 넘으면 'a'를 utf-8 형태로 인코딩하여 시리얼 통신으로 송신함
    # 학습을 시킬 때는 반드시 디폴트 이미지를 학습시키는 것이 오류를 예방할 수 있는 지름길임
    if prediction[:, 0] > 0.7 :
        # 'a'를 utf-8 형식으로 인코딩 하여 send 변수에 넣음
        send = (str('a')+'\n').encode("utf-8")
        # send 변수에 들어있는 값을 시리얼통신으로 송신함
        ser.write(send)
        # 송신이 되면 화면에 send 변수에 들어가 있는 값을 출력함
        print(send)

    # prediction의 두번째 리스트값이 0.7을 넘으면 'b'를 utf-8 형태로 인코딩하여 시리얼 통신으로 송신함
    if prediction[:, 1] > 0.7 :
        send = (str('b')+'\n').encode("utf-8")
        ser.write(send)
        print(send)

    # prediction의 세번째 리스트값이 0.7을 넘으면 'c'를 utf-8 형태로 인코딩하여 시리얼 통신으로 송신함
    if prediction[:, 2] > 0.7 :
        send = (str('c')+'\n').encode("utf-8")
        ser.write(send)
        print(send)

    # 'q'버튼을 누르면 프로그램이 종료됨
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# 동작이 종료되면 비디오 프레임 캡쳐를 중단함
cap.release()
# 모든 창을 닫음
cv2.destroyAllWindows()
