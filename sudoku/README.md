# Головоломка «Судоку»

Автор: Мустафина Екатерина


## Описание
Данное приложение является реализацией головоломки «Судоку».


## Требования
* Модуль tkinter


## Состав
* Консольная версия: `sudoku_file.py`, sudoku_samurai_file.py`
* Графическая версия: `sudoku_graphic.py`, 
`sudoku_samurai_graphic.py`, `general_sudoku.py`
* Тестовые файлы: `Tests/`
* Текстовые файлы: `SudokuSamuraiTEMP.txt`, `save1.txt`


## Консольная версия
Справка по запуску: 
`python sudoku_file.py --help`, `python sudoku_file.py help`,
`python sudoku_samurai_file.py --help`, `python sudoku_samurai_file.py help`

Пример запуска: 
`python sudoku_file.py [file/line]`, `python sudoku_samurai_file.py [file/line]`

file - текстовый файл txt в котором находится обычный судоку, 
записанный в одну строку, состоящую из 81 символа или 
судоку-самурай, записанный в одну строку, состоящую из 441 символа
line - обычный судоку, записанный в одну строку, состоящую из 81 символа
или судоку-самурай, записанный в одну строку, состоящую из 441 символа


## Графическая версия
Справка по запуску: 
`python sudoku_graphic.py --help`, `python sudoku_graphic.py help`,
`python sudoku_samurai_graphic.py --help`, `python sudoku_samurai_graphic.py help`,
`python general_sudoku.py --help`, `python general_sudoku.py help`

Пример запуска: 
`python sudoku_graphic.py`
`python sudoku_samurai_graphic.py`
`python general_sudoku.py`


## Подробности реализации
В основе реализации решения обычного судоку 9*9 лежит класс Sudoku, 
расположенный в файле `sudoku_file.py`. Этот модуль импортируется в файл
`sudoku_graphic.py` для графической версии головоломки.
В файле `sudoku_graphic.py` лежит класс Sudoku_window, реализующий графическое 
представление головоломки.
В основе реализации решения судоку-самурай лежит класс Sudoku_Samurai, 
расположенный в файле `sudoku_samurai_file.py`. Этот модуль импортируется в файлы 
`sudoku_samurai_graphic.py` для графической версии головоломки.
В файле `sudoku_samurai_graphic.py` лежит класс  Sudoku_samurai_window, 
реализующий графическое представление головоломки.

На модуль Sudoku из файла `sudoku_file.py` и на модуль Sudoku_Samurai из файла
`sudoku_samurai_file.py`. написаны тесты.
Покрытие по строкам составляет :

    sudoku_file.py  81%  
	sudoku_samurai_file.py 85%