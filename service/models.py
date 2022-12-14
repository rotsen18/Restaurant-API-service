from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    menus = models.ManyToManyField("Menu", through="RestaurantMenu")

    class Meta:
        unique_together = ("name", "address")

    def __str__(self):
        return self.name


class Dish(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title


class Menu(models.Model):
    dishes = models.ManyToManyField(Dish, related_name="menus")


class RestaurantMenu(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    menu = models.ForeignKey("Menu", on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        """Restaurant has only one menu for each day"""
        unique_together = ("restaurant", "date")

    def __str__(self):
        return f"{self.date} {self.restaurant} {self.menu}"


class Vote(models.Model):
    """Each vote is assigned to one RestaurantMenu item"""
    restaurant_menu = models.ForeignKey(
        RestaurantMenu,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rate = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        """One user can vote for one menu in restaurant per one day"""
        unique_together = ("restaurant_menu", "user")

    def __str__(self):
        return f"Rate: {self.rate} for {self.restaurant_menu}"
