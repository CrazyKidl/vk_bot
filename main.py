import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import wikipedia
from vk_api import VkUpload
import requests
import emoji
import time
from bs4 import BeautifulSoup
import cfscrape
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from yandex_translate import YandexTranslate


def main():

    with open('audio_list.txt', 'r') as audiolist:
        audio_list = []
        audio = audiolist.read().splitlines()
        for i in audio:
            a, b = i.split(', ')
            audio_list.append([int(a), int(b)])
    vk_session = vk_api.VkApi(
        token="a29402b61e4d81ecbd0c0bafca4bfe9e5fca66942fd5e283c1946abbc50d38f084a33ee6fe98fe717bbec")
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, 192674616)
    wikipedia.set_lang("RU")
    upload = VkUpload(vk_session)
    session = requests.Session()
    translate = YandexTranslate('trnsl.1.1.20200420T104155Z.20651825ec88b646.9a67150ea679d890a8bb3d0d22f2040f3e283f0b')
    abc = {'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', 'a': 'ф',
           's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', 'z': 'я', 'x': 'ч', 'c': 'с',
           'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', '[': 'х', ']': 'ъ', ',': 'б', '.': 'ю', "'": 'э', ' ': ' ', 'Q': 'Й',
           'W': 'Ц', 'E': 'У', 'R': 'К', 'T': 'Е', 'Y': 'Н', 'U': 'Г', 'I': 'Ш', 'O': 'Щ', 'P': 'З', 'A': 'Ф',
           'S': 'Ы', 'D': 'В', 'F': 'А', 'G': 'П', 'H': 'Р', 'J': 'О', 'K': 'Л', 'L': 'Д', 'Z': 'Я', 'X': 'Ч', 'C': 'С',
           'V': 'М', 'B': 'И', 'N': 'Т', 'M': 'Ь', '{': 'Х', '}': 'Ъ', '<': 'Б', '>': 'Ю', '"': 'Э', ';': 'ж', ':': 'Ж'}
    cba = {'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u', 'ш': 'i', 'щ': 'o', 'з': 'p', 'ф': 'a',
           'ы': 's', 'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l', 'я': 'z', 'ч': 'x', 'с': 'c',
           'м': 'v', 'и': 'b', 'т': 'n', 'ь': 'm', 'х': '[', 'ъ': ']', 'б': 'k', 'ю': '>', "э": "'", ' ': ' ', 'Й': 'Q',
           'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U', 'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Ф': 'A',
           'Ы': 'S', 'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L', 'Я': 'Z', 'Ч': 'X', 'С': 'C',
           'М': 'V', 'И': 'B', 'Т': 'N', 'Ь': 'M', 'Х': '{', 'Ъ': '}', 'Б': '<', 'Ю': '>', 'Э': '"', 'ж': ';', 'Ж': ':'}
    chars = 'abcdefghijklnopqrstuvwxyz123456789'

    def to_fixed(num, digits=0):
        return f"{num:.{digits}f}"

    def pic():
        site = 'https://prnt.sc/'
        for i in range(6):
            site += random.choice(chars)
        soup = BeautifulSoup(cfscrape.create_scraper().get(site).content.decode('utf-8'), 'html.parser')
        for l in soup.find_all('img'):
            try:
                send_img(l.get('src'))
                return True
            except Exception as e:
                print('Картинки не было найдено(')
                pass

    def send(mes):
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=mes)

    def send_att(mes, att):
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=mes, attachment=att)

    def send_audio(a):
        attachments = []
        audio_list_copy = audio_list
        while a != 0:
            if a > 11:
                send('Даун я же сказал до 10')
                break
            random_audio = random.choice(audio_list_copy)
            aud = f"audio{random_audio[0]}_{random_audio[1]}"
            attachments.append(aud)
            a -= 1
        if a == 0:
            send_att(mes='', att=','.join(attachments))

    def send_text_img(mes, img):
        attachments = []
        image = session.get(img, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
        vk.messages.send(chat_id=event.chat_id, attachment=','.join(attachments), random_id=get_random_id(),
                         message=mes)
        attachments.remove('photo{}_{}'.format(photo['owner_id'], photo['id']))

    def send_img(image_url):
        attachments = []
        image = session.get(image_url, stream=True)
        photo = upload.photo_messages(photos=image.raw)[0]
        attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
        vk.messages.send(chat_id=event.chat_id, attachment=','.join(attachments), random_id=get_random_id(),
                         message='')
        attachments.remove('photo{}_{}'.format(photo['owner_id'], photo['id']))

    def send_k(*butt, mes):
        keyboard = VkKeyboard(one_time=True)
        i = 0
        while i != len(butt) - 2:
            keyboard.add_button(butt[i], color=VkKeyboardColor.PRIMARY)
            i += 1
            if i % 3 == 0:
                keyboard.add_line()
        keyboard.add_line()
        keyboard.add_button(butt[len(butt) - 2], color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(butt[len(butt) - 1], color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), keyboard=keyboard.get_keyboard(),
                         message=mes)

    def send_keyboard(*butt, mes):
        keyboard = VkKeyboard(one_time=True)
        i = 0
        while i != len(butt):
            keyboard.add_button(butt[i], color=VkKeyboardColor.PRIMARY)
            if i % 2 != 0 and len(butt) - 1 != i and i != 0:
                keyboard.add_line()
            i += 1
        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), keyboard=keyboard.get_keyboard(),
                         message=mes)

    def send_mes(imgs, mes):
        attachments = []
        i = 0
        print('i')
        while i <= len(imgs):
            if i <= 9 and i >= 0:
                while i <= 9 and i != len(imgs):
                    image = session.get(imgs[i], stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    i += 1
                if i == 10:
                    send_att(att=','.join(attachments), mes='Лови\n' + mes)
                    attachments = []
                    continue
                else:
                    send_att(att=','.join(attachments), mes='Лови\n' + mes)
                    break
            elif i <= 19 and i >= 10:
                while i != len(imgs) and i <= 19:
                    image = session.get(imgs[i], stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    i += 1
                if i == 20:
                    send_att(att=','.join(attachments), mes=mes)
                    attachments = []
                    continue
                else:
                    send_att(att=','.join(attachments), mes=mes)
                    break
            elif i <= 29 and i >= 20:
                while i != len(imgs) and i <= 29:
                    image = session.get(imgs[i], stream=True)
                    photo = upload.photo_messages(photos=image.raw)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    i += 1
                if i == 30:
                    send_att(att=','.join(attachments), mes=mes)
                    attachments = []
                    continue
                else:
                    send_att(att=','.join(attachments), mes=mes)
                    return 0

    def send_ex(file, site, n):
        try:
            for event in longpoll.listen():
                if event.object.text.lower() == 'отмена':
                    send('Ну ладна пака((9(')
                    return 'break'
                try:
                    int(event.object.text)
                except Exception as e:
                    send('Тяжело ввести число штолле')
                    print(e)
                    return 'break'
                if n == 0:
                    site_ = site + str(event.object.text)
                    file = open(file + str(event.object.text) + '.txt', 'r')
                    print(file)
                else:
                    site_ = site + str(event.object.text) + n
                    file = open(file + n + str(event.object.text) + '.txt', 'r')
                images = file.read().splitlines()
                print(images)
                send_mes(images, site_)
                return 'break'
        except Exception as e:
            send('Такого номера нет довн\nПопробуйте ввести ' + str(int(event.object.text) - 1) + ' или ' + str(
                int(event.object.text) + 1) + '\nДля отмены напишите "Отмена"')
            print(e)
            if send_ex(file=file, site=site, n=n) == 'break': return 'break'
            return 'break'

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
            print(event.object.text)
            if event.object.text.lower() == 'разрабы' or event.object.text.lower() == 'разработчики':
                send('@lev_poznyakov(Лев Позняков) \nПри поддержке \n@lilechkapetushok(Лиля Петухова)')
            elif event.object.text.lower() == 'гдз' or event.object.text.lower() == 'gdz' or event.object.text.lower() == 'ulp' or event.object.text.lower() == 'пвя':
                site = 'https://gdz.ru/'
                file = 'gdz/'
                send_k('7 класс', '6 класс', 'Поддержка разрабов деньгами', 'Отмена', mes='Выберите действие: ')
                for event in longpoll.listen():
                    if event.object.text.lower() == '[club192674616|@dapizdabot] поддержка разрабов деньгами' or event.object.text.lower() == '[club192674616|да (бот)] поддержка разрабов деньгами':
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=192674616&aid=6222115")
                        vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(),
                                         keyboard=keyboard.get_keyboard(),
                                         message='Можно не деньгами просто потестируй меня(')
                        break
                    elif event.object.text.lower() == '[club192674616|@dapizdabot] 7 класс' or event.object.text.lower() == '[club192674616|да (бот)] 7 класс':
                        site += 'class-7/'
                        file += 'class-7/'
                        send_keyboard('Алгебра', 'Русский язык', 'История', 'Физика', 'Геометрия',
                                      mes='Выберите предмет: ')
                        for event in longpoll.listen():
                            if event.object.text.lower() == '[club192674616|@dapizdabot] алгебра' or event.object.text.lower() == '[club192674616|да (бот)] алгебра':
                                site += 'algebra/'
                                file += 'algebra/'
                                send_keyboard('Просвещение', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] просвещение' or event.object.text.lower() == '[club192674616|да (бот)] просвещение':
                                        site += 'makarichev-18/'
                                        file += 'makarichev-18/'
                                        send_keyboard('Задания', 'Контрольные задания и вопросы', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] задания' or event.object.text.lower() == '[club192674616|да (бот)] задания':
                                                send('Введите номер задания: ')
                                                if send_ex(file=file, site=site, n='-nom/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] контрольные задания и вопросы' or event.object.text.lower() == '[club192674616|да (бот)] контрольные задания и вопросы':
                                                send('Введите номер задания: ')
                                                if send_ex(file=file, site=site, n='-knom/') == 'break': break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    else:
                                        send('Ты чо сказал я не понял пака')
                                        break
                                break
                            elif event.object.text.lower() == '[club192674616|@dapizdabot] русский язык' or event.object.text.lower() == '[club192674616|да (бот)] русский язык':
                                site += 'russkii_yazik/'
                                file += 'russkii_yazik/'
                                send_keyboard('Разумовская', 'Ладыженская, Баранова', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] разумовская' or event.object.text.lower() == '[club192674616|да (бот)] разумовская':
                                        site += 'razumovskaja-lvova-7/'
                                        file += 'razumovskaja-lvova-7/'
                                        send_keyboard('Упражнения', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] упражнения' or event.object.text.lower() == '[club192674616|да (бот)] упражнения':
                                                send('Введите номер упражнения: ')
                                                if send_ex(file=file, site=site, n='/') == 'break': break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    elif event.object.text.lower() == '[club192674616|@dapizdabot] ладыженская, баранова' or event.object.text.lower() == '[club192674616|да (бот)] ладыженская, баранова':
                                        site += 'baranova/'
                                        file += 'baranova/'
                                        send_keyboard('Упражнения', 'Материал для самостоятельных наблюдений',
                                                      'Контрольные',
                                                      'Контрольные (2019)', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] упражнения' or event.object.text.lower() == '[club192674616|да (бот)] упражнения':
                                                send('Введите номер упражнения: ')
                                                if send_ex(file=file, site=site, n='-nom/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] материал для самостоятельных наблюдений' or event.object.text.lower() == '[club192674616|да (бот)] материал для самостоятельных наблюдений':
                                                send('Введите номер параграфа: ')
                                                if send_ex(file=file, site=site, n='-item/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] контрольные' or event.object.text.lower() == '[club192674616|да (бот)] контрольные':
                                                send('Введите номер страницы: ')
                                                if send_ex(file=file, site=site, n='-kontrol/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] контрольные (2019)' or event.object.text.lower() == '[club192674616|да (бот)] контрольные (2019)':
                                                send_keyboard('1 Часть', '2 Часть', mes='Выберите часть учебника: ')
                                                for event in longpoll.listen():
                                                    if event.object.text.lower() == '[club192674616|@dapizdabot] 1 часть' or event.object.text.lower() == '[club192674616|да (бот)] 1 часть':
                                                        site = site + '1-prt-'
                                                        file = file + '1-prt-/'
                                                        send('Введите номер страницы: ')
                                                        if send_ex(file=file, site=site, n=0) == 'break': break
                                                        break
                                                    elif event.object.text.lower() == '[club192674616|@dapizdabot] 2 часть' or event.object.text.lower() == '[club192674616|да (бот)] 2 часть':
                                                        site = site + '2-prt-'
                                                        file = file + '2-prt-/'
                                                        send('Введите номер страницы: ')
                                                        if send_ex(file=file, site=site, n=0) == 'break': break
                                                        break
                                                    else:
                                                        send('Ты чо сказал я не понял пака')
                                                        break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    else:
                                        send('Ты чо сказал я не понял пака')
                                        break
                                break
                            elif event.object.text.lower() == '[club192674616|@dapizdabot] история' or event.object.text.lower() == '[club192674616|да (бот)] история':
                                site += 'istoriya/'
                                file += 'istoriya/'
                                send_keyboard('История России (Арсентьев)', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] история россии (арсентьев)' or event.object.text.lower() == '[club192674616|да (бот)] история россии (арсентьев)':
                                        site += 'arsentjev/'
                                        file += 'arsentjev/'
                                        send_keyboard('Параграфы', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] параграфы' or event.object.text.lower() == '[club192674616|да (бот)] параграфы':
                                                send('Введите номер параграфа: ')
                                                if send_ex(file=file, site=site, n='-item/') == 'break': break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    else:
                                        send('Ты чо сказал я не понял пака')
                                        break
                                break
                            elif event.object.text.lower() == '[club192674616|@dapizdabot] физика' or event.object.text.lower() == '[club192674616|да (бот)] физика':
                                site += 'fizika/'
                                file += 'fizika/'
                                send_keyboard('Перышкин', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] перышкин' or event.object.text.lower() == '[club192674616|да (бот)] перышкин':
                                        site += 'peryshkin-7/'
                                        file += 'peryshkin-7/'
                                        send_keyboard('Упражнения', 'Вопросы в конце параграфа',
                                                      'Задания. Параграфы',
                                                      'Проверь себя. Глава', 'Лабораторные работы', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] упражнения' or event.object.text.lower() == '[club192674616|да (бот)] упражнения':
                                                send('Введите номер упражнения: ')
                                                for event in longpoll.listen():
                                                    try:
                                                        int(event.object.text)
                                                    except Exception as e:
                                                        print(e)
                                                        send('Тяжело ввести число штолле')
                                                        break
                                                    site += event.object.text + '-nom-'
                                                    file += event.object.text + '-nom-/'
                                                    send('Введите номер задания: ')
                                                    if send_ex(file=file, site=site, n=0) == 'break': break
                                                    break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] вопросы в конце параграфа' or event.object.text.lower() == '[club192674616|да (бот)] вопросы в конце параграфа':
                                                send('Введите номер параграфа: ')
                                                if send_ex(file=file, site=site, n='-quest/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] задания. параграфы' or event.object.text.lower() == '[club192674616|да (бот)] задания. параграфы':
                                                send('Введите номер параграфа: ')
                                                if send_ex(file=file, site=site, n='-inom/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] проверь себя. глава' or event.object.text.lower() == '[club192674616|да (бот)] проверь себя. глава':
                                                send('Введите номер главы: ')
                                                if send_ex(file=file, site=site, n='-chec/') == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] лабораторные работы' or event.object.text.lower() == '[club192674616|да (бот)] лабораторные работы':
                                                send('Введите номер работы: ')
                                                if send_ex(file=file, site=site, n='-laborator/') == 'break': break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    else:
                                        send('Ты чо сказал я не понял пака')
                                        break
                                break
                            elif event.object.text.lower() == '[club192674616|@dapizdabot] геометрия' or event.object.text.lower() == '[club192674616|да (бот)] геометрия':
                                site += 'geometria/'
                                file += 'geometria/'
                                send_keyboard('Погорелов', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] погорелов' or event.object.text.lower() == '[club192674616|да (бот)] погорелов':
                                        site += 'pogorelov-9/'
                                        file += 'pogorelov-9/'
                                        send_keyboard('Параграфы', mes='Выберите: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] параграфы' or event.object.text.lower() == '[club192674616|да (бот)] параграфы':
                                                send('Введите номер параграфа: ')
                                                for event in longpoll.listen():
                                                    try:
                                                        int(event.object.text)
                                                    except Exception as e:
                                                        print(e)
                                                        send('Тяжело ввести число штолле')
                                                        break
                                                    site += event.object.text + '-item-'
                                                    file += event.object.text + '-item-/'
                                                    send('Введите номер задания: ')
                                                    if send_ex(file=file, site=site, n=0) == 'break': break
                                                    break
                                                break
                            else:
                                send('Ты чо сказал я не понял пака')
                                break
                        break
                    elif event.object.text.lower() == '[club192674616|@dapizdabot] 6 класс' or event.object.text.lower() == '[club192674616|да (бот)] 6 класс':
                        site += 'class-6/'
                        file += 'class-6/'
                        send_keyboard('Английский', mes='Выберите предмет: ')
                        for event in longpoll.listen():
                            if event.object.text.lower() == '[club192674616|@dapizdabot] английский' or event.object.text.lower() == '[club192674616|да (бот)] английский':
                                site += 'english/'
                                file += 'english/'
                                send_keyboard('Афанасьева', mes='Выберите учебник: ')
                                for event in longpoll.listen():
                                    if event.object.text.lower() == '[club192674616|@dapizdabot] афанасьева' or event.object.text.lower() == '[club192674616|да (бот)] афанасьева':
                                        site += 'afanaseva-14/'
                                        file += 'afanaseva-14/'
                                        send_keyboard('1 часть', '2 часть', mes='Выберите часть: ')
                                        for event in longpoll.listen():
                                            if event.object.text.lower() == '[club192674616|@dapizdabot] 1 часть' or event.object.text.lower() == '[club192674616|да (бот)] 1 часть':
                                                site = site + '1-prt-'
                                                file = file + '1-prt-/'
                                                send('Введите номер страницы: ')
                                                if send_ex(file=file, site=site, n=0) == 'break': break
                                                break
                                            elif event.object.text.lower() == '[club192674616|@dapizdabot] 2 часть' or event.object.text.lower() == '[club192674616|да (бот)] 2 часть':
                                                site = site + '2-prt-'
                                                file = file + '2-prt-/'
                                                send('Введите номер страницы: ')
                                                if send_ex(file=file, site=site, n=0) == 'break': break
                                                break
                                            else:
                                                send('Ты чо сказал я не понял пака')
                                                break
                                        break
                                    else:
                                        send('Ты чо сказал я не понял пака')
                                        break
                                break
                            else:
                                send('Ты чо сказал я не понял пака')
                                break
                        break
                    elif event.object.text.lower() == '[club192674616|@dapizdabot] отмена' or event.object.text.lower() == '[club192674616|да (бот)] отмена':
                        send('Ну ладна пака')
                        break
                    else:
                        send('Ты чо сказал я не понял пака')
                        break
            elif event.object.text.lower() == 'переводчик' or event.object.text.lower() == 'p' or event.object.text.lower() == 'п':
                send('На какой язык?\nНапример: Русский - ru, Английский - en')
                for event in longpoll.listen():
                    translateTo = event.object.text
                    send('Введите фразу, которую надо перевести: ')
                    for event in longpoll.listen():
                        try:
                            translateFrom = translate.detect(event.object.text)
                            translated = translate.translate(event.object.text, translateFrom + '-' + translateTo)
                            send(translated['text'])
                            break
                        except Exception as e:
                            send('Ты даун не')
                            print(e)
                            break
                    break
            elif event.object.text.lower() == 'случайная картинка':
                while 1:
                    if pic() == True:
                        break
                    else:
                        pass
            elif event.object.text.lower() == "добавь аудио" or event.object.text.lower() == "добавить аудио" or event.object.text.lower() == "+аудио":
                send("Какое аудио? И сколько песен?")
                for event in longpoll.listen():
                    try:
                        i = int(event.object.text)
                    except Exception as e:
                        send('Довн число введи')
                        print(e)
                        break
                    while i != 0:
                        audio = event.object['attachments'][i - 1].get('audio')
                        audio_id = audio.get('id')
                        audio_owner_id = audio.get('owner_id')
                        aud = open('audio_list.txt', 'a')
                        aud.write('\n' + str(audio_owner_id) + ', ' + str(audio_id))
                        aud.close()
                        i -= 1
                    send('Добавил')
                    break
            elif event.object.text.lower() == "кик" or event.object.text.lower() == "kick":
                admins = []
                for element in vk.messages.getConversationMembers(peer_id=event.obj.peer_id, fields='items')['items']:
                    try:
                        if element['is_admin'] == True:
                            admins.append(element['member_id'])
                    except KeyError:
                        pass
                try:
                    i = len(admins) - 1
                    while i >= 0:
                        if event.object['from_id'] == event.object.reply_message.get('from_id'):
                            send('Че себя кикаешь дурень')
                            break
                        else:
                            if event.object['from_id'] == admins[i]:
                                send('Проверяю ты админ или пидорас...')
                                send('Поздравляю! Ты не пидорас')
                                vk.messages.removeChatUser(chat_id=event.chat_id, random_id=get_random_id(),
                                                           member_id=event.object.reply_message.get('from_id'))
                                break
                            else:
                                if i == 0:
                                    send('Проверяю ты админ или пидорас...')
                                i -= 1
                    if i >= 0:
                        pass
                    else:
                        send('ВОТ ПИДОРАС ЕБУЧИЙ')
                except Exception as e:
                    send("Кого мне кикать-то, дурашка, сообщение перешли")
                    print(e)
            elif event.object.text.lower() == "name" or event.object.text.lower() == "название":
                send("Введите название: ")
                for event in longpoll.listen():
                    vk.messages.editChat(chat_id=event.chat_id, random_id=get_random_id(), title=event.object.text)
                    break
            elif event.object.text.lower() == 'аудио' or event.object.text.lower() == 'музыка':
                send('Сколько песен скинуть?(До 10)')
                for event in longpoll.listen():
                    try:
                        a = int(event.object.text)
                        a += 1
                        send_audio(a)
                        break
                    except Exception as e:
                        send('Число ввести слабо?')
                        print(e)
                        break
            elif event.object.text.lower() == 'переведи' or event.object.text.lower() == 'перевод':
                word = ''
                send('Введите текст: ')
                for event in longpoll.listen():
                    for i in event.object.text:
                        try:
                            word += abc.get(i)
                        except Exception:
                            pass
                    send(word)
                    break
            elif event.object.text.lower() == '-переведи' or event.object.text.lower() == '-перевод':
                word = ''
                send('Введите текст: ')
                for event in longpoll.listen():
                    for i in event.object.text:
                        try:
                            word += cba.get(i)
                        except Exception:
                            pass
                    send(word)
                    break
            elif event.object.text.lower() == 'калькулятор' or event.object.text.lower() == 'счет' or event.object.text.lower() == 'считать' or event.object.text.lower() == 'посчитать' or event.object.text.lower() == 'счёт':
                send(
                    "Сложение: + \nВычитание: - \nУмножение: * \nСтепень: ** \nДеление: / \nЦелочисленное деление: // \nОстаток: %")
                send("Введите первое число: ")
                for event in longpoll.listen():
                    a = event.object.text.lower()
                    send("Введите второе число: ")
                    break
                for event in longpoll.listen():
                    b = event.object.text.lower()
                    send("Введите действие: ")
                    break
                for event in longpoll.listen():
                    c = event.object.text.lower()
                    break
                try:
                    int(a)
                    int(b)
                except Exception as e:
                    send("Даун научись калькулятором пользоваться")
                    print(e)
                    continue
                a = float(a)
                b = float(b)
                if c == '+':
                    send(a + b)
                elif c == '-':
                    send(a - b)
                elif c == '*':
                    send(to_fixed(a * b, 3))
                elif c == '**':
                    send(to_fixed(a ** b, 3))
                elif c == '/':
                    send(to_fixed(a / b, 3))
                elif c == '//':
                    send(a // b)
                elif c == '%':
                    send(to_fixed(a % b, 3))
                else:
                    send("Даун научись калькулятором пользоваться")
            elif event.object.text.lower() == 'вики' or event.object.text.lower() == 'википедия' or event.object.text.lower() == 'wiki' or event.object.text.lower() == 'wikipedia':
                send('Введите запрос: ')
                for event in longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        try:
                            send('Вот что я нашёл: \n' + str(wikipedia.summary(event.object.text, sentences=5)))
                            break
                        except Exception as e:
                            send('Ниче не нашел(')
                            print(e)
                            break
                continue
            elif event.object.text.lower() == '5+5' or event.object.text.lower() == '5 + 5' or event.object.text.lower() == '5+5=' or event.object.text.lower() == '5 + 5 =':
                i = 10
                while i != 0:
                    send(str(i))
                    time.sleep(1)
                    i -= 1
                send(emoji.emojize('БУМ :collision:', use_aliases=True))
                continue
            elif event.object.text.lower() == 'да':
                send('Нет')
            elif event.object.text.lower() == 'нет':
                send('Да')
            elif event.object.text.lower() == 'бот':
                send('Не на месте я иди нахуй')
            elif event.object.text.lower() == 'лол':
                send('Кек')
            elif event.object.text.lower() == 'пидор':
                send('Тима')
            elif event.object.text.lower() == 'пидорас':
                send('Пидорасина')
            elif event.object.text.lower() == 'депрессия':
                send('В 0 лет')
            elif event.object.text.lower() == 'тима':
                send('Пидор')
            elif event.object.text.lower() == 'бля' or event.object.text.lower() == 'пиз':
                send('здец')
            elif event.object.text.lower() == 'даун':
                send('Артем')
            elif event.object.text.lower() == 'артем':
                send('Даун')
            elif event.object.text.lower() == 'кек':
                send('Лол')
            elif event.object.text.lower() == 'ytn':
                send('Lf')
            elif event.object.text.lower() == 'хрюшка':
                send('Павтарюшка')
            elif event.object.text.lower() == 'полиночка':
                send(emoji.emojize('Спасибки):two_hearts:'))
            elif event.object.text.lower() == 'lf':
                send('ytn')
            elif event.object.text.lower() == 'питон' or event.object.text.lower() == 'питончик' or event.object.text.lower() == 'питоньчик' or event.object.text.lower() == 'питон)' or event.object.text.lower() == 'питончик)' or event.object.text.lower() == 'питоньчик)' or event.object.text.lower() == 'python' or event.object.text.lower() == 'python)' or event.object.text.lower() == 'python))0)':
                send("ИТС МАЙ ЛАААЙФ")
            elif event.object.text.lower() == 'ъ' or event.object.text.lower() == 'ъ)':
                send('Ъ)')
            elif event.object.text.lower() == 'ага' or event.object.text.lower() == 'ага)':
                send('Ага)')
            elif event.object.text.lower() == 'пиу':
                send('ПАУ')
            elif event.object.text.lower() == 'пинг':
                send('ПОНГ')
            elif event.object.text.lower() == 'хуле да' or event.object.text.lower() == 'хули да':
                send('Если нет')
            elif event.object.text.lower() == 'хуле нет' or event.object.text.lower() == 'хули нет':
                send('Если да')
            elif event.object.text.lower() == 'спасибо бот' or event.object.text.lower() == 'спасиба бот' or event.object.text.lower() == 'бот спасиба' or event.object.text.lower() == 'бот спасибо':
                send('Всегда пожалуйста братан)')
            elif event.object.text.lower() == 'молодец бот' or event.object.text.lower() == 'молодца бот' or event.object.text.lower() == 'бот молодец' or event.object.text.lower() == 'бот молодца':
                send('Дада мы)')
            elif event.object.text.lower() == 'случайное число':
                send(random.randint(0, 100))
            elif event.object.text.lower() == 'чмок' or event.object.text.lower() == 'чмоки':
                send(emoji.emojize('Чмок) :heart:', use_aliases=True))
            elif event.object.text.lower() == 'тру' or event.object.text.lower() == 'tru' or event.object.text.lower() == 'true' or event.object.text.lower() == 'правда':
                send(emoji.emojize('люблю тебя лилечка ты самая лучшая моя любимая обожаю тебя) (с) твоя львица :heart:', use_aliases=True))
            elif event.object.text.lower() == 'клик':
                send('Клак')
            elif event.object.text.lower() == 'кто умный?' or event.object.text.lower() == 'кто умный' or event.object.text.lower() == 'кто умные' or event.object.text.lower() == 'кто умные?':
                send('Мы умные)')
            elif event.object.text.lower() == 'ахуеть':
                send('СПАСИБО ЛЕВА')
            elif event.object.text.lower() == 'сука кто я' or event.object.text.lower() == 'сука кто я?':
                send('Я ГОРЯЧИЙ МЕКСИКАНЕЦ')
            elif event.object.text.lower() == 'лош' or event.object.text.lower() == 'тима пидор' or event.object.text.lower() == 'тима пидорас' or event.object.text.lower() == 'артем даун':
                send('+')
            elif event.object.text.lower() == 'кто я' or event.object.text.lower() == 'кто я?':
                send('Ты пидорас')
            elif event.object.text.lower() == 'вика':
                send('фломастер))0)')
            elif event.object.text.lower() == 'бомбануло' or event.object.text.lower() == 'бомбит' or event.object.text.lower() == 'бомбануло?' or event.object.text.lower() == 'бомбит?' or event.object.text.lower() == 'бомбанул' or event.object.text.lower() == 'бомбанул?':
                send(emoji.emojize('БУМ :collision:', use_aliases=True))
            elif event.object.text.lower() == 'че' or event.object.text.lower() == 'че блять' or event.object.text.lower() == 'что' or event.object.text.lower() == 'что блять' or event.object.text.lower() == 'чо' or event.object.text.lower() == 'чо блять':
                send('Не ебу')
            elif event.object.text.lower() == 'мне похуй':
                send('Я панк')
            elif event.object.text.lower() == 'я панк':
                send('Мне похуй')
            elif event.object.text.lower() == 'мне панк':
                send('Я похуй')
            elif event.object.text.lower() == 'панк я':
                send('Похуй мне')
            elif event.object.text.lower() == 'дурка' or event.object.text.lower() == 'дурку':
                send('Ебать')
            elif event.object.text.lower() == 'ебать':
                send('Дурка')
            elif event.object.text.lower() == 'лсп':
                send(emoji.emojize('One Love :heart:', use_aliases=True))
            elif event.object.text.lower() == 'люблю':
                send(emoji.emojize('Лилечку :heart:', use_aliases=True))
            elif event.object.text.lower() == 'лилечка' or event.object.text.lower() == 'лиля':
                send_text_img(emoji.emojize('Ля какая :heart:', use_aliases=True), "https://sun9-32.userapi.com/c849220/v849220230/153590/bUGjTXEIG60.jpg")
            elif event.object.text.lower() in emoji.UNICODE_EMOJI:
                send(event.object.text.lower() + " (с) Львица")
            elif event.object.text.lower() == 'фото дауна':
                send_img("https://sun9-69.userapi.com/c543107/v543107423/8412a/xl1H1dBZIrE.jpg")
            elif event.object.text.lower() == 'фото пидора':
                send_img("https://sun9-8.userapi.com/c543107/v543107318/7b096/Bie14KxpvQc.jpg")
            elif event.object.text.lower() == 'любимая':
                send_img("https://sun9-3.userapi.com/c847216/v847216594/204d11/Xo9T_nBahVs.jpg")
            elif event.object.text.lower() == 'выглядит' or event.object.text.lower() == 'выглядит ебательно':
                send_img("https://sun9-16.userapi.com/c855524/v855524321/2da6e/omMY_wWGm_A.jpg")
            elif event.object.text.lower() == 'спасибо':
                send_img("https://memepedia.ru/wp-content/uploads/2019/01/eqtw6mdl3ui.jpg")
            elif event.object.text.lower() == 'похуй' or event.object.text.lower() == 'похуй.' or event.object.text.lower() == 'похуй..' or event.object.text.lower() == 'похуй...':
                send_img("https://i.pinimg.com/564x/59/de/c1/59dec12dd54bd30cfb9de5c284baf293.jpg")
            elif event.object.text.lower() == 'иди нахуй' or event.object.text.lower() == 'нахуй иди':
                send_img("https://sun1-27.userapi.com/miewqCfNfQ6TKm1RWNPhGpHt8SvuAa44ig3OWw/qKqlmngEgDU.jpg")
            elif event.object.text.lower() == 'ля какой' or event.object.text.lower() == 'ля какая :heart:':
                send_img("https://sun9-28.userapi.com/c846219/v846219102/192c16/vbxJU7DbHkQ.jpg")
            elif event.object.text.lower() == 'наеб' or event.object.text.lower() == 'наебываешь':
                send_img("https://sun9-28.userapi.com/c846219/v846219102/192c16/vbxJU7DbHkQ.jpg")
            elif event.object.text.lower() == 'грустишь?' or event.object.text.lower() == 'кто грустит':
                send_img("https://sun9-56.userapi.com/c856028/v856028702/1e2bb/SaIyVbRvdq8.jpg")
            elif event.object.text.lower() == 'врешь' or event.object.text.lower() == 'вреш':
                send_img("https://sun9-22.userapi.com/c855416/v855416905/53042/RZZK0dnc2oc.jpg")
            elif event.object.text.lower() == 'пруфы' or event.object.text.lower() == 'пруфы будут' or event.object.text.lower() == 'пруф' or event.object.text.lower() == 'пруфы будут?' or event.object.text.lower() == 'пруф будет' or event.object.text.lower() == 'пруф будет?':
                send_img("https://sun9-13.userapi.com/c849532/v849532940/1bdf83/SePChPc5Td4.jpg")
            elif event.object.text.lower() == 'блять':
                send_img("https://sun9-55.userapi.com/c854216/v854216184/7055d/WfymJF8jrJQ.jpg")
            elif event.object.text.lower() == 'такая сука' or event.object.text.lower() == 'ты такая сука' or event.object.text.lower() == 'я такая сука' or event.object.text.lower() == 'сука' or event.object.text.lower() == 'ты сука':
                send_img("https://sun9-57.userapi.com/c635102/v635102968/4713f/p__2YEsKFoE.jpg")
            elif event.object.text.lower() == 'полиция' or event.object.text.lower() == 'это полиция' or event.object.text.lower() == 'полиция секса' or event.object.text.lower() == 'это полиция секса':
                send_img("https://sun9-69.userapi.com/c856020/v856020879/8f96d/ox_HjApZJjw.jpg")
            elif event.object.text.lower() == 'нет слов' or event.object.text.lower() == 'слов нет':
                send_img("https://sun9-69.userapi.com/c849220/v849220210/1c9cb9/IyrBg2mOkcg.jpg")
            elif event.object.text.lower() == 'ахуела?' or event.object.text.lower() == 'ахуела' or event.object.text.lower() == 'ахуел' or event.object.text.lower() == 'ахуело':
                send_img("https://sun9-61.userapi.com/c850036/v850036013/1d98c6/OakSDsEiJMY.jpg")
            elif event.object.text.lower() == 'нихуя се' or event.object.text.lower() == 'нихуя себе':
                send_img("https://sun9-65.userapi.com/c851416/v851416795/17987c/p7x-3Wd2rMw.jpg")
            elif event.object.text.lower() == 'пиздец нахуй блять' or event.object.text.lower() == 'пиздец нахуй':
                send_img("https://sun9-60.userapi.com/c855624/v855624733/b9437/BN_VZSZ1gms.jpg")
            elif event.object.text.lower() == 'превращаю в пидора' or event.object.text.lower() == 'превращаю в':
                send_img("https://sun9-30.userapi.com/c858320/v858320784/460e2/9M0V2a1LRi4.jpg")
            elif event.object.text.lower() == 'твой диагноз' or event.object.text.lower() == 'твой диагноз долбоеб':
                send_img("https://sun9-11.userapi.com/c854020/v854020300/c39d3/FQAl3y4Dnek.jpg")
            elif event.object.text.lower() == 'заебал' or event.object.text.lower() == 'заебали' or event.object.text.lower() == 'заебала' or event.object.text.lower() == 'заебало':
                send_img("https://sun9-43.userapi.com/c857416/v857416737/48c4e/zfwf02hiMAM.jpg")
            elif event.object.text.lower() == 'мое уважение' or event.object.text.lower() == 'уважение' or event.object.text.lower() == 'мое увожение' or event.object.text.lower() == 'увожение':
                send_img("https://sun9-2.userapi.com/c854228/v854228206/edf51/DZ0VUmB_gCQ.jpg")
            elif event.object.text.lower() == 'пизда' or event.object.text.lower() == 'пезда':
                send_img("https://sun9-34.userapi.com/c851120/v851120039/1cbaaf/hM0X0v7S4tI.jpg")
            elif event.object.text.lower() == 'похуй абсолютно' or event.object.text.lower() == 'абсолютно похуй':
                send_img("https://sun9-11.userapi.com/c7004/v7004072/6e015/dzHMNCP3iTQ.jpg")
            elif event.object.text.lower() == 'вапше пахую' or event.object.text.lower() == 'вабще пахую' or event.object.text.lower() == 'вапше похую' or event.object.text.lower() == 'вабще похую':
                send_img("https://sun9-18.userapi.com/c851528/v851528057/1d6bad/t8BsgBCXHMc.jpg")
            elif event.object.text.lower() == 'балдеж' or event.object.text.lower() == 'балдею' or event.object.text.lower() == 'девочки балдеж' or event.object.text.lower() == 'девочки балдею' or event.object.text.lower() == 'девачки балдеж' or event.object.text.lower() == 'девачки балдею':
                send_img("https://sun9-20.userapi.com/c854532/v854532952/15f4ec/9V10i09Uejs.jpg")
            elif event.object.text.lower() == 'обезьяны' or event.object.text.lower() == 'вместе' or event.object.text.lower() == 'обезьяны вместе' or event.object.text.lower() == 'сила':
                send_img("https://sun9-56.userapi.com/c543103/v543103200/55772/IQ5R9TF5fU4.jpg")
            elif event.object.text.lower() == 'расстрелять':
                send_img("https://sun1-19.userapi.com/30udiRA8BCgPmxkp45z0qaXd4DFaHPccOzi9UQ/WvWY61Y4_Ck.jpg")
            elif event.object.text.lower() == 'ищу смысл' or event.object.text.lower() == 'ищу смысол':
                send_img("https://sun9-20.userapi.com/c635103/v635103424/807da/oYsPbv568JA.jpg")
            elif event.object.text.lower() == 'стонкс' or event.object.text.lower() == 'stonks':
                send_img("https://sun9-55.userapi.com/c635103/v635103762/41e71/mb_W8NnNLUs.jpg")
            elif event.object.text.lower() == 'беды' or event.object.text.lower() == 'беды с башкой' or event.object.text.lower() == 'беды с бошкой' or event.object.text.lower() == 'бе ды с башкой' or event.object.text.lower() == 'бе ды с бошкой':
                send_img("https://sun1-20.userapi.com/c543108/v543108012/7659c/pNnrufRlcfY.jpg")
            elif event.object.text.lower() == 'гениально' or event.object.text.lower() == 'genius':
                send_img("https://sun9-16.userapi.com/c857636/v857636428/14f4cb/nGiji7qK9Gs.jpg")
            elif event.object.text.lower() == 'вопрос' or event.object.text.lower() == 'вопрос интимного характера':
                send_img("https://sun9-63.userapi.com/c543104/v543104511/6d607/ucwVhXqIhSE.jpg")
            elif event.object.text.lower() == 'кайфую' or event.object.text.lower() == 'кайфую)':
                send_img("https://sun1-19.userapi.com/ViqeEFcQYtC9GTMm48pEwpXXHHzYOVF1GOeK2w/Tm5hDq7pWt0.jpg")
            elif event.object.text.lower() == 'кайфуем' or event.object.text.lower() == 'кайфуем)':
                send_img("https://sun1-97.userapi.com/HjliB-vdBgknaUtXfGYwtpoGCVVw2uOwCVjgzw/KbKfHby73Jg.jpg")
            elif event.object.text.lower() == 'бляздец':
                send_img("https://sun9-39.userapi.com/c855128/v855128936/2032cd/3TIIrf3Gjso.jpg")
            elif event.object.text.lower() == 'жиза' or event.object.text.lower() == 'жиз':
                send_img("https://sun1-25.userapi.com/9m27fY1-jBE37uEk-huoZqFzYoTwoTo4r8mYzw/C0aiBiL9Hfw.jpg")
            elif event.object.text.lower() == 'нахуя' or event.object.text.lower() == 'зачем':
                send_img("https://sun1-18.userapi.com/loiya2AKn47ds56MHyT1s29XTmEFnxPFZD_BcQ/YUX9cE7vi9Y.jpg")
            elif event.object.text.lower() == 'пиздец(' or event.object.text.lower() == 'пиздец((9(':
                send_img("https://sun1-83.userapi.com/foRBmDZs0HyL0g8MhrUV312cpBwPrQEZ2V9nVg/3W2ruY50DEc.jpg")
            elif event.object.text.lower() == 'пиздец':
                send_img("https://sun9-61.userapi.com/c543105/v543105549/81208/apScB2ynjqg.jpg")
            elif event.object.text.lower() == 'прошу прощения' or event.object.text.lower() == 'прошу прощение':
                send_img('https://sun1-26.userapi.com/mcj8xpZaM4xeIgmRDgsjMopcUu2aiq9qB9J4FA/ETX60GMe5pg.jpg')
            elif event.object.text.lower() == 'о вы из англии' or event.object.text.lower() == 'о да вы из англии' or event.object.text.lower() == 'вы из англии' or event.object.text.lower() == 'да вы из англии' or event.object.text.lower() == 'вы из англии':
                send_img("https://sun9-35.userapi.com/c7003/v7003464/7b2d9/NTDRvgXMvIw.jpg")


if __name__ == '__main__':
    main()
