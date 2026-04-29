import cv2
import os

def show_signs(text):
    for ch in text.upper():
        if ch.isalpha():
            folder = f"data/asl_alphabet/{ch}"
            if not os.path.exists(folder):
                continue

            img_name = os.listdir(folder)[0]
            img_path = os.path.join(folder, img_name)
            img = cv2.imread(img_path)

            if img is None:
                continue

            cv2.imshow("Text to Sign", img)
            cv2.waitKey(700)

    cv2.destroyAllWindows()
