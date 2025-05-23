questions = [
    {
        "question": "Какой ваш любимый цвет?",
        "options": [
            {"text": "Красный", "animal": 2},   # Тигр
            {"text": "Синий", "animal": 4},     # Сова
            {"text": "Зелёный", "animal": 0},   # Бобр
            {"text": "Жёлтый", "animal": 3},    # Лемур
        ]
    },
    {
        "question": "Какое ваше любимое время года?",
        "options": [
            {"text": "Зима", "animal": 5},      # Гадюка
            {"text": "Весна", "animal": 3},     # Лемур
            {"text": "Лето", "animal": 1},      # Слон
            {"text": "Осень", "animal": 4},     # Сова
        ]
    },
    {
        "question": "Вы в компании — вы скорее...",
        "options": [
            {"text": "Заводила", "animal": 3},  # Лемур
            {"text": "Наблюдатель", "animal": 4},  # Сова
            {"text": "Организатор", "animal": 1},  # Слон
            {"text": "Шутник", "animal": 0},    # Бобр
        ]
    },
    {
        "question": "Где бы вы хотели жить?",
        "options": [
            {"text": "В горах", "animal": 5},   # Гадюка
            {"text": "На пляже", "animal": 3},  # Лемур
            {"text": "В лесу", "animal": 2},    # Тигр
            {"text": "В городе", "animal": 0},  # Бобр
        ]
    },
    {
        "question": "Как вы обычно решаете проблемы?",
        "options": [
            {"text": "Думаю логически", "animal": 4},   # Сова
            {"text": "Смотрю на эмоции", "animal": 1},  # Слон
            {"text": "Действую быстро", "animal": 2},   # Тигр
            {"text": "Обхожу их с юмором", "animal": 0}, # Бобр
        ]
    },
    {
        "question": "Какая черта вам ближе всего?",
        "options": [
            {"text": "Независимость", "animal": 5},  # Гадюка
            {"text": "Доброта", "animal": 1},        # Слон
            {"text": "Любознательность", "animal": 4},  # Сова
            {"text": "Игривость", "animal": 3},      # Лемур
        ]
    },
]

results = {
    0: ("Бобр", "images/beaver.png", "Бобры — отличные строители!"),
    1: ("Африканский слон", "images/elephant.png", "Слоны известны своей мудростью."),
    2: ("Амурский тигр", "images/tiger.png", "Тигры — символ силы и грации."),
    3: ("Лемур", "images/lemur.png", "Лемуры — очень общительные и игривые."),
    4: ("Болотная сова", "images/owl.png", "Совы — мудрые и загадочные существа."),
    5: ("Габонская гадюка", "images/viper.png", "Гадюки — мастера маскировки."),
}
