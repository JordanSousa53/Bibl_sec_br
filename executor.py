import sys
from PyQt6.QtWidgets import QApplication

from janela import Janela
from leitor_csv import LeitorCSV

app = QApplication(sys.argv)

leitor = LeitorCSV()
leitor.carregar_arquivo(r'C:\Users\Jordan\OneDrive\Projetos Python\Desenho seções\Biblioteca seções.CSV')
leitor.criar_dicionario()

janela = Janela()
janela.carregar_dados(leitor.dicionario, leitor.tipos)
janela.preencher_combobox()
janela.e_tipo.setCurrentText('I')
janela.show()

sys.exit(app.exec())
