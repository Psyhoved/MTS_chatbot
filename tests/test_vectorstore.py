import os
import sys
import pytest
import tempfile
# Добавьте корневую директорию проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vectorstore import make_vectorstore, load_vectorstore
from langchain.vectorstores import FAISS

# Пути для тестовых данных
TEST_PDF_PATH = "../База знаний фейк.pdf"
VECTORSTORE_SAVE_PATH = "test_data/test_vectorstore"
VECTORSTORE_LOAD_PATH = "test_data/test_vectorstore"


@pytest.fixture
def setup_vectorstore():
    """
    Фикстура для подготовки и удаления тестового векторного хранилища.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

        # Удаление всех файлов в директории, если они существуют
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                os.remove(os.path.join(root, file))

def test_make_vectorstore(setup_vectorstore):
    """
    Тест функции make_vectorstore.
    """
    vectorstore_save_path = os.path.join(setup_vectorstore, "vectorstore")
    make_vectorstore(TEST_PDF_PATH, vectorstore_save_path)
    assert os.path.exists(vectorstore_save_path), "Vectorstore was not saved."


def test_load_vectorstore(setup_vectorstore):
    """
    Тест функции load_vectorstore.
    """
    vectorstore_save_path = os.path.join(setup_vectorstore, "vectorstore")
    make_vectorstore(TEST_PDF_PATH, vectorstore_save_path)
    vectorstore = load_vectorstore(vectorstore_save_path)
    assert isinstance(vectorstore, FAISS), "Loaded object is not a FAISS instance."


def test_vectorstore_content(setup_vectorstore):
    """
    Тест содержимого векторного хранилища.
    """
    vectorstore_save_path = os.path.join(setup_vectorstore, "vectorstore")
    make_vectorstore(TEST_PDF_PATH, vectorstore_save_path)
    vectorstore = load_vectorstore(vectorstore_save_path)
    # Проверка, что векторное хранилище содержит данные
    assert vectorstore.index.ntotal > 0, "Vectorstore is empty."
