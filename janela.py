from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsItem, QApplication
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGridLayout, QWidget, QGroupBox, QHBoxLayout
from PyQt6.QtWidgets import QLabel, QSizePolicy, QScrollArea, QComboBox
from PyQt6.QtWidgets import QSpacerItem
from PyQt6.QtGui import QFont

from secao_path import SecaoParametricaDesenho
from tela_desenho import TelaRobusta
from dimensoes_pyqt import CampoNum


class Janela(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dicionario = None
        self.tipos = None
        self.secao_desenho = SecaoParametricaDesenho()

        widget = QWidget()
        self.lay = QGridLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)
        widget.setLayout(self.lay)
        self.setCentralWidget(widget)

        # Configurações iniciais da janela
        self.setWindowTitle("Seções")
        self.setGeometry(100, 100, 844, 522)
        self.setMinimumSize(844, 522)
        fonte = QFont('Segoe UI', 8)
        QApplication.setFont(fonte)

        # Frames
        self.cria_menu_superior()
        self.cria_tela()
        self.cria_lateral()
        self.cria_barra_status()

    def cria_lateral(self):
        politica_tamanho = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        # 📦 Widget interno que será rolável
        conteudo_rolavel = QWidget()
        conteudo_rolavel.setSizePolicy(politica_tamanho)
        conteudo_rolavel.setFixedWidth(200)

        layout_conteudo = QVBoxLayout()
        layout_conteudo.setSpacing(3)
        layout_conteudo.setContentsMargins(9, 9, 0, 9)
        conteudo_rolavel.setLayout(layout_conteudo)

        # Grupo Dimensões do perfil
        grupo1 = QGroupBox(title='Dimensões do perfil')
        grupo1.setSizePolicy(politica_tamanho)
        lay1 = QGridLayout()
        descr1 = QLabel(text='Parâmetros geométricos exclusivos de cada tipo de perfil, usados para calcular propriedades estruturais específicas.\n')
        descr1.setWordWrap(True)
        descr1.setStyleSheet('font-style: italic; color: #888888')
        lay1.addWidget(descr1, 1, 1, 1, 3)

        lista1 = ['h :', 'd :', 'b<sub>f</sub> :', 't<sub>w</sub> :', 't<sub>f</sub> :', 'r :']
        lista2 = ['mm', 'mm', 'mm', 'mm', 'mm', 'mm']
        self.__add_labels_grid(lista1, lay1, 40, 2, 1, True)
        self.__add_labels_grid(lista2, lay1, 25, 2, 3, False)
        self.h, self.d, self.bf, self.tw = CampoNum(), CampoNum(), CampoNum(), CampoNum()
        self.tf, self.raio = CampoNum(), CampoNum()
        lista3 = [self.h, self.d, self.bf, self.tw, self.tf, self.raio]
        self.__add_widget_grid(lista3, lay1, 2, 2)
        grupo1.setLayout(lay1)

        # Grupo geometria da seção
        grupo2 = QGroupBox(title='Geometria da seção')
        grupo2.setSizePolicy(politica_tamanho)
        lay2 = QGridLayout()
        descr2 = QLabel(text='Propriedades básicas que descrevem o tamanho e a forma da seção transversal, essenciais para cálculos estruturais iniciais.')
        descr2.setWordWrap(True)
        descr2.setStyleSheet('font-style: italic; color: #888888')
        lay2.addWidget(descr2, 1, 1, 1, 3)
        lista1 = ['A<sub>s</sub> :', 'y<sub>c</sub> :', 'z<sub>c</sub> :',
                  'r<sub>y</sub> :','r<sub>z</sub> :', 'W<sub>y sup</sub> :',
                  'W<sub>y inf</sub> :', 'W<sub>z sup</sub> :', 'W<sub>z inf</sub> :',
                  'Z<sub>y</sub> :', 'Z<sub>z</sub> :']
        lista2 = ['cm²', 'cm', 'cm', 'cm', 'cm', 'cm³', 'cm³', 'cm³', 'cm³', 'cm³', 'cm³']
        self.__add_labels_grid(lista1, lay2, 40, 2, 1, True)
        self.__add_labels_grid(lista2, lay2, 25, 2, 3, False)
        self.area = CampoNum()
        self.yc, self.zc = CampoNum(), CampoNum()
        self.ry, self.rz = CampoNum(), CampoNum()
        self.wysup, self.wyinf = CampoNum(), CampoNum()
        self.wzsup, self.wzinf = CampoNum(), CampoNum()
        self.zy, self.zz = CampoNum(), CampoNum()
        lista3 = [self.area, self.yc, self.zc, self.ry, self.rz, self.wysup, self.wyinf, self.wzsup, self.wzinf, self.zy, self.zz]
        self.__add_widget_grid(lista3, lay2, 2, 2)
        grupo2.setLayout(lay2)

        # Grupo Momentos de inércia
        grupo3 = QGroupBox(title='Momentos de inércia')
        grupo3.setSizePolicy(politica_tamanho)
        lay3 = QGridLayout()
        descr3 = QLabel(text='Medidas da distribuição de massa em torno dos eixos principais, determinam a resistência à flexão e à rotação.\n')
        descr3.setWordWrap(True)
        descr3.setStyleSheet('font-style: italic; color: #888888')
        lay3.addWidget(descr3, 1, 1, 1, 3)
        lista1 = ['I<sub>y</sub> :', 'I<sub>z</sub> :', 'I<sub>p</sub> :', 'θ<sub>p</sub> :']
        lista2 = ['cm<sup>4</sup>', 'cm<sup>4</sup>', 'cm<sup>4</sup>', 'rad']
        self.__add_labels_grid(lista1, lay3, 40, 2, 1, True)
        self.__add_labels_grid(lista2, lay3, 25, 2, 3, False)
        self.iy, self.iz = CampoNum(), CampoNum()
        self.ip, self.theta = CampoNum(), CampoNum()
        lista3 = [self.iy, self.iz, self.ip, self.theta]
        self.__add_widget_grid(lista3, lay3, 2, 2)
        grupo3.setLayout(lay3)

        # Grupo Torção e empenamento
        grupo4 = QGroupBox(title='Torção e empenamento')
        grupo4.setSizePolicy(politica_tamanho)
        lay4 = QGridLayout()
        descr4 = QLabel(text='Propriedades que indicam a rigidez da seção à torção, incluindo efeitos de torção uniforme e não uniforme (empenamento).\n')
        descr4.setWordWrap(True)
        descr4.setStyleSheet('font-style: italic; color: #888888')
        lay4.addWidget(descr4, 1, 1, 1, 3)
        lista1 = ['J :', 'C<sub>w</sub> :']
        lista2 = ['cm<sup>4</sup>', 'cm<sup>6</sup>']
        self.__add_labels_grid(lista1, lay4, 40, 2, 1, True)
        self.__add_labels_grid(lista2, lay4, 25, 2, 3, False)
        self.j, self.cw = CampoNum(), CampoNum()
        lista3 = [self.j, self.cw]
        self.__add_widget_grid(lista3, lay4, 2, 2)
        grupo4.setLayout(lay4)

        # ➕ Adiciona o grupo ao layout do conteúdo rolável
        layout_conteudo.addWidget(grupo1)
        layout_conteudo.addWidget(grupo2)
        layout_conteudo.addWidget(grupo3)
        layout_conteudo.addWidget(grupo4)

        # 📜 Área de rolagem
        scroll_area = QScrollArea()
        scroll_area.setFixedWidth(218)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(conteudo_rolavel)

        # 🔗 Adiciona a área de rolagem ao layout principal
        self.lay.addWidget(scroll_area, 2, 2)

    def cria_tela(self):
        self.tela = TelaRobusta()
        self.lay.addWidget(self.tela, 2, 1)
        self.tela.tela_principal.addItem(self.secao_desenho)
    
    def cria_menu_superior(self):
        frame = QFrame()
        lay1 = QHBoxLayout()
        lay1.setContentsMargins(3, 3, 3, 3)
        t1 = QLabel(text='Tipo:')
        t2 = QLabel(text='Seção:')
        self.e_tipo = QComboBox()
        self.e_tipo.setFixedWidth(50)
        self.e_tipo.currentTextChanged.connect(self.filtrar_combobox)
        self.e_secao = QComboBox()
        self.e_secao.setFixedWidth(100)
        self.e_secao.currentTextChanged.connect(self.preencher_entradas)
        self.descricao_tipo = QLabel(text='')
        self.descricao_tipo.setStyleSheet('font-style: italic; color: #888888')

        lay1.addWidget(t1)
        lay1.addWidget(self.e_tipo)
        lay1.addWidget(t2)
        lay1.addWidget(self.e_secao)
        lay1.addWidget(self.descricao_tipo)
        
        espaco = QSpacerItem(1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        lay1.addSpacerItem(espaco)

        frame.setLayout(lay1)
        self.lay.addWidget(frame, 1, 1, 1, 2)
    
    def cria_barra_status(self):
        frame = QFrame()
        layout = QHBoxLayout()
        self.coords_mouse = QLabel(text='(0, 0) mm')
        layout.addWidget(self.coords_mouse)
        frame.setLayout(layout)

        self.tela.olho_principal.conectar_label_coordenadas(self.coords_mouse)
        self.lay.addWidget(frame, 3, 1)

    def carregar_dados(self, dados: list[dict], tipos: set):
        """Carrega dados para mostrar na janela"""
        self.dicionario = dados
        self.tipos = tipos
    
    def enviar_dados_desenhar(self, dimensoes: dict):
        """Envia os dados da escolha do usuário para desenhar a seção"""
        tipo = self.e_tipo.currentText()
        
        self.secao_desenho.limpar_caminho()
        self.secao_desenho.tipo_da_secao(tipo, dimensoes)
        self.secao_desenho.desenhar_secao()
        #self.desenhar_cotas(tipo)

        # Ajusta CG
        secao = self.e_secao.currentText()
        for dado in self.dicionario:
            if dado['Nome'] == secao:
                cx = dado['yc'] * 10
                cy = dado['zc'] * 10
                break

        self.tela.tela_principal.edita_pontos(cx, cy)
        self.tela.tela_principal.ajustar_area_logica()
    
    def desenhar_cotas(self, tipo: str):
        """Desenha as cotas na tela"""
        self.secao_desenho.desenhar_cotas(tipo)
        dicionario: dict = self.secao_desenho.cotas
        for chave in dicionario.keys():
            item: QGraphicsItem = dicionario[chave]
            self.tela.tela_principal.addItem(item)
    
    def preencher_combobox(self):
        """Preenche as combobox's ao abrir a janela"""
        self.e_tipo.addItems(self.tipos)        
    
    def filtrar_combobox(self):
        """Preenche as comboboxs com dados"""
        self.e_secao.currentTextChanged.disconnect(self.preencher_entradas)
        self.e_secao.clear()

        # Preenche a descrição do tipo
        tipo_atual = self.e_tipo.currentText()
        descr = ''
        for dado in self.dicionario:
            if dado['Tipo'] == tipo_atual:
                descr = dado['Descrição tipo']
                break
        self.descricao_tipo.setText(descr)
        
        # Filtra as seções por tipo
        lista = []
        for dado in self.dicionario:
            if dado['Tipo'] == tipo_atual:
                lista.append(dado['Nome'])
        self.e_secao.addItems(lista)
        self.e_secao.currentTextChanged.connect(self.preencher_entradas)
        self.preencher_entradas()
    
    def preencher_entradas(self):
        """Ao selecionar uma seção, preenche os dados nos QLineEdit's"""
        nome = self.e_secao.currentText()

        for item in self.dicionario:
            if item['Nome'] == nome:
                dimensoes = item
        
        self.h.setValue(dimensoes['h'])
        self.d.setValue(dimensoes['d'])
        self.bf.setValue(dimensoes['bf'])
        self.tf.setValue(dimensoes['tf'])
        self.tw.setValue(dimensoes['tw'])
        self.raio.setValue(dimensoes['r alma'])
        
        self.area.setValue(dimensoes['As'])
        self.yc.setValue(dimensoes['yc'])
        self.zc.setValue(dimensoes['zc'])
        self.ry.setValue(dimensoes['ry'])
        self.rz.setValue(dimensoes['rz'])
        self.wysup.setValue(dimensoes['wysup'])
        self.wyinf.setValue(dimensoes['wyinf'])
        self.wzsup.setValue(dimensoes['wzsup'])
        self.wzinf.setValue(dimensoes['wzinf'])
        self.zy.setValue(dimensoes['Zy'])
        self.zz.setValue(dimensoes['Zz'])

        self.iy.setValue(dimensoes['Iy'])
        self.iz.setValue(dimensoes['Iz'])
        self.ip.setValue(dimensoes['Ip'])
        self.theta.setValue(dimensoes['theta'])

        self.j.setValue(dimensoes['J'])
        self.cw.setValue(dimensoes['Cw'])

        self.enviar_dados_desenhar(dimensoes)

    @staticmethod
    def __add_labels_grid(textos: list[str], layout: QGridLayout, largura: int, linha: int, coluna: int, setstyle: bool):
        """Adiciona vários labels em linhas, num layout QGridLayout"""
        for cont, texto in enumerate(textos):
            label = QLabel(text=texto)
            label.setFixedWidth(largura)
            if setstyle: label.setStyleSheet("font-size: 11pt;")
            layout.addWidget(label, linha + cont, coluna)
            
    @staticmethod
    def __add_widget_grid(widgets: list[QWidget], layout: QGridLayout, linha: int, coluna: int):
        """Adiciona qualquer widget em linhas, num layout QGridLayout"""
        for cont, widget in enumerate(widgets):
            layout.addWidget(widget, linha + cont, coluna)
