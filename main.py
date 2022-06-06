import copy
import os, random
from picture import *
from gameplay import *

CANVAS = 'hangman/canvas.png'
MOSAIC_RATE = 20
points = 0
answer_label = ""

# def on_mouse(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         value = param[y,x,:]
#         # print("왼쪽 버튼 눌림 \t x : {} y : {} 좌표의 픽셀값은 : {}".format(x,y, value) )
#         global shrinked_cords
#         global hangman
#
#         for val in shrinked_cords:
#              if x>=val['xmin']+576 and x<=val['xmax']+576 and y>=val['ymin']+100 and y<=val['ymax']+100:
#                  hangman = cv2.rectangle(hangman, (int(val['xmin']) + 576, int(val['ymin']) + 100),
#                                          (int(val['xmax']) + 576, int(val['ymax']) + 100), (255, 255, 255), 2)
#                  print(shrinked_cords.index(val))
#                  cv2.imshow("Hangman",hangman)
#
#     return

def keyboard_chooseobj():
    global shrinked_cords
    global hangman
    index_num = 0

    while shrinked_cords:
        key = cv2.waitKeyEx(30)
        if key == 0x270000:
            index_num += 1
            if index_num > len(shrinked_cords) - 1:
                index_num = 0
        elif key == 0x250000:
            index_num -= 1
            if index_num < 0:
                index_num = len(shrinked_cords) - 1
        elif key == 13:  # enter
            for val in shrinked_cords:
                if shrinked_cords.index(val) == index_num:
                    # print(val['name'])
                    return val
        elif key == 0x1B:  # esc
            break
        for val in shrinked_cords:
            if shrinked_cords.index(val) == index_num:
                hangman = cv2.rectangle(hangman, (int(val['xmin']) + 576, int(val['ymin']) + 100),
                                        (int(val['xmax']) + 576, int(val['ymax']) + 100), (255, 255, 255), 2)
            else:
                hangman = cv2.rectangle(hangman, (int(val['xmin']) + 576, int(val['ymin']) + 100),
                                        (int(val['xmax']) + 576, int(val['ymax']) + 100), (255, 0, 0), 2)
            cv2.imshow("Hangman", hangman)


def draw_hangman(index, img):
    if index == 0:
        cv2.circle(img, (245, 190), 40, (0, 0, 0), thickness=2, \
                   lineType=cv2.LINE_AA)
        cv2.imshow("Hangman", img)

    if index == 1:
        cv2.line(img, (245, 230), (245, 320), \
                 (0, 0, 0), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.imshow("Hangman", img)

    if index == 2:
        cv2.line(img, (245, 270), (185, 200), \
                 (0, 0, 0), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.imshow("Hangman", img)

    if index == 3:
        cv2.line(img, (245, 270), (305, 200), \
                 (0, 0, 0), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.imshow("Hangman", img)

    if index == 4:
        cv2.line(img, (245, 320), (185, 360), \
                 (0, 0, 0), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.imshow("Hangman", img)

    if index == 5:
        cv2.circle(img, (245, 190), 40, (0, 0, 255), thickness=2, \
                   lineType=cv2.LINE_AA)
        cv2.line(img, (245, 230), (245, 320), \
                 (0, 0, 255), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.line(img, (245, 270), (185, 200), \
                 (0, 0, 255), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.line(img, (245, 270), (305, 200), \
                 (0, 0, 255), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.line(img, (245, 320), (185, 360), \
                 (0, 0, 255), thickness=2, \
                 lineType=cv2.LINE_AA)
        cv2.line(img, (245, 320), (305, 360), \
                 (0, 0, 255), thickness=2, \
                 lineType=cv2.LINE_AA)
        reveal_answer(chosen_answer, hangman, char_rects)
        cv2.imshow("Hangman", img)

for i in range(5):
    all_right = True
    IMAGE = "./photos/" + random.choice(os.listdir("./photos"))
    try:
        erase_mat()
    except:
        pass

    object_cords1 = object_cords(IMAGE)  # 원래 이미지의 좌표값과 레이블을 구한다
    removing_list = []
    for x in object_cords1:
        if x['confidence'] < 0.5:
            removing_list.append(x)
    for val in removing_list:
        object_cords1.remove(val)


    while object_cords1:
        new_object_cords = copy.deepcopy(object_cords1)


        dst, shrinked_cords = picture_yolo_mosaic(IMAGE, MOSAIC_RATE,
                                                  new_object_cords)  # 이미지를 모자이크 하고, 사진을 축소하는 과정에서 객체들의 캔버스의 절대 좌표값도 구한다


        hangman = show_quiz()  # 행맨 캔버스를 띄운다
        cv2.putText(hangman, "Letters used:", (80, 540), \
                    cv2.FONT_HERSHEY_SIMPLEX, 1, \
                    (0, 0, 0), 2)
        erase_area(hangman)
        draw_points(hangman, points)
        cv2.imshow("Hangman", hangman)

        show_question(dst, hangman)  # 문제를 보여주고 다시 띄운다

        chosen_value = keyboard_chooseobj()
        if not chosen_value:
            break
        chosen_answer = chosen_value['name']
        object_cords_index = shrinked_cords.index(chosen_value)
        chosen_answer_lower = chosen_answer.lower()
        char_rects = get_char_coords(chosen_answer)
        draw_blank_rects(chosen_answer, char_rects, hangman)

        chars_entered = []
        letter_x = 300
        letter_y = 540

        index = 0
        while True:
            letter_count = 0
            for letters in chosen_answer.strip():
                if letters in chars_entered:
                    letter_count += 1
            if letter_count == len(chosen_answer.replace(' ', '')):
                points += 10
                erase_area(hangman)
                cv2.imshow("Hangman", hangman)
                draw_points(hangman, points)
                cv2.imshow("Hangman", hangman)
                draw_won(hangman)
                cv2.waitKey()
                letter_x = 300
                letter_y = 540
                chars_entered = []
                del object_cords1[object_cords_index]
                # shrinked_cords.remove(chosen_value)
                break
            key = cv2.waitKey()
            if 65 <= key <= 90 or 97 <= key <= 122:
                key = chr(key).lower()
                if key not in chars_entered:
                    chars_entered.append(key)
                    cv2.putText(hangman, key, (letter_x, letter_y), \
                                cv2.FONT_HERSHEY_SIMPLEX, 1, \
                                (255, 0, 0), 2)
                    letter_x += 30
                    erase_area(hangman)
                    draw_points(hangman, points)
                    cv2.imshow("Hangman", hangman)
                    if key in chosen_answer_lower:
                        displayLetter(hangman, key, chosen_answer_lower, char_rects)
                    else:
                        draw_hangman(index, hangman)
                        index += 1
                        if index == 4:
                            hangman1 = copy.deepcopy(hangman)
                            hangman1 = draw_hint(hangman1)
                            cv2.imshow("Hangman", hangman1)
                            cv2.waitKey(1000)

                            object_cords2 = copy.deepcopy(object_cords1)
                            delete_val = object_cords2[object_cords_index]
                            del object_cords2[object_cords_index]
                            delete_val_list = []
                            delete_val_list.append(delete_val)
                            dst, a = picture_yolo_mosaic(IMAGE, MOSAIC_RATE, object_cords2)
                            show_question(dst, hangman)
                            delete_val_list = shrink_object_cords(IMAGE, delete_val_list)
                            box_on_hangman(delete_val_list, hangman, (255, 255, 255))
                            points -= 5
                            erase_area(hangman)
                            draw_points(hangman, points)
                            cv2.imshow("Hangman", hangman)
                            cv2.waitKey(1000)
                        if index == 6:
                            del object_cords1[object_cords_index]
                            hangman2 = copy.deepcopy(hangman)
                            hangman2 = draw_wrong(hangman2)
                            points -= 10
                            all_right = False
                            erase_area(hangman)
                            draw_points(hangman, points)
                            cv2.imshow("Hangman", hangman2)
                            cv2.waitKey()
                            break
            elif key == 27:
                break

    # cv2.waitKey(0)
    # if chosen_answer:
    #     reveal_answer(chosen_answer, hangman, char_rects)

    if all_right:
        points+=30
        erase_area(hangman)
        draw_points(hangman, points)
        cv2.imshow("Hangman", hangman)
        show_answer(hangman)
    else:
        show_answer(hangman)
    end_key = cv2.waitKeyEx()
    if end_key == 0x1B:
        break
    # 정답을 보여주고 다시 띄운다
    # box_on_hangman(shrinked_cords, hangman)  # 구한 바뀐 좌표값을 박스친다

erase_all_area(hangman)
draw_final_points(hangman, points)
cv2.imshow("Hangman", hangman)
cv2.waitKey()
cv2.destroyAllWindows()
erase_mat()
