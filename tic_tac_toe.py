def show_field(field):
    print (f"{'':^1}{'0':^3}{'1':^3}{'2':^3}")
    for i in range(3):
        print(f"{i}", end="")
        for j in range(3):
            print(f"{field[i][j]:^3}", end="")
        print()


def next_step(field, player):
    result = input("Ходит игрок %s: " % player).split(",")
    result = list(filter(correct_coordinates, result))
    if len(result) != 2:
        print("Координаты введены неверно! Введи индекс колонки, индекс строки. Например: 0,1")
        return False
    c, r = map(int, result)
    if field[r][c] != "-":
        print("Ход с такими координатами уже выполнен.")
        return False
    field[r][c] = player
    return True


def correct_coordinates(coord):
    coord = coord.strip()
    if not coord:
        return False
    if not coord.isdecimal():
        return False
    return 0 <= int(coord) <= 2


def win_indexes():
    # Строки
    for r in range(3):
        yield [(r, c) for c in range(3)]
    # Колонки
    for c in range(3):
        yield [(r, c) for r in range(3)]
    # Диагональ лев.верх - прав.низ
    yield [(i, i) for i in range(3)]
    # Диагональ прав.верх - лев.низ
    yield [(i, 3 - 1 - i) for i in range(3)]


def win(field, player):
    for indexes in win_indexes():
        if all(field[r][c] == player for r, c in indexes):
            print("Победил игрок %s!" % player)
            return True
    return False


def game():
    field = [["-" for j in range(1, 4)] for i in range(1, 4)]
    player = "x"
    step = 0

    while True:
        step += 1

        if not next_step(field, player):
            continue

        show_field(field)

        if win(field, player):
            break

        if step == 9:
            print("Увы, но партия сыграна вничью")
            break

        player = "o" if player == "x" else "x"


print("Ходы вводятся в формате индекс колонки, индекс строки. Погнали!")
game()