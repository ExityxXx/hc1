from bs4 import BeautifulSoup, Tag
from tags import (
    Element,
    Heading,
    Button,
    Input,
    Div,
    Label,
    Link,
    Script,
    Br
)
from context import Context

class Html:
    _сurrent_site = None

    def __init__(self, site_title=""):
        self.site_title = site_title
        self.htmlsheet = BeautifulSoup(
            f'<!DOCTYPE html><html lang="ru"><html><head><meta charset="UTF-8"><title>{site_title}</title></head><body></body></html>',
            "html.parser"
        )
        Html._current_site = self

    def __enter__(self):
        Context.push(self)
        return self
    
    def __exit__(self, *args):
        Context.pop()
        Html._current_site = None

    def set_title(self, new_title: str) -> None:
        if new_title:
            self.form_title = new_title
    
    def sheet(self) -> BeautifulSoup:
        return self.htmlsheet

    def save_html(self, file) -> None:
        with open(file, mode='w', encoding='utf-8') as f:
            f.write(self.sheet().prettify())
        print(f"Файл \"{file}\" сохранен.")
        return f
    
    def set_stylesheet(self, source_file: str) -> None:
        """
        ? Устанавливает стиль .css для сайта,
        * Аргументы:
            source_file: str
            - файл для подключения стиля
            - ожидает .css в конце
            - он должен быть в директорий
        
        ! Примечание 
        Классы-теги (Link входит в них)
        создаются автоматически внутри конкретного контекста. 

        ! Что это значит?
        Допустим если вы создадите ссылку
        внутри контекстного менеджера Div()
        то ссылка тоже создастся внутри этого контейнера  
        
        * Код:
            with Div():
                # Стиль создастся внутри этого <div>
                site.set_stylesheet("src.js")
        """
        Link(rel="stylesheet", href=source_file)

    def set_javascript(self, source_file: str) -> None:
        """
        ? Устанавливает скрипт .js для сайта,
        * Аргументы:
            source_file: str
            - файл для подключения скрипта
            - ожидает .js в конце
            - он должен быть в директорий
        
        ! Примечание 
        Классы-теги (Script входит в них)
        создаются автоматически внутри конкретного контекста.

        ! Что это значит?
        Если вы создадите скрипт
        внутри контекстного менеджера Div()
        то скрипт тоже создастся внутри этого контейнера:

        * Код:
            with Div():
                # Скрипт создастся внутри этого <div>
                site.set_javascript("src.js")
        """
        Script(src=source_file)
