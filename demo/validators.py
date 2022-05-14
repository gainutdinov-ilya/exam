from django.core.validators import RegexValidator


def validate_cyr_only(value):
    regex = RegexValidator("^[а-яА-Я -]+$", message="Допускаются только кирилица, пробелы, тире")
    regex(value)


def validate_eng_only(value):
    regex = RegexValidator("^[a-zA-Z -]+$")
    regex(value)
