from django.urls import path
from .views import payment_details


urlpatterns = [
    path('payment_details/<int:payment_id>', payment_details, name="payment_details"),

]
