from django.shortcuts import render, HttpResponse, redirect
from .models import *
from .orders_updater import update_orders_data


# главная страница
def index(request):
    orders = Order.objects.order_by('id').all()
    total_cost_usd = 0
    dates_cost = {}
    orders_date_cost = Order.objects.order_by('-supply_date').values_list('supply_date', 'cost_usd')
    for order in orders:
        total_cost_usd += order.cost_usd

    for order in orders_date_cost:
        if not dates_cost.get(order[0]):
            dates_cost[order[0]] = order[1]
        else:
            dates_cost[order[0]] += order[1]

    return render(request, 'index.html', {'orders': orders, 'total_cost_usd': int(total_cost_usd),
                  'dates_cost': dates_cost.items()})


# обновление данных о заказах через аякс
def update_data(request):
    update_orders_data()
    return HttpResponse('success')