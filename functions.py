from bitstring import BitArray
from PIL import Image
import os.path
from typing import Tuple

def convertStr2Bytes(data : str) -> str:
    return ''.join([ format(ord(i), "08b") for i in data ])

def convertStr2Int(data : str) -> int:
    return sum([ ord(i) for i in data ])

def convertBytes2Int(data : str) -> int:
    return int(data, 2)

def convertBytes2Str(data : str) -> str:
    return chr(int(data, 2))

def getFileNameAndSizeFromUser() -> Tuple[str, Tuple[int, int]]:
    while True:
        fileName = input("Введите название файла в формате \"image.png\":")
        if os.path.exists(f"data/{fileName}"):
            print("Принято!")
            break
        print("Такого файла нет. Проверь свое название.")
    img = Image.open(f'data/{fileName}').convert("RGB")
    return fileName, img.size

def getOptionFromUser() -> int:
    while True:
        option = input("Введи \"1\" для извлечения информации, \"2\" для внедрения информации:")
        if option in ["1", "2"]:
            print("За работу!")
            break
        print("Никак не пойму, что ты от меня хочешь!")
    return int(option)

def getLengthFromUser() -> int:
    while True:
        length = input("Кстати, примерно сколько бит текста мне рассмотреть?")
        if length.isdigit():
            print("Понял!")
            break
        print("Лучше введи число!")
    return int(length)

def getLastOptionFromUser() -> int:
    while True:
        last = input("При замене больше 2 послежних символов, картинка может переставать быть естественной, поэтому введи \"1\" или \"2\":")
        if last in ["1", "2"]:
            print("За работу!")
            break
        print("Никак не пойму, что ты от меня хочешь!")
    return int(last)

def getTextFromUser(block : int) -> str:
    while True:
        text = input("Ваш текст для внедрения:")
        if len(text) <= block:
            print("Начинаю внедрение!")
            break
        print("Слишком, много символов!")
    return text

def getPasswordFromUser(shape : Tuple[int, int]) -> int:
    passwordStr = input("Ваш пароль:")
    print("Запомнил!")
    password = convertStr2Int(passwordStr) % (shape[0] * shape[1] // 2)
    return password

def calculateAndExtract(fileName : str, length : int, password : int) -> None:
    img = Image.open(f'data/{fileName}').convert("RGB")

    text1 = ''
    text2 = ''
    bytes1 = ''
    bytes2 = ''
    width, height = img.size
    counter = 0
    offsetCounter = 0
    offsetFlag = False

    for i in range(width): 
        for j in range(height):
            offsetCounter += 1
            if offsetCounter >= password:
               offsetFlag = True 
            if offsetFlag: 
                r, g, b = img.getpixel((i, j))

                rb = format(r, "08b")
                gb = format(g, "08b")
                bb = format(b, "08b")

                l1 = [rb[-1], gb[-1], bb[-1]]
                l2 = [rb[-2], gb[-2], bb[-2]]

                bytes1 += max(l1, key = l1.count)
                bytes2 += max(l1, key = l1.count)
                bytes2 += max(l2, key = l2.count)

                if len(bytes1) == 8:
                    text1 += convertBytes2Str(bytes1)
                    bytes1 =''
                if len(bytes2) == 8:
                    print(bytes2)
                    text2 += convertBytes2Str(bytes2)
                    bytes2 = ''
                counter += 1
                if counter >= length:
                    break
        else:
            continue
        break
    
    with open("output/text_out", "w") as f:
        f.write("Текст встренный в последний бит :" + text1 + "\n")
        f.write("Текст встроенный в два последних бита :" + text2 + "\n")
    print(f"Результат экстракта текста из изображения {fileName} находится в файле output/text_out!")


def calculateAndEmbed(fileName : str, text : str, mode : int, password : int) -> None:
    img = Image.open(f'data/{fileName}').convert("RGB")

    textb1 = convertStr2Bytes(text)
    print(textb1)
    pixel_map = img.load()

    width, height = img.size
    counter = len(textb1)
    offsetCounter = 0
    offsetFlag = False

    for i in range(width): 
        for j in range(height):
            offsetCounter += 1
            if offsetCounter >= password:
               offsetFlag = True 
            if offsetFlag:
                r, g, b = img.getpixel((i, j))

                rb = format(r, "08b")
                gb = format(g, "08b")
                bb = format(b, "08b")

                print(rb, gb, bb)

                if mode == 1:
                    rb = rb[:-1] + textb1[len(textb1) - counter]  
                    gb = gb[:-1] + textb1[len(textb1) - counter]  
                    bb = bb[:-1] + textb1[len(textb1) - counter]  
                    print(rb, gb, bb)

                    rNew = convertBytes2Int(rb)
                    gNew = convertBytes2Int(gb)
                    bNew = convertBytes2Int(bb)
                    print((rNew, gNew, bNew))

                    pixel_map[i, j] = (rNew, gNew, bNew)
                    counter -= 1
                else: 
                    rb = rb[:-2] + textb1[len(textb1) - counter + 1] + textb1[len(textb1) - counter]  
                    gb = gb[:-2] + textb1[len(textb1) - counter + 1] + textb1[len(textb1) - counter]  
                    bb = bb[:-2] + textb1[len(textb1) - counter + 1] + textb1[len(textb1) - counter] 
                    
                    print(rb, gb, bb)

                    rNew = convertBytes2Int(rb)
                    gNew = convertBytes2Int(gb)
                    bNew = convertBytes2Int(bb)
                    print((rNew, gNew, bNew))
                    pixel_map[i, j] = (rNew, gNew, bNew)
                    counter -= 2
                if counter == 0:
                    break
        else:
            continue
        break

    img.save(f"output/{fileName}_embeded.bmp")
    with open("output/text_out", "w") as f:
        f.write("Встроенный текст :" + text + "\n")
    print(f"Полученная картинка находится по пути output/{fileName}_embeded.bmp!")
    print(f"Ваш текст находится в файле output/text_out!")

