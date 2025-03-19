# Як взаємодіяти

Встановити python, fastapi, uvicorn, sqlalchemy, MongoDB Community та pymongo
1) у консолі перейти у директорію ...\MongoDB\bin\
2) ввести .\mongod.exe --dbpath диск:\шлях\data для запуску mongo сервера

Щоб запустити сервер виконати uvicorn Main.Main:app --reload у директорії Program. Запускати треба саме з директорії Program інакше програма незнатиме де брати імпорти інших файлів.
1) Main. — шлях до файлу 
2) main — назва файлу
3) app — змінна, де створено FastAPI()
4) --reload — увімкнення автоматичного перезапуску при зміні коду

Документація API
1) Swagger UI: http://127.0.0.1:8000/docs
2) Redoc: http://127.0.0.1:8000/redoc

У програмі щоб працючати як адмін пишіть пароль 123