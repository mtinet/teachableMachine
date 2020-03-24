# teachableMachine

## 1. python_local_converted_keras  
### 파이썬에 tensorflow, keras, PIL(pillow), numpy, cv2, serial 라이브러리를 설치해 사용함  
- 로컬에서 웹캠 영상을 가져와서 학습된 모델에 있는 레이블의 비율로 데이터를 출력함  
- tensorflow는 아직 3.7까지만 지원을 하므로, 파이썬을 3.7버전으로 설치해야 함  
- 그 외 오류는 오류나는 부분을 카피해서 구글에 물어보면 해답을 얻을 수 있음  
- PIL을 설치할 때는 pip install pillow로 설치를 해야함  
- serial을 설치할 때는 pip install pyserial로 설치를 해야함
- cv2는 pip install opencv-python로 설치해야 함  

OpenCV의 main module만 사용한다면 아래처럼 설치
```{.python} 
pip install opencv-python
```
만약 main module과 extra module을 같이 사용하고 싶다면 아래처럼 설치합니다.
```{.python} 
pip install opencv-contrib-python  
```

### 파일 구동은 아래 명령어로 하면 됨, 프로그램 정지는 'q'버튼  
```{.python}  
$python video.py  
```  
### 그 외 파일들의 기능은 다음과 같다.  
- keras_model.h5 : teachable machine 홈페이지에서 Export한 모델파일, 이 파일이 머신러닝 학습의 결과이며, 이 파일을 이용해 학습된 내용을 활용함, 현재는 파란색, 흰색, 초록색을 구분하는 모델파일이 올라가 있음  
- labels : 모델을 만들 때 레이블을 몇개로 해 학습을 시켰느냐에 따라 다양한 반응을 낼 수 있음  
- image : 사진 한 장으로 모델 파일을 구동해 추론한 결과를 확인할 수 있는 파이썬 파일  
- imageResize : cv2를 이용해 이미지 사이즈를 바꾸는 예제, teachable machine에서 카피해서 만든 image 파일은 PIL(pillow)를 사용해 이미지 사이즈를 변경하는데 이것이 영상을 처리할 때는 오류를 내기 때문에 영상을 추론하는 최종 파일인 video.py파일은 cv2로 이미지 사이즈를 변경하는 방법을 적용해야 했음  
- video : 학습된 모델 파일로 웹캠에서 입력되는 영상을 분석하여 추론해주는 파일, 이 파일이 이 프로젝트의 핵심, 추후 라즈베리파이에 탑재해서 로봇을 제어하는데 사용할 예정  
- video_record : 웹캠으로 들어오는 영상을 녹화하는 프로그램  
- outpy.avi : video_record 파일을 실행하면 만들어지는 녹화영상  
- image 폴더 : image 파일이 구동될 때 사용하는 이미지가 들어있는 폴더  
- dataReceive.ino : 학습된 데이터를 기반으로 추론한 결과가 특정 퍼센티지를 넘을 때 바이트 형태의 데이터를 전송하는데, 그 때 아두이노에서 데이터가 잘 받아지는지를 확인하는 코드, 'a'가 바이트의 형태로 잘 넘어오면 13번 핀(또는 칩LED)가 점멸함  
- 2 situations_coke : 펩시 콜라 캔을 웹캠의 좌우로 이동하는 것을 학습한 모델파일이 들어 있음  
- 3 situations_coke, motordriver, CD case : 펩시콜라캔, 마이크로비트 모터 드라이버, 초록, 녹색의 색이 들어가있는 CD 케이스로 학습한 모델파일이 들어 있음(이 안의 파일을 기본파일로 폴더 바깥쪽에 복사해놓았으며, 콜라 캔을 좌우로 이동하는 화면을 추론하는 모델을 사용하려면 위의 폴더에 들어있는 모델파일과 레이블 파일을 바깥으로 카피해 놓으면 됨  

## 2. web  
### github에 올려놓는 버전과 파이썬으로 로컬서버를 만들어 구동하는 버전으로 나뉘어 있음
### 이 안에 있는 index.html파일은 서버로 구축되지 않고 그냥 파일만 실행했을 때에는 동작하지 않음  
#### github server  
- image_green_black : 녹색과 검정색의 이미지를 구분하는 모델이 들어있음  
[https://mtinet.github.io/teachableMachine/web/github%20server/image_green_black/](https://mtinet.github.io/teachableMachine/web/github%20server/image_green_black/)  
- pose_left_right_hand : 왼손과 오른손의 포즈를 구분하는 모델이 들어있음  
[https://mtinet.github.io/teachableMachine/web/github%20server/pose_left_right_hand/](https://mtinet.github.io/teachableMachine/web/github%20server/pose_left_right_hand/)  
#### python server  
- 해당 파일이 있는 폴더로 이동해서 아래 명령어로 파이썬 서버를 구동하고 브라우저로 localhost:8080에 접속하면 자동으로 구동됨  
```{.python}  
$python app.py  
```  
- 왼손을 드는 포즈와 오른손을 드는 포즈로 학습된 모델임  
- 모델파일은 my_model폴더에 들어 있음  
- 웹 기반 모델은 python을 기반으로 하는 tensorflow, keras 라이브러리를 사용하지 않으며, tensorflow.js를 사용하고, 모델파일과 메타데이타파일은 json파일로, 웨이트 파일은 바이너리파일로 되어 있다.  
