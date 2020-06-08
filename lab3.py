import time
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from math import sqrt, pi, cos
import cv2
from PIL import Image, ImageDraw
from scipy import fftpack
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

def fooDCT(mas):
    return fftpack.dct(fftpack.dct(mas, axis=0, norm='ortho'), axis=1, norm='ortho')
def fooIDCT(mas):
    return fftpack.idct(fftpack.idct(mas, axis=0, norm='ortho'), axis=1, norm='ortho')

def change(curBit, num):
    if num + 1 == 256:
        num -= 2
    if (int)(curBit) ^ (num % 2) == 1:
        return num + 1
    else:
        return num

def hideWord(wrd):
    image = Image.open(FILENAME)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.

    for ih in range((int)(height / N)):
        for jw in range((int)(width / N)):
            mas = np.array(pix[8 * ih:8 * (ih + 1), 8 * jw:8 * (jw + 1)])
            blueDCT = [[] for i in range(N)]
            for i in range(N):
                fBlue = []
                for j in range(N):
                    fBlue.append(mas[i][j][2])
                blueDCT[i].append(fooDCT(fBlue))
            blueLCB = [[] for i in range(N)]
            for i in range(N):
                for j in range(N):
                    blueLCB[i].append(change(wrd[j + i*N + jw*N + ih*N*N], blueDCT[i]))
                if (i+1)*N + jw*N + ih*N*N >= len(wrd):
                    break

            for i in range(N):
                for j in range(N):
                    a = []
                    a.append(mas[i][j][0])
                    a.append(mas[i][j][1])
                    a.append(fooIDCT(blueLCB[i][j]))
                    draw.point((i + ih*N, j + jw*N), (a[0], a[1], a[2]))
                if (i+1)*N + jw*N + ih*N*N >= len(wrd):
                    break

    image.save("image3.bmp", "BMP")  # Сохраняем новое изображение
    del draw  # Удаляем инструмент


    #print (len(wrd))
    for i in range(width):
        for j in range(height):
            a = []
            for k in range(3):
                if 3*j + (height * i) + k < len(wrd):
                    a.append(change(wrd[3*j + height * i + k], pix[i, j][k]))
                    #print(a[k])
                elif 3*j + (height * i) + k < (len(wrd) + 12):
                    a.append(change(0, pix[i, j][k]))
                    #print(a[k])
                else:
                    a.append(pix[i, j][k])
            draw.point((i, j), (a[0], a[1], a[2]))

    image.save("output.bmp", "BMP")

    del draw

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
