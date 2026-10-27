from PySide6.QtCore import QMarginsF, QRect, Qt
from PySide6.QtGui import QColor, QFont, QPageLayout, QPageSize, QPainter, QPdfWriter, QPixmap


CAIXA_BLUE = QColor("#005ca9")
TEXT = QColor("#1d3557")


def export_bid_details_to_pdf(dialog, file_path: str, percent_multiplier: float):
    """Exporta relatório do lote com fotos originais em fluxo vertical paginado."""
    writer = QPdfWriter(file_path)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setResolution(180)
    writer.setPageLayout(
        QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(16, 16, 16, 16),
            QPageLayout.Unit.Millimeter,
        )
    )
    painter = QPainter(writer)
    page = writer.pageLayout().paintRectPixels(writer.resolution())
    width, height = page.width(), page.height()
    x, y = 0, 0
    page_number = 0

    def header():
        nonlocal y, page_number
        page_number += 1
        painter.fillRect(QRect(0, 0, width, 58), CAIXA_BLUE)
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        painter.drawText(QRect(20, 0, width - 40, 34), Qt.AlignmentFlag.AlignVCenter, "Leilão Vitrine de Joias")
        painter.setFont(QFont("Arial", 9))
        painter.drawText(
            QRect(20, 30, width - 40, 22),
            Qt.AlignmentFlag.AlignVCenter,
            f"Lote {dialog.data.batch_number}  |  Página {page_number}",
        )
        painter.setPen(TEXT)
        y = 78

    def new_page():
        writer.newPage()
        header()

    def ensure(space: int):
        nonlocal y
        if y + space > height:
            new_page()

    def draw_heading(text: str):
        nonlocal y
        ensure(38)
        painter.setPen(CAIXA_BLUE)
        painter.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        painter.drawText(QRect(x, y, width, 30), Qt.AlignmentFlag.AlignVCenter, text)
        painter.setPen(TEXT)
        y += 36

    def draw_wrapped(text: str, font: QFont, leading: int = 5):
        nonlocal y
        painter.setFont(font)
        metrics = painter.fontMetrics()
        words = str(text or "N/A").split()
        line = ""
        line_height = metrics.height() + leading
        for word in words:
            candidate = f"{line} {word}".strip()
            if not line or metrics.horizontalAdvance(candidate) <= width:
                line = candidate
                continue
            ensure(line_height)
            painter.drawText(QRect(x, y, width, line_height), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, line)
            y += line_height
            line = word
        if line:
            ensure(line_height)
            painter.drawText(QRect(x, y, width, line_height), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, line)
            y += line_height

    header()
    value = _parse_brl(dialog.data.value)
    extra = value * percent_multiplier
    draw_heading("Resumo financeiro")
    painter.setFont(QFont("Arial", 14, QFont.Weight.Bold))
    ensure(30)
    painter.drawText(QRect(x, y, width, 28), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, f"Lance mínimo: {_format_brl(value)}")
    y += 32
    if percent_multiplier:
        draw_wrapped(f"Acréscimo ({percent_multiplier * 100:.2f}%): {_format_brl(extra)}", QFont("Arial", 10))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        ensure(28)
        painter.drawText(QRect(x, y, width, 28), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, f"Total: {_format_brl(value + extra)}")
        y += 34

    draw_heading("Descrição")
    draw_wrapped(dialog.description.text(), QFont("Arial", 10))
    y += 12
    draw_heading("Informações do lote")
    for key, value in dialog.info_labels.items():
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        draw_wrapped(f"{key} {value or 'N/A'}", painter.font())
        y += 4

    photos = [pixmap for pixmap in getattr(dialog, "photo_pixmaps", []) if not pixmap.isNull()]
    draw_heading("Fotos do lote")
    if photos:
        for index, pixmap in enumerate(photos, 1):
            painter.setFont(QFont("Arial", 9, QFont.Weight.DemiBold))
            label_height = 20
            max_photo_height = int(height * 0.62)
            scaled = pixmap.scaled(
                width,
                max_photo_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            ensure(label_height + scaled.height() + 22)
            painter.drawText(
                QRect(x, y, width, label_height),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                f"Foto {index} de {len(photos)}",
            )
            y += label_height
            painter.drawPixmap(x + (width - scaled.width()) // 2, y, scaled)
            y += scaled.height() + 22
    else:
        draw_wrapped("Imagem indisponível.", QFont("Arial", 10))
    painter.end()


def _parse_brl(value) -> float:
    try:
        return float(str(value).replace("R$", "").replace(".", "").replace(",", ".").strip())
    except ValueError:
        return 0.0


def _format_brl(value: float) -> str:
    return f"R${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
