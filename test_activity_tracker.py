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
        expected_log = {
            "test": {
                "activity": {
                    "time": 30,
                    "timestamp": datetime.now().isoformat()
                }
            }
        }
        mock_save.assert_called_once()
        saved_log = mock_save.call_args[0][0]
        self.assertEqual(saved_log["test"]["activity"]["time"], 30)
        self.assertIn("timestamp", saved_log["test"]["activity"])

    @patch('activity_tracker.load_activity_log', return_value={})
    @patch('activity_tracker.save_activity_log')
    def test_log_time(self, mock_save, mock_load):
        activity_tracker.log_time("test/activity", 15)
        expected_log = {
            "test": {
                "activity": {
                    "time": 15,
                    "timestamp": datetime.now().isoformat()
                }
            }
        }
        mock_save.assert_called_once()
        saved_log = mock_save.call_args[0][0]
        self.assertEqual(saved_log["test"]["activity"]["time"], 15)
        self.assertIn("timestamp", saved_log["test"]["activity"])

    @patch('activity_tracker.load_activity_log', return_value={
        "test": {
            "activity": {
                "time": 15,
                "timestamp": "2023-12-01T10:00:00"
            }
        }
    })
    def test_print_activities(self, mock_load):
        with patch('builtins.print') as mock_print:
            activity_tracker.print_activities()
            mock_print.assert_called_once()
            printed_log = json.dumps(mock_load.return_value, indent=4)
            mock_print.assert_called_with(printed_log)

if __name__ == '__main__':
    unittest.main()