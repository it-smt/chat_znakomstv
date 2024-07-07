import secrets


def generate_secret_token():
    """Генерирует auth_token для пользователя."""
    token = secrets.token_hex(128)
    if 256 > len(token) > 256:
        generate_secret_token()
    return token
