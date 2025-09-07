import math

class SecaoParametrica:
    """Calcula coordenadas de seções pré-definidas"""
    def __init__(self):
        self.lista_pontos = []
        self.lista_discret = []
        self.descricao = {"H": "Altura da seção",
                          "B": "Base da seção",
                          "tw": "Espessura da alma",
                          "tf": "Espessura da mesa (média)",
                          "r": "Raio da mesa"}
        self.dados = {}
    
    def desenha_secao_i(self, H: float, B: float, tw: float, tf: float, r: float):
        """Calcula as coordenadas de uma seção I"""
        self.dados['H'] = H
        self.dados['B'] = B
        self.dados['tw'] = tw
        self.dados['tf'] = tf
        self.dados['r'] = r

        # Variáveis
        vetor_incl_unit = (1, 0.1667)  # No site da fabricante AcelorMittal diz que seus perfis tem uma inclinação de 16,67%
        dist_aba = (B / 2) - (tw / 2)
        vetor_incl_aba = (dist_aba, dist_aba * vetor_incl_unit[1] / vetor_incl_unit[0])

        # Pontos
        p1 = {'x': 0, 'y': 0, 'Tipo': "Inicio"}
        p2 = {'x': B, 'y': 0, 'Tipo': "LinhaPara"}
        p3 = {'x': B, 'y': tf - vetor_incl_aba[1] / 2, 'Tipo': "LinhaPara"}
        p4 = {'x': dist_aba + tw, 'y': p3['y'] + vetor_incl_aba[1], 'Tipo': "LinhaPara"}
        p5 = {'x': p4['x'], 'y': H - p4['y'], 'Tipo': "LinhaPara"}
        p6 = {'x': B, 'y': p5['y'] + vetor_incl_aba[1], 'Tipo': "LinhaPara"}
        p7 = {'x': B, 'y': H, 'Tipo': "LinhaPara"}
        p8 = {'x': 0, 'y': H, 'Tipo': "LinhaPara"}
        p9 = {'x': 0, 'y': p6['y'], 'Tipo': "LinhaPara"}
        p10 = {'x': dist_aba, 'y': p5['y'], 'Tipo': "LinhaPara"}
        p11 = {'x': dist_aba, 'y': p4['y'], 'Tipo': "LinhaPara"}
        p12 = {'x': 0, 'y': p3['y'], 'Tipo': "LinhaPara"}
        print(f'Cota d = {p5["y"] - p4["y"]}')

        # Arcos
        a1 = self.calcula_arco(p3, p2, p4, r)
        a2 = self.calcula_arco(p4, p3, p5, r)
        a3 = self.calcula_arco(p5, p4, p6, r)
        a4 = self.calcula_arco(p6, p5, p7, r)
        a5 = self.calcula_arco(p9, p8, p10, r)
        a6 = self.calcula_arco(p10, p9, p11, r)
        a7 = self.calcula_arco(p11, p10, p12, r)
        a8 = self.calcula_arco(p12, p11, p1, r)

        # Add nas listas para desenho
        lista_desenho = [p1, p2, a1, a2, a3, a4, p7, p8, a5, a6, a7, a8]
        self.lista_pontos.extend(lista_desenho)
    
    def desenha_secao_u(self, H: float, B: float, tw: float, tf: float, ra: float, rm: float):
        """Calcula as coordenadas de uma seção U"""
        self.dados['H'] = H
        self.dados['B'] = B
        self.dados['tw'] = tw
        self.dados['tf'] = tf
        self.dados['r mesa'] = rm
        self.dados['r alma'] = ra

        # Variáveis
        vetor_incl_unit = (1, 0.1667)
        dist_aba = B - tw
        vetor_incl_aba = (dist_aba, dist_aba * vetor_incl_unit[1] / vetor_incl_unit[0])

        # Pontos
        p1 = {'x': 0, 'y': 0, 'Tipo': "Inicio"}
        p2 = {'x': B, 'y': 0, 'Tipo': "LinhaPara"}
        p3 = {'x': B, 'y': tf - vetor_incl_aba[1] / 2, 'Tipo': "LinhaPara"}
        p4 = {'x': tw, 'y': p3['y'] + vetor_incl_aba[1], 'Tipo': "LinhaPara"}
        p5 = {'x': p4['x'], 'y': H - p4['y'], 'Tipo': "LinhaPara"}
        p6 = {'x': B, 'y': p5['y'] + vetor_incl_aba[1], 'Tipo': "LinhaPara"}
        p7 = {'x': B, 'y': H, 'Tipo': "LinhaPara"}
        p8 = {'x': 0, 'y': H, 'Tipo': "LinhaPara"}
        print(f"Cota d = {p5['y'] - p4['y']}")

        # Arcos
        a1 = self.calcula_arco(p3, p2, p4, rm)
        a2 = self.calcula_arco(p4, p3, p5, ra)
        a3 = self.calcula_arco(p5, p4, p6, ra)
        a4 = self.calcula_arco(p6, p5, p7, rm)

        # Add nas listas para desenho
        lista_desenho = [p1, p2, a1, a2, a3, a4, p7, p8]
        self.lista_pontos.extend(lista_desenho)
    
    def desenha_secao_w(self, H: float, B: float, tw: float, tf: float, r: float):
        """Calcula as coordenadas de uma seção W"""
        self.dados['H'] = H
        self.dados['B'] = B
        self.dados['tw'] = tw
        self.dados['tf'] = tf
        self.dados['r alma'] = r

        # Variáveis
        dist_aba = (B - tw) / 2

        # Pontos
        p1 = {'x': 0, 'y': 0, 'Tipo': "Inicio"}
        p2 = {'x': B, 'y': 0, 'Tipo': "LinhaPara"}
        p3 = {'x': B, 'y': tf, 'Tipo': "LinhaPara"}
        p4 = {'x': B - dist_aba, 'y': tf, 'Tipo': "LinhaPara"}
        p5 = {'x': p4['x'], 'y': H - tf, 'Tipo': "LinhaPara"}
        p6 = {'x': B, 'y': p5['y'], 'Tipo': "LinhaPara"}
        p7 = {'x': B, 'y': H, 'Tipo': "LinhaPara"}
        p8 = {'x': 0, 'y': H, 'Tipo': "LinhaPara"}
        p9 = {'x': 0, 'y': p5['y'], 'Tipo': "LinhaPara"}
        p10 = {'x': dist_aba, 'y': p5['y'], 'Tipo': "LinhaPara"}
        p11 = {'x': p10['x'], 'y': tf, 'Tipo': "LinhaPara"}
        p12 = {'x': 0, 'y': tf, 'Tipo': "LinhaPara"}

        # Arcos
        a1 = self.calcula_arco(p4, p3, p5, r)
        a2 = self.calcula_arco(p5, p4, p6, r)
        a3 = self.calcula_arco(p10, p9, p11, r)
        a4 = self.calcula_arco(p11, p10, p12, r)

        # Add nas listas para desenho
        lista_desenho = [p1, p2, p3, a1, a2, p6, p7, p8, p9, a3, a4, p12]
        self.lista_pontos.extend(lista_desenho)

    def retorna_pontos(self):
        return self.lista_pontos

    def retorna_estilo_propsection(self):
        """Mostra no terminal uma lista de como a seção deve ser construída no propsection"""
        cont = 0
        for ponto in self.lista_pontos:
            if ponto['Tipo'] == 'LinhaPara':
                print(f"{str(cont)} - Ponto Absoluto: x = {ponto['x']}, y = {ponto['y']}")
            elif ponto['Tipo'] == 'Arco':
                print(f"{str(cont)} - Ponto Absoluto: x = {ponto['Pontos tangência'][0][0]}, y = {ponto['Pontos tangência'][0][1]}")
                cont += 1
                print(f"{str(cont)} - Arco: raio = {self.dados['r']}, ângulo = {ponto['Ângulo extensão']}°")
            else:
                print(ponto)
            cont += 1

    def calcula_arco(self, pcentral: dict, pinic: dict, pfinal: dict, raio: float) -> dict:
        """Calcula os parâmetros de um arco tangente a duas retas, usando vetores unitários para bissetriz"""

        # Vetores das retas
        vetor_u = (pinic['x'] - pcentral['x'], pinic['y'] - pcentral['y'])
        vetor_v = (pfinal['x'] - pcentral['x'], pfinal['y'] - pcentral['y'])

        # Normalização
        norm_u = math.hypot(*vetor_u)
        norm_v = math.hypot(*vetor_v)
        u_unit = (vetor_u[0] / norm_u, vetor_u[1] / norm_u)
        v_unit = (vetor_v[0] / norm_v, vetor_v[1] / norm_v)

        # Ângulo entre os vetores
        produto_escalar = u_unit[0] * v_unit[0] + u_unit[1] * v_unit[1]
        produto_escalar = max(-1.0, min(1.0, produto_escalar))
        theta_uv = math.acos(produto_escalar)

        # Cálculo do vetor bissetriz unitário
        bissetriz_unit = self.vetor_bissetriz(vetor_u, vetor_v)

        # Distância do ponto central ao centro do arco
        dist_centro = raio / math.sin(theta_uv / 2)

        # Centro do arco
        centro_circulo = (
            pcentral['x'] + dist_centro * bissetriz_unit[0],
            pcentral['y'] + dist_centro * bissetriz_unit[1])

        # Pontos de tangência
        valor_T = math.sqrt(dist_centro ** 2 - raio ** 2)
        ponto_1 = (
            pcentral['x'] + u_unit[0] * valor_T,
            pcentral['y'] + u_unit[1] * valor_T)
        ponto_2 = (
            pcentral['x'] + v_unit[0] * valor_T,
            pcentral['y'] + v_unit[1] * valor_T)

        # Retângulo delimitador
        retangulo_circulo = [
            centro_circulo[0] - raio,
            centro_circulo[1] + raio,
            2 * raio,
            -2 * raio]

        # Ângulos de posição dos pontos de tangência em relação ao centro
        angulo_inicio = math.atan2(ponto_1[1] - centro_circulo[1], ponto_1[0] - centro_circulo[0])
        angulo_fim = math.atan2(ponto_2[1] - centro_circulo[1], ponto_2[0] - centro_circulo[0])

        # Diferença direta
        delta = angulo_fim - angulo_inicio

        # Ajustar delta para o intervalo [-π, π]
        if delta > math.pi:
            delta -= 2 * math.pi
        elif delta < -math.pi:
            delta += 2 * math.pi
        angulo_extensao = delta  # positivo → sentido anti-horário

        # Conversão para graus
        angulo_inicio_deg = math.degrees(angulo_inicio)
        angulo_extensao_deg = math.degrees(angulo_extensao)

        return {'Pontos tangência': (ponto_1, ponto_2),
                'Retângulo delimitador': retangulo_circulo,
                'Ângulo início': angulo_inicio_deg,
                'Ângulo extensão': angulo_extensao_deg,
                'Tipo': 'Arco',
                'Ângulo início rad': angulo_inicio,
                'Ângulo extensão rad': angulo_extensao,
                'Centro círculo': centro_circulo,
                'raio': raio}
    
    def limpa_secao(self):
        """Limpa as coordenadas calculadas caso queira recalcular"""
        self.lista_pontos.clear()
        self.dados.clear()

    @staticmethod
    def vetor_bissetriz(vetor1: tuple[float], vetor2: tuple[float]) -> tuple[float]:
        """Calcula o vetor bissetriz unitário entre dois vetores"""
        norma_u = math.hypot(vetor1[0], vetor1[1])
        norma_v = math.hypot(vetor2[0], vetor2[1])

        u_unit = (vetor1[0] / norma_u, vetor1[1] / norma_u)
        v_unit = (vetor2[0] / norma_v, vetor2[1] / norma_v)

        u_v = (u_unit[0] + v_unit[0], u_unit[1] + v_unit[1])
        norma_uv = math.hypot(u_v[0], u_v[1])

        u_v_unit = (u_v[0] / norma_uv, u_v[1] / norma_uv)
        return u_v_unit
