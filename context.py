class Context:
    _parents = []

    @classmethod
    def parent(cls): 
        if cls._parents:
            return cls._parents[-1]
        print("Не найден родитель")
        print(f"Класс для которого нужно найти родителя: {cls}")
        return None

    @classmethod
    def push(cls, value):
        if value is not None:
            cls._parents.append(value)
            print(f"Pushed: {value}")
            return True
        raise ValueError("Значение value при добавлений контекстного стека равна None")

    @classmethod
    def pop(cls):
        if cls._parents:
            return cls._parents.pop()
        raise ValueError("При удалений из стека контекста произошла ошибка: СТЕК ПУСТ!")
 