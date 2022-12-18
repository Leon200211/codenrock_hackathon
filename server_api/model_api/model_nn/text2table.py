import re
from text_to_num import alpha2digit
import jellyfish
import pandas as pd
from .audio2text import get_text

termins = ['колесная пара', 'колпак скользуна', 'боковая рама', 'надрессорная балка', 'триангель тележки',
           'рассорный комплект', 'фрикционный клин', 'подвижная функциональная планка',
           'неподвижная функциональная планка', 'износостойкая прокладка', 'износостойкая прокладка в буксовый проем']
ok_words = ['год', 'завод']
comments = ['шайба', 'без', 'буксы', 'гайка', 'одна', 'букса', 'брак']
rest_words = ['ошибка', 'номер', 'китай']

dictionary_number = {
    'ноль': 0, 'ноля': 0, 'нулевой': 0, 'нулевого': 0,
    'один': 1, 'одного': 1, 'одна': 1, 'одной': 1, 'первый': 1, 'первого': 1,
    'два': 2, 'две': 2, 'двух': 2, 'второй': 2, 'вторая': 2, 'второго': 2,
    'три': 3, 'третий': 3, 'трех': 3, 'трёх': 3, 'третьей': 3, 'третьего': 3, 'четыре': 4,
    'четвертая': 4, 'четвертой': 4, 'четвертого': 4, 'четырех': 4, 'четырёх': 4, 'четвёрт': 4,
    'пять': 5, 'пятый': 5, 'пятая': 5, 'пятого': 5, 'пятой': 5, 'пяти': 5,
    'шесть': 6, 'шестой': 6, 'шести': 6, 'шестого': 6,
    'семь': 7, 'седьмой': 7, 'седьмого': 7, 'семи': 7,
    'восемь': 8, 'восьмой': 8, 'восьмого': 8, 'восьми': 8, 'восьмую': 8,
    'девять': 9, 'девятый': 9, 'девятой': 9, 'девяти': 9,
    'десять': 10, 'десятый': 10, 'десяти': 10, 'десятого': 10,
    'одиннадцать': 11, 'одиннадцатый': 11, 'одиннадцатой': 11, 'одиннадцатая': 11,
    'двенадцать': 12, 'двенадцатый': 12, 'двенадцатая': 12, 'двенадцатой': 12,
    'тринадцать': 13, 'тринадцатый': 13, 'тринадцатая': 13, 'тринадцатой': 13,
    'четырнадцать': 14, 'четырнадцатый': 14, 'четырнадцатой': 14, 'четырнадцатая': 14,
    'пятнадцать': 15, 'пятнадцатый': 15, 'пятнадцатой': 15, 'пятнадцатая': 15,
    'шестнадцать': 16, 'шестнадцатый': 16,'шестнадцатой': 16, 'шестнадцатая': 16,
    'семнадцать': 17, 'семнадцатый': 17, 'семнадцатой': 17, 'семнадцатая': 17,
    'восемнадцать': 18, 'восемнадцатый': 18, 'восемнадцатой': 18, 'восемнадцатая': 18,
    'девятнадцать': 19, 'девятнадцатый': 19, 'девятнадцатой': 19, 'девятнадцатая': 19,
    'двадцать': 20, 'двадцатый': 20, 'двадцатой': 20, 'двадцатая': 20,
    'тридцать': 30, 'тридцатый': 30, 'тридцатой': 30, 'тридцатая': 30,
    'сорок': 40, 'сороковой': 40, 'сороковая': 40, 'сорокового': 40,
    'пятьдесят': 50, 'пятидесятый': 50, 'пятидесятого': 50, 'пятидесятая': 50, 'пятидесятой': 50,
    'шестьдесят': 60, 'шестидесятый': 60, 'шестидесятая': 60, 'шестидесятой': 60, 'шестидесятого': 60,
    'семьдесят': 70, 'семидесятый': 70, 'семидесятого': 70, 'семидесятая': 70, 'семидесятой': 70,
    'восемьдесят': 80, 'восьмидесятый': 80, 'восьмидесятого': 80, 'восьмидесятая': 80, 'восьмидесятой': 80,
    'девяносто': 90, 'девяностый': 90, 'девяностого': 90, 'девяностая': 90, 'девяностой': 90,
    'сто': 100, 'сотый': 0, 'сотого': 0, 'сотая': 0, 'сотой': 0,
    'двести': 200, 'двухсотый': 200, 'двухсотая': 200, 'двухсотой': 200, 'двухсотого': 200,
    'триста': 300, 'трехсотый': 300, 'трехсотая': 300, 'трехсотого': 300, 'трехсотой': 300,
    'четыреста': 400, 'четырехсотый': 400, 'четырехсотого': 400, 'четырехсотая': 400, 'четырехсотой': 400,
    'пятьсот': 500, 'пятисотый': 500, 'пятисотого': 500, 'пятисотая': 500, 'пятисотой': 500,
    'шестьсот': 600, 'шестисотый': 600, 'шестисотого': 600, 'шестисотая': 600, 'шестисотой': 600,
    'семьсот': 700, 'семисотый': 700, 'семисотого': 700, 'семисотая': 700, 'семисотой': 700,
    'восемьсот': 800, 'восьмисотый': 800, 'восьмисотого': 800, 'восьмисотая': 800, 'восьмисотой': 800,
    'девятьсот': 900, 'девятисотый': 900, 'девятисотого': 900, 'девятисотая': 900, 'девятисотой': 900,
    'тысяча': 1000, 'тысячи': 1000,  'тысячного': 1000, 'тысячной': 1000,
    'тысячный': 1000, 'тысяч': 1000,
    'миллион': 1000000, 'миллиона': 10000000,
}

decimal_words = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']

ending = ['ый', 'ий', 'ое', 'ой', 'ая', 'ые', 'ого', 'ых', 'ому', 'ым', 'ую', 'ыми', 'ом']



def number_formation(number_words):
    '''Форматирование чисел'''
    numbers = []
    for number_word in number_words:
        numbers.append(dictionary_number[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]



def get_decimal_sum(decimal_digit_words):
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(dictionary_number[dec_word])
    final_decimal_string = '0.' + ''.join(map(str, decimal_number_str))
    return float(final_decimal_string)


def word_to_num(number_sentence):
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string! Please enter a valid number word "
                         "(eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()  # converting input to lowercase

    if (number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []
    index = []
    return_str = ''

    for word in range(len(split_words)):
        if split_words[word] in dictionary_number:
            clean_numbers.append(split_words[word])
            index.append(word)

    # Error if user enters million,billion, thousand or decimal point twice
    if clean_numbers.count('тысяча') > 1 or clean_numbers.count('миллион') > 1\
            or clean_numbers.count('тысячи') > 1:
        raise ValueError("Redundant number word! Please enter a valid number word "
                         "(eg. two million twenty three thousand and forty nine)")

    # separate decimal part of number (if exists)
    if clean_numbers.count('point') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('point')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('point')]

    billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    million_index = clean_numbers.index('миллион') if 'миллион' in clean_numbers else -1
    thousand_index = clean_numbers.index('тысячи') if 'тысячи' in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or \
            (million_index > -1 and million_index < billion_index):
        raise ValueError("Malformed number! Please enter a valid number word "
                         "(eg. two million twenty three thousand and forty nine)")

    total_sum = []  # storing the number to be returned

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
                #total_sum += dictionary_number[clean_numbers[0]]
                total_sum.append(dictionary_number[clean_numbers[0]])
                #print(total_sum)

        else:
            if len(clean_numbers) == 2:
                for i in range(len(clean_numbers)):
                    total_sum.append(dictionary_number[clean_numbers[i]])
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum.append(dictionary_number[clean_numbers[0]])

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum.append(million_multiplier * 1000000)


            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum.append(million_multiplier * 1000000)

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:])
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:])
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum.append(hundreds)

    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_sum(clean_decimal_numbers)
        total_sum.append(decimal_sum)

    if len(index) == 0:
        return_str = " ".join(str(x) for x in split_words)

    elif len(index) == 1:
        a = str(index[0])
        b = int(a)
        return_str = " ".join(str(x) for x in split_words[:b]) + ' ' + str(total_sum[0]) + ' ' \
                 + " ".join(str(x) for x in split_words[b+1:])

    else:
        if len(index) == 2:
            a = str(index[0])
            b = str(index[1])
            c = int(a)
            d = int(b)
            return_str = " ".join(str(x) for x in split_words[:c]) + ' ' + str(total_sum[0]) + ' ' \
                         + " ".join(str(x) for x in split_words[c + 1:d]) + ' ' + str(total_sum[1]) + ' ' \
                            + " ".join(str(x) for x in split_words[d+1:])

    return return_str

def pars_endings(texts):
    '''Парсинг окончаний для числительных'''
    return_texts = []
    for string in texts:
        split_string = string.strip().split()
        for index in range(len(split_string)):
            s_word = split_string[split_string.index(split_string[index])]
            if not split_string[index].isalpha():
                word = re.sub(r'[а-я]+\s?', '', split_string[index]).strip()
                s_word = word
            split_string[index] = s_word
        return_string = ' '.join(split_string)
        return_texts.append(return_string)

    return return_texts


def parse(texts):
    '''Замена числительных, написанных словами, на цифры'''
    new_text = []
    for i in texts:
        new_text.append(word_to_num(i))
    new_text = pars_endings(new_text)
    return new_text

def merge_dictionary(mas):
    dict1 = mas[0]
    dict2 = mas[1]
    dict3 = dict1.copy()
    for key, value in dict2.items():
        dict3[key] = value

    return dict3



def dataframe(large_mas):
    '''Создание датафрейма'''
    dict_dict = []
    for index in large_mas:
        dict_dict.append(merge_dictionary(index))
    df = pd.DataFrame.from_dict(dict_dict, orient='columns')
    df.set_index(['наименование'], inplace=True)
    df = df.replace('-', '', regex=True)
    new_df = df.reindex(columns=['номер', 'год', 'завод', 'комментарий'])
    new_df['комментарий'] = new_df['комментарий'].str.replace('без,', 'без')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='без букса', value='без буксы')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='гайка, букса', value='гайка, без буксы')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='гайка, без букса', value='гайка, без буксы')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='букса', value='одна букса')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='гайка, букса', value='гайка, одна букса')
    new_df['комментарий'] = new_df.комментарий.replace(to_replace='шайба, букса', value='шайба, одна букса')
    new_index = []
    new_df['завод'] = new_df['завод'].fillna(0)
    for index in new_df.завод:
        if (type(index) == int or type(index) == float):
            if index > 2000:
                index = index - 2000
            elif 1900 <= index < 2000:
                index = index - 1900
            new_index.append(int(index))
        else:
            new_index.append(index)
    new_df['завод'] = new_index

    return new_df

def convert_csv(d_f):
    '''Конвертирование датафрейма в csv'''
    d_f.to_csv('output.csv')

def format_string(str):
    '''Исправление неправильных вариаций ключевых слов'''
    str = str.replace("зовут", "завод")
    str = str.replace("заводы", "завод")
    str = str.replace("зао", "завод")
    str = str.replace("живот", "завод")
    str = str.replace("город", "завод")
    str = str.replace("нам", "номер")
    str = " ".join(sorted(set(str.split()), key=str.split().index))
    return str

def find_name(str):
    '''Поиск названия детали в подстроке'''
    name = ''
    pos = re.search(r"\d", str)
    new_name = str[0:pos.start()].strip()
    information = str[pos.start():].strip().split(' ')
    return [new_name, information]

def clear_str(str):
    result = list()
    words = []
    str = str.split(" ")
    for i in range(len(str)):
        if str[i].isdigit() == True:
            result.append()

def delete_bad_words(str):
    '''Удаление лишних слов, которые не относятся к составлению таблицы'''
    info = list()
    comment = list()
    if type(str) != list:
        str = str.split(" ")
    try:
        z = str.index("завод")
    except ValueError:
        z = -1
        info.append('завод-')
    try:
        g = str.index("год")
    except ValueError:
        g = -1
        info.append('год-')
    last_ok_word = [z if z > g else g][0]
    for words in str:
        if words == 'китай':
            info.append(words)
        if z == len(str) - 1  or g == len(str) - 1:
            if words.isdigit() == False:
                if words in ok_words:
                    info.append(words)
            else:
                info.append(words)
        elif z != -1 or g != -1:
            if words.isdigit() == False:
                if words in ok_words:
                    info.append(words)
                elif str.index(words) > last_ok_word and words in comments:
                    comment.append("комментарий")
                    comment.append(words)
            else:
                info.append(words)

    if len(comment) != 0:
        if len(comment) != 1:
            for i in range(len(comment)):
                info.append(comment[i])
        else:
            info.append(comment[0])
    return info

def convert_num(num):
    '''Функция для конвертиации годов в указанный формат'''
    if float(num) < 2000.0 and float(num) > 1900.0:
        return float(num)
    elif float(num) > 23.0 and float(num) < 2000.0:
        return float(num) + 1900.0
    elif float(num) >= 1 and float(num) <= 22:
        return float(num) + 2000.0
    elif float(num) >= 2000:
        return float(num)

def parse_info(mas):
        '''Парсер всех парамтеров, кроме "наименования, а также составление словаря для будущего датафрейма'''
        dict = {}
        comment = list()
        number = ''
        last_info_index = 100
        i = 0
        count = 0
        if 'комментарий' in mas:
            for i in range(len(mas)):
                if mas[i] == 'комментарий':
                    count += 1
            if "год" in mas:
                if abs(mas.index("комментарий") - mas.index("год")) == 3 and \
                        (mas[mas.index("год") + 1].isdigit() and mas[mas.index("год") + 2].isdigit()):
                    mas[mas.index("год") + 1] = str(int(mas[mas.index("год") + 1]) + int(mas[mas.index("год") + 2]))
                    mas.pop(mas.index("год") + 2)
        if "завод" not in mas and "год" not in mas:
            return dict
        elif 'завод-' in mas and 'год-' not in mas and "год" in mas:
                dict['завод'] = '-'
                mas.pop(mas.index('завод-'))
                last_info_index = mas.index('год')
                last_index_num = len(mas) - count * 2 - 2
        elif 'завод-' not in mas and 'год-' in mas and "завод" in mas:
            dict['год'] = '-'
            last_info_index = mas.index('завод')
            last_index_num = len(mas) - count * 2 - 2
        else:
            if 'китай' in mas:
                dict['завод'] = 'китай'
                if mas.index('китай') == mas.index('завод') - 1:
                    last_index_num = mas.index('китай') - 1
                elif mas.index('китай') == mas.index('завод') + 1:
                    last_index_num = mas.index('завод') - 1
            elif mas.index('год') + 1 == mas.index('завод') and mas.index('завод') == len(mas) - 1:
                dict['завод'] = '-'
                last_index_num = mas.index('год') - 1
            elif mas.index('год') == mas.index('завод') + 1 and mas.index('год') == len(mas) - 1:
                dict['год'] = '-'
                last_index_num = mas.index('завод') - 1
            elif mas.index('год') + 1 == mas.index('завод'):
                dict['год'] = convert_num(mas[mas.index('год') - 1])
                dict['завод'] = convert_num(mas[mas.index('завод') + 1])
                last_index_num = mas.index('год') - 1
            elif mas.index('год') == mas.index('завод') + 1:
                dict['год'] = convert_num(mas[mas.index('год') + 1])
                dict['завод'] = convert_num(mas[mas.index('завод') - 1])
                last_index_num = mas.index('завод') - 1
            else:
                last_info_index = [mas.index('завод') if mas.index('завод') > mas.index('год') else mas.index('год')][0]
                last_index_num = len(mas) - count * 2 - 4
        for i in range(0, last_index_num):
            if mas[i].isdigit() == True:
                number += mas[i]
            else:
                last_index_num -= 1
                continue
        dict['номер'] = number
        i = last_index_num
        if 'комментарий' not in mas[i] and mas[-1].isdigit() == True:
            mas = mas[0:last_info_index + 2]
        k = 0
        while i != len(mas) or k == 4:
            if 'завод' in dict and 'год' in dict and i + 1 == len(mas):
                break
            elif i + 1 == len(mas):
                i += 1
            elif mas[i] == 'год' and mas[i + 1].isdigit() == True:
                i += 1
                if float(mas[i]) < 2000.0 and float(mas[i]) > 1900.0:
                    dict['год'] = float(mas[i])
                    i += 1
                elif float(mas[i]) > 23.0 and float(mas[i]) < 2000.0:
                    dict['год'] = float(mas[i]) + 1900.0
                    i += 1
                elif float(mas[i]) >= 1 and float(mas[i]) <= 22:
                    dict['год'] = float(mas[i]) + 2000.0
                    i += 1
                elif float(mas[i]) >= 2000:
                    dict['год'] = float(mas[i])
                    i += 1
            elif mas[i + 1] == 'год' and mas[i].isdigit() == True:
                if float(mas[i]) < 2000.0 and float(mas[i]) > 1900.0:
                    dict['год'] = float(mas[i])
                    i += 2
                elif float(mas[i]) > 23.0 and float(mas[i]) < 2000.0:
                    dict['год'] = float(mas[i]) + 1900.0
                    i += 2
                elif float(mas[i]) >= 2000:
                    dict['год'] = float(mas[i])
                    i += 2
                elif float(mas[i]) >= 1 and float(mas[i]) <= 22:
                    dict['год'] = float(mas[i]) + 2000.0
                    i += 2
            elif mas[i] == 'завод' and 'завод' not in dict:
                if mas[i + 1].isdigit() == True:
                    i += 1
                    dict['завод'] = int(mas[i])
                    i += 1
                elif mas[i] == 'китай':
                    i += 1
                    dict['завод'] = mas[i]
                    i += 1
            elif mas[i + 1] == 'завод' and 'завод' not in dict:
                if mas[i].isdigit() == True:
                    dict['завод'] = int(mas[i])
                    i += 2
                elif mas[i] == 'китай':
                    dict['завод'] = mas[i]
                    i += 2
            elif mas[i] == 'комментарий':
                i += 1
                comment.append(mas[i])
                i += 1
            else:
                i += 1
        if len(comment) != 0:
            dict['комментарий'] = ', '.join(comment)
        return dict



def format_text(filename):
    '''Функция форматирования исходного текста'''
    with open(filename) as f:
      text = f.read()
    text = text.strip("\n\"\"")
    text = alpha2digit(text, "ru")
    result = re.split(r"следующая | начало | записи | следующий | следующее | следующей | следующие", text)
    #result = re.split(r"след", result)
    print(result)
    result = parse(result)
    result = list(filter(None, result))  # удаление пустых подмасивов
    #result.pop(result.index('начало'))
    for i in range(len(result)):
        if len(result[i].split(" ")) > 40 or len(result[i].split(" ")) <= 4:
            continue
        result[i] = re.split(r"номер | ошибка | нам", result[i])
        for j in range(len(result[i])):
            result[i][j] = format_string(result[i][j])
        result[i] = list(filter(None, result[i]))  # удаление пустых строк
        if len(result[i]) > 2:
            result[i] = result[i][0:len(result[i]) - 1]
            '''if len(result[i][1].split(' ')) < 2:
                continue'''
        for j in range(len(result[i])):
            result[i][j] = result[i][j].strip()
        if len(result[i]) == 1:
            result[i] = find_name(result[i][0])
            result[i][0] = ''.join([i for i in result[i][0] if not i.isdigit()])
            dict = {}
            if len(result[i][0].split(" ")) > 2:
                buf = result[i][0].split(" ")[1] + " " + result[i][0].split(" ")[2]
                result[i][0] = buf
            dict['наименование'] = result[i][0]
            result[i][0] = dict
            result[i][1] = delete_bad_words(result[i][1])
            continue
        elif result[i][1][0].isdigit() == False and len(result[i][1]) == 2:
                result[i] = find_name(result[i][1])

        result[i][0] = ''.join([i for i in result[i][0] if not i.isdigit()]).strip()
        dict = {}
        if len(result[i][0].split(" ")) > 2:
            buf = result[i][0].split(" ")[1] + " " + result[i][0].split(" ")[2]
            result[i][0] = buf
        dict['наименование'] = result[i][0]
        result[i][0] = dict
        result[i][1] = delete_bad_words(result[i][1])
    result = fix_command(result)
    for i in range(len(result)):
        result[i][1] = parse_info(result[i][1])
    df = dataframe(result)
    print(df)
    convert_csv(df)
    return result

def fix_command(text):
    '''Определение названия детали для разных вариаций ее написание'''
    count = 0
    result = list()
    for mas in text:
        if type(mas[0]) == dict:
            num = 10000
            name = mas[0].get('наименование')
            for i in range(len(termins)):
                if type(mas[0].get('наименование')) == list:
                    buf = mas[0].get('наименование')[0] + " " + mas[0].get('наименование')[1]
                    res = jellyfish.damerau_levenshtein_distance(buf, termins[i])
                else:
                    res = jellyfish.damerau_levenshtein_distance(mas[0].get('наименование'), termins[i])
                if res < num:
                    num = res
                    name = termins[i]
            mas[0]['наименование'] = name
            result.append(mas)
            #print(mas)
    return result

def main(filename):
    #get_text(filename) #раскомментить надо
    mas_text = format_text("data.txt")

#filename = 'здесь название файла должно быть'
#main(filename)
mas_text = format_text("data.txt")