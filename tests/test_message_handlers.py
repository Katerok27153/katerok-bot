import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestMessageHandlers:
    """Тесты для обработчиков сообщений"""

    def test_about_command_content(self):
        """Тест содержания команды /about"""
        import main

        # Создаем mock сообщение
        mock_message = Mock()
        mock_message.chat.id = 12345

        # Мокаем bot.send_message чтобы перехватить вызов
        with patch.object(main.bot, 'send_message') as mock_send:
            main.about_cmd(mock_message)

            # Проверяем что send_message был вызван
            mock_send.assert_called_once()

            # Получаем переданный текст
            call_args = mock_send.call_args
            sent_text = call_args[0][1]  # второй аргумент - текст

            # Проверяем содержание
            assert "Верниковская Екатерина Андреевна" in sent_text
            assert "Версия: 1.0.3" in sent_text

    def test_help_command_structure(self):
        """Тест что команда /help содержит основные команды"""
        import main

        mock_message = Mock()
        mock_message.chat.id = 12345

        with patch.object(main.bot, 'send_message') as mock_send:
            main.help_cmd(mock_message)

            mock_send.assert_called_once()
            call_args = mock_send.call_args
            sent_text = call_args[0][1]

            # Проверяем наличие основных команд в помощи
            assert "/start" in sent_text
            assert "/help" in sent_text
            assert "/about" in sent_text
            assert "/sum" in sent_text