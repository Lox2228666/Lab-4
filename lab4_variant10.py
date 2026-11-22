"""Лабораторная работа №4. Вариант 10: задача о рюкзаке."""

from itertools import combinations

# Обозначение, размер в ячейках, очки выживания.
ITEMS = [
    ("r", 3, 25),  # Винтовка
    ("p", 2, 15),  # Пистолет
    ("a", 2, 15),  # Боекомплект
    ("m", 2, 20),  # Аптечка
    ("i", 1, 5),   # Ингалятор
    ("k", 1, 15),  # Нож
    ("x", 3, 20),  # Топор
    ("t", 1, 25),  # Оберег
    ("f", 1, 15),  # Фляжка
    ("d", 1, 10),  # Антидот
    ("s", 2, 20),  # Еда
    ("c", 2, 20),  # Арбалет
]

ROWS = 3
COLUMNS = 3
CAPACITY = ROWS * COLUMNS
START_POINTS = 10
TOTAL_POINTS = sum(points for _, _, points in ITEMS)


def find_best_set():
    """Перебрать наборы предметов и найти самый выгодный допустимый."""
    best_set = ()
    best_score = None

    # combinations выбирает предметы без повторов: каждый есть в одном экземпляре.
    for count in range(len(ITEMS) + 1):
        for selected in combinations(ITEMS, count):
            used_cells = sum(size for _, size, _ in selected)
            if used_cells > CAPACITY:
                continue

            taken_points = sum(points for _, _, points in selected)
            left_points = TOTAL_POINTS - taken_points
            final_score = START_POINTS + taken_points - left_points

            if final_score > 0 and (best_score is None or final_score > best_score):
                best_set = selected
                best_score = final_score

    return best_set, best_score


def make_inventory(selected):
    """Разложить выбранные предметы по строкам рюкзака 3x3."""
    inventory = [[] for _ in range(ROWS)]

    # Сначала крупные предметы: ячейки одного предмета идут подряд.
    for code, size, _ in sorted(selected, key=lambda item: item[1], reverse=True):
        for row in inventory:
            if len(row) + size <= COLUMNS:
                row.extend([code] * size)
                break
        else:
            raise RuntimeError("Не удалось разместить предметы по строкам")

    return inventory


def main():
    selected, score = find_best_set()

    if score is None:
        print("Нет набора предметов с положительными очками выживания.")
        return

    inventory = make_inventory(selected)

    print("Лабораторная работа №4. Вариант 10")
    print("Инвентарь 3x3:")
    for row in inventory:
        padded_row = row + [" "] * (COLUMNS - len(row))
        print(" ".join(f"[{code}]" for code in padded_row))

    used_cells = sum(size for _, size, _ in selected)
    taken_points = sum(points for _, _, points in selected)
    left_points = TOTAL_POINTS - taken_points

    print("\nВзятые предметы:", ", ".join(code for code, _, _ in selected))
    print(f"Использовано ячеек: {used_cells} из {CAPACITY}")
    print(f"Начальные очки: {START_POINTS}")
    print(f"Очки за взятые предметы: +{taken_points}")
    print(f"Очки за оставленные предметы: -{left_points}")
    print(f"Итоговые очки выживания: {score}")


if __name__ == "__main__":
    main()
