from django.db.models import Count, Avg


def collect_result_data(restaurant_menu):
    """
    This function get day summary data for one restaurant with dedicated menu
    :param restaurant_menu:
    :return: dict with collected data
    """
    restaurant = restaurant_menu.restaurant
    menu = restaurant_menu.menu
    date = restaurant_menu.date

    rate_data = restaurant_menu.votes.all().aggregate(
        amount=Count("id"),
        average=Avg("rate")
    )

    return {
        "restaurant": restaurant,
        "menu": menu,
        "date": date,
        "rate_amount": rate_data["amount"],
        "average_rate": rate_data["average"],
    }
