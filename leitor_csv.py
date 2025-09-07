import csv

class LeitorCSV:
    def __init__(self):
        self.arquivo = None
        self.dados = None
        self.dicionario = []
        self.tipos = set()
    
    def carregar_arquivo(self, path: str):
        """Carrega o arquivo csv na memória"""
        self.arquivo = path
        lista = []

        with open(self.arquivo, 'r') as dados:
            leitor = csv.reader(dados, delimiter=';')
            for dado in leitor:
                lista.append(list(dado))
        
        self.dados = lista
    
    def criar_dicionario(self):
        """Cria uma estrutura dict para guardar os dados do csv"""
        cabecalho = self.dados[0]
        for i in range(1, len(self.dados)):
            dicionario = {}
            numeros = self.converter_para_float(self.dados[i])
            for cont, titulo in enumerate(cabecalho):
                dicionario[titulo] = numeros[cont]
            self.tipos.add(dicionario['Tipo'])
            self.dicionario.append(dicionario)
    
    @staticmethod
    def converter_para_float(lista: list[str]) -> list[float]:
        """Converte números strings para floats"""
        numeros = []
        for dado in lista:
            dado = dado.replace(',', '.')
            try:
                dado = float(dado)
            except ValueError:
                pass
            numeros.append(dado)
        return numeros


if __name__ == "__main__":
    leitor = LeitorCSV()
    leitor.carregar_arquivo(r'C:\Users\Jordan\OneDrive\Projetos Python\Desenho seções\Biblioteca seções.CSV')
    leitor.criar_dicionario()
    for d in leitor.dicionario:
        print(d)
