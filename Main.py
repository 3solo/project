from json import *
from enum import Enum

class OrderStatus(Enum):
    NONE = "None"
    IN_PROCESS = "В обработке"
    COOKING = "Готовится"
    READY = "Готов"

def load_data():
    with open('Users.json', 'r', encoding='utf-8') as file:
        users = load(file)
    with open('Wishes.json', 'r', encoding='utf-8') as file:
        wishes = load(file)
    return users, wishes


def load_orders():
    with open('Orders.json', 'r', encoding='utf-8') as file:
        orders = load(file)
    return orders


def save_orders(orders):
    with open('Orders.json', 'w', encoding='utf-8') as file:
        dump(orders, file, ensure_ascii=False, indent=4)


def show_orders(orders):
    for i, order in enumerate(orders):
        print(
            f'Номер заказа: {order["order_number"]}, Пользователь: {order["user"]}, Блюдо: {order["bludo"]}, Количество: {order["quantity"]}, Статус: {order["state"]}')


def edit_order_status(orders):
    order_num = int(input('Введите номер заказа для редактирования: ')) - 1
    if 0 <= order_num < len(orders):
        print(f'Текущий статус: {orders[order_num]["state"]}')
        print('Доступные статусы:')
        print('1. None')
        print('2. В обработке')
        print('3. Готовится')
        print('4. Готов')

        status_choice = int(input('Выберите новый статус (1-4): '))


        status_mapping = {
            1: OrderStatus.NONE,
            2: OrderStatus.IN_PROCESS,
            3: OrderStatus.COOKING,
            4: OrderStatus.READY,
        }

        if status_choice in status_mapping:
            orders[order_num]["state"] = status_mapping[status_choice].value
            save_orders(orders)
            print('Статус успешно обновлен!')
        else:
            print('Неверный выбор статуса!')
    else:
        print('Неверный номер заказа!')


def admin_menu():
    print('Вы вошли как админ!')
    orders = load_orders()

    while True:
        print('Список заказов:')
        show_orders(orders)

        yn = int(input('\nЖелаете редактировать статус заказа? 0-Да 1-Нет: '))
        if yn == 0:
            edit_order_status(orders)
            orders = load_orders()
        elif yn == 1:
            print('Вы успешно вышли!')
            return

def show_menu(wishes):
    print('Меню!')
    for wish in wishes:
        print(f'{wish["numbers"]}.{wish["bludo"]}')


def make_order(log, wishes):
    show_menu(wishes)

    while True:
        nymnym = int(input('Для выбора блюда введите его номер:')) - 1

        if nymnym < 0 or nymnym > 3:
            print('Такого блюда нету, повторите попытку!')
        else:
            wish = wishes[nymnym]['bludo']
            print(f'Вы выбрали {wish}')
            quantity = int(input('Введите количество:'))

            try:
                with open('Orders.json', 'r', encoding='utf-8') as file:
                    orders = load(file)
                    max_order_number = max(int(order.get("order_number", 0)) for order in orders)
                    next_order_number = max_order_number + 1
            except (FileNotFoundError, ValueError):
                orders = []
                next_order_number = 1

            order = {
                "order_number": next_order_number,
                "user": log,
                "bludo": wish,
                "quantity": quantity,
                "state": "None"
            }

            orders.append(order)
            save_orders(orders)

            print(f'Заказ успешно сохранен! Номер вашего заказа: {next_order_number}')
            return

def user_menu(log, wishes):
    print(f'Вы вошли в свой аккаунт {log}!\nЧто бы вы хотели заказать?')
    make_order(log, wishes)

users, wishes = load_data()

while True:
    log = input('Введите логин: ')
    pas = input('Введите пароль: ')

    if log == 'admin' and pas == 'admin':
        admin_menu()
        continue
    else:
        user_found = False
        for user in users:
            if user['login'] == log and user['password'] == pas:
                user_menu(log, wishes)
                user_found = True
                break

        if user_found:
            break

        print('Вы ввели логин или пароль не верно!')
        bre = int(input('Для выхода из программы введите 0, для повторного логина 1: '))
        if bre == 0:
            print('Вы успешно вышли')
            break
        elif bre == 1:
            print('Введите значения заново!')
            continue