from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'address', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'г. Калуга, ул. Ленина, 1'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Дополнительные пожелания'}),
        }
        labels = {
            'name': 'Ваше имя',
            'phone': 'Телефон для связи',
            'address': 'Адрес доставки',
            'comment': 'Комментарий к заказу',
        }
