import pytest
from unittest.mock import Mock, patch
from DetectAntivirusService  import check_auto_start_services  # Импортируйте вашу функцию
#

def test_get_auto_start_services_empty():
    # Тест на отсутствие служб в списке
    with patch('builtins.open', pytest.mock.mock_open(read_data="")):
        assert check_auto_start_services("av_services.txt") == []

@patch('DetectAntivirusService.winreg')
@patch('winreg.OpenKey')
@patch('winreg.QueryInfoKey', return_value=(1, 0))
@patch('winreg.EnumKey', return_value='SomeAntivirusService')
@patch('winreg.QueryValueEx', return_value=(2, 'REG_DWORD'))
def test_get_auto_start_services_found(mock_openkey, mock_queryinfokey, mock_enumkey, mock_queryvalueex):
    # Тест на наличие службы с автозапуском в списке
    with patch('builtins.open', pytest.mock.mock_open(read_data="SomeAntivirusService")):
        services = check_auto_start_services("av_services.txt")
        assert services == ['SomeAntivirusService']
        mock_openkey.assert_called_with(winreg.HKEY_LOCAL_MACHINE, r"SYSTEMCurrentControlSetServicesSomeAntivirusService", access=winreg.KEY_READ)

# Можно добавить больше тестов для различных сценариев
