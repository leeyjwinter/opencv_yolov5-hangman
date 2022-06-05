
import shutil
import json
import cv2
import torch


IMAGE = 'people.jpg'
CANVAS = 'hangman/canvas.png'


def resize_picture(img):
    shrink_img = cv2.imread(img)
    origin_width = shrink_img.shape[1]  # width
    # height
    width = origin_width

    while width > 531:
        width = width * 0.9
        width = int(width)
    shrink_img = cv2.resize(shrink_img, (0, 0), fx=width / origin_width, fy=width / origin_width)

    origin_height = shrink_img.shape[0]
    height = origin_height
    while height > 548:
        height = height * 0.9
        height = int(height)
    shrink_img = cv2.resize(shrink_img, (0, 0), fx=height / origin_height, fy=height / origin_height)
    # print(shrink_img.shape[0],shrink_img.shape[1])

    return shrink_img


def erase_mat():
    # result_img = cv2.imread('runs/detect/exp/image0.jpg',cv2.IMREAD_ANYCOLOR)
    # cv2.imshow("result",result_img)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    # os.remove('runs/detect/exp/image0.jpg')
    shutil.rmtree('runs/detect//')


def picture_yolo_save(img):  # 객체탐지한 결과물을 저장
    im3 = cv2.imread(img)[..., ::-1]  # 색 반전 안되도록
    # imgs = []
    # imgs.append(im2)
    # # imgs.append(im1)
    # imgs.append(im3)
    result = model(im3, size=640)
    result.save()  # runs/detect/exp/image0.jpg로 저장
    return result


def show_answer(hangman):
    answer_img = resize_picture('runs/detect/exp/image0.jpg')
    # answer_img = cv2.imread('runs/detect/exp/image0.jpg',cv2.IMREAD_ANYCOLOR)
    height, width, channel = answer_img.shape
    # answer_img = resize_picture(answer_img)
    hangman[100:height + 100, 576:576 + width] = answer_img
    cv2.imshow("Hangman", hangman)
    # cv2.imshow("answer",answer_img)
    # cv2.waitKey()
    # cv2.destroyWindow("answer")


def show_question(img, hangman):  # hangman 캔버스에 문제 보여줌
    height, width, channel = img.shape
    hangman[100:height + 100, 576:576 + width] = img
    cv2.imshow("Hangman", hangman)
    # cv2.imshow("question", img)
    # cv2.waitKey(0)
    # cv2.destroyWindow("question")


def show_quiz():  # hangman 캔버스를 띄움
    img = cv2.imread(CANVAS)  # width = 640, height = 425
    cv2.namedWindow("Hangman", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Hangman", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Hangman", img)
    # img = np.full((640,480,3),(255,255,255),np.uint8)
    # cv2.imshow("quiz",img)
    # cv2.waitKey(0)
    return img


def object_cords(img):  # 탐지한 객체들의 좌표와 레이블을 반환해줌
    return json.loads(picture_yolo_save(img).pandas().xyxy[0].to_json(orient="records"))


def box_on_hangman(shrinked_cords, hangman, color):
    for val in shrinked_cords:
        hangman = cv2.rectangle(hangman, (int(val['xmin']) + 576, int(val['ymin']) + 100),
                                (int(val['xmax']) + 576, int(val['ymax']) + 100), color, 2)
    cv2.imshow("Hangman", hangman)


def picture_yolo_mosaic(img, rate, object_cords):  # yolo_save한 결과물을 가져와 모자이크를 줌
    win_title = 'mosaic'
    # result_vals = json.loads(picture_yolo_save(img).pandas().xyxy[0].to_json(orient="records"))#dict 형으로 x,y, 레이블 가져옴
    result_img = cv2.imread(img, cv2.IMREAD_ANYCOLOR)

    for val in object_cords:  # 모자이크될 좌표 지정
        x = int(val['xmin'])
        y = int(val['ymin'])
        w = int(val['xmax']) - int(val['xmin'])
        h = int(val['ymax']) - int(val['ymin'])

        if w and h:
            roi = result_img[y:y + h, x:x + w]  # 관심영역 지정
            roi = cv2.resize(roi, (w // rate + 1, h // rate + 1))  # 1/rate 비율로 축소
            # 원래 크기로 확대
            roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_AREA)
            result_img[y:y + h, x:x + w] = roi  # 원본 이미지에 적용
        else:
            continue

        result_img = cv2.rectangle(result_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    origin_width = result_img.shape[1]  # width
    width = origin_width

    while width > 531:
        width = width * 0.9
        for val in object_cords:
            val['xmin'] = 0.9 * int(val['xmin'])
            val['xmax'] = 0.9 * int(val['xmax'])
            val['ymin'] = 0.9 * int(val['ymin'])
            val['ymax'] = 0.9 * int(val['ymax'])
        width = int(width)
    result_img = cv2.resize(result_img, (0, 0), fx=width / origin_width, fy=width / origin_width)

    origin_height = result_img.shape[0]
    height = origin_height

    while height > 548:
        height = height * 0.9
        for val in object_cords:
            val['xmin'] = 0.9 * int(val['xmin'])
            val['xmax'] = 0.9 * int(val['xmax'])
            val['ymin'] = 0.9 * int(val['ymin'])
            val['ymax'] = 0.9 * int(val['ymax'])
        height = int(height)
    result_img = cv2.resize(result_img, (0, 0), fx=height / origin_height, fy=height / origin_height)

    return result_img, object_cords


def shrink_object_cords(img, object_cords):
    result_img = cv2.imread(img, cv2.IMREAD_ANYCOLOR)
    origin_width = result_img.shape[1]  # width
    width = origin_width

    while width > 531:
        width = width * 0.9
        for val in object_cords:
            val['xmin'] = 0.9 * int(val['xmin'])
            val['xmax'] = 0.9 * int(val['xmax'])
            val['ymin'] = 0.9 * int(val['ymin'])
            val['ymax'] = 0.9 * int(val['ymax'])
        width = int(width)
    result_img = cv2.resize(result_img, (0, 0), fx=width / origin_width, fy=width / origin_width)

    origin_height = result_img.shape[0]
    height = origin_height

    while height > 548:
        height = height * 0.9
        for val in object_cords:
            val['xmin'] = 0.9 * int(val['xmin'])
            val['xmax'] = 0.9 * int(val['xmax'])
            val['ymin'] = 0.9 * int(val['ymin'])
            val['ymax'] = 0.9 * int(val['ymax'])
        height = int(height)
    result_img = cv2.resize(result_img, (0, 0), fx=height / origin_height, fy=height / origin_height)

    return object_cords


# def edge_show(hangman,object_cord):
#     x = int(object_cord['xmin'])
#     y = int(object_cord['ymin'])
#     w = int(object_cord['xmax']) - int(object_cord['xmin'])
#     h = int(object_cord['ymax']) - int(object_cord['ymin'])
#     print(x,y,w,h)
#     result_img = cv2.rectangle(hangman, (x, y), (x + w, y + h), (255, 0, 0), 1)
#     # roi = hangman[y:y+h,x:x+w]
#     result_img = cv2.GaussianBlur(result_img,(5,5),0)
#     canny_img = cv2.Canny(result_img,1,10)
#     # hangman[y:y+h,x:x+w] = roi
#     return hangman


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
