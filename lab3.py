from cv2 import dct, idct
from PIL import Image
import numpy as np
from math import sqrt, pi, cos
FILENAME = "input.bmp"

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
    pix = np.array(image.getdata(2))
    pix = pix.reshape(height, width)
    wrdLen = 0
    for ih in range(int(width / 8)):
        if wrdLen < len(wrd):
            for jw in range(int(height / 8)):
                mas = np.array(pix[8 * ih:8 * (ih + 1), 8 * jw:8 * (jw + 1)])
                #print(pix[8 * jw:8 * (jw + 1), 8 * ih:8 * (ih + 1)])
                #for i in range(8 * jw, 8 * (jw + 1)):
                #    for j in range(8 * ih, 8 * (ih + 1)):
                #        print(i, ' ', j)
                mas = mas.astype('float32')
                masDCT = dct(mas)
                masDCT = np.around(masDCT)
                for i in range(8):
                    for j in range(8):
                        if wrdLen < len(wrd):
                            masDCT[i][j] = change(wrd[wrdLen], masDCT[i][j])
                        wrdLen += 1

                    masIDCT = np.around(idct(masDCT))
                    #print(len(masIDCT[7]))

                    for i in range(8):
                        for j in range(8):
                            newBlk = list(obj[ih*8 + i, jw*8 + j])
                            newBlk[2] = masIDCT[i][j]
                            objOut[ih*8 + i, jw*8 + j] = tuple(newBlk)
                            #print("i = ", ih*8 + i, "  j = ",  jw*8 + j, "  i*8+j = ", i*8+j)
                if wrdLen >= len(wrd):
                    break
        else:
            imageOutput.save("output.bmp", "BMP")
            break


def findWrd(wrd, binWrd):
    binMsg = []
    imageOutput = Image.open("output.bmp")
    width = imageOutput.size[0]  # Определяем ширину.
    height = imageOutput.size[1]  # Определяем высоту.
    pix = np.array(imageOutput.getdata(1))
    pix = pix.reshape(height, width)
    binWrdLen = 0
    for ih in range(int(width / 8)):
        if (binWrdLen < len(binWrd)):
            for jw in range(int(height / 8)):
                mas = np.array(pix[8 * ih:8 * (ih + 1), 8 * jw:8 * (jw + 1)])
                #print(pix[8 * jw:8 * (jw + 1), 8 * ih:8 * (ih + 1)])
                #for i in range(8 * jw, 8 * (jw + 1)):
                #    for j in range( 8 * ih, 8 * (ih + 1)):
                #        print(i, ' ', j)

                mas = mas.astype('float32')
                masDCT = dct(mas)
                masDCT = np.around(masDCT)
                if (binWrdLen < len(binWrd)):
                    for i in range(8):
                        for j in range(8):
                            if (binWrdLen < len(binWrd)):
                                binMsg.append(int(masDCT[i][j] % 2))
                                #print("i = ", ih * 8 + i, "  j = ", jw * 8 + j, "  i*8+j = ", i * 8 + j)
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
    print('При передаче %d бит искажено' % mistake, "из", len(binWrd))
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
