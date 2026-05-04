"""Forms used in the store application."""

from django import forms
from .models import Product
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal


class ProductForm(forms.ModelForm):
    """Form for creating and editing products."""
    class Meta:
        model = Product
        fields = "__all__"

    def clean_price(self):
        """Validate product price limit."""
        price = self.cleaned_data["price"]
        if price >= Decimal("1000000"):
            raise forms.ValidationError("Max price is 999,999")
        return price


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Registration form with buyer/vendor role selection."""
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('vendor', 'Vendor'),
    ]

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        """Save user with selected role."""
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        role = self.cleaned_data['role']

        user.is_vendor = (role == 'vendor')

        if commit:
            user.save()

        return user
