"""URL routing for the store application."""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import stores_by_vendor

from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StoreViewSet, ReviewViewSet

# API router
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'reviews', ReviewViewSet)

# Normal URLs
urlpatterns = [
    path('', views.view_products, name='view_products'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('store/<int:store_id>/', views.view_store, name='store_detail'),
    path('buyer/', views.buyer_dashboard, name='buyer_dashboard'),

    path(
         'password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'
         ),
    path(
         'password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'
         ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
        ),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'
         ),

    path('store/create/', views.create_store, name='create_store'),
    path('store/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('store/<int:store_id>/delete/',
         views.delete_store, name='delete_store'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:product_id>/edit/', views.edit_product,
         name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product,
         name='delete_product'),

    path('api/vendors/<int:vendor_id>/stores/', stores_by_vendor),
    path('api/stores/<int:store_id>/products/', views.products_by_store),
    path('api/vendor/reviews/', views.vendor_reviews),

    path('reddit/', views.reddit_feed, name='reddit_feed'),
]

# Add API URLs
urlpatterns += router.urls
