import  numpy
import math
import cv2

from PIL import Image, ImageDraw

FILENAME = "input.bmp"

def ordTo8b (num):
    a = bin(num)[2:]
    if num == 32:
        a = '00000' + a

    return a

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

def findWord():
    image = Image.open("output.bmp")  # Открываем изображение.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
    massBit = []
    flag0 = 0
    flagOut = 0
    currentNum = 0
    for i in range(width):
        for j in range(height):
            for k in range(3):
                currentPix = (pix[i, j][k]) % 2
                massBit.append(currentPix)
                if currentPix == 0:
                    flag0 += 1
                currentNum = (i*height + j*3 + k) % 11
                print(currentNum, ' ', flag0)
                if currentNum == 0 and flag0 != 11:
                        flag0 = 0
                elif currentNum == 0 and flag0 == 11:
                        flagOut = 1
                        break
            if flagOut == 1:
                break
        if flagOut == 1:
            break
    ourWord = "".join(chr(int("".join(map(str, massBit[i:i + 11])), 2)) for i in range(0, len(massBit), 11))
    print(ourWord)


def hideWord(wrd):
    image = Image.open(FILENAME)  # Открываем изображение.
    draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    pix = image.load()  # Выгружаем значения пикселей.
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
                    print(a[k])
                else:
                    a.append(pix[i, j][k])
            draw.point((i, j), (a[0], a[1], a[2]))

    image.save("output.bmp", "BMP")

    del draw

def initData():
    findType = input("Вы хотите встроить слово? y/n\n")
    if findType != 'y':
            findWord()
    else:
        word = input("Введите слово - ")
        wordInBin = ''.join(str(ordTo8b(ord(i))) for i in word)
        #print(len(wordInBin))
        hideWord(wordInBin)

initData()
fooPSNR()