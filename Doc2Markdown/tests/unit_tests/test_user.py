import pytest
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User  # Cambia a tus modelos específicos
from config.database import Base
from config.config import Config 

# Crear el motor de conexión a SQL Server usando SQLAlchemy
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para la base de datos
@pytest.fixture(scope="module")
def db():
    # Crear una sesión de base de datos
    db_session = SessionLocal()
    yield db_session  # Esto es lo que será inyectado en las pruebas

    # Limpiar después de las pruebas
    db_session.close()

# Ejemplo de prueba de verificación de sesión (autenticación)
def test_user_authentication(db):
    # Suponiendo que el usuario ya existe en la base de datos, lo buscamos
    user = db.query(User).filter_by(username="Jaime").first()

    # Verifica que el usuario existe en la base de datos
    assert user is not None
    assert user.username == "Jaime"
    assert user.email == "jaime.doe@example.com"

    # Verifica si la contraseña proporcionada es válida usando bcrypt
    is_password_correct = bcrypt.checkpw(
        "123".encode('utf-8'), 
        user.password_hash.encode('utf-8')
    )

    assert is_password_correct is True  # Aseguramos que la contraseña sea correcta

def test_user_authentication_failed(db):
    # Caso 1: El usuario no existe
    user = db.query(User).filter_by(username="NoExiste").first()
    assert user is None  # El usuario no debería existir

    # Caso 2: Contraseña incorrecta
    user = db.query(User).filter_by(username="Jaime").first()  # Usamos un usuario que sí existe
    assert user is not None  # Confirmamos que el usuario existe

    incorrect_password = "contraseña_incorrecta"
    # Usamos bcrypt para verificar la contraseña
    is_password_correct = bcrypt.checkpw(
        incorrect_password.encode('utf-8'),
        user.password_hash.encode('utf-8')
    )
    assert is_password_correct is False 