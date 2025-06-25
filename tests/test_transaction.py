import unittest
from unittest.mock import patch, MagicMock
from finance_manager import tracker, auth, database, budget, report

#to test transactions crud functions 

class TestTransactions(unittest.TestCase):

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    @patch("finance_manager.tracker.get_total_expense_for_category", return_value=600)
    @patch("finance_manager.tracker.get_budget", return_value=1000)
    @patch("builtins.input", return_value="2025-06-24")
    def test_add_transaction_with_budget_warning(self, mock_input, mock_get_budget, mock_get_total, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        tracker.add_transaction(1, 500, "Expense", "Food")

        mock_print.assert_any_call("warning: This will exceed your budget!")
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_add_transaction_income(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        tracker.add_transaction(1, 1000, "Income", "Salary")

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_print.assert_called_with("\nIncome of ₹1000 added successfully under category 'Salary'.")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_view_transactions_with_data(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "type": "Income", "amount": 5000, "category": "Salary", "date": "2025-06-01"}
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.view_transactions(1)

        mock_print.assert_any_call("\n--- Transaction History ---")
        mock_print.assert_any_call("ID: 1 | Income | ₹5000 | Salary | 2025-06-01")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_view_transactions_empty(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.view_transactions(1)
        mock_print.assert_called_with("\nNo Transactions found!!")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_update_transaction_success(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.update_transactions(1, 1, 1000, "Expense", "Groceries")

        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_with("Transaction updated successfully.")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_update_transaction_not_found(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.update_transactions(1, 1, 1000, "Expense", "Groceries")

        mock_print.assert_called_with("Transaction not found or not authorized.")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_delete_transaction_success(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 1
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.delete_transactions(1, 1)

        mock_cursor.execute.assert_called_once()
        mock_print.assert_called_with("Transaction deleted successfully.")

    @patch("finance_manager.tracker.get_db_connection")
    @patch("finance_manager.tracker.print")
    def test_delete_transaction_not_found(self, mock_print, mock_get_conn):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        tracker.delete_transactions(1, 1)

        mock_print.assert_called_with("Transaction not found or not authorized.")


#test code to test budget limit function

class TestBudget(unittest.TestCase):
    @patch('finance_manager.budget.database.set_budget')
    @patch('builtins.input', side_effect=['Food', '2025-06', '2500'])
    def test_set_budget(self, mock_input, mock_set_budget):
        budget.set_budget(user_id=1)
        mock_set_budget.assert_called_once_with(1, 'food', '2025-06', 2500.0)

    @patch('finance_manager.budget.database.get_total_expense_for_category', return_value=1200.0)
    @patch('finance_manager.budget.database.get_budget', return_value=2000.0)
    @patch('builtins.input', side_effect=['Food', '2025-06'])
    def test_view_budget_with_existing_budget(self, mock_input, mock_get_budget, mock_get_expense):
        with patch('builtins.print') as mock_print:
            budget.view_budget(user_id=1)
            mock_get_budget.assert_called_once_with(1, 'Food', '2025-06')
            mock_get_expense.assert_called_once_with(1, 'Food', '2025-06')
            mock_print.assert_any_call("Budget : 2000.00")
            mock_print.assert_any_call("Spent : 1200.00")
            mock_print.assert_any_call("Remaining : 800.00")

    @patch('finance_manager.budget.database.get_total_expense_for_category', return_value=0.0)
    @patch('finance_manager.budget.database.get_budget', return_value=None)
    @patch('builtins.input', side_effect=['Food', '2025-06'])
    def test_view_budget_without_existing_budget(self, mock_input, mock_get_budget, mock_get_expense):
        with patch('builtins.print') as mock_print:
            budget.view_budget(user_id=1)
            mock_print.assert_any_call("No budget set for this category/month.")

    @patch('finance_manager.budget.database.delete_budget')
    @patch('builtins.input', side_effect=['Food', '2025-06', '2500'])
    def test_delete_budget(self, mock_input, mock_delete_budget):
        budget.delete_budget(user_id=1)
        mock_delete_budget.assert_called_once_with(1, 'food', '2025-06', 2500.0)


#test code to test report generation function

class TestReport(unittest.TestCase):

    @patch('finance_manager.report.fetch_transactions')
    @patch('builtins.print')
    def test_generate_report_all_time(self, mock_print, mock_fetch):
        mock_fetch.return_value = [
            ('2025-01-01', 'Salary', 5000.0, 'income'),
            ('2025-01-10', 'Groceries', 1200.0, 'expense'),
        ]

        report.generate_report(user_id=1)

        mock_fetch.assert_called_once_with(1, None, None)
        mock_print.assert_any_call("Total Income : 5000.00")
        mock_print.assert_any_call("Total Expense : 1200.00")
        mock_print.assert_any_call("Total Savings : 3800.00")

    @patch('finance_manager.report.fetch_transactions')
    @patch('builtins.print')
    def test_generate_report_year_only(self, mock_print, mock_fetch):
        mock_fetch.return_value = []

        report.generate_report(user_id=1, year=2024)

        mock_fetch.assert_called_once_with(1, '2024-01-01', '2024-12-31')
        mock_print.assert_any_call("For year: 2024")

    @patch('finance_manager.report.fetch_transactions')
    @patch('builtins.print')
    def test_generate_report_year_and_month(self, mock_print, mock_fetch):
        mock_fetch.return_value = [
            ('2024-06-05', 'Freelance', 2000.0, 'income'),
            ('2024-06-10', 'Transport', 300.0, 'expense'),
        ]

        report.generate_report(user_id=2, year=2024, month=6)

        mock_fetch.assert_called_once_with(2, '2024-06-01', '2024-06-31')
        mock_print.assert_any_call("For: 2024-06")
        mock_print.assert_any_call("Total Income : 2000.00")
        mock_print.assert_any_call("Total Expense : 300.00")
        mock_print.assert_any_call("Total Savings : 1700.00")


if __name__ == '__main__':
    unittest.main()
