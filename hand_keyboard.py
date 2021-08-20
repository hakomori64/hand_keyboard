import cv2
from time import time, sleep
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280) 
cap.set(4, 720)

text = ""
detector = HandDetector(detectionCon=0.5, maxHands=1)
keys = [
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']
]

delay = 0
MAX_DELAY = 0.3

def draw_all(img, button_list):
    for button in button_list:
        img = button.draw(img, (80, 80, 80), (255, 255, 255))
    
    return img

class Button():
    def __init__(self, pos, text, size = (70, 70)):
        self.pos = pos
        self.size = size
        self.text = text
    
    def draw(self, img, background_color, font_color):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x + w, y + h), background_color, cv2.FILLED)
        cv2.putText(img, self.text, (x + 25, y + 50), cv2.FONT_HERSHEY_PLAIN, 2, font_color, 2)

        return img

button_list = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button((100 * j + 50, 100 * i + 50), key))

while True:
    start = time()
    success, img = cap.read()
    h, w, c = img.shape
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)

    img = draw_all(img, button_list)

    if lmList:
        for button in button_list:
            x, y = button.pos
            w, h = button.size

            if (x <= lmList[8][0] < x + w and
                y <= lmList[8][1] < y + h):
                img = button.draw(img, (40, 40, 40), (255, 255, 255))

                if delay <= 0:
                    l, _, _ = detector.findDistance(4, 12, img, draw=False)

                    if l < 80:
                        img = button.draw(img, (20, 20, 20), (255, 255, 255))
                        text += button.text
                        delay = MAX_DELAY

            if delay <= 0:        
                l, _, _ = detector.findDistance(4, 8, img, draw=False)

                if l < 80:
                    text = text[:-1]
                    delay = MAX_DELAY
    
    h, w, c = img.shape
    print(h, w, c)
    img = Button((20, h - 150), text, size=(w - 100, 100)).draw(img, (0, 0, 0), (255, 255, 255))

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    delay -= (time() - start)