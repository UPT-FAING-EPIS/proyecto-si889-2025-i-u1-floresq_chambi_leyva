import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Document, User  # Asegúrate de importar el modelo User
from config.database import Base
from config.config import Config
from fastapi.testclient import TestClient
from app.app import app

# Crear el motor de conexión a SQL Server usando SQLAlchemy
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para el cliente de pruebas
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Fixture para la base de datos
@pytest.fixture(scope="module")
def db():
    db_session = SessionLocal()
    yield db_session
    db_session.close()

# Fixture para obtener un token válido
@pytest.fixture(scope="module")
def token(client):
    response = client.post(
        "/api/users/token",  # Ruta correcta para obtener el token
        data={"username": "Jaime", "password": "123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# Fixture para obtener un usuario existente
@pytest.fixture(scope="module")
def test_user(db):
    # Suponemos que "Jaime" ya existe en la base de datos
    user = db.query(User).filter(User.username == "Jaime").first()
    assert user is not None, "El usuario Jaime no existe en la base de datos"
    return user

# Test de listar documentos
def test_list_user_documents(client, db, test_user, token):
    headers = {"Authorization": f"Bearer {token}"}

    # Ahora que tenemos el token, podemos hacer la siguiente solicitud para obtener los documentos
    response = client.get("/api/documents/list", headers=headers)
    
    assert response.status_code == 200
    documents = response.json()["documents"]
    assert len(documents) >= 1
    assert any(doc["title"] == "Sample Document 1" for doc in documents)

@pytest.fixture
def upload_file():
    return {
        "file": ("test_document.txt", b"Esto es un archivo de prueba para el test", "text/plain")
    }
def test_upload_document(client, upload_file, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": "Test Document"} 
    response = client.post("/api/documents/upload/", files=upload_file, data=data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data

def test_delete_latest_document_version(client, token, db):
    # Obtener el último documento con el user_id = 1
    document = db.query(Document).filter(Document.user_id == 1).order_by(Document.version.desc()).first()

    # Obtener documento_id y versión
    document_id, version_number = document.document_id, document.version

    # Realizar la petición DELETE para eliminar la última versión
    client.delete(
        f"/api/documents/versions/{document_id}/{version_number}",
        headers={"Authorization": f"Bearer {token}"}
    )
