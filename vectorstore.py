from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path


def make_vectorstore(base_knowledge_path: str | Path, vectorstore_save_path: str | Path) -> None:
    """
    Создание и сохранение векторного хранилища из базы знаний в формате PDF документа.

    Параметры
    ----------
    base_knowledge_path : str или Path
        Путь к PDF документу, который будет загружен.
    vectorstore_save_path : str или Path
        Путь, по которому будет сохранено векторное хранилище.

    Возвращает
    ----------
    None

    Описание
    --------
    Функция загружает PDF документ, разбивает его текст на части,
    создает векторное хранилище с использованием модели встраивания
    и сохраняет это хранилище на локальный диск.

    Примеры
    --------
    make_vectorstore("path/to/pdf/document.pdf", "path/to/save/vectorstore")
    """
    # load a PDF
    documents = PyPDFLoader(base_knowledge_path).load()

    # Split text
    text = RecursiveCharacterTextSplitter().split_documents(documents)

    # Load embedding model
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5",
                                       encode_kwargs={"normalize_embeddings": True})

    # Create a vectorstore
    vectorstore = FAISS.from_documents(text, embeddings)

    # Save the documents and embeddings
    vectorstore.save_local(vectorstore_save_path)


def load_vectorstore(vectorstore_load_path: str | Path) -> FAISS:
    """
    Загрузка векторного хранилища из файла.

    Параметры
    ----------
    vectorstore_load_path : str или Path
        Путь к файлу, из которого будет загружено векторное хранилище.

    Возвращает
    ----------
    FAISS
        Загруженное векторное хранилище.

    Описание
    --------
    Функция загружает векторное хранилище с локального диска с использованием эмбеддингов.

    Примеры
    --------
    vectorstore = load_vectorstore("path/to/load/vectorstore")
    """
    # Load embedding model
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5",
                                       encode_kwargs={"normalize_embeddings": True})
    return FAISS.load_local(vectorstore_load_path, embeddings, allow_dangerous_deserialization=True)


if __name__ == '__main__':
    bk_path = "База знаний фейк.pdf"
    vec_store_save_path = "faik_FAISS_store.db"
    make_vectorstore(bk_path, vec_store_save_path)
