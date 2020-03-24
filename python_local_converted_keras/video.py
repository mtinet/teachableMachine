import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import serial

#setup serial communication
ser = serial.Serial(
    # check your Serial port
    # port='/dev/cu.usbmodem141201',
    port='COM17',
    baudrate=9600,
)

np.set_printoptions(suppress=True)

model = tensorflow.keras.models.load_model('keras_model.h5')

data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

cap = cv2.VideoCapture(0)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)

    image = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data[0] = normalized_image_array

    prediction = model.predict(data)

    # print(type(prediction))
    print(prediction)

    # numpy.ndarray로 되어 있는 prediction을 분해하는 방법
    # print(prediction[:, 0])
    # print(prediction[:, 1])
    # print(prediction[:, 2])

    if prediction[:, 0] > 0.7 :
        send = (str('a')+'\n').encode("utf-8")
        ser.write(send)
        print(send)

    if prediction[:, 1] > 0.7 :
        send = (str('b')+'\n').encode("utf-8")
        ser.write(send)
        print(send)

    if prediction[:, 2] > 0.7 :
        send = (str('c')+'\n').encode("utf-8")
        ser.write(send)
        print(send)


    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
