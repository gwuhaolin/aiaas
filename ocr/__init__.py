import numpy as np
import requests
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import cv2

ocr_rows_detection = None
ocr_txt_recognition = None


def ocr(img_path):
    global ocr_rows_detection, ocr_txt_recognition
    if ocr_rows_detection is None:
        ocr_rows_detection = pipeline(Tasks.ocr_detection, model='damo/cv_resnet18_ocr-detection-db-line-level_damo',
                                      device='cuda')
        ocr_txt_recognition = pipeline(Tasks.ocr_recognition, model='damo/cv_convnextTiny_ocr-recognition-general_damo',
                                       device='cuda')
    img = cv2.imread(img_path)
    data = ocr_rows_detection(img)['polygons']
    # 按照 y 轴排序
    keys = [data[:, 0], data[:, 1]]
    sorted_indices = np.lexsort(keys)
    sorted_data = data[sorted_indices]
    ret = []
    for x in sorted_data:
        t = ocr_txt_recognition(img[int(x[1]):int(x[5]), int(x[0]):int(x[4])])
        ret.extend(t['text'])
    return ret


def ocr_http(img_path):
    res = requests.post('http://192.168.2.2:5000/ocr', json={'img_path': img_path})
    return res.json()


if __name__ == '__main__':
    from flask import Flask
    from flask import request

    app = Flask(__name__)


    @app.route('/ocr', methods=['POST'])
    def ocr_http_server():
        # 获取 JSON 数据
        data = request.json
        return ocr(data['img_path'])


    app.run(host='0.0.0.0', port=5000)

