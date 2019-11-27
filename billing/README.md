# Биллинг

Автор: Мустафина Екатерина


## Описание
Данная программа парсит лог-файл АТС и выставляет счёт для каждого абонента с детализацией.


## Состав
* Консольная версия: `billing.py`
* Тестовые файлы: `test_billing.py`

## Консольная версия
Справка по запуску: 
`billing.py --help`, billing.py help`

Пример запуска: 
`python billing.py [file.txt]`
file.txt - текстовый файл txt с логами АТС

 
## Подробности реализации
В основе модуля `billing.py` лежит класс Parser, который распаковывает данные из
лог-файла АТС, парсит данные и выводит детализированную информацию о звонках для 
каждого абонента. 