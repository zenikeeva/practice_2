import os

import vk
import cv2
import urllib
import numpy as np

from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def facescount(request):
    vkid = request.POST['vkid']
    session = vk.Session("59b0026b59b0026b59b0026b0e59dba869559b059b0026b049a2dde8653f4718b7ee681")
    vk_api = vk.API(session, v=5.101)
    user = vk_api.users.get(user_id=vkid, fields='photo_max')

    os.remove("static/images/a.jpg")

    imagePath = user[0]['photo_max']
    cascPath = "haarcascade_frontalface_default.xml"

    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    resp = urllib.request.urlopen(imagePath)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    countf = len(faces)
    print("Found {0} faces!".format(countf))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imshow("Faces found", image)
    #cv2.waitKey(0)

    cv2.imwrite("static/images/a.jpg",image)
    temp_img_path = ""
    params = {"countf":countf, "temp_img_path":temp_img_path}

    return render(request, 'facescount.html', params)
