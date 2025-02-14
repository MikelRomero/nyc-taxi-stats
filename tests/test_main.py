import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import os
import json
from src.main import main, parse_args
from src.utils import generate_output_filename

class TestNYCTaxiStats(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{"average_price_per_mile": 7.65, "payment_type_distribution": {"1": 77969, "2": 19189, "0": 2234, "4": 1100, "3": 571}, "custom_indicator": 2.89}')
    @patch('os.path.isfile')
    @patch('src.main.load_data')
    @patch('src.main.compute_metrics')
    @patch('src.main.save_json')
    def test_main_existing_file(self, mock_save_json, mock_compute_metrics, mock_load_data, mock_isfile, mock_open):
        mock_isfile.return_value = True
        test_args = ["main.py", "--date", "2023-01-05"]
        with patch('sys.argv', test_args):
            main()
        mock_open.assert_called_once_with(os.path.join('output', '20230105_yellow_taxi_kpis.json'), 'r')
        mock_load_data.assert_not_called()
        mock_compute_metrics.assert_not_called()
        mock_save_json.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.isfile')
    @patch('src.main.load_data')
    @patch('src.main.compute_metrics')
    @patch('src.main.save_json')
    def test_main_new_file(self, mock_save_json, mock_compute_metrics, mock_load_data, mock_isfile, mock_open):
        mock_isfile.return_value = False
        mock_load_data.return_value = "mocked_data"
        mock_compute_metrics.return_value = {"average_price_per_mile": 7.65, "payment_type_distribution": {"1": 77969, "2": 19189, "0": 2234, "4": 1100, "3": 571}, "custom_indicator": 2.89}
        test_args = ["main.py", "--date", "2023-01-05"]
        with patch('sys.argv', test_args):
            main()
        mock_open.assert_called_once_with(os.path.join('output', '20230105_yellow_taxi_kpis.json'), 'w')
        mock_load_data.assert_called_once_with(datetime(2023, 1, 5))
        mock_compute_metrics.assert_called_once_with("mocked_data")
        mock_save_json.assert_called_once_with({"average_price_per_mile": 7.65, "payment_type_distribution": {"1": 77969, "2": 19189, "0": 2234, "4": 1100, "3": 571}, "custom_indicator": 2.89}, 'output', '20230105_yellow_taxi_kpis.json')

if __name__ == '__main__':
    unittest.main()