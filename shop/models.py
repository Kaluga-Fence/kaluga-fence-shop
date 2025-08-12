from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('panel', '3D-панель'),
        ('mesh', 'Сетка для габионов'),
        ('gabion', 'Готовый габион'),
    ]

    name = models.CharField("Название", max_length=200)
    category = models.CharField("Категория", max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField("Описание", blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Фото", upload_to="products/", blank=True, null=True)
    size = models.CharField("Размер", max_length=50, help_text="Например: 1.53×2.5 м")
    thickness = models.CharField("Толщина", max_length=20, blank=True, help_text="Например: 4 мм")
    available = models.BooleanField("В наличии", default=True)

    def __str__(self):
        return f"{self.name} ({self.size})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Order(models.Model):
    name = models.CharField("Имя", max_length=100)
    phone = models.CharField("Телефон", max_length=20)
    address = models.TextField("Адрес")
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField("Статус", max_length=20, default="Новый")

    def __str__(self):
        return f"Заказ {self.id} — {self.name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
