import logging
import os
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMessageBox
from views.search_window import SearchWindow
from utils.ui_theme import apply_theme
from utils.resources import resource_path

def main() -> int:
    app = QApplication(sys.argv)
    apply_theme(app)
    icon_path = resource_path("icon/caixa-logo.ico")
    app.setWindowIcon(QIcon(icon_path))

    window = SearchWindow()
    # Opcional, se quiser forçar na janela
    # window.setWindowIcon(QIcon(icon_path))
    window.show()
    return app.exec()


def report_startup_error(error: Exception) -> None:
    log_directory = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "LeilaoVitrineJoias"
    log_directory.mkdir(parents=True, exist_ok=True)
    log_path = log_directory / "startup-error.log"
    logging.basicConfig(filename=log_path, encoding="utf-8", level=logging.ERROR)
    logging.exception("Falha ao iniciar o aplicativo")
    app = QApplication.instance() or QApplication([])
    QMessageBox.critical(
        None,
        "Falha ao iniciar",
        f"O aplicativo não iniciou. Detalhes em:\n{log_path}\n\n{error}",
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        report_startup_error(error)
        raise
