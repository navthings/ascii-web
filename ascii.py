import cv2
import os

cap = cv2.VideoCapture(0)

os.system("\033[2J\033[H")

SHADES = " .,:;irsXA253hMHGS#9B&@"

while True:
    ok, frame = cap.read()

    if not ok:
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Keep colour frame for ANSI colours
    colour = frame.copy()

    # Greyscale only controls which ASCII character is used
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    width = 160
    height = int(gray.shape[0] / gray.shape[1] * width * 0.46)

    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_AREA)
    colour = cv2.resize(colour, (width, height), interpolation=cv2.INTER_AREA)

    gray = cv2.equalizeHist(gray)
    gray = cv2.convertScaleAbs(gray, alpha=1.35, beta=-25)

    output = []

    for y in range(height):
        line = []

        for x in range(width):
            brightness = gray[y, x]

            # Brightness chooses the ASCII character
            char = SHADES[int(brightness) * len(SHADES) // 256]

            # Original pixel chooses the text colour
            b, g, r = colour[y, x]

            # ANSI truecolour foreground
            line.append(
                f"\033[38;2;{r};{g};{b}m{char}"
            )

        output.append("".join(line))

    print("\033[H" + "\n".join(output), end="")

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

# Reset terminal colours
print("\033[0m")