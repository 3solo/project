from json import *

with open('Users.json', 'r', encoding='utf-8') as file:
    users = load(file)
with open('Wishes.json', 'r', encoding='utf-8') as file:
    wishes = load(file)

a = 1

while a == 1:
    log = input('Введите логин: ')
    pas = input('Введите пароль: ')
    if log == 'admin' and pas == 'admin':
        print('Вы вошли как админ!')
        with open('Orders.json', 'r+', encoding='utf-8') as file:
            orders = load(file)

        while a == 1:
            print('Список заказов:')
            for i, order in enumerate(orders):
                print( f'Номер заказа: {order["order_number"]}, Пользователь: {order["user"]}, Блюдо: {order["bludo"]}, Количество: {order["quantity"]}, Статус: {order["state"]}')

            yn = int(input('\nЖелаете редактировать статус заказа? 0-Да 1-Нет: '))
            if yn == 0:

                    order_num = int(input('Введите номер заказа для редактирования: ')) - 1
                    if 0 <= order_num < len(orders):
                        print(f'Текущий статус: {orders[order_num]["state"]}')
                        print('Доступные статусы:')
                        print('1. None')
                        print('2. В обработке')
                        print('3. Готовится')
                        print('4. Готов')

                        status_choice = int(input('Выберите новый статус (1-4): '))
                        status_ed = {
                            1: "None",
                            2: "В обработке",
                            3: "Готовится",
                            4: "Готов",
                           }

                        if status_choice in status_ed:
                            orders[order_num]["state"] = status_ed[status_choice]

                            with open('Orders.json', 'w', encoding='utf-8') as file:
                                dump(orders, file, ensure_ascii=False, indent=4)
                                print('Статус успешно обновлен!')
                        else:
                            print('Неверный выбор статуса!')
                    else:
                        print('Неверный номер заказа!')

            elif yn == 1:
                print('Вы успешно вышли!')
                break
        a = 0

    else:
        user_found = 0
        for user in users:
            if user['login'] == log and user['password'] == pas:
                print(f'Вы вошли в свой аккаунт {log}!\nЧто бы вы хотели заказать?')
                print('Меню!')

                for wish in wishes:
                    print(f'{wish["numbers"]}.{wish["bludo"]}')
                b = 1
                while b == 1:

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
                                max_order_number = max(order("order_number", 0) for order in orders)
                                next_order_number = max_order_number + 1

                        except FileNotFoundError:
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

                        with open('Orders.json', 'w', encoding='utf-8') as file:
                            dump(orders, file, ensure_ascii=False, indent=4)

                        print(f'Заказ успешно сохранен! Номер вашего заказа: {next_order_number}')
                        b = 0

                user_found = 1
                a = 0
                break

        if not user_found:
            print('Вы ввели логин или пароль не верно!')
            bre = int(input('Для выхода из программы введите 0, для повторного логина 1: '))
            if bre == 0:
                print('Вы успешно вышли')
                break
            if bre == 1:
                print('Введите значения заново!')