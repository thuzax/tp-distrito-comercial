# -*- coding: UTF-8 -*- #
from Estruturas import Vertice
from Grafo import *
import sys

def calcDispersao(lamb, beta, media):
    aux1 = ((1-lamb) * beta) - media
    if(aux1 < 0):
        aux1 = 0
    aux2 = media - ((1+lamb) * beta)
    if(aux2 <0):
        aux2 = 0
    return (aux1 + aux2)


def main():
    nomeArq = sys.argv[1]
    arquivo = open(nomeArq, 'r')
    linhas = arquivo.read().splitlines()    # leitura do arquivo, separando as linhas
    g = BeerHouse() 
    
    #leitura dos vertices#
    for i in range(int(linhas[0])):
        unidade_ref = linhas[i+1].split()
        vertice = Vertice(int(unidade_ref[0]), float(unidade_ref[1]), float(unidade_ref[2]), int(unidade_ref[3]), int(unidade_ref[4]), int(unidade_ref[5]))
        g.adiciona(vertice)
    ######################
    
    # for vertice in g.vertices:
    #     print(str(vertice.cod) + " " + str(vertice.c) + " " + str(vertice.d) + " " + str(vertice.w) + " " + str(vertice.peso))
    
    #leitura das arestas#
    linhaAtual = int(linhas[0]) + 1                     # para encontra a linha certa, 
    for i in range(int(linhas[linhaAtual])):            # somamos a quantidade de vertices + 1 
        aresta = linhas[linhaAtual + i + 1].split()     # (pois cada vertice ocupa uma linha + 1 da primeira linha)
        v1 = g.vertices[int(aresta[0])]
        v2 = g.vertices[int(aresta[1])]
        g.liga(v1, v2)
    #####################
    
    # for vertice in g.vertices:
    #     print("-------------------------")
    #     print(str(vertice.cod))
    #     print("olha os vizinhos aew")
    #     for vizinho in vertice.vizinhos:
    #         print(vizinho.cod)
            
    #leitura dos dados do problema#
    linhaAtual = int(linhas[linhaAtual]) + int(linhas[0]) + 2   # para encontrar a linha certa somamos
    dados = linhas[linhaAtual].split()                          # qnt vertices + qnt aresta + 2
    g.numReg = int(dados[0])                              # pois cada dado ocupa uma linha + 2 das linhas que
    g.lambC = float(dados[1])                     # cont?m a qnt de arestas e a qnt de vertices
    g.lambD = float(dados[2])
    g.lambW = float(dados[3])
    ##############################
    
    
    
    # Calcula a media ideal de cada parametro
    g.calcBeta()
    
    
    # Divide as regioes do grafo
    g.divideRegioes()
    
    
    
    for regiao in g.regioes:
        for i in range(len(regiao.vert)):
            regiao.vert[i].codNaRegiao = i
    
    
    d = 0
    c = 0
    w = 0
    
    # Calcula o quao distante os valores estao no intervalo utilizando a formula passada no enunciado
    for reg in g.regioes:
        d += calcDispersao(g.lambD, g.betaD, reg.mediaD)
        c += calcDispersao(g.lambC, g.betaC, reg.mediaC)
        w += calcDispersao(g.lambW, g.betaW, reg.mediaW)
    
    soma = d + c + w
    # Se o somatorio dispersao nao for 0, entao a solucao nao e' viavel
    if (soma > 0):
        # Caso nao seja viavel, tenta-se melhorar a solucao
        g.melhoraGrafo()
        
        d = 0
        c = 0
        w = 0
        
        # Recalcula as dispersoes
        for reg in g.regioes:
            d += calcDispersao(g.lambD, g.betaD, reg.mediaD)
            c += calcDispersao(g.lambC, g.betaC, reg.mediaC)
            w += calcDispersao(g.lambW, g.betaW, reg.mediaW)
        
        soma = d + c + w
        # Se a soma continuar sendo maior que 0, a solucao fica como inviavel
        if (soma > 0):
            qtdConexa = 0
            # Calcula a quantidade de regioes conexas
            for reg in g.regioes:
                if(reg.checaConexao()):
                    qtdConexa += 1
            # Imprime os resultados
            print("Solucao inviavel\n" + str(qtdConexa) + " Regioes conexas\n" + str(soma))
        else:
            # Caso se torne viavel, imprime os dados pedidos
            print("Solucao viavel\n" + str(g.minDiametro()))
    else:
        # Caso seja viavel imprime os dados pedidos
        print("Solucao viavel\n" + str(g.minDiametro()))
    
main()
