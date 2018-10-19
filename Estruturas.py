# -*- coding: UTF-8 -*-

class Vertice:
    cod = None              # Codigo do vertice
    codNaRegiao = None
    regiao = None           # Regiao que o vertice pertence
    vizinhos = None         # Vizinhos do vertice
    grau = None             # Grau do vertice
    c = None                # Parametro Clientes
    w = None                # Parametro Carga de Trabalho
    d = None                # Parametro Demanda
    peso = None             # Peso = C + W + D
    coordX = None           # Coordenada X no plano cartesiano
    coordY = None           # Coordenada Y no plano cartesiano
    
    
    # Construtor do vertice
    def __init__(self, cod, cX, cY, consumidores, demanda, cargaTrab):
        self.cod = cod
        self.coordX = cX
        self.coordY = cY
        self.vizinhos = []
        self.grau = 0
        self.c = consumidores
        self.d = demanda
        self.w = cargaTrab
        self.peso = self.c + self.w + self.d
    
    

class Regiao:
    cod = None          # Codigo da regiao
    vertices = None     # Vetor de vertices
    vert = None         # Vetor auxiliar utilizado para montar matrizes de adjacencia
    peso = None         # Peso acumulado (mediaC + mediaD + mediaW)
    vizinhos = None     # Vizinhos da regiao
    grau = None         # Grau da regiao
    mediaC = None       # Soma acumulada do parametro 'C' de todos os vertices da reigao
    mediaW = None       # Soma acumulada do parametro 'W' de todos os vertices da reigao
    mediaD = None       # Soma acumulada do parametro 'D' de todos os vertices da reigao
    
    # Cria uma regiao a partir de um vertice
    def __init__(self, cod, vertice):
        self.cod = cod
        self.peso = vertice.peso
        self.vertices = {}
        self.vert = []
        self.vertices[vertice.cod] = vertice
        self.vert.append(vertice)
        self.vizinhos = []
        for vizinho in vertice.vizinhos:
            self.vizinhos.append(vizinho)
        self.grau = vertice.grau
        self.mediaC = float(vertice.c)
        self.mediaW = float(vertice.w)
        self.mediaD = float(vertice.d)
    
    # Adiciona um vertice à regiao
    def adiciona (self, vertice):
        # Insere o vertice e atualiza os pesos
        self.vertices[vertice.cod] = vertice
        self.vert.append(vertice)
        self.peso += vertice.peso
        self.mediaC += vertice.c
        self.mediaW += vertice.w
        self.mediaD += vertice.d
        
        # Faz a uniao dos vizinhos, excluindo aqueles que fazem parte da subregiao
        for vizinho in vertice.vizinhos:
            if (not(self.jaEhVizinho(vizinho)) and not(vizinho.cod in self.vertices) and (vizinho.regiao == None)):
                self.vizinhos.append(vizinho)
        
        
        # Exclui o vertice inserido da lista de vizinhos
        for i in range(len(self.vizinhos)):
            vizinho = self.vizinhos[i]
            if(vizinho.cod == vertice.cod):
                del self.vizinhos[i]
                self.grau = len(self.vizinhos)
                return
        
        # Ajusta o grau da regiao
        self.grau = len(self.vizinhos)
        
    
    # Verifica se um vertice ja e vizinho da regiao
    def jaEhVizinho(self, vizinho):
        for v in self.vizinhos:
            if(v.cod == vizinho.cod):
                return True
        return False

    # Checa a conexidade de um grafo
    def checaConexao(self):
        # Se houver um unico vertice, e' conexo
        if(len(self.vertices) == 1):
            return True
        
        # Monta uma matriz de adjacencia com True, caso dois vertices sejam vizinhos e False, caso contrario
        matriz = []
        for i in range(len(self.vert)):
            vetor = []
            for j in range(len(self.vert)):
                if((self.vert[j] in self.vert[i].vizinhos) or (self.vert[i] in self.vert[j].vizinhos)):
                    vetor.append(True)
                else:
                    vetor.append(False)
            matriz.append(vetor)

        
        # Aplica Warshall na matriz
        for k in range(len(self.vert)):
            for i in range(len(self.vert)):
                for j in range(len(self.vert)):
                    matriz[i][j] = (matriz[i][j])  or (matriz[i][k] and matriz[k][j])
        
        # Se houver ao menos False, significa que ha desconexao
        for i in range(len(self.vert)):
            for j in range(len(self.vert)):
                if (not(matriz[i][j])):
                    return False
        
        # Senao o grafo e' conexo
        return True

    # Remove um vertice de uma regiao
    def remove(self, v):
        # Ajusta os pesos
        self.peso -= v.peso
        self.mediaC -= v.c
        self.mediaD -= v.d
        self.mediaW -= v.w
        
        # Remove o vertice da lista de vertices
        del self.vertices[v.cod]
        tam =  len(self.vert)
        
        i = 0
        # Busca no vetor auxiliar (vert)
        while (i < tam):
            if (v.cod == self.vert[i].cod):
                del self.vert[i]
                tam -= 1
                i -= 1
            i += 1
        if(self.checaConexao()):
            self.vizinhos.append(v)
            i = 0
            while(i < len(v.vizinhos)):
                achou = False
                viz = v.vizinhos[i]
                j = 0
                while(not(achou) and j < len(viz.vizinhos)):
                    vizDoViz = viz.vizinhos[j]
                    if((v.cod != vizDoViz.cod) and (vizDoViz.cod in self.vertices)):
                        achou = True
                    j += 1
                if(viz.cod not in self.vertices and  not(achou)):
                    j = 0
                    while(not(achou) and j < (len(self.vizinhos))):
                        if(viz.cod == self.vizinhos[j].cod):
                            del self.vizinhos[j]
                            achou = True
                            j -= 1
                        j += 1
                i += 1
            
            self.grau = len(self.vizinhos)
            
            return True
        
        self.grau = len(self.vizinhos)
        return False





