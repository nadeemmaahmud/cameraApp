import cv2

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    cv2.imshow("Output", frame)

    if cv2.waitKey(10) == ord('c'):
        cv2.imwrite("/Users/nadimmahmud/Documents/Coding/Phitron/basicCameraApp/myCaps/cameraPy.jpg", frame)
        print("Image saved!")

    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()