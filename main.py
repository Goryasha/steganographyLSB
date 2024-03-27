from functions import *

def main():
    print("Доброго дня я программа для стеганографии на основе алгоритма LSB.")
    print("Введите название файла, в который я зашифрую твой текст.")
    print("Обращаю внимание на то, что я возвращаю 24-битный BMP, следовательно в картинках будет игнорироваться альфаканал (прозрачность).")
    print("Если вы еще не загрузили файл, то это можно всегда сделать в папку data")
    fileName, shape= getFileNameAndSizeFromUser()

    print("Введите пароль. На его основе информация будет записана в определенную область картинки")
    password = getPasswordFromUser(shape = shape)
    print(password)
    print("Что мы сделаем с этим файлом?")
    option = getOptionFromUser()
    if option == 1:
        print("Проверю встраивание в последний бит и в последние два бита каждого цвета.")
        print("Буду считать, что для противостояния зашумленности последние биты каждого цвета имели при внедрении текста одинаковые значения.")
        print("Декодирование строится на предположение, что символ занимает 8 бит (английсткий алфавит в основном).")
        length = getLengthFromUser()
        calculateAndExtract(fileName = fileName, length = length, password = password)
    else:
        print("Сколько последних символов мы будем заменять?")
        last = getLastOptionFromUser()
        block = shape[0] * shape[1] // (8 // last) - password
        print("Отлично введи текст, который ты хочешь загрузить!")
        print(f"Помни, в файл поместится максимум {block} символов!")
        text = getTextFromUser(block = block)
        calculateAndEmbed(fileName = fileName, text = text, mode = last, password = password)

    print("Спасибо за использование программы!")

if __name__ == '__main__':
    main()


