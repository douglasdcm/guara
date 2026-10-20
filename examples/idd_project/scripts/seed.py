# seed.py
from bakery.backend.entities import User
from bakery.backend.repository import Repository

repo = Repository()

gerente = User(id=1, name="gerente", role="Gerente", secret="qwerty123", logged_in=False)
atendente = User(id=2, name="atendente", role="Atendente", secret="qwerty123", logged_in=False)

repo.add_user(gerente)
repo.add_user(atendente)
