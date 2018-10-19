# -*- coding: UTF-8 -*-

from Estruturas import *
from math import sqrt


# variavel para representar um valor infinito (usado em floydWarshall)
INFINITO = 999999999999


class BeerHouse:
    vertices = None
    regioes = None
    numReg = None
    lambD = None
    lambW = None
    lambC = None
    betaD = None
    betaW = None
    betaC = None
    
    def __init__(self):
        # self.numReg = numReg
        # self.lambD = lambD
        # self.lambW = lambW
        # self.lambC = lambC
        self.betaD = 0
        self.betaW = 0
        self.betaC = 0
        self.vertices = []
        self.regioes = []
    
    # Adiciona um vertice ao grafo
    def adiciona(self, vertice):
        self.vertices.append(vertice)
        
        
    # Liga dois vertices no grafo
    def liga(self, v1, v2):
        v1 = self.vertices[v1.cod]
        v2 = self.vertices[v2.cod]
        v1.grau += 1
        v2.grau += 1
        v1.vizinhos.append(v2)
        v2.vizinhos.append(v1)
        #~ v1.grau += 1
    
    # Calcula os valores da media ideal
    def calcBeta(self):
        for v in self.vertices:
            self.betaC += v.c
            self.betaW += v.w
            self.betaD += v.d
        self.betaC = float(self.betaC) / self.numReg
        self.betaW = float(self.betaW) / self.numReg
        self.betaD = float(self.betaD) / self.numReg

    # Escolhe o vizinho que sera anexado a uma regiao
    def pegaAnexado(self, regiao):
        # Ordena os vizinhos da regiao
        vizOrdenados = self.selectionSort(regiao.vizinhos)
        tam = len(vizOrdenados)
        
        i = 0
        # Percorre todos os vizinhos da regiao
        while(i < tam):
            # Se algum deles ja pertencer a alguma regiao
            if(vizOrdenados[i].regiao != None):
                # Remove-o da lista
                del vizOrdenados[i]
                i -= 1
                tam -= 1
            i += 1
        
        tam = len(vizOrdenados)
        # Se nao sobrou nenhum vizinho na lista, retorna nulo
        if(tam <= 0):
            return None
        
        # Senao considera que o vertice a ser anexado e' o ultimo da lista
        escolhido = vizOrdenados[tam - 1]
        i = tam - 2
        
        # Procura o vertice de menor grau com o mesmo peso do vertice de maior peso
        while((i > -1) and (escolhido.peso == vizOrdenados[i].peso)):
            i -= 1
        
        
        escolhido = vizOrdenados[i + 1]
        
        return escolhido
    
    
    # Gera as regioes conexas
    def divideRegioes(self):
        # Cria as k regioes
        self.regioes = self.criaRegioes()
        
        # Enquanto houver vertices sem regiao
        while (not self.acabou()):
            # Ordena as regioes
            self.regioes = self.selectionSort(self.regioes)
            # Busca a primeira regiao com vizinhos
            i = 0
            while((i < self.numReg) and (self.regioes[i].grau <= 0)):
                i += 1
                
            # Se nenhuma regiao tiver vizinhos significa que todos estao em uma regiao
            if(i == self.numReg):
                return
            
            # Testa se a regiao tem vizinhos
            if(len(self.regioes[i].vizinhos) > 0):
                continua = True
                # Enquanto nao foi anexado nenhum vertice ou nao acabaram as regioes
                while((i < self.numReg) and (continua)):
                    # Busca um possivel vertice a ser anexado
                    viz = self.pegaAnexado(self.regioes[i])
                    # Se o retorno da funcao e nulo, nao ha vertice que essa regiao pode anexar, por isso olha-se a proxima
                    if(viz != None):
                        # Se nao for nulo, adiciona na regiao i
                        self.regioes[i].adiciona(viz)
                        self.vertices[viz.cod].regiao = self.regioes[i].cod
                        # E para a execucao do while
                        continua = False
                    i += 1
    
    # Verifica se ha vertices sem regiao
    def acabou (self):
        for vertice in self.vertices:
            if(vertice.regiao == None):
                return False
        return True
    
    
    # Gera as k regioes iniciais
    def criaRegioes(self):
        # As primeiras regioes sao os vertices de maior peso
        maiores = self.pegaMaiores()
        regioes = []
        cod = 1
        # Percorre a lista com os k maiores vertices criando uma regiao para cada
        for vertice in maiores:
            reg = Regiao(cod, vertice)
            self.vertices[vertice.cod].regiao = reg.cod
            cod += 1
            regioes.append(reg)
        return regioes

    
    # Calcula a distancia entre dois vertices no plano cartesiano
    def dist(self, v1, v2):
        return sqrt(((v1.coordX - v2.coordX)*(v1.coordX - v2.coordX)) + ((v1.coordY - v2.coordY)*(v1.coordY - v2.coordY)))    

    
    
    
    # Ordena os vertices em ordem decrescente
    # Critérios:
    #   1 - Maior peso
    #   2 - Maior grau
    def selectionSort(self, itens):
        vertices = []
        for v in itens:
            vertices.append(v)
        for i in range(len(vertices) - 1, 0, -1):
            posMaior = 0
            for j in range(1, i + 1):
                if vertices[j].peso > vertices[posMaior].peso:
                    posMaior = j
                elif vertices[j].peso == vertices[posMaior].peso:
                    if vertices[j].grau > vertices[posMaior].grau:
                        posMaior = j
                    
            aux = vertices[i]
            vertices[i] = vertices[posMaior]
            vertices[posMaior] = aux
        return vertices
    
    
    
    # Ordena os vertices em ordem decrescente
    # Critérios:
    #   1 - Maior peso
    #   2 - Maior grau
    def selectionSort2(self, itens):
        vertices = []
        for v in itens:
            vertices.append(v)
        for i in range(len(vertices) - 1, 0, -1):
            posMenor = 0
            for j in range(1, i + 1):
                if vertices[j].peso < vertices[posMenor].peso:
                    posMenor = j
                elif vertices[j].peso == vertices[posMenor].peso:
                    if vertices[j].grau > vertices[posMenor].grau:
                        posMenor = j
                    
            aux = vertices[i]
            vertices[i] = vertices[posMenor]
            vertices[posMenor] = aux
        return vertices
    
    # Pega os k menores vertices (Onde k e' o numero de regioes)
    def pegaMenores(self):
        # Ordena os vertices em ordem crescente
        ordenado = self.selectionSort(self.vertices)
        menores = []
        for i in range(self.numReg):
            if(ordenado[i].regiao == None):         #depois tenta tirar
                menores.append(ordenado[i])
                
            else:
                print("DEU RUIM PA DEDEU")
        return menores
        
    
    
    # Pega os k maiores vertices (Onde k e' o numero de regioes)
    def pegaMaiores(self):
        # Ordena os vertices em ordem decrescente
        ordenado = self.selectionSort2(self.vertices)
        maiores = []
        for i in range(self.numReg):
            if(ordenado[i].regiao == None):         #depois tenta tirar
                maiores.append(ordenado[i])
            else:
                print("DEU RUIM PA DEDEU")
        return maiores
    
    
    def floydWarshall(self):                
        resultados = []
        for regiao in self.regioes:
            matriz = []
            for i in range(len(regiao.vert)):
                vetor = []
                for j in range(len(regiao.vert)):
                    if((regiao.vert[j] in regiao.vert[i].vizinhos) or (regiao.vert[i] in regiao.vert[j].vizinhos)):
                        vetor.append(self.dist(regiao.vert[i], regiao.vert[j]))
                        
                    else:
                        vetor.append(INFINITO)
                matriz.append(vetor)

            
        
            for k in range(len(regiao.vert)):
                    for i in range(len(regiao.vert)):
                        for j in range(len(regiao.vert)):
                            if(matriz[i][j] > (matriz[i][k] + matriz[k][j])):
                                    matriz[i][j] = matriz[i][k] + matriz[k][j]


            resultados.append((regiao.cod, matriz))
        return resultados
    
    # Calcula o diametro de cada regiao
    def pegaDiametros(self):
        # Calcula a menor distancia de todos para todos
        distancias = self.floydWarshall()
        resultados = []
        # Para cada regiao, busca-se a maior das menores distancias calculadas
        for distancia in distancias:
            maior = distancia[1][0][0]
            for i in range(len(distancia[1][0])):
                for j in range(len(distancia[1][0])):
                    if((i != j) and (distancia[1][i][j] != INFINITO) and (maior < distancia[1][i][j])):
                        maior = distancia[1][i][j]
            
            item = (distancia[0], maior)
            resultados.append(item)
        return resultados
    
    # Pega o menor diametro entre as regioes
    def minDiametro(self):
        # Calcula todos os diametros
        diametros = self.pegaDiametros()
        menor = diametros[0][1]
        # Busca o menor deles
        for diametro in diametros:
            if(diametro[1] < menor):
                menor = diametro[1]
        return menor
    
    
    # Melhora a distribuicao das regioes calculadas
    def melhoraGrafo(self):
        for i in range(len(self.regioes)):
            # Ordena as regioes em ordem decrescente
            self.regioes = self.selectionSort2(self.regioes)
            tam = len(self.regioes)
            # Para cada regiao
            for i in range(tam):
                reg = self.regioes[i]
                aux = dict(reg.vertices)
                # Para cada vertice da regiao
                for v in aux:
                    vertice = aux[v]
                    # Para cada vizinho do vertice
                    for viz in vertice.vizinhos:
                        # Se o vizinho pertence a outra regiao
                        if(viz.cod not in reg.vertices):
                            # Busca a regiao desse vizinho
                            posR2 = self.buscaRegiao(viz.cod)
                            # Se, ao transferir o vizinho para a regiao atual o peso dessa regiao continuar
                            # menor ou igual ao peso da regiao do vertice
                            if(reg.peso + viz.peso <= self.regioes[posR2].peso - viz.peso):
                                # Remove o vizinho de sua regiao e testa se tal regiao manteve conexa
                                if(self.regioes[posR2].remove(viz)):
                                    # Se manteve a conexidade, insere o vizinho na regiao atual
                                    viz.regiao = self.regioes[i].cod
                                    self.regioes[i].adiciona(viz)
                                    tam += 1
                                else:
                                    # Senao, insere o vizinho na sua regiao antiga
                                    viz.regiao = self.regioes[posR2].cod
                                    self.regioes[posR2].adiciona(viz)
    
    
    
    # Busca a regiao de um vertice a partir de seu codigo
    def buscaRegiao(self, cod):
        for i in range (len(self.regioes)):
            if(cod in self.regioes[i].vertices):
                return i
