import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtWidgets import QApplication, QLabel

from views.search_window import SearchWindow


class SearchWindowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(["test", "-platform", "offscreen"])

    def test_initial_calendar_selection_starts_schedule_request(self):
        with patch.object(QThreadPool, "start") as start:
            window = SearchWindow()
            try:
                self.assertEqual(window.year_input.currentIndex(), 0)
                self.assertEqual(window.month_input.currentIndex(), 0)
                self.assertIsNotNone(window.year_input.currentData())
                self.assertIsNotNone(window.month_input.currentData())
                self.assertTrue(window.year_input.isEnabled())
                self.assertTrue(window.month_input.isEnabled())
                start.assert_called_once()
            finally:
                window.close()

    def test_dropdowns_limit_visible_items_and_enable_scrolling(self):
        with patch.object(QThreadPool, "start"):
            window = SearchWindow()
            try:
                self.assertEqual(window.year_input.maxVisibleItems(), 8)
                self.assertEqual(
                    window.year_input.view().verticalScrollBarPolicy(),
                    Qt.ScrollBarPolicy.ScrollBarAsNeeded,
                )
            finally:
                window.close()

    def test_banner_image_is_loaded(self):
        with patch.object(QThreadPool, "start"):
            window = SearchWindow()
            try:
                banner = window.findChild(QLabel, "brandLogo")
                self.assertIsNotNone(banner)
                self.assertIsNotNone(banner.pixmap())
                self.assertFalse(banner.pixmap().isNull())
            finally:
                window.close()


if __name__ == "__main__":
    unittest.main()
