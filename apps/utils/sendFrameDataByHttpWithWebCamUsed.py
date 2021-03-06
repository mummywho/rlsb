import sys
import cv2
import numpy
import time
import base64

from urllib.request import urlopen
from urllib.parse import urlencode

from attendance.models import  AttendanceInfo
from facedata.models import FaceData

import hashlib
import json

import threading


def sendFrameDataWithWebCam(userForWebCam, pwdForWebCam, ipForWebCam, portForWebCam, frequencyCatched=100):
    global framesList
    webCamUrl = "rtsp://%s:%s@%s:%s/h264/ch1/main/av_stream" % (
    userForWebCam, pwdForWebCam, ipForWebCam, portForWebCam);

    video_capture = cv2.VideoCapture(webCamUrl)

    if not video_capture.isOpened():
        print("网络摄像头尚未开启，请检查后再试。")
        return

    frameNum = 0
    while (video_capture.isOpened()):
        ret, frame = video_capture.read()

        if not ret:
            continue



        if frameNum % frequencyCatched == 0:
            if frame is not None:
                millisecond_timestamp = int(round(time.time() * 1000))
                framesList.append((millisecond_timestamp, frame))
            frameNum = 0

        frameNum += 1

    return


def sendFrameDataByHttpV1(clientId, clientSecret, webCamId, millisecond_timestamp, frame,encode_param,server_url):
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    if not result:
        return

    imgData = numpy.array(imgencode)
    stringImgData = imgData.tostring()
    base64ImgData = base64.b64encode(stringImgData)

    params = {"client_id": clientId, "client_secret": clientSecret, "webcam_id": webCamId, "image": base64ImgData,
              "millisecond_timestamp": millisecond_timestamp}

    paramNamesForSignature = sorted(["client_secret", "client_id", "millisecond_timestamp", "webcam_id"], key=str.lower)

    paramValuesStr = ""
    for index in range(0, len(paramNamesForSignature)):
        param = paramNamesForSignature[index]
        paramValuesStr += str(params[param])

    m = hashlib.md5()
    m.update(paramValuesStr.encode("utf-8"))
    signatureStr = m.hexdigest()

    params["signature"] = signatureStr

    params = urlencode(params).encode('utf-8')
    reply = urlopen(server_url, params).read()
    result = reply.decode("utf-8")
    ret = json.loads(result)
    print(ret)

    return



def processFrameData(clientId, clientSecret, webCamId,encode_param,server_url):
    global framesList
    while True:
        if len(framesList) > 0:
            millisecond_timestamp, frame = framesList.pop(0)
            send_local_image = sendFrameDataByHttpV1(clientId, clientSecret, webCamId, millisecond_timestamp, frame,encode_param,server_url)
            if send_local_image['result'] == 'success':
                if send_local_image['recognized_face_num'] > 0:

                    face_ids = send_local_image['recognized_face_ids_list'].split('#')

                    # department = request.user.department
                    # if department:  # 找到所在的单位
                    #     if department.parent:
                    #         parent = department.parent
                    #         index_depart = 1
                    #     else:
                    #         parent = department
                    #         index_depart = 2

                    for face_id in face_ids:
                        facedata = FaceData.objects.get(face_id=face_id)
                        attendate = AttendanceInfo(facedata=facedata, image=frame,
                                                   recorded_datetime=send_local_image['datetime'])
                        attendate.save()

                    res = {
                        'status': 'success',
                        'send_local_image': '{}识别成功！'.format(face_ids),
                        'face_cname': facedata.face_cname,
                        'depart': facedata.department,

                    }
                else:
                    res = {
                        'status': 'fail',
                        'send_local_image': '未识别出对象！'
                    }
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = send_local_image['error_msg']

            res = {
                'status': 'fail',
                'send_local_image': errors
            }
    return

def main(userForWebCam,pwdForWebCam,ipForWebCam,portForWebCam,clientId,webCamId,clientSecret):

    # server_url = "http://192.168.1.219/cgi-bin/v0.13/facerecognize/doRecognizeWithVideoFrame.py"
    # server_url = "http://192.168.1.219/v0.13/facerecognize/doRecognizeWithVideoFrame"
    server_url = "http://222.128.127.3:8185/v0.13/facerecognize/doRecognizeWithVideoFrame"
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    #
    # if len(sys.argv) < 8:
    #     print("错误: ", "缺少脚本所需参数")
    #     exit()
    #
    # userForWebCam = sys.argv[1]
    # pwdForWebCam = sys.argv[2]
    # ipForWebCam = sys.argv[3]
    # portForWebCam = sys.argv[4]
    # clientId = int(sys.argv[5])
    # webCamId = int(sys.argv[6])
    # clientSecret = sys.argv[7]
    #
    # python sendFrameDataByHttpWithWebCamTestV1.py "admin" "MHQAFM" "192.168.1.243" "554" 33 9 "abc123"
    # python sendFrameDataByHttpWithWebCamTestV1.py "admin" "MHQAFM" "192.168.1.243" "554" 33 9 "1234567890"

    """
    userForWebCam = "admin"
    pwdForWebCam = "MHQAFM"
    ipForWebCam = "192.168.1.243"
    portForWebCam = "554"
    clientId = 33
    webCamId = 9
    #clientSecret = "abc123"
    clientSecret = "1234567890"
    """
    frequencyCatched = 20
    framesList = []
    threadObj = threading.Thread(target=processFrameData, args=(clientId, clientSecret, webCamId,encode_param,server_url))  # 创建线程
    threadObj.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
    threadObj.start()  # 开启线程
    sendFrameDataWithWebCam(userForWebCam, pwdForWebCam, ipForWebCam, portForWebCam,frequencyCatched)
    print (frequencyCatched)


