from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
import requests
from .models import Product, Order
from .forms import OrderForm

def home(request):
    panels = Product.objects.filter(category='panel')[:3]
    gabions = Product.objects.filter(category='gabion')[:3]
    return render(request, 'shop/home.html', {'panels': panels, 'gabions': gabions})

def catalog(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/catalog.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart(request):
    cart_ids = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_ids)
    total = sum(p.price for p in products)
    return render(request, 'shop/cart.html', {'products': products, 'total': total})

def add_to_cart(request, id):
    cart = request.session.get('cart', [])
    if id not in cart:
        cart.append(id)
        request.session['cart'] = cart
        messages.success(request, "Товар добавлен в корзину!")
    return redirect('catalog')

def remove_from_cart(request, id):
    cart = request.session.get('cart', [])
    if id in cart:
        cart.remove(id)
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    cart_ids = request.session.get('cart', [])
    if not cart_ids:
        messages.error(request, "Корзина пуста!")
        return redirect('catalog')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            # Отправка в Telegram
            send_telegram_message(order, request.session.get('cart'))
            # Очистка корзины
            request.session['cart'] = []
            messages.success(request, f"Спасибо за заказ, {order.name}! Мы свяжемся с вами в ближайшее время.")
            return redirect('home')
    else:
        form = OrderForm()

    products = Product.objects.filter(id__in=cart_ids)
    total = sum(p.price for p in products)
    return render(request, 'shop/checkout.html', {'form': form, 'total': total, 'products': products})

def send_telegram_message(order, cart_ids):
    # Замени на свой токен и ID
    BOT_TOKEN = "ВАШ_ТОКЕН"
    CHAT_ID = "ВАШ_CHAT_ID"
    
    product_names = [p.name for p in Product.objects.filter(id__in=cart_ids)]
    message = (
        f"📦 <b>НОВЫЙ ЗАКАЗ</b>\n"
        f"Имя: {order.name}\n"
        f"Телефон: {order.phone}\n"
        f"Адрес: {order.address}\n"
        f"Товары: {', '.join(product_names)}\n"
        f"Комментарий: {order.comment or 'нет'}\n"
        f"Время: {order.created_at.strftime('%H:%M %d.%m.%Y')}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data)
    except:
        pass
