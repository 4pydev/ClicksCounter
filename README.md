# ClicksCounter
Скрипт позволяет создать "короткую" ссылку на сервисе 
`bit.ly` или получить общее количество кликов по уже 
созданной "короткой" ссылке, размещенной в сети Интернет.  
## Использование
Для использования необходим установленный интерпретатор 
`Python 3`.  
Также необходимо установить некоторые модули:  
```bash
$ pip install -r requirements.txt
```
После этого нужно создать в папке `./clicks_counter/` файл 
`.env` и поместить в него Ваш `generic access token (GAT)` 
от сервиса `bit.ly`:  
```bash
$ echo ACCESS_TOKEN=here_enter_your_GAT > ./clicks_counter/.env 
```
После запуска:  
```bash
$ python3 ./clicks_counter/clicks_counter.py
```
Вам будет предложено ввести ссылку. Если введена 
"короткая" ссылка типа `http://bit.ly/JHGcjx2j`, то 
скрипт вернет общее количество кликов по данной ссылке.  
Если введена обычная (полная) то будет выведена "короткая" 
ссылка.
## Цели проекта
Код создан в учебных целях. 
В рамках учебного курса по веб-разработке - 
[DEVMAN.org](https://dvmn.org)
