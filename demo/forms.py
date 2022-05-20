from django import forms
from django.contrib.auth.forms import UserCreationForm
from demo.models import User
from demo.validators import *


class UserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        validators=[validate_eng_only_with_numeric],
        required=True,
        error_messages={
            'unique': "Данный логин уже занят"
        }
    )
    checkbox = forms.BooleanField(
        label="Соглашаюсь с правилами",
        initial=True,
        required=True
    )

    email = forms.EmailField(
        label="Электронная почта",
        required=True
    )

    patronymic = forms.CharField(
        label="Отчество",
        required=False
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль",
        validators=[validate_password]
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль (Повторно)",
        validators=[validate_password]
    )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data['password2']

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'name',
            'surname',
            'patronymic',
            'checkbox'
        ]


class OrderForm(forms.ModelForm):
    def clean(self):
        status = self.cleaned_data.get('status')
        rejection_reason = self.cleaned_data.get('rejection_reason')
        if self.instance.status != 'new':
            raise ValidationError({'status': 'Статус можно изменить только у новых заказов'})
        if status == 'canceled' and not rejection_reason:
            raise ValidationError({'rejection_reason': 'При отказе нужно указать причину'})