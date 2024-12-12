import unittest
from unittest.mock import patch, mock_open
import activity_tracker
from datetime import datetime
import os

class TestActivityTracker(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_load_activity_log(self, mock_file):
        expected_log = {}
        log = activity_tracker.load_activity_log()
        self.assertEqual(log, expected_log)
        mock_file.assert_called_with(os.path.expanduser('~/Documents/activity_log.json'), 'r')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_activity_log(self, mock_file):
        log = {"test": "data"}
        activity_tracker.save_activity_log(log)
        mock_file.assert_called_with(os.path.expanduser('~/Documents/activity_log.json'), 'w')
        handle = mock_file()
        handle.write.assert_has_calls([
            unittest.mock.call('{'),
            unittest.mock.call('\n    '),
            unittest.mock.call('"test"'),
            unittest.mock.call(': '),
            unittest.mock.call('"data"'),
            unittest.mock.call('\n'),
            unittest.mock.call('}')
        ])

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

    @patch('activity_tracker.save_activity_log')
    def test_delete_entry(self, mock_save):
        log = {
            "test": {
                "time": 0,
                "timestamp": "",
                "subactivity": {
                    "time": 15,
                    "timestamp": ""
                }
            },
            "test/subactivity": {
                "time": 15,
                "timestamp": ""
            }
        }
        expected_log = {}

        activity_tracker.delete_entry(log, "test")
        
        self.assertEqual(log, expected_log)
        mock_save.assert_called_once()

    @patch('activity_tracker.load_activity_log', return_value={'test': {'subactivity': {'time': 15, 'timestamp': ''}}})
    @patch('activity_tracker.save_activity_log')
    def test_delete_entry(self, mock_save_activity_log, mock_load_activity_log):
        log = mock_load_activity_log.return_value
        activity_tracker.delete_entry(log, 'test/subactivity')
        expected_log = {'test': {}}
        self.assertEqual(log, expected_log)
        mock_save_activity_log.assert_called_once_with(expected_log)

    @patch('activity_tracker.load_activity_log')
    @patch('builtins.print')
    @patch('builtins.input', return_value="test")
    @patch('activity_tracker.save_activity_log')
    def test_prompt_delete_entry(self, mock_save, mock_input, mock_print, mock_load_activity_log):
        mock_load_activity_log.return_value = {
            "test": {
                "time": 0,
                "timestamp": "",
                "subactivity": {
                    "time": 15,
                    "timestamp": ""
                }
            },
            "test/subactivity": {
                "time": 15,
                "timestamp": ""
            }
        }
        expected_log = {}

        activity_tracker.prompt_delete_entry()
        
        self.assertEqual(mock_load_activity_log.return_value, expected_log)
        mock_save.assert_called_once()
        mock_print.assert_any_call("Deleted entry 'test' and its subentries.")

    @patch('activity_tracker.load_activity_log', return_value={'test': {'subactivity': {'time': 15, 'timestamp': ''}}})
    @patch('activity_tracker.save_activity_log')
    @patch('builtins.input', return_value='test/subactivity')
    def test_prompt_delete_entry(self, mock_input, mock_save_activity_log, mock_load_activity_log):
        activity_tracker.prompt_delete_entry()
        expected_log = {'test': {}}
        self.assertEqual(mock_load_activity_log.return_value, expected_log)
        mock_save_activity_log.assert_called_once_with(expected_log)

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