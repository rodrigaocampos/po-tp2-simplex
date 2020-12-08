
import numpy as np

# gera uma matriz vazia com tamanho adequado para variaveis e restrições.
def gera_matriz(variavel,restricao):
    tab = np.zeros((restricao+1, variavel+restricao+2))
    return tab

# verifica a coluna mais à direita para valores negativos ACIMA da última linha. Se existirem valores negativos, outro pivô é necessário
def verifica_coluna_direita(tabela):
    m = min(tabela[:-1,-1])
    if m>= 0:
        return False
    else:
        return True

# verifica se a linha inferior, excluindo a coluna final, tem valores negativos. Se existirem valores negativos, outro pivô é necessário.
def verifica_linha_abaixo(tabela):
    numero_de_linhas = len(tabela[:,0])
    m = min(tabela[numero_de_linhas-1,:-1])
    if m>=0:
        return False
    else:
        return True

# Semelhante à função verifica_coluna_direita, mas retorna o índice da linha do elemento negativo na coluna mais à direita
def verifica_negativo_direita(tabela):
    numero_de_coluna = len(tabela[0,:])
    # pesquisa cada linha (excluindo a última linha) na coluna final para o valor mínimo
    m = min(tabela[:-1,numero_de_coluna-1])
    if m<=0:
        # n = índice de linha de m localização
        n = np.where(tabela[:-1,numero_de_coluna-1] == m)[0][0]
    else:
        n = None
    return n

# retorna o índice da coluna do elemento negativo na linha inferior
def verifica_negativo(tabela):
    numero_de_linhas = len(tabela[:,0])
    m = min(tabela[numero_de_linhas-1,:-1])
    if m<=0:
        # n = índice de linha para m
        n = np.where(tabela[numero_de_linhas-1,:-1] == m)[0][0]
    else:
        n = None
    return n

# localiza o elemento pivô no quadro para remover o elemento negativo da coluna mais à direita.
def localiza_pivo_direita(tabela):
        total = []
        # r = índice de linha de entrada negativa
        r = verifica_negativo_direita(tabela)
        # encontra todos os elementos na linha, r, excluindo a coluna final
        linha = tabela[r,:-1]
        # encontra o valor mínimo na linha (excluindo a última coluna)
        m = min(linha)
        # c = índice de coluna para entrada mínima na linha
        c = np.where(linha == m)[0][0]
        # todos os elementos na coluna
        coluna = tabela[:-1,c]
        # precisa passar por esta coluna para encontrar a menor razão positiva
        for i, b in zip(coluna,tabela[:-1,-1]):
            # i não pode ser igual a 0 e b / i deve ser positivo.
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # espaço reservado para elementos que não atenderam aos requisitos acima. Caso contrário, nosso número de índice estaria com defeito.
                total.append(0)
        elemento = max(total)
        for t in total:
            if t > 0 and t < elemento:
                elemento = t
            else:
                continue

        indice = total.index(elemento)
        return [indice,c]
# processo semelhante, retorna um elemento de matriz específico para ser dinamizado.
def localiza_pivo(tabela):
    if verifica_linha_abaixo(tabela):
        total = []
        n = verifica_negativo(tabela)
        for i,b in zip(tabela[:-1,n],tabela[:-1,-1]):
            if i**2>0 and b/i>0:
                total.append(b/i)
            else:
                # espaço reservado para elementos que não atenderam aos requisitos acima. Caso contrário, nosso número de índice estaria com defeito.
                total.append(0)
        elemento = max(total)
        for t in total:
            if t > 0 and t < elemento:
                elemento = t
            else:
                continue

        indice = total.index(elemento)
        return [indice,n]

# Recebe a entrada de string e retorna uma lista de números a serem organizados no quadro
def converte(eq):
    eq = eq.split(',')
    if 'G' in eq:
        g = eq.index('G')
        del eq[g]
        eq = [float(i)*-1 for i in eq]
        return eq
    if 'L' in eq:
        l = eq.index('L')
        del eq[l]
        eq = [float(i) for i in eq]
        return eq

# A linha final do quadro em um problema mínimo é o oposto de um problema de maximização, então os elementos são multiplicados por (-1)
def converte_min(tabela):
    tabela[-1,:-2] = [-1*i for i in tabela[-1,:-2]]
    tabela[-1,-1] = -1*tabela[-1,-1]
    return tabela

# gera x1, x2, ... xn para o número variaveliável de variaveliáveis.
def gen_variavel(tabela):
    numero_de_coluna = len(tabela[0,:])
    numero_de_linhas = len(tabela[:,0])
    variavel = numero_de_coluna - numero_de_linhas -1
    v = []
    for i in range(variavel):
        v.append('x'+str(i+1))
    return v

# gira o quadro de modo que os elementos negativos sejam removidos da última linha e última coluna
def pivo(linha,coluna,tabela):
    # núemro de linhas
    numero_de_linhas = len(tabela[:,0])
    # número de coluna
    numero_de_coluna = len(tabela[0,:])
    t = np.zeros((numero_de_linhas,numero_de_coluna))
    pr = tabela[linha,:]
    if tabela[linha,coluna]**2>0: # novo
        e = 1/tabela[linha,coluna]
        r = pr*e
        for i in range(len(tabela[:,coluna])):
            k = tabela[i,:]
            c = tabela[i,coluna]
            if list(k) == list(pr):
                continue
            else:
                t[i,:] = list(k-r*c)
        t[linha,:] = list(r)
        return t
    else:
        print('não da pra girar.')

# verifica se há espaço na matriz para adicionar outra restrição
def add_restricao(tabela):
    numero_de_linhas = len(tabela[:,0])
    # quero saber se existem pelo menos 2 linhas de todos os elementos zero
    vazio = []
    # iterar em cada linha
    for i in range(numero_de_linhas):
        total = 0
        for j in tabela[i,:]:
            # use o valor quadrado para que (-x) e (+ x) não se cancelem
            total += j**2
        if total == 0:
            # acrescente zero à lista SOMENTE se todos os elementos em uma linha forem zero
            vazio.append(total)
    # Existem pelo menos 2 linhas com todos os elementos zero se o seguinte for verdadeiro
    if len(vazio)>1:
        return True
    else:
        return False

# adiciona uma restrição à matriz
def restricao(tabela,eq):
    if add_restricao(tabela) == True:
        numero_de_coluna = len(tabela[0,:])
        numero_de_linhas = len(tabela[:,0])
        variavel = numero_de_coluna - numero_de_linhas -1
        # configurar contador para iterar através do comprimento total das linhas
        j = 0
        while j < numero_de_linhas:
            # Iterar por linha
            linha_ok = tabela[j,:]
            # o total será a soma das entradas na linha
            total = 0
            # Encontre a primeira linha com todas as 0 entradas
            for i in linha_ok:
                total += float(i**2)
            if total == 0:
                # Encontramos a primeira linha com todas as entradas zero
                linha = linha_ok
                break
            j +=1

        eq = converte(eq)
        i = 0
        # iterar através de todos os termos na função de restrição, excluindo o último
        while i<len(eq)-1:
            # atribuir valores de linha de acordo com a equação
            linha[i] = eq[i]
            i +=1
        #linha[len(eq)-1] = 1
        linha[-1] = eq[-1]

        # adicione a variaveliável de folga de acordo com a localização no quadro.
        linha[variavel+j] = 1
    else:
        print('Não pode add outra restrição')

# verifica para determinar se uma função objetivo pode ser adicionada à matriz
def add_obj(tabela):
    numero_de_linhas = len(tabela[:,0])
    # quero saber se existe exatamente uma linha de todos os elementos zero
    vazio = []
    # iterar em cada linha
    for i in range(numero_de_linhas):
        total = 0
        for j in tabela[i,:]:
            # use o valor quadrado para que (-x) e (+ x) não se cancelem
            total += j**2
        if total == 0:
            # acrescente zero à lista SOMENTE se todos os elementos em uma linha forem zero
            vazio.append(total)
    # Existe exatamente uma linha com todos os elementos zero se o seguinte for verdadeiro
    if len(vazio)==1:
        return True
    else:
        return False

# adiciona a função objetivo à matriz.
def obj(tabela,eq):
    if add_obj(tabela)==True:
        eq = [float(i) for i in eq.split(',')]
        numero_de_linhas = len(tabela[:,0])
        linha = tabela[numero_de_linhas-1,:]
        i = 0
    # iterar através de todos os termos na função de restrição, excluindo o último
        while i<len(eq)-1:
            # atribuir valores de linha de acordo com a equação
            linha[i] = eq[i]*-1
            i +=1
        linha[-2] = 1
        linha[-1] = eq[-1]
    else:
        print('Você deve terminar de adicionar restrições antes que a função objetivo possa ser adicionada.')

# resolva o problema de maximização para uma solução ótima, retorna o dicionário com as teclas / x1, x2 ... xn e max.
def maximiza(tabela, saida='resumo'):
    while verifica_coluna_direita(tabela)==True:
        tabela = pivo(localiza_pivo_direita(tabela)[0],localiza_pivo_direita(tabela)[1],tabela)
    while verifica_linha_abaixo(tabela)==True:
        tabela = pivo(localiza_pivo(tabela)[0],localiza_pivo(tabela)[1],tabela)

    numero_de_coluna = len(tabela[0,:])
    numero_de_linhas = len(tabela[:,0])
    variavel = numero_de_coluna - numero_de_linhas -1
    i = 0
    val = {}
    for i in range(variavel):
        coluna = tabela[:,i]
        s = sum(coluna)
        m = max(coluna)
        if float(s) == float(m):
            loc = np.where(coluna == m)[0][0]
            val[gen_variavel(tabela)[i]] = tabela[loc,-1]
        else:
            val[gen_variavel(tabela)[i]] = 0
    val['max'] = tabela[-1,-1]
    for k,v in val.items():
        val[k] = round(v,6)
    if saida == 'tabela':
        return tabela
    else:
        return val

# resolva problemas de minimização para uma solução ótima, retorna dicionário com as teclas / x1, x2 ... xn e min.
def minimiza(tabela, saida='resumo'):
    tabela = converte_min(tabela)

    while verifica_coluna_direita(tabela)==True:
        tabela = pivo(localiza_pivo_direita(tabela)[0],localiza_pivo_direita(tabela)[1],tabela)
    while verifica_linha_abaixo(tabela)==True:
        tabela = pivo(localiza_pivo(tabela)[0],localiza_pivo(tabela)[1],tabela)

    numero_de_coluna = len(tabela[0,:])
    numero_de_linhas = len(tabela[:,0])
    variavel = numero_de_coluna - numero_de_linhas -1
    i = 0
    val = {}
    for i in range(variavel):
        coluna = tabela[:,i]
        s = sum(coluna)
        m = max(coluna)
        if float(s) == float(m):
            loc = np.where(coluna == m)[0][0]
            val[gen_variavel(tabela)[i]] = tabela[loc,-1]
        else:
            val[gen_variavel(tabela)[i]] = 0
    val['min'] = tabela[-1,-1]*-1
    for k,v in val.items():
        val[k] = round(v,6)
    if saida == 'tabela':
        return tabela
    else:
        return val

if __name__ == "__main__":

    m = gera_matriz(4,3)
    restricao(m,'1,1,1,1,L,15')
    restricao(m,'7,5,3,2,L, 120')
    restricao(m,'3,5,10,15,L,100')
    obj(m,'4,5,9,11,0')
    print(maximiza(m))


