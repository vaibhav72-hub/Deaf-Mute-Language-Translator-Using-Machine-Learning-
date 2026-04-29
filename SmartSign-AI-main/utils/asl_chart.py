import os
import cv2
import numpy as np
import string

def show_asl_chart():
    """
    Displays a professional ASL alphabet chart using dataset images.
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_DIR = os.path.join(BASE_DIR, "data", "asl_alphabet_train")

    letters = list(string.ascii_uppercase)
    images = []

    for letter in letters:
        letter_dir = os.path.join(DATASET_DIR, letter)

        if not os.path.exists(letter_dir):
            continue

        # pick first image from folder
        img_name = os.listdir(letter_dir)[0]
        img_path = os.path.join(letter_dir, img_name)

        img = cv2.imread(img_path)
        img = cv2.resize(img, (120, 120))
        images.append((letter, img))

    # grid size
    cols = 7
    rows = int(np.ceil(len(images) / cols))

    canvas = np.zeros((rows * 140, cols * 140, 3), dtype=np.uint8)

    for idx, (letter, img) in enumerate(images):
        r = idx // cols
        c = idx % cols

        y = r * 140 + 10
        x = c * 140 + 10

        canvas[y:y+120, x:x+120] = img
        cv2.putText(canvas, letter, (x + 45, y + 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.imshow("ASL Alphabet Chart", canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
