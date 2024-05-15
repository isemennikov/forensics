import pytest
from unittest.mock import Mock, patch

# Мокируем модуль winreg внутри нашего тестового модуля
@patch('DetectAntivirusService.winreg', create=True)
def test_check_auto_start_services(mock_winreg):
    # Настройка моков для winreg
    mock_key = Mock()
    mock_winreg.OpenKey.return_value = mock_key
    mock_winreg.EnumKey.return_value = 'SomeService'
    mock_winreg.QueryValueEx.return_value = (2, 'REG_DWORD')

    # Теперь импортируем функцию, которую хотим протестировать
    from DetectAntivirusService import check_auto_start_services

    # Теперь вызываем вашу функцию
    result = check_auto_start_services()

    # Проверяем, что функция отработала корректно
    # Например, мы ожидаем, что функция вернет список служб
    assert result == ['SomeService']

    # Проверяем, что были вызваны правильные функции из winreg
    mock_winreg.OpenKey.assert_called_once()
    mock_winreg.EnumKey.assert_called_once()
    mock_winreg.QueryValueEx.assert_called_once()
