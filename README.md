# Тестове завдання для компанії BackEnd iSi Technology

[Демо користувачі ](#demo_users)

[Авторизація по API](#api_authentitication)

[Можливості та точки входу](#api_backend)

---
### Запуск через Docker
- Скачуємо цей репозиторій
- Відкриваэмо у консолі кореневу папку проекту. У папці розташован файл **docker-compose.yml**
- Запускаємо програму. Програма сама створить образ та запустить його та
завантажить у себе демо данні. Буде доступна на 80 порту, тобто вам не треба вказувати порт у браузері
лише адресу  http://localhost

```
docker-compose up --build
``` 


### Запуск нативним методом без докера
- Скачати цей репозиторій
- Відкриваємо у консолі кореневу папку проекту. У папці розташован файл **requirements.txt**
- Створити віртуальне середовище для цього виконуємо команду `python -m venv venv`
- Інсталювати залежності для цього виконуємо команду `pip install -r requirements.txt`
- У консолі перети до папки **Backend_iSi**
- Створити міграції `python manage.py makemigrations`
- Застосувати міграції `python manage.py migrate`
- Завантажити демо данні користувачів `python manage.py loaddata chat`
- Запустити проект на вбудованому вебсервері `python manage.py runserver` 
сервіс буде доступний по стандартній адресі Django http://127.0.0.1:8000

Загалом
```text
python -m venv venv
pip install -r requirements.txt
cd Backend_iSi
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata chat
python manage.py runserver
``` 


---

<a name="api_backend"> </a>

### Функціональні можливості бекенд сервера:
Сервер має такі точки входу:
- http://localhost/thread  &nbsp;  примає методи `POST, DELETE` 
    - Для створення каналу виконуємо метод  `POST` *(якщо Thread з такими ім'ям та вашим користувачем існує то повертає цей Thread, 
якщо тред з таким імя'м має двох користувачів, тобто повний, то повертає помилку)*
    - Для видалення Thread'а виконуємо метод `DELETE`
    
    Для створення або виалення передаємо назву каналу
    ```
    {
      "name": "Your chanel name"
    }
    ```
  
  
  
  
- http://localhost/all-Threds  &nbsp;  примає метод `GET`
  
    по замовченню видає список усіх Thread'ів. Можна відфільтрувати список для будь-якого user'a
    для цього у URL додаємо параметр `?participants=1`, де 1 це ID клієнту. Фільтрувати підтримує фільтрацію по списку юзерів
    для цього додаємо декілька параметрів `?participants=2&participants=3` 
    *(у кожному Thread'e є останнє повідомлення, якщо таке є)*;  ~~Буде непогано виводити лише непрочитані~~
    
    `http://localhost/all-Threds/?participants=2&participants=3`
  
    
     
     
- http://localhost/messages  &nbsp;  підтримує методи `GET, POST`

    по замовченню виводить усі повідомлення,
    для фільтрації приймає паремтри в URL `?thread=1`, де 1 це ID потоку
    створення повідомлень теж тут можливо
    ```json
    {
        "text": "Текст повідомлення",
        "is_read": false,
        "thread": null
    }
    ```
  
- http://localhost/mark-read &nbsp; підтримує методи `GET, PUT`

    - GET видає перелік непрочитоних повідомлень та кількість цих повідомлень.
    - PUT змінює стан повідомлення у статус прочитано *(is_read=True)*
    може прийтмати як номер повідомлення так і список номерів поведомлень.
    
        ```json
        {
          "id": 1
        }
         ```
        або
        ``` 
        {
          "id": [1,2,3]
        }
        ```
    

<a name="api_authentitication"> </a>

### Для отримання токіну чи оновлення часу дії токену діють такі ендпоінти:
- http://localhost/api/token/ 
*Отримання токіную обовязккові значення*
    ```
    {
        "username": "root",
        "password": "root"
    }
    ```
- http://localhost/api/token/refresh/


<a name="demo_users"> </a>

## Данні по демо користоувачам:


    ```
    SuperAdmin 
    User: root 
    Password: root
    
    ------------------------
    User: Dasha 
    Password: [^p_$"Qi]TJT
    -
    User: Masha 
    Password: qBy"*:u-XT0I
    -
    User: Petya 
    Password: x&9L!6<H27OV
    -
    User: Vasya 
    Password: <PFFzF]dE*$U
    ```

## Додатково

    Для наглядності система має веб-інтерфейс і має переходи на скріни у браузері 
    http://localhost/ 
    
    у переліку не виведено тільки останій скрін http://localhost/mark-read  
