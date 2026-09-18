import cv2
from cvzone.HandTrackingModule import HandDetector


# =========================================================
# INITIALIZE WEBCAM
# =========================================================

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

if not cap.isOpened():
    print("❌ Cannot open webcam")
    exit()


# =========================================================
# HAND DETECTOR
# =========================================================

detector = HandDetector(
    detectionCon=0.8,
    maxHands=1
)


# =========================================================
# DEFINE 5 RECTANGLES
# [center_x, center_y, width, height, color]
# =========================================================

rectangles = [
    [200, 200, 150, 150, (255, 0, 255)],
    [500, 200, 150, 150, (255, 0, 255)],
    [800, 200, 150, 150, (255, 0, 255)],
    [350, 400, 150, 150, (255, 0, 255)],
    [700, 400, 150, 150, (255, 0, 255)],
]


# =========================================================
# DRAG SETTINGS
# =========================================================

drag_index = -1

# Easier pinch detection
PINCH_DISTANCE = 60

# Distance at which pinch is definitely released
RELEASE_DISTANCE = 75

# Extra area around rectangle for easier selection
SELECTION_MARGIN = 25

# Previous finger position for smoother movement
previous_x = None
previous_y = None

# Smoothing value
SMOOTHING = 0.7


# =========================================================
# HAND CONNECTIONS
# =========================================================

connections = [

    # Thumb
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),

    # Index finger
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),

    # Middle finger
    (0, 9),
    (9, 10),
    (10, 11),
    (11, 12),

    # Ring finger
    (0, 13),
    (13, 14),
    (14, 15),
    (15, 16),

    # Pinky
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),

    # Palm
    (5, 9),
    (9, 13),
    (13, 17)
]


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    success, img = cap.read()

    if not success:
        print("❌ Failed to read frame")
        break


    # Mirror webcam
    img = cv2.flip(img, 1)


    # =====================================================
    # DETECT HAND
    # =====================================================

    hands, img = detector.findHands(
        img,
        draw=False,
        flipType=False
    )


    # =====================================================
    # HAND DETECTED
    # =====================================================

    if hands:

        hand = hands[0]

        lmList = hand["lmList"]


        # =================================================
        # INDEX + MIDDLE FINGER
        # =================================================

        index_finger = lmList[8]
        middle_finger = lmList[12]

        index_x = index_finger[0]
        index_y = index_finger[1]

        middle_x = middle_finger[0]
        middle_y = middle_finger[1]


        # =================================================
        # FIND DISTANCE BETWEEN INDEX + MIDDLE
        # =================================================

        length, _, _ = detector.findDistance(
            index_finger[:2],
            middle_finger[:2],
            None
        )


        # =================================================
        # MIDPOINT BETWEEN INDEX + MIDDLE
        # =================================================

        center_x = (index_x + middle_x) // 2
        center_y = (index_y + middle_y) // 2


        # =================================================
        # PINCH DETECTION
        # =================================================

        if length < PINCH_DISTANCE:

            # ---------------------------------------------
            # SELECT A RECTANGLE
            # ---------------------------------------------

            if drag_index == -1:

                for i, (cx, cy, w, h, _) in enumerate(rectangles):

                    # Add extra margin to make selection easier
                    left = cx - w // 2 - SELECTION_MARGIN
                    right = cx + w // 2 + SELECTION_MARGIN

                    top = cy - h // 2 - SELECTION_MARGIN
                    bottom = cy + h // 2 + SELECTION_MARGIN


                    # Check midpoint inside rectangle
                    if (
                        left < center_x < right
                        and
                        top < center_y < bottom
                    ):

                        drag_index = i

                        # Start smoothing from current position
                        previous_x = center_x
                        previous_y = center_y

                        break


            # ---------------------------------------------
            # MOVE SELECTED RECTANGLE
            # ---------------------------------------------

            if drag_index != -1:

                # Smooth movement
                if previous_x is None:
                    previous_x = center_x
                    previous_y = center_y


                smooth_x = int(
                    previous_x * (1 - SMOOTHING)
                    + center_x * SMOOTHING
                )

                smooth_y = int(
                    previous_y * (1 - SMOOTHING)
                    + center_y * SMOOTHING
                )


                # Update rectangle position
                rectangles[drag_index][0] = smooth_x
                rectangles[drag_index][1] = smooth_y


                # Save current position
                previous_x = smooth_x
                previous_y = smooth_y


        # =================================================
        # RELEASE PINCH
        # =================================================

        elif length > RELEASE_DISTANCE:

            drag_index = -1

            previous_x = None
            previous_y = None


        # =================================================
        # WHITE HAND TRACING
        # =================================================

        # Draw lines connecting hand landmarks
        for start, end in connections:

            x1 = lmList[start][0]
            y1 = lmList[start][1]

            x2 = lmList[end][0]
            y2 = lmList[end][1]


            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                3
            )


        # Draw white landmark points
        for point in lmList:

            x = point[0]
            y = point[1]

            cv2.circle(
                img,
                (x, y),
                5,
                (255, 255, 255),
                -1
            )


        # =================================================
        # DRAW PINCH LINE
        # =================================================

        cv2.line(
            img,
            (index_x, index_y),
            (middle_x, middle_y),
            (255, 255, 255),
            2
        )


    # =====================================================
    # NO HAND DETECTED
    # =====================================================

    else:

        drag_index = -1
        previous_x = None
        previous_y = None


    # =====================================================
    # DRAW RECTANGLES
    # =====================================================

    for i, (cx, cy, w, h, _) in enumerate(rectangles):

        # Green when selected
        if i == drag_index:

            color = (0, 255, 0)

        # Magenta normally
        else:

            color = (255, 0, 255)


        cv2.rectangle(
            img,
            (
                int(cx - w // 2),
                int(cy - h // 2)
            ),
            (
                int(cx + w // 2),
                int(cy + h // 2)
            ),
            color,
            cv2.FILLED
        )


    # =====================================================
    # IMPORTANT:
    # DRAW HAND TRACING AGAIN
    # SO IT APPEARS OVER THE RECTANGLES
    # =====================================================

    if hands:

        for start, end in connections:

            x1 = lmList[start][0]
            y1 = lmList[start][1]

            x2 = lmList[end][0]
            y2 = lmList[end][1]

            cv2.line(
                img,
                (x1, y1),
                (x2, y2),
                (255, 255, 255),
                3
            )


        for point in lmList:

            x = point[0]
            y = point[1]

            cv2.circle(
                img,
                (x, y),
                5,
                (255, 255, 255),
                -1
            )


    # =====================================================
    # QUIT INSTRUCTION
    # =====================================================

    cv2.rectangle(
        img,
        (980, 20),
        (1260, 75),
        (0, 0, 0),
        cv2.FILLED
    )

    cv2.putText(
        img,
        "Press Q to Quit",
        (1000, 58),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # =====================================================
    # SHOW WINDOW
    # =====================================================

    cv2.imshow(
        "5 Draggable Rectangles",
        img
    )


    # =====================================================
    # QUIT WITH Q
    # =====================================================

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# =========================================================
# CLEANUP
# =========================================================

cap.release()
cv2.destroyAllWindows()




# RUN FROM VS CODE TERMINAL
# python drag.py
# To stop the application:
# Press Q on your keyboard.