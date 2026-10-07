import cv2, os

cap = cv2.VideoCapture(0)
os.system("\033[2J\033[H\033[40m\033[37m")

SHADES = " .,:;irsXA253hMHGS#9B&@"

while True:
    ok, frame = cap.read()
    if not ok:
        break

    gray = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    width = 160
    height = int(gray.shape[0] / gray.shape[1] * width * 0.46)
    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_AREA)

    gray = cv2.equalizeHist(gray)
    gray = cv2.convertScaleAbs(gray, alpha=1.35, beta=-25)

    lines = [
        "".join(SHADES[int(p) * len(SHADES) // 256] for p in row)
        for row in gray
    ]

    print("\033[H" + "\n".join(lines), end="")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("\033[0m")
