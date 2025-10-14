# utils/resources.py
import os, sys

def resource_path(rel_path: str) -> str:
    # Quando empacotado, PyInstaller extrai os dados para sys._MEIPASS
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        # Em dev, use a pasta do executável/script principal
        base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, rel_path)