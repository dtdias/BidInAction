import os
import tempfile
import unittest
from types import SimpleNamespace

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QLabel

from components.image_viewer import ImageViewer
from components.pdf_exporter import _format_brl, _parse_brl, export_bid_details_to_pdf


class MediaAndPdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(["test", "-platform", "offscreen"])

    def _pixmap(self):
        pixmap = QPixmap(640, 480)
        pixmap.fill(Qt.GlobalColor.blue)
        return pixmap

    def test_image_viewer_keeps_original_pixmap_and_resets_zoom(self):
        pixmap = self._pixmap()
        viewer = ImageViewer(pixmap, "Foto")
        try:
            viewer.view.setTransform(viewer.view.transform().scale(2, 2))
            viewer.view.zoom_100()
            self.assertEqual(viewer.view._item.pixmap().size(), pixmap.size())
            self.assertEqual(viewer.view.transform().m11(), 1.0)
        finally:
            viewer.close()

    def test_pdf_contains_vertical_photos_and_is_valid(self):
        description = QLabel("Descrição do lote")
        dialog = SimpleNamespace(
            data=SimpleNamespace(value="R$3.430,00", batch_number="0281.000003-9"),
            description=description,
            info_labels={"Número do lote:": "0281.000003-9"},
            photo_pixmaps=[self._pixmap(), self._pixmap()],
        )
        with tempfile.TemporaryDirectory() as directory:
            output = os.path.join(directory, "lote.pdf")
            export_bid_details_to_pdf(dialog, output, 0.05)
            with open(output, "rb") as file:
                self.assertEqual(file.read(5), b"%PDF-")
            self.assertGreater(os.path.getsize(output), 1_000)

    def test_brl_helpers_preserve_portuguese_currency_format(self):
        self.assertEqual(_parse_brl("R$3.430,00"), 3430.0)
        self.assertEqual(_format_brl(3430), "R$3.430,00")


if __name__ == "__main__":
    unittest.main()
