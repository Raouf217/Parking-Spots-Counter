import cv2
import pickle

#to draw 12 rec in one click
twelve = False
#box width
width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        positions = pickle.load(f)
except:
    positions = []


def mouseclick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if twelve:
            for i in range(12):
                positions.append((x, y+height*i))
        else:positions.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(positions, f)


while True:
    img = cv2.imread('./Images/carParkImg.png')

    for pos in positions:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.putText(img,str(twelve),(50,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
    cv2.imshow("Image", img)
    cv2.setMouseCallback('Image', mouseclick)
    k=cv2.waitKey(1) & 0xFF
    if k==ord('e'):
        for i in range(12):
            if positions:
                positions.pop()
    if k==ord('2'):
        twelve = not twelve
    if k == ord('q'):
        break
cv2.destroyAllWindows()
