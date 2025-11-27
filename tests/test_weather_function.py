import pytest
import sys
import os
from unittest.mock import Mock, patch

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class TestWeatherFunction:
    """Тесты для функции погоды"""

    def test_fetch_weather_function_exists(self):
        """Тест что функция погоды существует и имеет правильную сигнатуру"""
        import main

        # Проверяем что функция существует
        assert hasattr(main, 'fetch_weather_moscow_open_meteo')

        # Проверяем что это функция
        assert callable(main.fetch_weather_moscow_open_meteo)

        # Проверяем что функция не требует аргументов
        import inspect
        sig = inspect.signature(main.fetch_weather_moscow_open_meteo)
        assert len(sig.parameters) == 0

    def test_fetch_weather_returns_string(self):
        """Тест что функция погоды возвращает строку"""
        import main

        # Мокаем requests.get чтобы избежать реального сетевого запроса
        with patch('main.requests.get') as mock_get:
            # Создаем mock ответ
            mock_response = Mock()
            mock_response.json.return_value = {
                "current": {
                    "temperature_2m": 15.5
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = main.fetch_weather_moscow_open_meteo()

            # Проверяем что результат - строка
            assert isinstance(result, str)
            assert len(result) > 0

    def test_fetch_weather_contains_expected_location(self):
        """Тест что в ответе содержится ожидаемое местоположение"""
        import main

        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = {
                "current": {
                    "temperature_2m": 20.0
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            result = main.fetch_weather_moscow_open_meteo()

            # Проверяем что в ответе есть Австралия и Brisbane
            assert "Австралия" in result
            assert "Brisbane" in result

    def test_fetch_weather_handles_temperature_formatting(self):
        """Тест форматирования температуры"""
        import main

        test_cases = [
            (15.5, "15°C"),  # округление вниз
            (15.9, "16°C"),  # округление вверх
            (-5.2, "-5°C"),  # отрицательная температура
            (0.0, "0°C"),  # ноль
        ]

        for temp_input, expected_in_output in test_cases:
            with patch('main.requests.get') as mock_get:
                mock_response = Mock()
                mock_response.json.return_value = {
                    "current": {
                        "temperature_2m": temp_input
                    }
                }
                mock_response.raise_for_status.return_value = None
                mock_get.return_value = mock_response

                result = main.fetch_weather_moscow_open_meteo()

                # Проверяем что отформатированная температура есть в результате
                assert expected_in_output in result

    def test_fetch_weather_exception_handling(self):
        """Тест обработки исключений в функции погоды"""
        import main

        # Тестируем случай когда запрос падает с исключением
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = Exception("Сетевая ошибка")

            result = main.fetch_weather_moscow_open_meteo()

            # Проверяем что при ошибке возвращается сообщение об ошибке
            assert isinstance(result, str)
            assert "Не удалось получить погоду" in result

    def test_weather_command_integration(self):
        """Тест что команда /weather вызывает функцию погоды"""
        import main

        # Создаем mock сообщение
        mock_message = Mock()
        mock_message.chat.id = 12345

        # Мокаем функцию погоды чтобы проверить вызов
        with patch.object(main, 'fetch_weather_moscow_open_meteo') as mock_weather:
            mock_weather.return_value = "Тестовая погода: 25°C"

            # Мокаем bot.send_message
            with patch.object(main.bot, 'send_message') as mock_send:
                main.weather_cmd(mock_message)

                # Проверяем что функция погоды была вызвана
                mock_weather.assert_called_once()

                # Проверяем что бот отправил сообщение
                mock_send.assert_called_once()

                # Проверяем что отправлен текст из функции погоды
                call_args = mock_send.call_args
                sent_text = call_args[0][1]
                assert "Тестовая погода: 25°C" in sent_text