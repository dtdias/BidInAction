# pdf_exporter.py
from PySide6.QtCore import Qt, QSize, QRect, QMarginsF
from PySide6.QtGui import QFont, QPageSize, QPageLayout, QPainter, QPixmap
from PySide6.QtGui import QPdfWriter

def export_bid_details_to_pdf(dialog, file_path: str, percent_multiplier):
    """
    Gera um PDF a partir do conteúdo já renderizado no diálogo BidDetails.
    
    Args:
        dialog: Diálogo com os dados do lote
        file_path: Caminho onde o PDF será salvo
        percent_multiplier: Porcentagem a ser aplicada sobre o valor (ex: 0.05 para 5%)
    """    
    writer = QPdfWriter(file_path)
    writer.setPageSize(QPageSize(QPageSize.A4))
    writer.setResolution(300)  # Define resolução para 300 DPI (padrão para PDFs)
    
    # Margens em milímetros
    page_layout = QPageLayout(
        QPageSize(QPageSize.A4), 
        QPageLayout.Portrait, 
        QMarginsF(20, 20, 20, 20),
        QPageLayout.Millimeter
    )
    writer.setPageLayout(page_layout)

    painter = QPainter(writer)
    
    # Obter dimensões da página em pixels (considerando a resolução)
    page_rect = writer.pageLayout().paintRectPixels(writer.resolution())
    page_width = page_rect.width()
    page_height = page_rect.height()
    
    # Posição inicial e margens
    x = 0
    y = 0
    margin = 40  # Margem entre elementos
    
    # Título
    title_font = QFont("Arial", 24, QFont.Weight.Bold)
    painter.setFont(title_font)
    title_height = 80
    painter.drawText(
        QRect(x, y, page_width, title_height), 
        Qt.AlignLeft | Qt.AlignVCenter, 
        "Detalhes do Lote"
    )
    y += title_height + margin

    def pixmap_from_label(lbl) -> QPixmap | None:
        pm = lbl.pixmap()
        return pm if pm and not pm.isNull() else None

    # Layout de imagens: principal à esquerda, thumbnails à direita
    images_start_y = y
    
    # Imagem principal (ocupa 60% da largura)
    main_img_width = int(page_width * 0.55)
    main_img_height = int(main_img_width * 0.75)  # Proporção 4:3
    
    main_pm = pixmap_from_label(dialog.main_image)
    if main_pm:
        scaled = main_pm.scaled(
            main_img_width, 
            main_img_height, 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        painter.drawPixmap(x, y, scaled)
        img_bottom = y + scaled.height()
    else:
        painter.drawRect(QRect(x, y, main_img_width, main_img_height))
        painter.setFont(QFont("Arial", 14))
        painter.drawText(
            QRect(x, y, main_img_width, main_img_height),
            Qt.AlignCenter,
            "Imagem principal\nindisponível",
        )
        img_bottom = y + main_img_height

    # Thumbnails ao lado direito
    thumb_x = main_img_width + margin
    thumb_y = images_start_y
    thumb_size = 750  # Tamanho fixo para thumbnails
    
    painter.setFont(QFont("Arial", 12))
    for lbl in getattr(dialog, "thumb_labels", []):
        pm = pixmap_from_label(lbl)
        if pm:
            scaled = pm.scaled(
                thumb_size, 
                thumb_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            painter.drawPixmap(thumb_x, thumb_y, scaled)
            thumb_y += scaled.height() + 20
        else:
            painter.drawRect(QRect(thumb_x, thumb_y, thumb_size, thumb_size))
            painter.drawText(
                QRect(thumb_x, thumb_y, thumb_size, thumb_size),
                Qt.AlignCenter,
                "Miniatura\nindisponível",
            )
            thumb_y += thumb_size + 20

    # Avança y para depois das imagens
    y = max(img_bottom, thumb_y) + margin

    # Cálculo de valores com porcentagem
    # Extrai o valor numérico (remove "R$" e converte vírgula para ponto)
    value_str = dialog.data.value.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        base_value = float(value_str)
    except ValueError:
        base_value = 0.0
    
    extra_value = base_value * percent_multiplier
    total_value = base_value + extra_value
    
    # Função para formatar valor em Real brasileiro
    def format_brl(value):
        return f"R${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    # Preço (agora depois das imagens)
    price_font = QFont("Arial", 18, QFont.Weight.Bold)
    painter.setFont(price_font)
    price_height = 60
    value_spacing = 20  # Espaçamento entre as linhas de valores
    
    # Linha 1: Lance mínimo
    painter.drawText(
        QRect(x, y, page_width, price_height),
        Qt.AlignLeft | Qt.AlignVCenter,
        f"Valor do lance mínimo: {format_brl(base_value)}",
    )
    y += price_height + value_spacing  # Adiciona espaçamento de 20
    
    # Linha 2: Adicional (se houver porcentagem)
    if percent_multiplier > 0:
        painter.setFont(QFont("Arial", 14))
        painter.drawText(
            QRect(x, y, page_width, price_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Adicional ({percent_multiplier * 100:.1f}%): {format_brl(extra_value)}",
        )
        y += price_height + value_spacing  # Adiciona espaçamento de 20
        
        # Linha 3: Total
        painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        painter.drawText(
            QRect(x, y, page_width, price_height),
            Qt.AlignLeft | Qt.AlignVCenter,
            f"Valor Total: {format_brl(total_value)}",
        )
        y += price_height + value_spacing  # Adiciona espaçamento de 20
    
    y += margin

    # Descrição
    desc_title_font = QFont("Arial", 16, QFont.Weight.Bold)
    painter.setFont(desc_title_font)
    desc_title_height = 100
    painter.drawText(
        QRect(x, y, page_width, desc_title_height), 
        Qt.AlignLeft | Qt.AlignVCenter, 
        "Descrição:"
    )
    y += desc_title_height + 10

    painter.setFont(QFont("Arial", 12))
    desc = dialog.description.text() if getattr(dialog, "description", None) is not None else ""
    y = _draw_text_block(
        painter, 
        desc, 
        x, 
        y, 
        page_width, 
        page_height, 
        line_height=50,
        writer=writer,
        leading=15
    )

    y += margin

    # Informações
    info_title_font = QFont("Arial", 16, QFont.Weight.Bold)
    painter.setFont(info_title_font)
    info_title_height = 80
    painter.drawText(
        QRect(x, y, page_width, info_title_height), 
        Qt.AlignLeft | Qt.AlignVCenter, 
        "Informações:"
    )
    y += info_title_height + 10

    # Lista de informações com quebra de linha para valores longos
    info_font = QFont("Arial", 12)
    painter.setFont(info_font)
    
    # Altura de linha consistente para chave e valor
    info_line_height = 50
    
    for key, value in dialog.info_labels.items():
        # Verifica se precisa de nova página antes de desenhar
        if y + info_line_height > page_height:
            writer.newPage()
            y = 0
        
        # Desenha chave em negrito
        key_font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(key_font)
        metrics = painter.fontMetrics()
        key_width = metrics.horizontalAdvance(key + " ")
        
        # Desenha a chave com altura adequada e alinhamento vertical centralizado
        painter.drawText(
            QRect(x, y, key_width, info_line_height),  # Mesma altura que o valor
            Qt.AlignLeft | Qt.AlignVCenter,  # Centralizado verticalmente
            key
        )
        
        # Desenha valor com quebra de linha se necessário
        painter.setFont(QFont("Arial", 12))
        value_text = value or "N/A"
        
        # Usa _draw_info_value para quebrar linhas longas
        y = _draw_info_value(
            painter,
            value_text,
            x + key_width,
            y,
            page_width - key_width,
            page_height,
            line_height=info_line_height,
            writer=writer,
            leading=6
        )
        
        y += 30  # Espaço entre itens

    painter.end()


def _draw_text_block(painter: QPainter, text: str, x: int, y: int, 
                     max_width: int, page_height: int, line_height: int, 
                     writer: QPdfWriter, leading: int = 0) -> int:
    """
    Desenha um bloco de texto com quebra de linha automática.
    Retorna a posição Y após o texto.
    """
    if not text:
        return y
    
    words = text.split()
    if not words:
        return y

    metrics = painter.fontMetrics()
    line = ""
    
    for word in words:
        test_line = (line + " " + word).strip() if line else word
        
        if metrics.horizontalAdvance(test_line) <= max_width:
            line = test_line
        else:
            # Desenha a linha atual
            if line:
                if y + line_height > page_height:
                    writer.newPage()
                    y = 0
                painter.drawText(
                    QRect(x, y, max_width, line_height), 
                    Qt.AlignLeft | Qt.AlignVCenter,  # Centralizado verticalmente
                    line
                )
                y += line_height + leading
            line = word
    
    # Desenha a última linha
    if line:
        if y + line_height > page_height:
            writer.newPage()
            y = 0
        painter.drawText(
            QRect(x, y, max_width, line_height), 
            Qt.AlignLeft | Qt.AlignVCenter,  # Centralizado verticalmente
            line
        )
        y += line_height + leading

    return y


def _draw_info_value(painter: QPainter, text: str, x: int, y: int,
                     max_width: int, page_height: int, line_height: int,
                     writer: QPdfWriter, leading: int = 0) -> int:
    """
    Desenha o valor de uma informação com quebra de linha se necessário.
    Retorna a posição Y após o texto.
    """
    if not text:
        painter.drawText(QRect(x, y, max_width, line_height), Qt.AlignLeft | Qt.AlignVCenter, "N/A")
        return y + line_height + leading
    
    metrics = painter.fontMetrics()
    words = text.split()
    line = ""
    
    for word in words:
        test_line = (line + " " + word).strip() if line else word
        
        if metrics.horizontalAdvance(test_line) <= max_width:
            line = test_line
        else:
            # Desenha a linha atual
            if line:
                if y + line_height > page_height:
                    writer.newPage()
                    y = 0
                    x = 0  # Reset x na nova página
                painter.drawText(
                    QRect(x, y, max_width, line_height),
                    Qt.AlignLeft | Qt.AlignVCenter,  # Centralizado verticalmente
                    line
                )
                y += line_height + leading
            line = word
    
    # Desenha a última linha
    if line:
        if y + line_height > page_height:
            writer.newPage()
            y = 0
            x = 0
        painter.drawText(
            QRect(x, y, max_width, line_height),
            Qt.AlignLeft | Qt.AlignVCenter,  # Centralizado verticalmente
            line
        )
        y += line_height + leading
    
    return y