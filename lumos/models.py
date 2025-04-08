from django.db import models

class Artist(models.Model):
    first_name = models.TextField("Имя")
    last_name = models.TextField("Фамилия")
    phone = models.TextField("Номер телефона")
    balance = models.DecimalField("Баланс", max_digits=8, decimal_places=2)
    performances = models.ManyToManyField("Performance",through="ArtistPerformance")
    orders = models.ManyToManyField("Order",through="Earning")

    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}" 

class Type(models.Model):
    show_type = models.TextField("Тип шоу")
    
    class Meta:
        verbose_name = "Тип шоу"
        verbose_name_plural = "Типы шоу"

    def __str__(self) -> str:
        return self.show_type   
    
class ShowRate(models.Model):
    show_type = models.ForeignKey("Type", on_delete=models.CASCADE)
    rate = models.DecimalField("Ставка", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"

    def __str__(self) -> str:
        return f"{self.rate}"

class Performance(models.Model):
    title = models.TextField("Название")
    duration = models.IntegerField("Продолжительность")
    cost = models.DecimalField("Стоимость", max_digits=8, decimal_places=2)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    cnt_artists = models.IntegerField("Количество артистов")

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"

    def __str__(self) -> str:
        return self.title 

class ArtistPerformance(models.Model):
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    performance = models.ForeignKey("Performance", on_delete=models.CASCADE)
    rate = models.ForeignKey("ShowRate", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Номер и артист"
        verbose_name_plural = "Номера и артисты"

class Order(models.Model):
    date = models.DateField("Дата")
    location = models.TextField("Место выступления")
    performance = models.ForeignKey("Performance", on_delete=models.CASCADE)
    amount = models.DecimalField("Стоимость", max_digits=8, decimal_places=2)
    comment = models.TextField("Комментарий")
    completed = models.BooleanField("Статус выполнения")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self) -> str:
        return f"{self.date}, {self.performance}"

class Earning(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE)
    amount = models.DecimalField("Зарплата", max_digits=8, decimal_places=2)
    paid = models.BooleanField("Статус выплаты")

    class Meta:
        verbose_name = "Заказ и артист"
        verbose_name_plural = "Заказы и артисты"
