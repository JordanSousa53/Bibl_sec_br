from PyQt6.QtWidgets import QGraphicsPathItem, QGraphicsEllipseItem, QGraphicsItem
from PyQt6.QtGui import QPainterPath, QPen, QColor, QBrush
from PyQt6.QtCore import QRectF, QPointF, QSizeF

from secao import SecaoParametrica
from linhas_cota import Cotas

class SecaoParametricaDesenho(QGraphicsPathItem):
    def __init__(self):
        super().__init__()
        self.secao = SecaoParametrica()
        self.caminho = QPainterPath()
        self.cotas = {}
        self.tinta = QBrush(QColor(231, 247, 17, 179))
        self.caneta = QPen(QColor(56, 52, 40), 2)
        self.caneta.setCosmetic(True)
        self.setPen(self.caneta)
        self.setBrush(self.tinta)
    
    def tipo_da_secao(self, tipo: str, dimensoes: dict):
        """Escolhe as regras de desenho conforme o tipo de seção"""
        match tipo:
            case 'I':
                cota_h = dimensoes['h']
                cota_bf = dimensoes['bf']
                cota_tw = dimensoes['tw']
                cota_tf = dimensoes['tf']
                raio = dimensoes['r alma']
                self.secao.desenha_secao_i(cota_h, cota_bf, cota_tw, cota_tf, raio)
            case 'U':
                cota_h = dimensoes['h']
                cota_bf = dimensoes['bf']
                cota_tw = dimensoes['tw']
                cota_tf = dimensoes['tf']
                r_alma = dimensoes['r alma']
                r_mesa = dimensoes['r mesa']
                self.secao.desenha_secao_u(cota_h, cota_bf, cota_tw, cota_tf, r_mesa, r_alma)
            case 'W':
                cota_h = dimensoes['h']
                cota_bf = dimensoes['bf']
                cota_tw = dimensoes['tw']
                cota_tf = dimensoes['tf']
                raio = dimensoes['r alma']
                self.secao.desenha_secao_w(cota_h, cota_bf, cota_tw, cota_tf, raio)
            case _:
                pass
        
    def desenhar_cotas(self, tipo: str):
        """Pelo tipo de perfil, desenha as cotas necessárias"""
        coordenadas = self.secao.retorna_pontos()
        match tipo:
            case 'I':
                p1 = QPointF(coordenadas[0]['x'], coordenadas[0]['y'])
                p2 = QPointF(coordenadas[7]['x'], coordenadas[7]['y'])
                p3 = QPointF(coordenadas[1]['x'], coordenadas[1]['y'])

                cota_h = Cotas(p1, p2)
                cota_bf = Cotas(p3, p1)
                self.cotas['Cota h'] = cota_h
                self.cotas['Cota bf'] = cota_bf
            case _:
                pass

    def desenhar_secao(self):
        """Recebe os dados e trata antes de desenhar"""
        dados = self.secao.retorna_pontos()
        for dado in dados:
            if dado['Tipo'] == 'Inicio':
                self.caminho.moveTo(dado['x'], dado['y'])
            elif dado['Tipo'] == 'LinhaPara':
                self.caminho.lineTo(dado['x'], dado['y'])
            elif dado['Tipo'] == 'Arco':
                ponto_superior = QPointF(dado['Retângulo delimitador'][0], dado['Retângulo delimitador'][1])
                tamanho = QSizeF(dado['Retângulo delimitador'][2], dado['Retângulo delimitador'][3])
                retangulo = QRectF(ponto_superior, tamanho)
                self.caminho.lineTo(dado['Pontos tangência'][0][0], dado['Pontos tangência'][0][1])
                self.caminho.arcTo(retangulo, dado['Ângulo início'], dado['Ângulo extensão'])
                
        self.caminho.closeSubpath()
        self.setPath(self.caminho)
    
    def limpar_caminho(self):
        """Deleta o path existente para desenhar de novo"""
        self.caminho.clear()
        self.secao.limpa_secao()
        self.setPath(self.caminho)


class Pontos(QGraphicsEllipseItem):
    """Classe personalizada para representar um ponto. Funciona apenas com a classe Tela"""
    def __init__(self, x, y, tamanho=5):
        super().__init__(0, 0, tamanho, tamanho)
        self.tamanho = tamanho
        self.centro = QPointF(x, y)
        self.setPos(x-tamanho/2, y-tamanho/2)
        self.setTransformOriginPoint(tamanho/2, tamanho/2)
        self.setZValue(10)

        # Cores
        self.transparente = QColor(0, 0, 0, 0)
        self.cor_padrao = QColor("#080808")

        # Estado para hover
        self.hovering = False

        self.setPen(QPen(self.transparente))
        self.setBrush(QBrush(self.cor_padrao))
    
    def paint(self, painter, option, widget=None):
        # Alterar a cor com base no estado de seleção
        if self.isSelected() or self.hovering:
            painter.setBrush(QBrush(self.cor_selec))
            painter.setPen(QPen(self.cor_selec, 2))
        else:
            painter.setBrush(QBrush(self.cor_padrao))
            painter.setPen(QPen(self.transparente))

        # Desenhar apenas a elipse original
        painter.drawEllipse(self.rect())
    
    def __repr__(self):
        """Representação legível do objeto"""
        return f"Ponto(x={self.centro.x()}, y={self.centro.y()})"

    def __hash__(self):
        """Permite que o objeto seja armazenado em um set()"""
        return hash((self.centro.x(), self.centro.y()))

    def __eq__(self, other):
        """Compara dois pontos pelo posicionamento"""
        return isinstance(other, Pontos) and self.x() == other.x() and self.y() == other.y()