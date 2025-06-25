import unittest
from unittest.mock import patch,mock_open, MagicMock
import sqlite3
import os
from finance_manager import auth, database, backup


#to test authentication function

class TestUserAuth(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_init_db_creates_users_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        auth.init_db()

        mock_cursor.execute.assert_called_once()
        self.assertIn("CREATE TABLE IF NOT EXISTS users", mock_cursor.execute.call_args[0][0])

    @patch('builtins.input', return_value='testuser')
    @patch('getpass.getpass', return_value='testpass')
    @patch('sqlite3.connect')
    def test_register_success(self, mock_connect, mock_getpass, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        with patch('builtins.print') as mock_print:
            auth.register()
            args, _ = mock_cursor.execute.call_args
            self.assertIn("INSERT INTO users", args[0])
            self.assertEqual(args[1], ('testuser', 'testpass'))
            mock_print.assert_called_with("User registered successfully!")

    @patch('builtins.input', return_value='existinguser')
    @patch('getpass.getpass', return_value='pass123')
    @patch('sqlite3.connect')
    def test_register_username_exists(self, mock_connect, mock_getpass, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: users.username")

        with patch('builtins.print') as mock_print:
            auth.register()
            mock_print.assert_called_with("Username already exists. Try another.")

    @patch('builtins.input', return_value='testuser')
    @patch('getpass.getpass', return_value='testpass')
    @patch('sqlite3.connect')
    def test_login_success(self, mock_connect, mock_getpass, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 'testuser', 'testpass')
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        with patch('builtins.print') as mock_print:
            user_id = auth.login()
            self.assertEqual(user_id, 1)
            mock_print.assert_called_with("Welcome testuser!")

    @patch('builtins.input', return_value='wronguser')
    @patch('getpass.getpass', return_value='wrongpass')
    @patch('sqlite3.connect')
    def test_login_failure(self, mock_connect, mock_getpass, mock_input):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value.__enter__.return_value = mock_conn

        with patch('builtins.print') as mock_print:
            user_id = auth.login()
            self.assertFalse(user_id)
            mock_print.assert_called_with("Invalid credentials.")


#to test database functions

class TestDatabaseFunctions(unittest.TestCase):

    @patch("finance_manager.database.sqlite3.connect")
    def test_create_transactions_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        database.create_transactions_table()

        mock_cursor.execute.assert_called_once()
        self.assertIn("CREATE TABLE IF NOT EXISTS transactions", mock_cursor.execute.call_args[0][0])
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("finance_manager.database.sqlite3.connect")
    def test_fetch_transactions_with_dates(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("2025-01-01", "Food", 200.0, "Expense")]
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = database.fetch_transactions(1, "2025-01-01", "2025-01-31")

        mock_cursor.execute.assert_called()
        self.assertEqual(result, [("2025-01-01", "Food", 200.0, "Expense")])
        mock_conn.close.assert_called_once()

    @patch("finance_manager.database.sqlite3.connect")
    def test_create_budget_table(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        database.create_budget_table()

        mock_cursor.execute.assert_called_once()
        self.assertIn("CREATE TABLE IF NOT EXISTS budgets", mock_cursor.execute.call_args[0][0])
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("finance_manager.database.sqlite3.connect")
    def test_set_budget_insert_update(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        database.set_budget(1, "food", "2025-06", 1000.0)

        mock_cursor.execute.assert_called_once()
        self.assertIn("ON CONFLICT", mock_cursor.execute.call_args[0][0])
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("finance_manager.database.sqlite3.connect")
    def test_get_budget_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1500.0]
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = database.get_budget(1, "food", "2025-06")

        self.assertEqual(result, 1500.0)

    @patch("finance_manager.database.sqlite3.connect")
    def test_get_budget_not_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = database.get_budget(1, "food", "2025-06")

        self.assertIsNone(result)

    @patch("finance_manager.database.sqlite3.connect")
    def test_get_total_expense_for_category_found(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [1200.0]
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = database.get_total_expense_for_category(1, "food", "2025-06")

        self.assertEqual(result, 1200.0)

    @patch("finance_manager.database.sqlite3.connect")
    def test_get_total_expense_for_category_none(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = [None]
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        result = database.get_total_expense_for_category(1, "food", "2025-06")

        self.assertEqual(result, 0)

    @patch("finance_manager.database.sqlite3.connect")
    def test_delete_budget(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        database.delete_budget(1, "food", "2025-06", 1000.0)

        mock_cursor.execute.assert_called_once()
        self.assertIn("DELETE FROM budgets", mock_cursor.execute.call_args[0][0])
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()


#to test backup restore functions

class TestBackupRestore(unittest.TestCase):

    @patch("finance_manager.backup.shutil.copyfile")
    @patch("finance_manager.backup.os.makedirs")
    @patch("finance_manager.backup.os.path.exists", side_effect=[False])  # No backup folder
    @patch("finance_manager.backup.datetime")
    def test_auto_backup_creates_backup_folder_and_file(self, mock_datetime, mock_exists, mock_makedirs, mock_copyfile):
        mock_datetime.now.return_value.strftime.return_value = "20250624_120000"
        
        with patch("builtins.print") as mock_print:
            backup.auto_backup()
            mock_makedirs.assert_called_once_with("backup")
            mock_copyfile.assert_called_once_with("finance_manager.db", "backup/backup_20250624_120000.db")
            mock_print.assert_called_with("Backup saved as backup_20250624_120000.db")

    @patch("finance_manager.backup.shutil.copyfile")
    @patch("finance_manager.backup.os.path.exists", side_effect=[True])  # DB already exists
    def test_auto_restore_skips_if_db_exists(self, mock_exists, mock_copyfile):
        backup.auto_restore()
        mock_copyfile.assert_not_called()

    @patch("finance_manager.backup.shutil.copyfile")
    @patch("finance_manager.backup.os.listdir", return_value=[])
    @patch("finance_manager.backup.os.path.exists", side_effect=[False, True])  # DB not exists, folder exists
    def test_auto_restore_no_backup_files(self, mock_exists, mock_listdir, mock_copyfile):
        with patch("builtins.print") as mock_print:
            backup.auto_restore()
            mock_print.assert_called_with("!! No backup files found.")
            mock_copyfile.assert_not_called()

    @patch("finance_manager.backup.shutil.copyfile")
    @patch("finance_manager.backup.os.listdir", return_value=["backup_20250623_235959.db", "backup_20250624_000000.db"])
    @patch("finance_manager.backup.os.path.exists", side_effect=[False, True])  # DB not exists, folder exists
    def test_auto_restore_restores_latest_backup(self, mock_exists, mock_listdir, mock_copyfile):
        with patch("builtins.print") as mock_print:
            backup.auto_restore()
            mock_copyfile.assert_called_once_with("backup/backup_20250624_000000.db", "finance_manager.db")
            mock_print.assert_called_with("Restored DB from backup_20250624_000000.db")

    @patch("finance_manager.backup.os.path.exists", side_effect=[False, False])  # DB not exists, folder doesn't exist
    def test_auto_restore_no_folder(self, mock_exists):
        with patch("builtins.print") as mock_print:
            backup.auto_restore()
            mock_print.assert_called_with("!! No backup folder found.")


if __name__ == '__main__':
    unittest.main()

