import cv2
import qrcode

from pathlib import *


def make_qrcode(call, address):
    """creates qr code"""
    qr_img = qrcode.make(address)
    qr_img.save(f'users/qrcodes/{call.from_user.id}.png')
    return Path(f'users/qrcodes/{call.from_user.id}.png').resolve()


def decode_qrcode(user_id):
    """decodes qr code"""
    img_qr = cv2.imread(f'users/qrcodes/from/{user_id}.png')
    qr_data = cv2.QRCodeDetector()
    data, bbox, clear_qrcode = qr_data.detectAndDecode(img_qr)
    return data
