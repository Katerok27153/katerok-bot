import pytest
import sys
import os
from unittest.mock import Mock, patch

# Добавляем путь для импорта
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestMainUtils:
    """Тесты для вспомогательных функций main.py"""

    def test_is_int_token_valid_cases(self):
        """Тест функции проверки целых чисел"""
        # Импортируем внутри теста
        import main

        # Корректные целые числа
        assert main.is_int_token("123") == True
        assert main.is_int_token("-456") == True
        assert main.is_int_token("0") == True
        assert main.is_int_token("  789  ") == True

        # Некорректные значения
        assert main.is_int_token("12.34") == False
        assert main.is_int_token("abc") == False
        assert main.is_int_token("12a") == False
        assert main.is_int_token("") == False
        assert main.is_int_token("  ") == False

    def test_parse_ints_from_text_various_formats(self):
        """Тест парсинга чисел из текста в разных форматах"""
        import main

        test_cases = [
            # (input_text, expected_numbers)
            ("1 2 3", [1, 2, 3]),
            ("10, 20, 30", [10, 20, 30]),
            ("-5 0 5", [-5, 0, 5]),
            ("1,2,3,4,5", [1, 2, 3, 4, 5]),
            (" 42   -100  999 ", [42, -100, 999]),
            ("/sum 1 2 3", [1, 2, 3]),  # команда должна игнорироваться
            ("текст 10 другой 20 текст", [10, 20]),
            ("", []),
            ("нет чисел здесь", []),
            ("1.5 2.7", []),  # дробные числа не парсятся
        ]

        for input_text, expected in test_cases:
            result = main.parse_ints_from_text(input_text)
            assert result == expected, f"Для '{input_text}' ожидалось {expected}, получено {result}"

    def test_validate_user_input(self):
        """Тест валидации пользовательского ввода"""
        import main

        # Корректный ввод
        assert main.validate_user_input("текст") == True
        assert main.validate_user_input("123") == True
        assert main.validate_user_input("  текст с пробелами  ") == True

        # Некорректный ввод
        assert main.validate_user_input("") == False
        assert main.validate_user_input("   ") == False
        assert main.validate_user_input(None) == False

    def test_make_main_kb_structure(self):
        """Тест создания главной клавиатуры"""
        import main
        from telebot import types

        kb = main.make_main_kb()

        # Проверяем что возвращается правильный тип
        assert isinstance(kb, types.ReplyKeyboardMarkup)
        assert kb.resize_keyboard == True

        # Можно также проверить структуру кнопок
        assert hasattr(kb, 'keyboard')
        assert isinstance(kb.keyboard, list)