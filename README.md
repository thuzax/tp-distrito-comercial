# tp-distrito-comercial

Trabalho desenvolvido para solucionar o problema do distrito comercial na disciplina de Algoritmos em Grafos.

## Execução do programa

Para executar o programa digite o seguinte comando no diretório raiz do projeto:
       
        python3 Main.py <arquivo-de-entrada>

Onde o <arquivo-de-entrada> é a instância estruturada no formato abaixo.

## Estrutura do arquivo de entrada

O primeiro item a ser colocado no arquivo é a quantidade de vértices. Após isso devem ser listados todos os vértices e seus dados.
Depois, vem a quantidade de arestas e a lista com os vértices que compõem as arestas.
Por fim têm-se a quantidade de regiões e os valores para cálculo de factibilidade.
As instâncias de exemplo estão no diretório "instances".

número de unidades de referência
id_unidade_referencia coord_x coord_y consumidores_unid_ref demanda_unid_ref carga_trabalho_unid_ref
...

quantidade_arestas
unid_i unid_j (indica que, no grafo, a unidade i liga à unidade j)
...

qtde_regioes lambda_consumidores lambda_demanda lambda_carga_trabalho

## Desenvolvedores

Arthur Henrique Sousa Cruz (github: thuzax)
João Pedro Teodoro Silva (github: joaopedroteo)
Pedro Silveira Lopes (github: silventino)

