from cv2 import dct, idct, imread, PSNR
from PIL import Image
import numpy as np
from math import sqrt, pi, cos
FILENAME = "input.bmp"
comp = 0

def fooPSNR():
    original = imread("input.bmp")
    contrast = imread("output.bmp", 1)
    mse = np.mean((original - contrast) ** 2)
    if (mse == 0):
        return 100
    rmse = sqrt(mse)
    print('RMSE', rmse)
    psnrcv = PSNR(original, contrast)
    print('psnr = ', psnrcv)

def change(curBit, num):
    if num + 1 == 256:
        num -= 2
    if (int)(curBit) ^ (int)(num % 2) == 1:
        return num + 1
    else:
        return num

def hideWrd(wrd):
    image = Image.open(FILENAME)  # Открываем изображение.
    width = image.size[0]  # Определяем ширину.
    height = image.size[1]  # Определяем высоту.
    obj = image.load()
    #print(width, height)
    imageOutput = Image.open(FILENAME)
    objOut = imageOutput.load()
    pix = np.array(image.getdata(comp))
    pix = pix.reshape(height, width)
    wrdLen = 0
    for ih in range(int(width / 8)):
        if wrdLen < len(wrd):
            for jw in range(int(height / 8)):
                mas = np.array(pix[ 8 * jw:8 * (jw + 1), 8 * ih:8 * (ih + 1)])
                mas = mas.astype('float32')
                masDCT = dct(mas)
                masDCT = np.around(masDCT)
                for i in range(8):
                    for j in range(8):
                        if wrdLen < len(wrd):
                            masDCT[i][j] = change(wrd[wrdLen], masDCT[i][j])
                        wrdLen += 1

                masIDCT = np.around(idct(masDCT))

                for i in range(8):
                    for j in range(8):
                        newBlk = list(obj[ih*8 + i, jw*8 + j])
                        newBlk[comp] = masIDCT[i][j]
                        objOut[ih*8 + i, jw*8 + j] = tuple(newBlk)
                if wrdLen >= len(wrd):
                    break
        else:
            break
    imageOutput.save("output.bmp", "BMP")


def findWrd(wrd, binWrd):
    binMsg = []
    imageOutput = Image.open("output.bmp")
    width = imageOutput.size[0]  # Определяем ширину.
    height = imageOutput.size[1]  # Определяем высоту.
    pix = np.array(imageOutput.getdata(comp))
    pix = pix.reshape(height, width)
    binWrdLen = 0
    for ih in range(int(width / 8)):
        if (binWrdLen < len(binWrd)):
            for jw in range(int(height / 8)):
                mas = np.array(pix[8 * ih:8 * (ih + 1), 8 * jw:8 * (jw + 1)])
                mas = mas.astype('float32')
                masDCT = dct(mas)
                masDCT = np.around(masDCT)
                if (binWrdLen < len(binWrd)):
                    for i in range(8):
                        for j in range(8):
                            if (binWrdLen < len(binWrd)):
                                binMsg.append(int(masDCT[i][j] % 2))
                            binWrdLen += 1
                else:
                    break
            else:
                break
    answer = ''
    for i in range(len(wrd)):
        binStr = ''.join(str(x) for x in (binMsg[(i * 8):(i + 1) * 8]))
        if binStr == '10011000':
            answer += ' '
        else:
            answer += str(bytes([int(binStr, base=2)]), 'cp1251')
    print("Получено - ", answer)
    check = ''.join(str(x) for x in (binMsg))

    mistake = 0
    for l in range(len(binWrd)):
        if binWrd[l] != check[l]:
            mistake += 1
    mistake /= 2
    print('При передаче %d бит искажено' % mistake)
    print('Это %f процентов' % (100. * (float(mistake) / len(binWrd))))

def initData():
    inWrd = str(input("Введите слово - "))
    wrdInBin = ''
    for code in inWrd.encode('cp1251'):
        binCode = bin(code)[2:]
        while len(binCode) < 8:
            binCode = '0' + binCode
        wrdInBin += binCode
    hideWrd(wrdInBin)
    findWrd(inWrd, wrdInBin)

initData()
fooPSNR()
