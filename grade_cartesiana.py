from PyQt6.QtWidgets import QGraphicsItem
from PyQt6.QtGui import QPen, QColor, QPainter
from PyQt6.QtCore import QRectF, QLineF


class Grade(QGraphicsItem):
    def __init__(self, espacamento_pr: int = 10, espacamento_sec: int = 1):
        super().__init__()
        self.espacamento_pr = espacamento_pr
        self.espacamento_sec = espacamento_sec
        self._rect = QRectF(0, 0, 0, 0)  # boundingRect interno

        # Canetas
        self.caneta_secundaria = QPen(QColor(240, 200, 170), 1)  # bem clara
        self.caneta_secundaria.setCosmetic(True)

        self.caneta_principal = QPen(QColor(222, 142, 89), 1.5)  # cor tipo papel milimetrado
        self.caneta_principal.setCosmetic(True)

        self.caneta_eixo = QPen(QColor(202, 106, 40), 2)  # eixo em preto e mais grosso
        self.caneta_eixo.setCosmetic(True)

        self.setZValue(-100)
    
    def boundingRect(self) -> QRectF:
        return self._rect

    def atualizar_area(self, rect: QRectF):
        """Atualiza o boundingRect da grade"""
        self.prepareGeometryChange()
        self._rect = rect
    
    def paint(self, painter: QPainter, option, widget=None):
        """Desenha a grade na tela"""
        if not self.scene(): return
        retangulo = self.scene().sceneRect()

        # Escala atual da cena em pixels
        escala_x = abs(painter.transform().m11())
        escala_y = abs(painter.transform().m22())
        escala_media = (escala_x + escala_y) / 2.0

        # Limite em pixels para decidir quando mostrar a grade secundária
        # Exemplo: só mostra se 1 mm >= 3 pixels
        if escala_media >= 3:
            # Desenha grade secundária
            x = 0
            while x <= retangulo.right():
                if x != 0 and x % self.espacamento_pr != 0:
                    painter.setPen(self.caneta_secundaria)
                    painter.drawLine(QLineF(x, retangulo.top(), x, retangulo.bottom()))
                x += self.espacamento_sec
            
            x = -self.espacamento_sec
            while x >= retangulo.left():
                if x != 0 and x % self.espacamento_pr != 0:
                    painter.setPen(self.caneta_secundaria)
                    painter.drawLine(QLineF(x, retangulo.top(), x, retangulo.bottom()))
                x -= self.espacamento_sec

            y = 0
            while y <= retangulo.bottom():
                if y != 0 and y % self.espacamento_pr != 0:
                    painter.setPen(self.caneta_secundaria)
                    painter.drawLine(QLineF(retangulo.left(), y, retangulo.right(), y))
                y += self.espacamento_sec

            y = -self.espacamento_sec
            while y >= retangulo.top():
                if y != 0 and y % self.espacamento_pr != 0:
                    painter.setPen(self.caneta_secundaria)
                    painter.drawLine(QLineF(retangulo.left(), y, retangulo.right(), y))
                y -= self.espacamento_sec
        
        # Desenha a grade Primaria
        x = 0
        while x <= retangulo.right():
            if x != 0 and x % self.espacamento_pr == 0:
                painter.setPen(self.caneta_principal)
                painter.drawLine(QLineF(x, retangulo.top(), x, retangulo.bottom()))
            x += self.espacamento_pr
        
        x = -self.espacamento_pr
        while x >= retangulo.left():
            if x != 0 and x % self.espacamento_pr == 0:
                painter.setPen(self.caneta_principal)
                painter.drawLine(QLineF(x, retangulo.top(), x, retangulo.bottom()))
            x -= self.espacamento_pr

        y = 0
        while y <= retangulo.bottom():
            if y != 0 and y % self.espacamento_pr == 0:
                painter.setPen(self.caneta_principal)
                painter.drawLine(QLineF(retangulo.left(), y, retangulo.right(), y))
            y += self.espacamento_pr

        y = -self.espacamento_pr
        while y >= retangulo.top():
            if y != 0 and y % self.espacamento_pr == 0:
                painter.setPen(self.caneta_principal)
                painter.drawLine(QLineF(retangulo.left(), y, retangulo.right(), y))
            y -= self.espacamento_pr
    
        # Desenha os eixos 0
        painter.setPen(self.caneta_eixo)
        painter.drawLine(QLineF(0, retangulo.top(), 0, retangulo.bottom()))
        painter.drawLine(QLineF(retangulo.left(), 0, retangulo.right(), 0))
