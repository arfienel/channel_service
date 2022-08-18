import requests
import gspread
import psycopg2
from datetime import datetime


def update_orders_data():
    """
    Функция чтобы обновлять и добавлять данные о заказах в бд из гугл таблицы
    """
    # получение данных из гугл таблицы
    acc = gspread.service_account(filename='/code/credentials.json')
    spreadsheet = acc.open("test_data")
    orders_data = spreadsheet.sheet1.get_all_values()

    # получения курса доллара к рублю от ЦБ РФ
    cbr_exchange_rates = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    usd_rub = cbr_exchange_rates['Valute']['USD']['Value']

    # подключение к бд
    conn = psycopg2.connect(dbname='channel_service_orders', user='channel_service_admin', password='coolpas123', host='db', port='5432')
    cursor = conn.cursor()

    # Удаление заказов которые есть в бд, но нет в гугл таблицах
    cursor.execute("select id from orders_order")
    orders_ids = (order_ids[0] for order_ids in orders_data[1:])
    for order_db_id in cursor.fetchall():
        if order_db_id[0] not in orders_ids:
            cursor.execute(f"delete from orders_order where id={order_db_id[0]}")

    # обновление, добавление данных о заказах в бд
    for order in orders_data[1:]:
        if order[0] == '' or order[1] == '' or order[2] == '' or order[3] == '':
            continue
        order_id = order[0]
        order_number = str(order[1])
        order_cost_usd = order[2]

        order_cost_rub = round(int(order_cost_usd) * float(usd_rub), 2)
        order_supply_date = datetime.strptime(order[3], "%d.%m.%Y")
        cursor.execute(f"SELECT * FROM orders_order WHERE id={order_id}")
        order_db = cursor.fetchone()

        if not order_db:
            cursor.execute(f"INSERT INTO orders_order (id, order_number, cost_usd, cost_rub, supply_date) VALUES "
                           f"({order_id}, '{order_number}', {order_cost_usd}, {order_cost_rub}, '{order_supply_date}')")
        elif order_db[1] != order_number or order_db[2] != int(order_cost_usd) or \
                order_db[3] != order_cost_rub or order_db[4] != order_supply_date:
            cursor.execute(f"UPDATE orders_order SET order_number='{order_number}', cost_usd={order_cost_usd},"
                           f" cost_rub={order_cost_rub}, supply_date='{order_supply_date}' WHERE id={order_id}")

    conn.commit()


if __name__ == "__main__":
    update_orders_data()
