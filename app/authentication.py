import bcrypt


def hash_password(password: str) -> str:
    """
    Функция преобразует пароль, заданный в виде строки
    в хэш для дальнейшего хранения в базе

    :param password: Передаваемый для преобразования пароль
    :return: Криптографический хэш пароля
    """

    # Преобразование строки в байтовый массив
    password = password.encode()

    # Преобразование пароля в безопасный криптографический хэш
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    # Приводим результат обратно к строке
    return password_hashed.decode()


def check_password(password: str, password_hashed: str) -> bool:
    """
    Функция проверки передаваемого пароля (сверка с сохраненным ранее хэш
    :param password: пароль в виде строки
    :param password_hashed: хэш пароля
    :return: результат сравнения
    """

    # Преобразование строки в байтовый массив
    password = password.encode()

    # Преобразование строки хэш в байтовый массив
    password_hashed = password_hashed.encode()

    # Сравнение
    return bcrypt.checkpw(password, password_hashed)