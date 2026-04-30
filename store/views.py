from functools import wraps
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .forms import CustomUserCreationForm
from .models import Product, Order, Store, Review
from .serializers import ProductSerializer, StoreSerializer, ReviewSerializer
from .functions.reddit import fetch_reddit_posts


# =========================
# PERMISSIONS
# =========================

def vendor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_vendor:
            return redirect('buyer_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# =========================
# API VIEWSETS
# =========================

def stores_by_vendor(request, vendor_id):
    stores = Store.objects.filter(owner_id=vendor_id)

    data = [
        {
            "id": s.id,
            "name": s.name,
            "owner": s.owner.username
        }
        for s in stores
    ]

    return JsonResponse(data, safe=False)


def products_by_store(request, store_id):
    products = Product.objects.filter(store_id=store_id)

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price)
        }
        for p in products
    ]

    return JsonResponse(data, safe=False)


@login_required
def vendor_reviews(request):
    if not request.user.is_vendor:
        return JsonResponse({"error": "Not a vendor"}, status=403)

    reviews = Review.objects.filter(product__store__owner=request.user)

    data = [
        {
            "product": r.product.name,
            "user": r.user.username,
            "content": r.content,
            "verified": r.verified
        }
        for r in reviews
    ]

    return JsonResponse(data, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        store_id = self.request.query_params.get('store')
        if store_id:
            return Product.objects.filter(store_id=store_id)
        return Product.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_vendor:
            raise PermissionDenied("Not a vendor")

        store = Store.objects.filter(owner=self.request.user).first()
        serializer.save(store=store)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        vendor_id = self.request.query_params.get('vendor')

        if vendor_id:
            return Store.objects.filter(owner_id=vendor_id)

        return Store.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_vendor:
            raise PermissionDenied("Not a vendor")

        serializer.save(owner=self.request.user)


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return Review.objects.filter(product_id=product_id)
        return Review.objects.all()


# =========================
# PUBLIC STORE VIEW
# =========================

def view_products(request):
    products = Product.objects.all()
    reviews = Review.objects.all()
    return render(request, 'store/list.html', {
        'products': products,
        'reviews': reviews
    })


# =========================
# CART
# =========================

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('view_products')


@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'store/cart.html', {'products': products})


@login_required
def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if not products:
        messages.error(request, "Your cart is empty")
        return redirect('view_cart')

    if not request.user.email:
        messages.error(request, "Please add an email to your profile first")
        return redirect('view_cart')

    order = Order.objects.create(user=request.user)
    order.products.set(products)

    total = sum(p.price for p in products)

    request.session['cart'] = []

    invoice_html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background: #0f172a; color: #e5e7eb; padding: 20px;">
        <h2 style="color: #f9fafb;">Order Invoice</h2>
        <p>Order ID: {order.id}</p>
        <p>Thank you for your order!</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background: #1f2937;">
                <th style="padding: 10px; text-align: left;">Product</th>
                <th style="padding: 10px;">Price</th>
            </tr>
            {''.join([f"<tr><td style='padding: 8px; border-bottom: 1px solid #374151;'>{p.name}</td><td style='padding: 8px; border-bottom: 1px solid #374151;'>${p.price}</td></tr>" for p in products])}
            <tr style="font-weight: bold;">
                <td style="padding: 10px;">Total</td>
                <td style="padding: 10px;">${total:.2f}</td>
            </tr>
        </table>
    </body>
    </html>
    """

    send_mail(
        'Your Order Invoice',
        f'Thanks for your order!\n\nOrder ID: {order.id}\n\n' + "\n".join([f"- {p.name}: ${p.price}" for p in products]) + f'\n\nTotal: ${total:.2f}',
        'from@example.com',
        [request.user.email],
        html_message=invoice_html,
    )

    return render(request, 'store/checkout_success.html', {'order': order})


# =========================
# REVIEWS
# =========================

@login_required
def add_review(request, product_id):
    if request.method == "POST":
        content = request.POST.get('content')

        if not content or content.strip() == "":
            return redirect('view_products')

        product = Product.objects.get(id=product_id)

        verified = Order.objects.filter(
            user=request.user,
            products__id=product.id
        ).exists()

        Review.objects.create(
            product=product,
            user=request.user,
            verified=verified,
            content=content
        )

        return render(request, 'store/review_success.html', {
            'content': content,
            'verified': verified
        })

    return redirect('view_products')


# =========================
# AUTH
# =========================

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('view_products')
    else:
        form = CustomUserCreationForm()

    return render(request, 'store/register.html', {'form': form})


def user_login(request):
    message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_vendor:
                return redirect('vendor_dashboard')
            return redirect('buyer_dashboard')

        else:
            message = "Invalid username or password"

    return render(request, 'store/login.html', {'message': message})


def user_logout(request):
    logout(request)
    return redirect('view_products')


def view_store(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)

    return render(request, 'store/store.html', {
        'store': store,
        'products': products
    })


# =========================
# DASHBOARDS
# =========================

@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        return redirect('buyer_dashboard')

    store = Store.objects.filter(owner=request.user).first()
    products = Product.objects.filter(store=store) if store else []

    return render(request, 'store/vendor_dashboard.html', {
        'store': store,
        'products': products
    })


@vendor_required
def store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    products = Product.objects.filter(store=store)

    is_owner = request.user.is_authenticated and request.user == store.owner

    return render(request, 'store/store.html', {
        'store': store,
        'products': products,
        'is_owner': is_owner
    })


@login_required
def buyer_dashboard(request):
    stores = Store.objects.all()
    return render(request, 'store/buyer_dashboard.html', {
        'stores': stores
    })


# =========================
# VENDOR ACTIONS
# =========================



@vendor_required
def create_store(request):
    existing = Store.objects.filter(owner=request.user).first()

    if existing:
        return redirect('vendor_dashboard')

    if request.method == "POST":
        name = request.POST.get('name')

        if not name or name.strip() == "":
            return render(request, 'store/store_form.html', {
                "error": "Store name cannot be empty"
            })

        name = name.strip()

        if len(name) < 3:
            return render(request, 'store/store_form.html', {
                "error": "Store name must be at least 3 characters"
            })

        if len(name) > 50:
            return render(request, 'store/store_form.html', {
                "error": "Store name too long (max 50)"
            })

        Store.objects.create(
            owner=request.user,
            name=name
        )
        messages.success(request, "Store created successfully")
        return redirect('vendor_dashboard')

    return render(request, 'store/store_form.html')


@vendor_required
def edit_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        name = request.POST.get('name')

        if not name or name.strip() == "":
            return render(request, 'store/store_form.html', {
                "error": "Store name cannot be empty",
                "store": store
            })

        name = name.strip()

        if len(name) < 3:
            return render(request, 'store/store_form.html', {
                "error": "Store name must be at least 3 characters",
                "store": store
            })

        store.name = name
        store.save()
        messages.success(request, "Store updated successfully")
        return redirect('vendor_dashboard')

    return render(request, 'store/store_form.html', {'store': store})


@vendor_required
def delete_store(request, store_id):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    store.delete()
    messages.success(request, "Store deleted successfully")
    return redirect('vendor_dashboard')


@vendor_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)
    stores = Store.objects.filter(owner=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        price_raw = request.POST.get("price")

        try:
            price = Decimal(price_raw)
        except:
            return render(request, "store/product_form.html", {
                "error": "Price must be a number",
                "product": product,
                "stores": stores,
            })

        if price >= Decimal("1000000"):
            return render(request, "store/product_form.html", {
                "error": "Max price is 999,999",
                "product": product,
                "stores": stores,
            })

        product.name = name
        product.price = price
        product.save()
        messages.success(request, "Product updated successfully")
        return redirect('store_detail', store_id=product.store.id)

    return render(request, "store/product_form.html", {"product": product, "stores": stores})


@vendor_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, store__owner=request.user)
    store_id = product.store.id
    product.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('store_detail', store_id=store_id)


@vendor_required
def add_product(request):
    store = Store.objects.filter(owner=request.user).first()

    # if no store then force create store
    if not store:
        return redirect('create_store')

    if request.method == "POST":
        name = request.POST.get("name")
        price_raw = request.POST.get("price")
        store_id = request.POST.get("store")

        # safety parse
        try:
            price = Decimal(price_raw)
        except:
            return render(request, "store/product_form.html", {
                "error": "Price must be a number",
                "stores": Store.objects.filter(owner=request.user),
            })

        if price >= Decimal("1000000"):
            return render(request, "store/product_form.html", {
                "error": "Max price is 999,999",
                "stores": Store.objects.filter(owner=request.user),
            })

        store = Store.objects.get(id=store_id, owner=request.user)

        Product.objects.create(
            name=name,
            price=price,
            store=store
        )

        return redirect('store_detail', store_id=store.id)

    return render(request, "store/product_form.html", {
        "stores": Store.objects.filter(owner=request.user)
    })


def reddit_feed(request):
    posts = fetch_reddit_posts("django")

    return render(request, "store/reddit_feed.html", {
        "posts": posts
    })
