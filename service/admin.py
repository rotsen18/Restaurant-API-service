from django.contrib import admin

from service.models import (
    Restaurant,
    Menu,
    Dish,
    Vote,
    RestaurantMenu,
)

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Dish)
admin.site.register(Vote)
admin.site.register(RestaurantMenu)
