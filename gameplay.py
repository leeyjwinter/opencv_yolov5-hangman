import cv2


def get_char_coords(word):
    x_coord = 230
    y_coord = 440

    char_ws = []
    char_hs = []

    for i in word:
        char_width, char_height = cv2.getTextSize(i, \
                                                  cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        char_ws.append(char_width)
        char_hs.append(char_height)

    max_char_h = max(char_hs)
    max_char_w = max(char_ws)

    char_rects = []

    for i in range(len(char_ws)):
        rect_coord = [(x_coord, y_coord - max_char_h), \
                      (x_coord + max_char_w, y_coord)]
        char_rects.append(rect_coord)
        x_coord = x_coord + max_char_w

    return char_rects


def draw_blank_rects(word, char_rects, img):
    for i in range(len(char_rects)):
        top_left, bottom_right = char_rects[i]
        if not word[i].isalpha() or \
                ord(word[i]) < 65 or \
                ord(word[i]) > 122 or \
                (ord(word[i]) > 90 and \
                 ord(word[i]) < 97):
            cv2.putText(img, word[i], (top_left[0], \
                                       bottom_right[1]), \
                        cv2.FONT_HERSHEY_SIMPLEX, \
                        1, (0, 0, 255), 2)
            continue
        cv2.rectangle(img, top_left, \
                      bottom_right, \
                      (0, 0, 255), thickness=2, \
                      lineType=cv2.LINE_8)
    cv2.imshow("Hangman", img)
    return img


def reveal_answer(word, img, char_rects):
    # img = cv2.imread(canvas_file,1)
    for i in range(len(word)):
        top_left, bottom_right = char_rects[i]
        cv2.putText(img, word[i], (top_left[0], bottom_right[1]), \
                    cv2.FONT_HERSHEY_SIMPLEX, \
                    1, (255, 0, 0), 2)
    cv2.imshow("Hangman", img)
    return img


def displayLetter(img, letter, word, char_rects):
    for i in range(len(word)):
        if word[i] == letter:
            top_left, bottom_right = char_rects[i]
            cv2.putText(img, word[i], \
                        (top_left[0], bottom_right[1]), \
                        cv2.FONT_HERSHEY_SIMPLEX, \
                        1, (0, 0, 0), 2)
    cv2.imshow("Hangman", img)
    return img


def draw_won(img):
    cv2.putText(img, "YOU'RE RIGHT! PRESS ENTER TO MOVE ON", (120, 60), \
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, \
                (0, 255, 0), 2)
    cv2.imshow("Hangman", img)


def draw_hint(img):
    cv2.putText(img, "HINT!, MOSAIC CLEARED", (120, 60), \
                cv2.FONT_HERSHEY_SIMPLEX, 1, \
                (0, 255, 0), 2)
    return img


def draw_wrong(img):
    cv2.putText(img, "WRONG! CHECK ANSWER AND PRESS ENTER TO MOVE ON", (120, 60), \
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, \
                (0, 255, 0), 2)
    return img


def draw_points(img, points):
    cv2.putText(img, "POINTS : " + str(points), (800, 60), \
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, \
                (0, 255, 0), 2)
    return img


def erase_area(img):
    cv2.rectangle(img, (800, 40), (1200, 80), (255, 255, 255), -1)

def erase_all_area(img):
    cv2.rectangle(img, (0, 0), (1200, 648), (255, 255, 255), -1)


def draw_final_points(img,points):
    cv2.putText(img, "YOUR POINT IS " + str(points), (285, 350), \
                cv2.FONT_HERSHEY_SIMPLEX, 2, \
                (0, 255, 0),2)
    return img