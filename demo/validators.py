from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_cyr_only(value):
    regex = RegexValidator("^[а-яА-Я -]+$", message="Допускаются только кирилица, пробелы, тире")
    regex(value)


def validate_eng_only(value):
    regex = RegexValidator("^[a-zA-Z -]+$", message="Допускаются только латиница, пробелы, тире")
    regex(value)


def validate_eng_only_with_numeric(value):
    regex = RegexValidator("^[a-zA-Z0-9 -]+$", message="Допускаются только латиница, пробелы, тире, цифры")
    regex(value)


def validate_password(value):
    if(len(value) < 6):
        raise ValidationError("Минимальная длинна 6 символов")