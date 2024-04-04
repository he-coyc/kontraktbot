import os
import time
import vk_api 
import random
import config
import requests
import json
import fake_useragent
from sys import platform
from time import gmtime, strftime
from vk_api import VkApi, VkUpload
from fake_useragent import UserAgent

#ПЕРЕНОСИМ НЕКОТОРЫЕ ДАННЫЕ ИЗ КОНФИГА + ИНИЦИАЛИЗАЦИЯ ГЛОБАЛЬНЫХ ПЕРЕМЕННЫХ
delay = abs(config.Settings.DELAY)
delay_area = abs(config.Settings.DELAY_AREA)
if delay_area > delay:
    delay_area = 0
timeout = config.Settings.TIMEOUT * 60
uid = 0
alltimePosts = []
key_startup = True #КЛЮЧ ЗАЖИГАНИЯ
albumID = ''
photoComID = ''
username = ''
comments_counter = 0


def clear(): #ОЧИЩАЕМ КОНСОЛЬКУ
    if platform == "linux" or platform == "linux2":
            os.system('clear')
    elif platform == "win32":
            os.system('cls')

def vk_auth(proxy_session): #ИНИЦИАЛИЗИРУЕМ СЕССИЮ
    if config.Proxy.using:
        vk_session = vk_api.VkApi(token = config.Settings.TOKEN, session=proxy_session)
    else:
        vk_session = vk_api.VkApi(token = config.Settings.TOKEN)

    vk = vk_session.get_api()
    return vk

def wait(): #ЗАДЕЖРКА ПЕРЕД СЛЕДУЮЩЕЙ ОТПРАВКОЙ КОНТЕНТА
    time.sleep(delay + random.randint(delay_area * -1,delay_area))

def init_album(api):
    global albumID
    try:
        albumID = api.photos.getAlbums(count=1)['items'][0]['id']
        api.photos.editAlbum(album_id=albumID, title=username, privacy_view='all')
        print('Альбом был подготовлен успешно ✅')
    except:
        try:
            albumID = api.photos.createAlbum(title=username)['id']
            print('Альбом был создан успешно ✅')
        except:
            print('К альбомам нет доступа пиздец ❗️')

def uploadPhotoFromPath(api, path):
    try:
        http = requests.Session()
        values = {}
        response = api.photos.getUploadServer(album_id=albumID)
        url = response['upload_url']
        response = http.post(
                            url,
                            files={'file': open(path, 'rb')}
                            )
        try:
            photo = api.photos.save(**response.json(), album_id=albumID)[0]['id']
            print('Фото успешно сохранено ✅')
            return photo
        except:
            print('Ошибка при сохранении фото ❗️')
            return 0
    except:
        print('Ошибка при загрузке фото ❗️')
        return 0

def doPrefab(api): #ИСПОЛЬЗОВАНИЕ ПЕРФАБА ДЛЯ НАСТРОЙКИ СТРАНИЧКИ
    print('Идет применение префаба...')
    #СТАВИМ НОВУЮ PFP
    if config.Prefab.PFP != '':
        http = requests.Session()
        values = {}
        response = api.photos.getOwnerPhotoUploadServer(**values)
        url = response['upload_url']
        response = http.post(
                            url,
                            files={'file': open(config.Prefab.PFP, 'rb')}
                            )
        api.photos.saveOwnerPhoto(**response.json())
        print('Аватарка установлена ✅')
    #СТАВИМ НОВЫЙ СТАТУС
    if config.Prefab.STATUS != '':
        api.status.set(text=config.Prefab.STATUS)
        print('Статус установлен ✅')
    #СТАВИМ НОВЫЙ ЗАКРЕП
    if config.Prefab.PIN_TEXT != '':
        attachments=''
        if config.Prefab.PIN_URL != '':
            attachments = config.Prefab.PIN_URL
        post = post_myWall(api,config.Prefab.PIN_TEXT, attachments)
        api.wall.pin(post_id=post['post_id']) 
        print('Закреп установлен ✅')
    #ПОДПИСЫВАЕМСЯ НА НАШИ ЛЮБИМЫЕ РИФМЫ И ПАНЧИ
    if len(config.Prefab.FOLLOW_GROUPS) > 0:
        for i in range (0, len(config.Prefab.FOLLOW_GROUPS),+1):
            try:
                api.groups.join(group_id=config.Prefab.FOLLOW_GROUPS[i])
                time.sleep(1)
            except:
                quecoo = 0
        print('Подписки оформлены ✅')
    config.Prefab.using = False
    print('Префаб применён ✅\n')

def post_myWall(api, text, attach):
    try:
        if text != '':
            if attach != '':
                post = api.wall.post(message=text, attachments=attach)
            else:
                post = api.wall.post(message=text)
            postID = post['post_id']
            sourceID = api.wall.get(count=1)['items'][0]['from_id']
            print(f'''Сделан пост ✅\n  ╠ Адрес: https://vk.com/wall{sourceID}_{postID}\n  ╚ Текст: {text}\n''')
            return post
    except:
        print('Непредвиденная ошибка при публикации поста ❗️')

def randMsg(): #СЛУЧАЙНОЕ СООБЩЕНИЕ ИЗ СПИСКА
    return random.choice(config.Settings.MESSAGE)

def get_ban(api): #ПРОВЕРКА НА СОБАЧКУ
    try:
        test = api.groups.get()
        return True
    except:
        return False

def print_account_info(api):
    global uid, username
    first_name = api.account.getProfileInfo()['first_name']
    last_name = api.account.getProfileInfo()['last_name']
    gender = api.account.getProfileInfo()['sex']
    if gender == 1:
        gender = 'Женский'
    if gender == 2:
        gender = 'Мужской'
    if gender == 0:
        gender = 'Не указан'
    try:
        phone = api.account.getProfileInfo()['phone']
    except:
        phone = 'Отсутствует'
    uid = api.account.getProfileInfo()['id']
    username = first_name + ' ' + last_name
    print(f'''
Информация об аккаунте 📝
╔ Имя: {username}
╠ Пол: {gender}
╠ Телефон: {phone}
╠ Валид: {get_ban(api)}
╚ Ссылка: https://vk.com/id{uid}
''')
    
    
def get_userGroups(api): #ПОДГОТОВКА СПИСКА ГРУПП К ПАРСИНГУ
    try:
        grps = api.groups.get()['items'] #ВОЗВРАЩАТЬ grps ЕСЛИ ХОЧЕШЬ СПАМ ПО ПОДПИСКАМ
        return config.Settings.GROUPS
    except:
        getBannedChokomode()
        return []

def parse_groups(api, groups, timestamp): #ПАРСИНГ СПИСКА ГРУПП И ОТПРАВКА КОММЕНТОВ
    for i in range (0, len(groups)-1,+1):
        ownerID = groups[i]
        try:
            posts = api.wall.get(owner_id=ownerID, count=config.Settings.POSTOUT)['items']
            if len(posts) > 0:
                for j in range (0, config.Settings.POSTOUT-1, +1):
                    try:
                        if posts[j]['comments']['can_post'] == 1 and posts[j]['date'] > timestamp - timeout: #ЕСЛИ МОЖНО КОММЕНТИТЬ И ПОСТ БЫЛ СДЕЛАН НЕ БОЛЕЕ X МИНУТ НАЗАД
                            postID = posts[j]['id']
                            if {ownerID, '-', postID} in alltimePosts:
                                None
                            else:
                                attachments=''
                                if config.Settings.MESSAGE_IMG != '':
                                    attachments = f'photo{uid}_{photoComID}'
                                alltimePosts.append({ownerID, '-', postID})
                                try:
                                    do_comment(api, ownerID, postID, randMsg(), attachments)
                                except:
                                    None
                                wait()
                    except:
                        #print('Непредвиденная ошибка при подготовке комментария ❗️')
                        #print( posts[j]['comments']['can_post'])
                        quecoo = 0
        except:
            quecoo = 0


def do_comment(api, wall, post, text, attach): #ОТПРАВИТЬ КОММЕНТ
    global comments_counter
    try:
        if attach != '':
            comment = api.wall.createComment(owner_id=wall, post_id=post, message=text, attachments=attach)
        else:
            comment = api.wall.createComment(owner_id=wall, post_id=post, message=text)
        if config.Settings.selflike:
            api.likes.add(type='comment', owner_id=wall, item_id={comment['comment_id']})
        print(f'''
    Коммент оставлен ✅
    ╔ Текст: "{text}"
    ╠ Ссылка: https://vk.com/wall{wall}_{post}?reply={comment['comment_id']}
    ╚ Время: {strftime('%H:%M:%S')}
    ''')
        comments_counter+=1
    except vk_api.exceptions.Captcha as captcha:
        print(f'''
    Появилась капча ❗️
    ╔ Ссылка: {captcha.get_url()}
    ╚ Время: {strftime('%H:%M:%S')}
''')
        captcha_key = input('✏️ Введите капчу:')
        captcha.try_again(captcha_key)
    except vk_api.exceptions.AccountBlocked:
        getBannedChokomode()
    except vk_api.exceptions.VkApiError as e:
        print(e)
    
def getBannedChokomode():
    global comments_counter
    print('🔒 Ваш аккаунт был заблокирован.\n╚ Отправлено комментариев:', comments_counter)
    key_startup = False
    exit()

def start(): #ЗАПУСК ЭТОЙ ХУЙНИ ЕБАНОЙ НАЧИНАЕТСЯ ОТСЮДА
    global photoComID
    clear()
    print(f'''
    .-------------------------------.
     | / |‾| | | ‾T‾ |‾| /‾\ | / ‾T‾
     |<  | | |-|  |  |_| |_| |<   |
     | | |_| | |  |  |   | | | |  |
    .-------------------------------.
     K O H T P A K T bot. by he_coyc

Текущие настройки ⚙️
╔ Префаб используется: {config.Prefab.using}
╠ Прокси используется: {config.Proxy.using}
╚ Задержка перед отправкой контента: от {delay-delay_area} до {delay+delay_area} сек.''')
    if config.Proxy.using == True: #ПОДРУБ ПРОКСИ ПО ТРЕБОВАНИЮ
        session = requests.Session()
        session.proxies = {'http': config.Proxy.ADDRESS, 'https': config.Proxy.ADDRESS}
        agent = fake_useragent.UserAgent()
        agent = agent.random
        session.headers = {'User-Agent': agent}
        api = vk_auth(session)
        print(f'''╔ Агент: {agent}
╚ Текущая прокси локация: proxyhere
''')
    else:
        api = vk_auth('')
    try:
        print_account_info(api)
    except:
        print('Произошла ошибка со стороны VK API либо токен введён неорректно ❗️')
        exit()

    if get_ban(api) == False: #ЕСЛИ АКК НЕЛИКВИД - ПРОГА ПРЕКРАЩАЕТ ВЫПОЛНЕНИЕ
        getBannedChokomode()

#    try:
#        print('Заявка на смену имени подана:', api.account.saveProfileInfo(first_name='Настюша', last_name='Астафьева', sex=2))
#    except:
#        print('Ошибка смены имени')
#    exit()

    if config.Settings.MESSAGE_IMG != '' or config.Prefab.PFP  !='':
        init_album(api)
    if config.Prefab.using == True: #ИСПОЛЬЗОВАНИЕ ПЕРФАБА ПО ТРЕБОВАНИЮ
        doPrefab(api)
        time.sleep(60)
    if config.Settings.MESSAGE_IMG != '':
        photoComID = uploadPhotoFromPath(api, config.Settings.MESSAGE_IMG)

    while(key_startup):
        timestamp = api.utils.getServerTime()
        parse_groups(api, get_userGroups(api), timestamp)
        wait()

start() #ЫААА ПОЕХАЛИЙ!!!!1!1!11!