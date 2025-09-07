from PyQt6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtGui import QColor, QBrush, QPen, QCursor, QPolygonF, QTransform, QPainter
from PyQt6.QtCore import Qt, QPoint, QPointF, QRectF

from secao_path import Pontos, SecaoParametricaDesenho
from grade_cartesiana import Grade

class Olho(QGraphicsView):
    """É o olho que vê o canvas"""
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setMouseTracking(True)
        self.coordenadas = None

        # Variáveis para zoom
        self.scale(5, -5)  # Altera o eixo y positivo para cima
        self.zoom_atual = 1.0
        self.zoom_factor = 1.1
        self.zoom_steps = 0
        self.zoom_step_limit = 8

        # Variáveis para pan
        self._pan = False
        self.ult_pos_mouse = QPoint()
    
    def conectar_label_coordenadas(self, label: QLabel):
        """Conecta o view à label de coordenadas"""
        self.coordenadas = label
    
    # Eventos sobrescritos =================================================================================================================
    # Funções de pan
    def mousePressEvent(self, event):
        """Funções do mouse"""
        if event.button() == Qt.MouseButton.MiddleButton:
            # Ativar Pan
            self._pan = True
            self.ult_pos_mouse = event.position().toPoint()
            self.setCursor(QCursor(Qt.CursorShape.SizeAllCursor))
        return super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._pan:
            delta = event.position().toPoint() - self.ult_pos_mouse
            self.ult_pos_mouse = event.position().toPoint()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
        
        # Mostrar coordenadas do mouse
        pos_view = event.position()
        pos_scene: QPointF = self.mapToScene(int(pos_view.x()), int(pos_view.y()))
        texto = f"({pos_scene.x():.0f}, {pos_scene.y():.0f}) mm"
        if self.coordenadas:
            self.coordenadas.setText(texto)

        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Desativar pan"""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._pan = False
            self.unsetCursor()
        return super().mouseReleaseEvent(event)
    
    # Função de zoom
    def wheelEvent(self, event):
        """Função personalisada de zoom na tela"""
        mouse_scene_pos = self.mapToScene(event.position().toPoint())
        if event.angleDelta().y() > 0:  # Zoom in
            if self.zoom_steps < self.zoom_step_limit:
                fator = self.zoom_factor
                self.zoom_steps += 1
            else:
                return
        else:  # Zoom out
            if self.zoom_steps > -self.zoom_step_limit:
                fator = 1 / self.zoom_factor
                self.zoom_steps -= 1
            else:
                return
        self.zoom_atual = self.zoom_factor ** self.zoom_steps

        mouse_viewport_pos = event.position().toPoint()
        self.scale(fator, fator)
        mouse_scene_pos_novo = self.mapToScene(mouse_viewport_pos)
        deslocamento = mouse_scene_pos_novo - mouse_scene_pos
        self.translate(deslocamento.x(), deslocamento.y())
    
    def resizeEvent(self, event):
        """Quando a janela for redimensionada, ajusta a área lógica da tela"""
        super().resizeEvent(event)
        if self.scene() and hasattr(self.scene(), "ajustar_area_logica"):
            self.scene().ajustar_area_logica()
    
    def centralizar_tela(self, cx: float, cy: float):
        """Centraliza um ponto na tela"""
        self.centerOn(QPointF(cx, cy))


class Tela(QGraphicsScene):
    """É a área do canvas, tudo é desenhado aqui"""
    def __init__(self):
        super().__init__()
        self.olho = None
        self.cria_pontos()
        self.grade = Grade()
        self.addItem(self.grade)
        self.sceneRectChanged.connect(self.grade.atualizar_area)
        
    # Outras geometrias
    def cria_pontos(self):
        """Cria pontos chave na tela"""
        self.ponto_0 = Pontos(0, 0, 1)
        self.ponto_cg = Pontos(10, 10, 1)
        self.addItem(self.ponto_0)
        self.addItem(self.ponto_cg)
    
    def edita_pontos(self, x: float, y: float):
        """Comando para editar o ponto CG"""
        x -= self.ponto_cg.tamanho / 2
        y -= self.ponto_cg.tamanho / 2
        self.ponto_cg.setPos(x, y)

    # Quem me vê? =======================================================================================================================
    def quem_me_ve(self, olho: Olho):
        """Dá uma referencia da classe QGraphicsView"""
        self.olho = olho
    
    # Ajuste de tamanho de tela
    def ajustar_area_logica(self):
        """Ajusta o tamanho da área lógica da tela"""
        # dados da janela e view
        janela_x = self.olho.viewport().width()
        janela_y = self.olho.viewport().height()
        zoom_minimo = ((1/self.olho.zoom_factor) ** self.olho.zoom_step_limit) * 5
        proporcao = janela_y / janela_x

        # dados do desenho
        for item in self.items():
            if isinstance(item, SecaoParametricaDesenho):
                rect_item = item.mapToScene(item.boundingRect()).boundingRect()
                break
        
        # Centro do item para manter centralizado
        cx = rect_item.center().x()
        cy = rect_item.center().y()

        # tamanho alvo da cena no zoom mínimo
        largura_alvo = janela_x / zoom_minimo
        altura_alvo  = janela_y / zoom_minimo

        # ajustar para manter a proporção da janela
        if altura_alvo / largura_alvo > proporcao:
            # Está mais alto que a janela, ajusta pela largura
            altura_alvo = (largura_alvo * proporcao) + rect_item.height()
        else:
            # Está mais largo que a janela, ajusta pela altura
            largura_alvo = (altura_alvo / proporcao) + rect_item.width()
        
        rect_cena = QRectF(cx - largura_alvo / 2,
                           cy - altura_alvo / 2,
                           largura_alvo,
                           altura_alvo)
        self.setSceneRect(rect_cena)
        self.olho.centralizar_tela(cx, cy)


class TelaRobusta(QWidget):
    """Cria a tela completa do programa"""
    def __init__(self):
        super().__init__()

        self.tela_principal = Tela()
        self.olho_principal = Olho(self.tela_principal)
        self.olho_principal.setParent(self)
        self.tela_principal.quem_me_ve(self.olho_principal)
        
        # Mini janela secundária
        self.mini_janela = QGraphicsScene()
        self.mini_olho = QGraphicsView(self.mini_janela, self)
        self.mini_olho.setFixedSize(150, 170)
        self.mini_olho.setSceneRect(-20, -20, 150, 150)
        self.mini_olho.setStyleSheet("background: transparent; border: none")
        self.mini_olho.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.mini_olho.scale(1, -1)
        self.desenha_simbologia()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.olho_principal.resize(self.width(), self.height())
        # Alinhar mini-olho ao canto inferior esquerdo.
        self.mini_olho.move(0, self.height() - self.mini_olho.height())
    
    def desenha_simbologia(self):
        """Desenha a simbologia da direção dos eixos"""
        cor = QColor('#888888')
        caneta = QPen(cor)
        pincel = QBrush(cor)
        tamanho = 40
        self.mini_janela.addLine(0, 0, 0, tamanho, caneta)
        self.mini_janela.addLine(0, 0, tamanho, 0, caneta)
        self.mini_janela.addEllipse(-2.5, -2.5, 5, 5, QPen(QColor(0, 0, 0, 0)), pincel)
        self.mini_janela.addPolygon(QPolygonF([QPointF(-2, tamanho), QPointF(2, tamanho), QPointF(0, tamanho+10)]), caneta, pincel)
        self.mini_janela.addPolygon(QPolygonF([QPointF(tamanho, -2), QPointF(tamanho+10, 0), QPointF(tamanho, 2)]), caneta, pincel)
        texto_z = self.mini_janela.addText("X")
        texto_z.setTransform(QTransform().scale(1, -1))
        texto_z.setPos(-15, 4)
        texto_z.setDefaultTextColor(cor)
        texto_y = self.mini_janela.addText("Z")
        texto_y.setTransform(QTransform().scale(1, -1))
        texto_y.setPos(-7.5, tamanho+34)
        texto_y.setDefaultTextColor(cor)
        texto_x = self.mini_janela.addText("Y")
        texto_x.setTransform(QTransform().scale(1, -1))
        texto_x.setPos(50, 12)
        texto_x.setDefaultTextColor(cor)
