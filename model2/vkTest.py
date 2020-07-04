import vk
import re
import cv2
import urllib
import numpy as np


def get_ids(filename, p_end):
    f = open(filename, encoding='cp1251')
    f2 = open('id.csv', 'w')
    for line in f:
        pattern = 'https://vk.com/'
        start = line.find(pattern) + len(pattern)
        end = line.find(p_end)
        f2.write(line[start:end] + '\n')
    f.close()
    f2.close()

#
# if __name__ == "__main__":
#     filename = "data.csv"
#     p_end = '",'
#     get_ids(filename, p_end)


session = vk.Session("59b0026b59b0026b59b0026b0e59dba869559b059b0026b049a2dde8653f4718b7ee681")
vk_api = vk.API(session, v=5.101)


def is_digit(str):
    pattern = r'id(\d+)'
    return re.search(pattern, str)


def find_users(file):
    f = open(file)
    users = []
    for line in f:
        if is_digit(line):
            user_id = line[2:-1]
        else:
            try:
                user_id = vk_api.utils.resolveScreenName(screen_name=line[:-1])['object_id']
            except TypeError:
                print('Неверное имя ползьователя.')
        user = vk_api.users.get(user_id=user_id, fields='photo_max')
        users.append(user)
        print(user)
    return users


def faces_count(user):
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

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Faces found", image)
    cv2.waitKey(0)


for user in find_users("id.csv"):
    faces_count(user)