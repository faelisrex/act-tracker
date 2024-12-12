import unittest
from unittest.mock import patch, mock_open
import json
import activity_tracker
from datetime import datetime

class TestActivityTracker(unittest.TestCase):

    @patch('activity_tracker.open', new_callable=mock_open, read_data='{}')
    def test_load_activity_log(self, mock_file):
        log = activity_tracker.load_activity_log()
        self.assertEqual(log, {})
        mock_file.assert_called_with('activity_log.json', 'r')

    @patch('activity_tracker.open', new_callable=mock_open)
    def test_save_activity_log(self, mock_file):
        log = {"test": {"time": 10, "timestamp": "2023-12-01T10:00:00"}}
        activity_tracker.save_activity_log(log)
        mock_file.assert_called_with('activity_log.json', 'w')
        
        # Combine all write calls into a single string
        written_data = ''.join(call.args[0] for call in mock_file().write.mock_calls)
        self.assertEqual(written_data, json.dumps(log, indent=4))

    @patch('activity_tracker.load_activity_log', return_value={})
    @patch('activity_tracker.save_activity_log')
    def test_add_time(self, mock_save, mock_load):
        activity_tracker.add_time("test/activity", 30)
        mock_save.assert_called_once()
        log = mock_load.return_value
        self.assertEqual(log["test"]["activity"]["time"], 30)

    @patch('activity_tracker.load_activity_log', return_value={})
    @patch('activity_tracker.save_activity_log')
    def test_add_time_ripples_upwards(self, mock_save, mock_load):
        log = {}
        mock_load.return_value = log
        
        activity_tracker.add_time("linux/unixhndbk/chapter-1", 50)
        
        expected_log = {
            "linux": {
                "time": 50,
                "unixhndbk": {
                    "time": 50,
                    "chapter-1": {
                        "time": 50
                    }
                }
            }
        }
        
        self.assertEqual(log, expected_log)
        mock_save.assert_called_once()

    @patch('activity_tracker.load_activity_log')
    @patch('builtins.print')
    def test_print_activities(self, mock_print, mock_load_activity_log):
        mock_load_activity_log.return_value = {
            "test": {
                "time": 0,
                "timestamp": "",
                "activity": {
                    "time": 15,
                    "timestamp": ""
                }
            }
        }
        
        activity_tracker.print_activities()
        
        expected_calls = [
            unittest.mock.call('test (0 minutes)'),
            unittest.mock.call('    activity (15 minutes)')
        ]
        mock_print.assert_has_calls(expected_calls, any_order=False)

if __name__ == '__main__':
    unittest.main()