from pathlib import Path


def resource_path(rel_path: str) -> str:
    """Resolve recursos a partir do bundle Nuitka ou da raiz do projeto."""
    return str(Path(__file__).resolve().parent.parent / rel_path)
