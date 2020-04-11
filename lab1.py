
def сhange(s, origneSymb, changeSymb):
    #заменяем русскую оrigneSymb на changeSymb
    fIn = open("input", "r", encoding='utf-8')
    fOut = open("output", "w", encoding='utf-8')
    i = 0
    simbol = fIn.read(1);
    while simbol:
        if i < len(s) and (simbol == origneSymb or simbol == changeSymb):
            if s[i] == '1':
                fOut.write(changeSymb)
            else:
                fOut.write(origneSymb)
            i += 1
        elif i == len(s) and (simbol == origneSymb or simbol == changeSymb):
            fOut.write(origneSymb)
        else:
            fOut.write(simbol)
        simbol = fIn.read(1);
    if i < len(s):
        print('Контейнер слишком мал для этого слова ')
    fOut.close()
    fIn.close()


def findWord(origneSymb, changeSymb):
    fOut = open("output", "r", encoding='utf-8')
    i = 0
    k = 0
    massBit = []
    simbol = fOut.read(1);

    while simbol:
        if simbol == origneSymb:
            massBit.append(0)
            #print(massBit)
            i += 1
            k += 1
        elif simbol == changeSymb:
            massBit.append(1)
            #print(massBit)
            k += 1
        if k % 11 == 0 and i != 11:
            i = 0
        elif k % 11 == 0 and i == 11:
            break
        simbol = fOut.read(1);
    #print(massBit)
    #print(massBit[0:(len(massBit) - 11)])
    ourWord = "".join(chr(int("".join(map(str, massBit[i:i+11])), 2)) for i in range(0, len(massBit), 11))
    print(ourWord)
    fOut.close()

findType = input("Вы хотите встроить слово? y/n\n")
if findType != 'y':
    findType = input("Вы хотите найти слово? y/n\n")
    if findType != 'y':
        exit('Что вы хотите?')
    else:
        findType = 'find'
else:
    findType = 'hide'

stegoType = (int)(input("Введите 1, 2 или 3 в зависимости от метода текстовой стеганографии. \n 1 - Прямая замена символов \n 2 - Добавление дополнительных пробелов \n 3 - Добавление служебных символов (замена пунктуации) \n"))
if stegoType < 1 or stegoType > 3:
    exit('wrong input')

if findType == 'hide':
    word = input("Введите слово - ")
    wordInBin = ''.join(format(ord(i), 'b') for i in word)
    #print(wordInBin)
    if stegoType == 1:
        сhange(wordInBin, 'о', 'o')
    elif stegoType == 2:
        сhange(wordInBin, chr(32), chr(9))
    elif stegoType == 3:
        сhange(wordInBin, '—', '-')
elif findType == 'find':
    if stegoType == 1:
        findWord('о', 'o')
    elif stegoType == 2:
        findWord(chr(32), chr(9))
    elif stegoType == 3:
        findWord('—', '-')


