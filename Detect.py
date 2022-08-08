import cv2
import pickle
import numpy as np


try:
    with open('CarParkPos', 'rb') as f:
        positions = pickle.load(f)
except:
    positions = []

width, height = 107, 48
cap = cv2.VideoCapture('carPark.mp4')

s=[]
def checkplace(img):
    global s
    free_spaces = 0
    for i, pos in enumerate(positions):
        x, y = pos
        imgCrop = img[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)
            thickness = 5
            free_spaces += 1
            cv2.putText(frame, f'{i} is free', (x, y+height-3), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,250,0), 2)
            s.append(i)

        else:
            color = (0, 0, 255)
            thickness = 2
            cv2.putText(frame, f'{i} busy', (x, y+height-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            if s:
                if i in s:
                    s.remove(i)

        cv2.rectangle(frame, pos, (pos[0] + width, pos[1] + height), color, thickness)
    cv2.putText(frame, f'Free: {free_spaces}/{len(positions)}', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,250,0), 2)


while True:
    _, frame = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkplace(imgDilate)

    cv2.imshow('Image', frame)

    k=cv2.waitKey(1) & 0xFF
    if k == ord('s'):
        s.clear()
        checkplace(imgDilate)
        print(f'[{len(s)}] spots are empty')

    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
