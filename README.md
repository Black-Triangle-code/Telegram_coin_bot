# Telegram_coin_bot
Бот для добывания криптовалюты, выполняя задания ботов [dogeclick](https://dogeclick.com/)

Для работы трабуется установить [Docker](https://www.docker.com/), [Selenoid](https://github.com/aerokube/selenoid) и зависимости проекта

## План действий

0. Создать аккаунт телеграм и начать диалог с ботом из конгломерата [dogeclick](https://dogeclick.com/) и не забывайте о правилах правильной регистрации, о которых говорилось в видео
1. Вносим в скрипт create_db.py данные Telegram аккаунта и запускаем его. Тем самым мы создаем базу аккаунтов и добавляем в нее запись с ботом. Повторяем этот пункт столько раз, сколько аккаунтов у нас есть.
2. Запускаем скрипт create_client.py тем самым генерируем файл-клиент для всех наших Telegram ботов
3. Для старта главной программы запускаем скрипт main.py. Они будут работать до тех пор, пока мы их не остановим. Если в процессе возникнет ошибка - цикл перезапустится и все равно продолжит работу, начиная с первого бота
4. Если мы хотим узнать сколько заработал каждый бот: останавливаем пункт 3 и запускаем скрипт balance.py и ждем завершения, скрипт выведет сколько заработал каждый бот и итоговую сумму

UDP: 5. Добавил скрипт для автаматического вывода Vivod.py проверяет баланс, если он больше минимального значения для вывода, переводит средства на тот кошелек, который вы привязали к аккаунту в процессе создания базы

## Видео демонстрация:
https://www.youtube.com/watch?v=ig3JxDsvYGw

## Что еще важно помнить.
При массовой регистрации аккаунтов рекомендуется менять IP адрес не реже чем на 10 аккаунтов и ставить пароль 2х этапной аутентификации, получать API, взаимодействовать с ботами не сразу, а через 3-5 дней отлёжки
