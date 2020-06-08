import time
import os
import numpy as np
from PIL import Image, ImageDraw
from math import sqrt, pi, cos
from cv2 import dct, idct
from PIL import Image, ImageDraw
FILENAME = "input.bmp"

N = 8

def fooPSNR():
    original = cv2.imread("input.bmp")
    contrast = cv2.imread("output.bmp", 1)
    psnrcv = cv2.PSNR(original, contrast)
    print('psnr = ', psnrcv)

def change(curBit, num):
    if num + 1 == 256:
        num -= 2
    if (int)(curBit) ^ (num % 2) == 1:
        return num + 1
    else:
        return num


def change(curBit, num):
    if (int)(curBit) ^ (int)(num % 2) == 1:
        return num + 1
    else:
        return num

def hideWord(wrd, imageOutput=None):
    image = Image.open(FILENAME)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = np.array(image.getdata(2))
    pix = pix.reshape(height, width)
    binWrdLen = 0
    for ih in range((int)(height / N)):
        for jw in range((int)(width / N)):
            mas = np.array(pix[8 * ih:8 * (ih + 1), 8 * jw:8 * (jw + 1)])
            mas = mas.astype('float32')
            masDCT = dct(mas)
            masDCT = np.around(masDCT)

            for i in range(8):
                for j in range(8):
                    if (binWrdLen < len(wrd)):
                         masDCT[i][j] = change(int(wrd[binWrdLen]), masDCT[i][j])

            masIDST = idct(masDCT)

            for i in range(N):
                for j in range(N):
                    draw.point((i + ih*N, j + jw*N), (masIDST[i][j], masIDST[i][j], masIDST[i][j]))
                if (i+1)*N + jw*N + ih*N*N >= len(wrd):
                    break
    image.save("output.bmp", "BMP")
    del draw  # Удаляем инструмент


def initData():
    findType = input("Вы хотите встроить слово? y/n\n")
    if findType != 'y':
            #findWord()
            i = 3
    else:
        inword = str(input("Введите слово - "))
        wordInBin = ''
        for code in inword.encode('cp1251'):
            binCode = bin(code)[2:]
            while len(binCode) < 8:
                binCode = '0' + binCode
            wordInBin += binCode
        hideWord(wordInBin)


inword = str(input("Введите слово - "))
wordInBin = ''
for code in inword.encode('cp1251'):
    binCode = bin(code)[2:]
    while len(binCode) < 8:
        binCode = '0' + binCode
    wordInBin += binCode
hideWord(wordInBin)

#initData()
#fooPSNR()
#lsbPic("input.bmp", "LSB_in.bmp")
#lsbPic("output.bmp", "LSB_out.bmp")
