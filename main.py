import time
from flet import app, Page
from flet_core import AppBar, Text, IconButton, ButtonStyle, colors, Column, ProgressBar, View, ScrollMode, \
    ElevatedButton, SnackBar, TextField


def main(page: Page):
    # Название окна приложения
    page.title = "Wallpaper Calculator"

    def result_button_clicked(e):
        # Проверка обязательных полей
        if (room_width.value == "0" or room_width.value == '' or room_length.value == "0" or room_length.value == '' or
                room_height.value == "0" or room_height.value == '' or roll_width.value == "0" or roll_width.value == '' or
                roll_length.value == "0" or roll_length.value == ''):
            show_snack_bar("Заполните все обязательные поля! (Помечены *)")
            page.update()
            return
        else:
            room_w = float(room_width.value)
            room_l = float(room_length.value)
            room_h = float(room_height.value)
            roll_w = float(roll_width.value) * 0.01
            roll_l = float(roll_length.value)

        # Проверка не обязательных полей на отсутствие ввода значения.
        if door_width.value == '':
            door_w = 0
        else:
            door_w = float(door_width.value)
        if door_length.value == '':
            door_l = 0
        else:
            door_l = float(door_length.value)
        if window_width.value == '':
            window_w = 0
        else:
            window_w = float(window_width.value)
        if window_length.value == '':
            window_l = 0
        else:
            window_l = float(window_length.value)
        if roll_price.value == '':
            roll_p = 0
        else:
            roll_p = float(roll_price.value)
        # Расчет площади стен комнаты.
        area_room = (room_w + room_l) * 2 * room_h
        # Расчет площади двери.
        area_door = door_w * door_l
        # Расчет площади окна.
        area_window = window_w * window_l
        # Расчет площади рулона.
        area_roll = roll_w * roll_l
        # Расчет необходимого кол-ва рулонов.
        result = (area_room - (area_door + area_window)) / area_roll
        result_rounded = 0
        # Округление
        if result % 1 > 0:
            result_rounded = (result // 1) + 1
        # расчет стоимости рулонов
        price_roll = roll_p * result_rounded

        result_formatter = f"Необходимое кол-во рулонов: {result_rounded}"
        price = f"Цена за все рулоны: {price_roll} (руб)"

        text_output1.value = result_formatter
        text_output2.value = price

        page.go("/result")

    def show_snack_bar(msg):
        snack_bar = SnackBar(content=Text(msg), bgcolor=colors.RED)
        page.snack_bar = snack_bar
        snack_bar.open = True

    def back_button(e):
        page.go("/")

    # Выбор режима по умолчанию, светлый или тёмный.
    page.theme_mode = "light"

    # ДОБАВЛЯЕМ ЭФФЕКТ ИНДИКАТОРА ПРОГРЕССА ПРИ СМЕНЕ СВЕТА ИЛИ ТЕМНОТЫ
    page.splash = ProgressBar(visible=False)

    def changeTheme(e):
        page.splash.visible = True
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        page.update()

        # ЭФФЕКТ ЗАДЕРЖКИ АНИМАЦИИ
        time.sleep(0.5)

        # ИЗМЕНЕНИЕ ЗНАЧКА В ТЕМНОМ ИЛИ СВЕТЛОМ РЕЖИМЕ
        toggleDarkLight.selected = not toggleDarkLight.selected

        # ОТКЛЮЧЕНИЕ ИНДИКАТОРА ВЫПОЛНЕНИЯ ПРИ СМЕНЕ ТЕМНОГО РЕЖИМА
        page.splash.visible = False

        # ОБНОВЛЕНИЕ СТРАНИЦЫ ДЛЯ ИЗМЕНЕНИЯ СОСТОЯНИЯ
        page.update()

    # СОЗДАНИЕ ПЕРЕКЛЮЧАЮЩЕЙ КНОПКИ НА ТЁМНЫЙ И СВЕТЛЫЙ РЕЖИМ

    toggleDarkLight = IconButton(
        on_click=changeTheme,
        icon="dark_mode",
        selected_icon="light_mode",
        style=ButtonStyle(
            # меняйте цвет, если он светлый или темный
            color={"": colors.BLACK, "selected": colors.WHITE}
        )
    )

    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Ввод данных", size=30),
                           bgcolor="indigo",
                           leading=IconButton(icon="menu"),
                           actions=[toggleDarkLight]),
                    input_column
                ],
                scroll=ScrollMode.ADAPTIVE
            )
        )
        if page.route == "/result":
            page.views.append(
                View(
                    "/result",
                    [
                        AppBar(title=Text("Результат", size=30),
                               bgcolor="indigo",
                               leading=IconButton(icon="menu"),
                               actions=[toggleDarkLight]),
                        output_column
                    ],
                    scroll=ScrollMode.ADAPTIVE
                )
            )
        page.update()

    # Контент приложения
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    room_width = TextField(label="Ширина комнаты (м)*", autofocus=True)
    room_length = TextField(label="Длина комнаты (м)*", autofocus=True)
    room_height = TextField(label="Высота комнаты (м)*", autofocus=True)
    door_width = TextField(label="Ширина двери (м)", autofocus=True)
    door_length = TextField(label="Длина двери (м)", autofocus=True)
    window_width = TextField(label="Ширина окна (м)", autofocus=True)
    window_length = TextField(label="Длина окна (м)", autofocus=True)
    roll_width = TextField(label="Ширина рулона (см)*", autofocus=True)
    roll_length = TextField(label="Длина рулона (м)*", autofocus=True)
    roll_price = TextField(label="Цена рулона (руб)", autofocus=True)
    result_button = ElevatedButton(text="Показать результат", on_click=result_button_clicked)
    b_button = ElevatedButton(text="Вернуться в начало", on_click=back_button)
    text_output1 = Text(size=28, selectable=True)
    text_output2 = Text(size=28, selectable=True)

    input_column = Column(
        [room_width, room_length, room_height, door_width, door_length, window_width, window_length, roll_width,
         roll_length, roll_price, result_button])
    output_column = Column([text_output1, text_output2, b_button])

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


if __name__ == "__main__":
    app(target=main)
