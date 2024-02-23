from django.core.validators import RegexValidator

USERNAME_SYMBOLS_REGEX = RegexValidator(r'^[\w.@+-]+\Z')
