# Optimus Prime
**Телеграм бот который следит за проверкой домашних работ на DVMN**

Эта простой телеграм-бот который даёт возможность получать уведомления о том, 
что домашняя работа на dvmn.org проверена.


### Как установить

Для работы бота необходито установить 3 переменные окружения: 

`TELEGRAM_BOT_TOKEN` - это токен телеграм-бота (можно получить с помощью BotFather)

`CHAT_ID` - id телеграм-чата в который нужно отправлять сообщения

`DVMN_TOKEN` - ваш токен для доступа к API девмана.

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить:

```console
$ python3 main.py
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).