import cv2 #---using AI for computer vision
from cvzone.HandTrackingModule import HandDetector #--- for detecting hand movements
from time import sleep #to prevent clicking more than once
import numpy as np #to make buttons transclucent
import cvzone #turning cam on

'''
Versions : 

mediapipe == 0.8.8
cvzone == 1.4.1

'''


cap = cv2.VideoCapture(0) 

#size of window
cap.set (3, 1280)
cap.set (4, 720)


detector = HandDetector(detectionCon = 0.8)

#nested list

keys = [["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["(", "0", ")"]]


#variables  

finalText = ""
evalText = ""
tempText = ""
errorText = ""
eraseText = ""
space = " "
buttonList = []


#drawing all buttons - numpy 

def drawAll(img, smallbuttonList) :

    # cv2.rectangle(img, (0,0), (1280 , 720), (87,28,0), cv2.FILLED)

    imgNew = np.zeros_like(img, np.uint8)

    cvzone.cornerRect(imgNew, (800 + 75, 50, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(800 + 75,50), (885 + 75, 135), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "+", (800 + 20 + 75, 50 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (800 + 75, 150, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(800 + 75,150), (885 + 75, 235), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "-", (800 + 20 + 75, 150 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)
    
    cvzone.cornerRect(imgNew, (800 + 75, 250, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(800 + 75,250), (885 + 75, 335), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "x", (800 + 20 + 75, 250 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (800 + 75, 350, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(800 + 75,350), (885 + 75, 435), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "/", (800 + 20 + 75, 350 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (400 + 75, 250, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(400 + 75,250), (485 + 75, 335), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "^", (400 + 20 + 75, 250 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (400 + 75, 50, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(400 + 75,50), (485 + 75, 135), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "%", (400 + 20 + 75, 50 + 55), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (400 + 75, 150, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(400 + 75,150), (485 + 75, 235), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "//", (400 + 10 + 75, 150 + 55), cv2.FONT_HERSHEY_PLAIN, 3, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (400 + 75, 350, 85, 85),20, rt=0)
    cv2.rectangle(imgNew ,(400 + 75,350), (485 + 75, 435), (139,0,0), cv2.FILLED)
    cv2.putText(imgNew, "-->", (400 + 10 + 75, 350 + 55), cv2.FONT_HERSHEY_PLAIN, 2, (230,216,173), 3)

    cvzone.cornerRect(imgNew, (1100, 350, 140, 85),20, rt=0)
    cv2.rectangle(imgNew ,(1100,350), (1240, 435), (0,255,255), cv2.FILLED)
    cv2.putText(imgNew, "=", (1100 + 50, 350 + 60), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,173), 3)

    cvzone.cornerRect(imgNew, (1100, 202, 140, 85),20, rt=0)
    cv2.rectangle(imgNew ,(1100,202), (1240, 287), (0,255,255), cv2.FILLED)
    cv2.putText(imgNew, "C", (1100 + 48, 202 + 65), cv2.FONT_HERSHEY_COMPLEX, 2, (0,0,173), 3)

    cvzone.cornerRect(imgNew, (1100, 50, 140, 85),20, rt=0)
    cv2.rectangle(imgNew ,(1100,50), (1240, 135), (0,255,255), cv2.FILLED)
    cv2.putText(imgNew, "Exit", (1100 + 13, 110), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,173), 3)


    for button in buttonList :
        x , y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),20, rt=0)
        cv2.rectangle(imgNew ,button.pos, (x + button.size[0], y + button.size[1]), (139,0,0), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 36 , y + 61), cv2.FONT_HERSHEY_COMPLEX, 2, (230,216,173), 3)
    

    #making buttons transluscent

    out = img.copy()
    alpha = 0
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out



class Button() :
    def __init__(self , pos , text , size = [85,85]) :
        self.pos = pos
        self.size = size
        self.text = text


for i in range (len(keys)) :
    for j , key in enumerate(keys [i]) :
        buttonList.append(Button([j*100+500+75,100*i+50], key))


while True :

    success, img = cap.read()
    img = cv2.flip(img,1) #flipping on x-axis
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonList)


    cv2.rectangle(img, (0 , 0), (330 , 480), (52,7,21), cv2.FILLED)
    cv2.rectangle(img, (0 , 480), (1280 , 720), (52,7,21), cv2.FILLED)


    if lmList :
        l,_, _ = detector.findDistance(8,4, img, draw = False)
        if l < 40 :
            if evalText == "" :
                if eraseText == "" :

                    if 800 + 75< lmList[8][0] < 885 + 75 and 50 < lmList [8][1] < 135 :   
                        cv2.rectangle(img,(800 + 75 , 50), (885 + 75, 135), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "+", (870 + 75, 110), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
                        finalText += "+"
                        tempText += "+"
                        sleep(1)
                    
                    if 800 + 75 < lmList[8][0] < 885 + 75 and 150 < lmList [8][1] < 235 :   
                        cv2.rectangle(img,(800 + 75 , 150), (885 + 75, 235), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "-", (870 + 75, 210), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
                        finalText += "-"
                        tempText += "-"
                        sleep(1)
                    
                    if 800 + 75 < lmList[8][0] < 885 + 75 and 250 < lmList [8][1] < 335 :   
                        cv2.rectangle(img,(800 + 75 , 250), (885 + 75, 335), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "x", (870 + 75, 310), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
                        finalText += "x"
                        tempText += "*"
                        sleep(1)

                    if 800 + 75 < lmList[8][0] < 885 + 75 and 350 < lmList [8][1] < 435 :   
                        cv2.rectangle(img,(800 + 75, 350), (885 + 75, 435), (0,255,0), cv2.FILLED)
                        cv2.putText(img, "/", (870 + 75, 410), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
                        finalText += "/"
                        tempText += "/"
                        sleep(1)

                    if 400 + 75 < lmList[8][0] < 485 + 75 and 50 < lmList [8][1] < 135 :
                        cv2.rectangle(img ,(400 + 75,50), (485 + 75, 135), (139,0,0), cv2.FILLED)
                        cv2.putText(img, "%", (400 + 30  + 75, 50 + 55), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
                        finalText += "%"
                        tempText += "%"
                        sleep(1)

                    if 400 + 75 < lmList[8][0] < 485 + 75 and 250 < lmList [8][1] < 335 :
                        cv2.rectangle(img ,(400 + 75,250), (485 + 75, 335), (139,0,0), cv2.FILLED)
                        cv2.putText(img, "^", (400 + 20 + 75, 250 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (230,216,173), 3)
                        finalText += "^^"
                        tempText += "**"
                        sleep (1)


                    if 400 + 75 < lmList[8][0] < 485 + 75 and 150 < lmList [8][1] < 225 :
                        cv2.rectangle(img ,(400 + 75,150), (485 + 75, 235), (139,0,0), cv2.FILLED)
                        cv2.putText(img, "//", (400 + 10 + 75 , 150 + 55), cv2.FONT_HERSHEY_PLAIN, 3, (230,216,173), 3)
                        finalText += "//"
                        tempText += "//"
                        sleep(1)

                else :
                    cv2.putText(img, "Clear First !", (825 , 550), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,255), 2)
            else : 
                cv2.putText(img, "Clear First !", (825 , 550), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,255), 2)

    
            if 1100 < lmList[8][0] < 1240 and 375 < lmList [8][1] < 460 :
                cv2.rectangle(img ,(1100,350), (1240, 435), (0,255,255), cv2.FILLED)
                cv2.putText(img, "=", (1100 + 50, 375 + 65), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 3)

                try :
                    evalText = str(eval(tempText)) #evaluating text
                    sleep(1)
                except Exception as e :
                    errorText = "Invalid Syntax !"
                    cv2.putText(img, errorText, (780 , 640), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,255), 2)
                    eraseText += "0"
                    sleep(1)


            if 1100 < lmList[8][0] < 1240 and 202 < lmList [8][1] < 287 :
                cv2.rectangle(img ,(1100,202), (1240, 287), (0,255,255), cv2.FILLED)
                cv2.putText(img, "C", (1100 + 52, 202 + 65), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 3)
                finalText = ""
                tempText = ""
                evalText = ""
                eraseText = ""

            if 1100 < lmList[8][0] < 1240 and 50 < lmList [8][1] < 135 :
                cv2.rectangle(img ,(1100,50), (1240, 135), (0,255,0), cv2.FILLED)
                cv2.putText(img, "Exit", (1100 + 13, 110), cv2.FONT_HERSHEY_PLAIN, 1.5, (238,244,21), 3)
                break

            if 400 + 75 < lmList[8][0] < 485 + 75 and 350 < lmList [8][1] < 435 : 
                cv2.rectangle(img ,(400 + 75,350), (485 + 75, 435), (139,0,0), cv2.FILLED)
                cv2.putText(img, "-->", (400 + 10 + 75 , 350 + 55), cv2.FONT_HERSHEY_PLAIN, 2, (230,216,173), 3)
                finalText = finalText[0:(len(finalText))-1]
                tempText = tempText[0:(len(tempText))-1]
                sleep(1)


        for button in buttonList :
            x , y = button.pos
            w , h = button.size

            if 1100 < lmList[8][0] < 1240 and 350 < lmList [8][1] < 435 :   
                cv2.rectangle(img ,(1100,350), (1240, 435), (169,0,0), cv2.FILLED)
                cv2.putText(img, "=", (1100 + 50, 350 + 60), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 3)

            if 800 + 75 < lmList[8][0] < 885 + 75 and 50 < lmList [8][1] < 135 :
                cv2.rectangle(img ,(800 + 75 , 50), (890 + 75, 140), (169,0,0), cv2.FILLED)
                cv2.putText(img, "+", (820 + 75, 110), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)

            if 800 + 75 < lmList[8][0] < 885 + 75 and 150 < lmList [8][1] < 235 :
                cv2.rectangle(img ,(800 + 75 , 150), (890 + 75, 240), (169,0,0), cv2.FILLED)
                cv2.putText(img, "-", (820 + 75, 210), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)

            if 800 + 75 < lmList[8][0] < 885 + 75 and 250 < lmList [8][1] < 335 :
                cv2.rectangle(img ,(800 + 75 , 250), (890 + 75, 340), (169,0,0), cv2.FILLED)
                cv2.putText(img, "x", (820 + 75, 310), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)

            if 800 + 75 < lmList[8][0] < 885 + 75 and 350 < lmList [8][1] < 435 :
                cv2.rectangle(img ,(800 + 75 , 350), (890 + 75, 440), (169,0,0), cv2.FILLED)
                cv2.putText(img, "/", (820 + 75, 410), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)

            if 400 + 75 < lmList[8][0] < 485 + 75 and 250 < lmList [8][1] < 335 :
                cv2.rectangle(img ,(400 + 75,250), (485 + 75, 335), (169,0,0), cv2.FILLED)
                cv2.putText(img, "^", (400 + 20 + 75, 250 + 63), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 3)

            if 400 + 75 < lmList[8][0] < 485 + 75 and 150 < lmList [8][1] < 225 :
                cv2.rectangle(img ,(400 + 75,150), (485 + 75, 235), (169,0,0), cv2.FILLED)
                cv2.putText(img, "//", (400 + 10 + 75, 150 + 55), cv2.FONT_HERSHEY_PLAIN, 3, (238,244,21), 3)

            if 400 + 75 < lmList[8][0] < 485 + 75 and 50 < lmList [8][1] < 135 :
                cv2.rectangle(img ,(400 + 75,50), (485 + 75, 135), (139,0,0), cv2.FILLED)
                cv2.putText(img, "%", (400 + 30 + 75, 50 + 55), cv2.FONT_HERSHEY_PLAIN, 4, (238,244,21), 4)
   
            if 400 + 75 < lmList[8][0] < 485 + 75 and 350 < lmList [8][1] < 435 : 
                cv2.rectangle(img ,(400 + 75,350), (485 + 75, 435), (139,0,0), cv2.FILLED)
                cv2.putText(img, "-->", (400 + 10 + 75, 350 + 55), cv2.FONT_HERSHEY_PLAIN, 2, (230,216,173), 3)

            if 1100 < lmList[8][0] < 1240 and 202 < lmList [8][1] < 287 :
                cv2.rectangle(img ,(1100,202), (1240, 287), (139,0,0), cv2.FILLED)
                cv2.putText(img, "C", (1100 + 48, 202 + 65), cv2.FONT_HERSHEY_COMPLEX, 2, (230,216,173), 3)

            if 1100 < lmList[8][0] < 1240 and 50 < lmList [8][1] < 135 :
                cv2.rectangle(img ,(1100,50), (1240, 135), (139,0,0), cv2.FILLED)
                cv2.putText(img, "Exit", (1100 + 13, 110), cv2.FONT_HERSHEY_COMPLEX, 1.5, (238,244,21), 3)

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h :
                cv2.rectangle(img ,button.pos, (x + button.size[0] + 5, y + button.size[1] + 5), (169,0,0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_COMPLEX, 2, (238,244,21), 4)
                l,_, _ = detector.findDistance(8,4, img, draw = False)


                #when clicked
                if l < 40 : 
                    if evalText == "" :
                        if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h :
                            cv2.rectangle(img,button.pos, (x + w, y + h), (0,255,0), cv2.FILLED)
                            cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_COMPLEX, 4, (238,244,21), 4)
                            finalText += button.text
                            tempText += button.text
                            sleep (1)
                    else :
                        cv2.putText(img, "Clear First !", (825 , 550), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255,255,255), 2)
            

    #Instructions text

    cv2.putText(img, "Instructions", (50 , 50 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 2)
    cv2.rectangle(img, (60 , 80 + 20), (240 , 80 + 20), (206,227,150), cv2.FILLED)
    cv2.putText(img, "Hover index", (20 , 130 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.putText(img, "finger in front", (20 , 165 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.putText(img, "of buttons.", (20 , 200 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.rectangle(img, (60 , 230 + 20), (240 , 230 + 20), (206,227,150), cv2.FILLED)
    cv2.putText(img, "To click,", (20 , 280 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.putText(img, "bring your index", (20 , 315 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.putText(img, "finger close to", (20 , 350 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.putText(img, "your thumb", (20 , 380 + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (206,227,150), 1)
    cv2.rectangle(img, (60 , 410 + 20), (240 , 410 + 20), (206,227,150), cv2.FILLED)


    #displaying working text and final answer

    cv2.putText(img, finalText, (30 , 570), cv2.FONT_HERSHEY_COMPLEX, 3, (206,227,150), 3)
    cv2.putText(img, "=" + evalText, (30 , 670), cv2.FONT_HERSHEY_COMPLEX, 3, (206,227,150), 3)   
    

    cv2.imshow("Image" , img)
    cv2.waitKey(1)
    
