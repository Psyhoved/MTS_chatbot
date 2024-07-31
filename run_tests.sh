#!/bin/bash
# Скрипт для запуска тестов

# Определение корневой директории проекта
PROJECT_ROOT="$(dirname "$(realpath "$0")")"

# Переход в директорию с тестами
cd "$PROJECT_ROOT/tests"

# Запуск тестов
pytest test_vectorstore.py
pytest test_llm_chat.py

# Ожидание нажатия клавиши перед закрытием окна
read -p "Press any key to continue..."