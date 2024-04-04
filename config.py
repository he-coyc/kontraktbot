#КОНФИГ ДЛЯ БОТА

class Settings:
        #ТОКЕН ОТ АККАУНТА ВК
        TOKEN = ''

        #ЗАДЕРЖКА ПОСЛЕ ОТПРАВКИ КОММЕНТА (В СЕКУНДАХ)
        DELAY = 10

        #РАЗБРОС ДЛЯ РАНДОМИЗАЦИИ ЗАДЕРЖКИ (В СЕКУНДАХ)
        DELAY_AREA = 5

        #СПИСОК СООБЩЕНИЙ ДЛЯ СПАМА
        MESSAGE = ['Детка 😏 покажи мне калифорнию 🔞', 'Клик клак клик bang 😎', 'Seventeen 🍑 got that dope 💦 Eazy blessin 😎 with your swag 💋', 'Все пототму 😫 что дора дypa 😰', 'А голова, чтобы думать 🤓 ноги, чтобы и ходить 🥵']

        #ЛОКАЛЬНЫЙ ПАТЧ НА КАРТИНКУ ПОД КОММЕНТОМ (НЕ ОТПРАВЛЯЕТСЯ ЕСЛИ ПУСТО)
        MESSAGE_IMG = ''

        #САМОЛАЙК (True/False)
        selflike = True

        #АЙДИ СТЕН ДЛЯ ПРОСПАМА (ЕСЛИ НУЖЕН ПРОСМПАМ ПРОФИЛЯ, ПИСАТЬ БЕЗ '-', ЕСЛИ НУЖЕН ПРОСПАМ ГРУПП ПИСАТЬ С '-' В НАЧАЛЕ АЙДИ)
        #УЗНАТЬ ID ГРУППЫ ЛИБО ПРОФИЛЯ МОЖНО НА https://regvk.com/id/
        GROUPS = ['-66678575', '-28905875']

        #ВРЕМЯ ПУБЛИКАЦИИ ПОСТА, ПОСЛЕ КОТОРОГО КОММЕНТ НЕ СТАВИТСЯ (В МИНУТАХ)
        TIMEOUT = 30

        #КОЛИЧЕСТВО ПОСТОВ У ПАБЛИКА ДЛЯ ПРОВЕРКИ
        POSTOUT = 5

class Prefab:
        #ИСПОЛЬЗОВАТЬ ПРЕФАБ?
        using = False

        #ЛОКАЛЬНЫЙ ПАТЧ НА НОВУЮ АВАТАРКУ (НЕ МЕНЯЕТСЯ ЕСЛИ ПУСТО)
        PFP = 'D:\spambot\profilepicture.png'

        #НОВЫЙ СТАТУС (НЕ МЕНЯЕТСЯ ЕСЛИ ПУСТО)
        STATUS = 'Привет! Я использую KOHTRAKT bot.!'

        #НАСТРОЙКА ЗАКРЕПА (НЕ КРЕПИТСЯ ЕСЛИ НЕТ ТЕКСТА)
        PIN_TEXT = ''
        PIN_URL = ''
        
        #АЙДИ ГРУПП ДЛЯ ПОДПИСКИ (ПИСАТЬ БЕЗ '-')
        FOLLOW_GROUPS = []

class Proxy:
        #ИСПОЛЬЗОВАНИЕ ПРОКСИ (True/False)
        using = False

        #АДРЕСС ПРОКСИ
        #В ФОРМАТЕ <PROXY_PROTOCOL>://<USERNAME>:<PASSWORD>@<PROXY_IP_ADDRESS>:<PROXY_PORT>
        ADDRESS = 'socks5://login:password@190.160.220.190:47700'
