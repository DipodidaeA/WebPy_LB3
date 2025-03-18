import os

# для збереження яку БД використовували останню
# щоб при запуску її і використовувати

dir = os.path.dirname(os.path.abspath(__file__))

filename = os.path.join(dir, "DbState.txt")

# запис позначки БД
def save(state: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(state)

# отримання позначки БД
def load():
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None