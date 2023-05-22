import cv2
import mediapipe as mp
import numpy as np
import PoseModule as pm
1
cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
recount = 0
direction = 0
form = 0
feedback = "Fix Form"

push = 1
squat = 2
choice = int(input('Enter your workout routine : '))

while cap.isOpened():
    ret, img = cap.read()  # 640 x 480
    # Determine dimensions of video - Help with creation of box in Line 43
    width = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)

    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        l_elbow = detector.findAngle(img, 11, 13, 15)
        l_shoulder = detector.findAngle(img, 13, 11, 23)
        l_hip = detector.findAngle(img, 11, 23, 25)
        r_elbow = detector.findAngle(img,12,14,16)
        r_shoulder = detector.findAngle(img,14,12,24)
        r_hip = detector.findAngle(img,12,24,26)
        l_knee = detector.findAngle(img, 23, 25, 27)
        r_knee = detector.findAngle(img, 24, 26, 28)


        if choice == 1:
            # Percentage of success of pushup
            per = np.interp(l_elbow, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(l_elbow, (90, 160), (380, 50))

            # Check to ensure right form before starting the program
            if l_elbow or r_elbow > 160 and l_shoulder or r_shoulder > 40 and l_hip or r_hip > 160:
                form = 1


            # Check for full range of motion for the pushup
            if form == 1:
                if per == 0:
                    if l_elbow or r_elbow <= 90 and l_hip or r_hip > 160:
                        feedback = "Up"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                    else:
                        feedback = "Fix Form"
                        recount += 1

                if per == 100:
                    if l_elbow or r_elbow > 160 and l_shoulder or r_shoulder > 40 and l_hip or r_hip > 160:
                        feedback = "Down"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                    else:
                        feedback = "Fix Form"
                        recount += 1
                        # form = 0

            print(count, recount)



        elif choice == 2:
            per = np.interp(l_knee, (90, 160), (0, 100))
            per1 = np.interp(l_hip, (90, 160), (0, 100))

            # Bar to show Pushup progress
            bar = np.interp(l_knee, (90, 160), (380, 50))
            # bar1 = np.interp(l_hip, (90, 160), (380, 50))
            # Check to ensure right form before starting the program
            # if l_elbow or r_elbow > 160 and l_shoulder or r_shoulder > 40 and l_hip or r_hip > 160:
            #     form = 1
            # elif l_elbow or r_elbow < 180 and l_elbow or r_elbow >30:
            #     form = 2

            # Check for full range of motion for the pushup
            # if form == 1:
            if per == 0:
                if l_hip or r_hip <= 180 and l_knee or r_knee <= 180:  # and l_elbow or r_elbow >=90
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1
                else:
                    feedback = "Fix Form"
                    recount += 1

            if per == 100:
                if l_hip or r_hip <= 70 and l_knee or r_knee >= 55:  # and l_elbow or r_elbow >=90
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0
                else:
                    feedback = "Fix Form"
                    recount += 1
                    # form = 0
                print(count, recount)

            cv2.putText(img, 'BICEP CURL', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)
        # if form == 2:
        #     if per == 0:
        #         if l_elbow or r_elbow <= 180:
        #             feedback = 'Straight'
        #             if direction == 0:
        #                 count += 0.5
        #                 direction = 1
        #         else:
        #             feedback = 'Fix Posture'
        #             recount += 1
        #
        #     if per == 100:
        #         if l_elbow or r_elbow >= 30:
        #             feedback = 'Bend'
        #             if direction == 1:
        #                 count += 0.5
        #                 direction = 0
        #         else:
        #             feedback = 'Fix Posture'
        #             recount += 1

        # Draw Bar


        # if form == 2:
        #     cv2.putText(img, 'BICEP CURL', (0, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        #     cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
        #     cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
        #                 (255, 0, 0), 2)

        # Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        cv2.rectangle(img, (100, 380), (200, 480), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, str(int(recount)), (125, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 255, 255), 5)

        # Feedback
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)


    cv2.imshow('Pushup counter', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()