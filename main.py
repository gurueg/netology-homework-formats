import json
import xml.etree.ElementTree as ET

from pprint import pprint


def most_popular_words(text, word_len=6, words_count=10):
    words = text.split(' ')
    words = sorted(words, key=lambda a: len(a), reverse=True)
    # words = [item.lower() for item in words]

    count_dict = {}
    
    for word in words:
        if len(word)<word_len:
            break
        if word not in count_dict.keys():
            count_dict[word] = 1
        else:
            count_dict[word]+=1

    out_list = []
    for word, length in count_dict.items():
        if len(out_list) < words_count:
            out_list.append(word)
        else:
            for idx, elem in enumerate(out_list):
                if count_dict[elem] < length:
                    out_list[idx] = word
                    break
        out_list.sort(key=lambda a:count_dict[a])

    return sorted(out_list, key=lambda a:count_dict[a], reverse=True)

def json_working():
    """ Возвращает словарь содержащий все заголовки и все новости по ключам titles и descriptions """

    with open('files/newsafr.json', encoding='utf-8') as f:
        json_data = json.load(f)

    all_news = json_data['rss']['channel']['items']

    descriptions = []
    titles = []
    for item in all_news:
        descriptions.append(item['description'])
        titles.append(item['title'])

    return {'titles': titles, 'descriptions': descriptions}


def xml_working():
    """ Возвращает словарь содержащий все заголовки и все новости по ключам titles и descriptions """

    parser = ET.XMLParser(encoding='utf-8')

    tree = ET.parse('files/newsafr.xml', parser)
    root = tree.getroot()

    all_news = root.findall('channel/item')

    descriptions = []
    titles = []
    for item in all_news:
        descriptions.append(item.find('description').text)
        titles.append(item.find('title').text)

    return {'titles': titles, 'descriptions': descriptions}


def main():
    commands = {
        'xml': xml_working,
        'json': json_working
    }

    while(True):
        command = input('Введите команду для работы(json или xml) или q для выхода: ')
        if command not in commands.keys():
            if command != 'q':
                print('Команда не найдена, завершение программы')
            return
        
        result = commands[command]()

        popular_titles = most_popular_words(' '.join(result['titles']))
        popular_titles_string = ', '.join(popular_titles)
        print( f'Самые популярные слова, встречающиеся в заголовках: {popular_titles_string}' )

        popular_desc = most_popular_words(' '.join(result['descriptions']))
        popular_desc_string = ', '.join(popular_desc)
        print( f'Самые популярные слова, встречающиеся в новостях: {popular_desc_string}' )


if __name__ == '__main__':
    main()
