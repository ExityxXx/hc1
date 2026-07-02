from .context import Context

class Element:
    def __init__(self, tag_name: str, **params: dict) -> None:
        self.tag_name: str = tag_name
        self.params: dict = params
        self.children = []

        # Context.parent() возвращает родителя этого Element в контексте
        # Первый родитель всегда Html
        # Если мы вообще не используем with конструкцию то
        # ничего не будет (сохранится старый стиль кода)

        self.this_parent = Context.parent()
        self.tag = self._create()

        print(f"Тег: {self}\n\tЕго родитель: {self.this_parent}")
        if self.this_parent and isinstance(self.this_parent, Element):
            self.this_parent.tag.append(self.tag)

    def __enter__(self):
        Context.push(self)
        return self
    
    def __exit__(self, *args):
        Context.pop()

    def _create(self):
        from .htmlconstructor import Html
        htmlsheet = Html._current_site.sheet()
        tag = htmlsheet.new_tag(self.tag_name)
        self._format_params(tag, self.params)
        htmlsheet.body.append(tag)
        return tag

    def _format_params(self, tag, params):
        for param, value in self.params.items():
            if param.endswith('_'):
                param = param[:len(param)-1]
            tag.attrs[param] = value
    
class Heading(Element):
    def __init__(self, text, level=1, **params):
        super().__init__(f"h{level}", **params)
        self.text = text
        self.level = level
        if self.text is not None:
            self.tag.string = self.text

class Button(Element):
    def __init__(self, text, **params):
        super().__init__(f"button", **params)
        self.text = text
        if self.text is not None:
            self.tag.string = self.text

class Input(Element):
    def __init__(self, **params):
        super().__init__(f"input", **params)
        allowed_types = {
            "text": "Для обычного текста",
            "email": "Для электронной почты",
            "password": "Для пароля",
            "checkbox": "Для кнопки-переключателя"
        }

        if "type" in params and params["type"] not in list(allowed_types.keys()):
                print(" Предупреждение!")
                print(f"Полный тег: {self.tag}")
                print(f"В теге <input> нету параметра type с именем {params['type']}")
                print(f"Допустимые имена:")
                
                for name, desc in allowed_types.items():
                    print(f"\t{name} - {desc}")

                print("Это не вызовет ошибку просто имейте ввиду что добавление")
                print("параметра с именем, который игнорируется тегом")
                print("в страницу не меняет абсолютно ничего (лишний мусор)")

class Div(Element):
    def __init__(self, **params):
        super().__init__(f"div", **params)

    def append(self, element: Element) -> None:
        if isinstance(element, Element):
            self.tag.append(element.tag)
        else:
            self.tag.append(element)

class Label(Element):
    def __init__(self, text, **params):
        super().__init__(f"label", **params)
        self.text = text
        if self.text is not None:
            self.tag.string = self.text

class Paragraph(Element):
    def __init__(self, text, **params):
        super().__init__(f"p", **params)
        self.text = text
        if self.text is not None:
            self.tag.string = self.text

class Link(Element):
    def __init__(self, **params):
        super().__init__(f"link", **params)

class Script(Element):
    def __init__(self, **params):
        super().__init__(f"script", **params)

class Br(Element):
    def __init__(self, **params):
        super().__init__(f"br", **params)
