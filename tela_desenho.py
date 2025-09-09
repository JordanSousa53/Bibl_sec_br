from PyQt6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QLabel
from PyQt6.QtGui import QColor, QBrush, QPen, QCursor, QPolygonF, QTransform, QPainter
from PyQt6.QtCore import Qt, QPoint, QPointF, QRectF, QSizeF

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
        self.zoom_atual = 1.0
        self.zoom_factor = 1.1
        self.zoom_steps = 0
        self.zoom_step_limit = 5

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
        print(self.zoom_atual)
        self.zoom_atual = self.zoom_factor ** self.zoom_steps
        self.scale(fator, fator)

        # Ajuste dos pontos
        for ponto in self.scene().items():
            if isinstance(ponto, Pontos):
                ponto.setScale(1 / self.zoom_atual)
    
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
    
    def ajustar_area_logica(self):
        """Ajusta a área lógica do desenho, baseado no nível mínimo de zoom, tamanho da seção desenhada e proporção da tela"""
        # Proporção da janela
        w_janela = self.olho.width()
        h_janela = self.olho.height()
        prop_janela = h_janela / w_janela

        # proporção da seção desenhada
        for item in self.items():
            if isinstance(item, SecaoParametricaDesenho):
                retang_item = item.mapToScene(item.boundingRect()).boundingRect()
                break
        w_secao = retang_item.width()
        h_secao = retang_item.height()
        prop_secao = h_secao / w_secao

        # Nível mínimo de zoom
        nivel_min = self.olho.zoom_factor ** -self.olho.zoom_step_limit
        
        # Ajustando proporção do retângulo da seção desenhada em relação à proporção da tela
        if prop_secao >= prop_janela:
            # Seção está mais alta que a viewport: sobe a largura para ajustar
            nw_secao = h_secao / prop_janela
            nh_secao = h_secao
        else:
            # Viewport está mais alta que seção: sobe a altura para ajustar
            nw_secao = w_secao
            nh_secao = w_secao * prop_janela
        
        # Adicionando fator do nível mínimo de zoom
        nw_secao /= nivel_min
        nh_secao /= nivel_min
        
        # Centro do desenho para calcular coordenadas do retangulo por ele
        cx = retang_item.center().x()
        cy = retang_item.center().y()
        
        # Dimensoes do novo retangulo + margens
        p_topleft = QPointF(cx - nw_secao / 2, cy - nh_secao / 2)
        n_tamanho = QSizeF(nw_secao, nh_secao)
        novo_retangulo = QRectF(p_topleft, n_tamanho)
        margem = 50
        novo_retangulo.adjust(-margem, -margem, margem, margem)

        # Calculando e aplicando novo fator de escala
        fator = round(w_janela / novo_retangulo.width(), 2)
        self.olho.resetTransform()
        self.olho.scale(fator, -fator)
        self.olho.zoom_atual = fator

        self.setSceneRect(novo_retangulo)
        self.olho.centerOn(cx, cy)


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
        cor = QColor("#343A36")
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
