from modules import users


def validate_user(form_data) -> dict:
    query = dict(username=form_data.username)
    user = users.get(query=query)
    if not user:
        return False, "Usuario no encontrado."
    if user.password != form_data.password:
        return False, "Contraseña incorrecta."
    return True, None

