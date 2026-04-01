# =============================================================================
# Aplicação: CaronaMack - Otimização de Rotas na Malha Viária de São Paulo
# =============================================================================
# Disciplina: Teoria dos Grafos - Turma 6G
# Professor:  Prof. Dr. Ivan Carlos Alcântara de Oliveira
# Instituição: Universidade Presbiteriana Mackenzie
# Faculdade de Computação e Informática
#
# Integrantes do Grupo:
#   - Daniela Pereira       RA: 10410906
#   - Eduardo Takashi        RA: 10417877
#   - Ricardo Lins Pires     RA: 10419394
#
# Síntese do Conteúdo:
#   Modelagem da malha viária da região Centro-Zona Leste de São Paulo
#   como um grafo orientado e ponderado (Tipo 6), com 80 vértices
#   (cruzamentos) e 210 arestas (vias com distâncias em km). Implementa
#   um menu completo para manipulação do grafo e análise de conexidade
#   por meio do algoritmo FCONEX.
#
# Linguagem: Python 3
#
# Histórico de Alterações:
#   2026-03-22 | Daniela Pereira   | Criação da estrutura base herdando da
#                                    classe Grafo do professor (grafoLista.py).
#                                    Implementação da leitura do grafo.txt,
#                                    suporte a pesos e rótulos nos vértices.
#   2026-03-22 | Eduardo Takashi   | Implementação das opções de gravação (b),
#                                    inserção de vértice (c) e aresta (d),
#                                    remoção de vértice (e) e aresta (f).
#                                    Correção do bug de reindexação em (e).
#   2026-03-22 | Ricardo Lins Pires| Implementação do algoritmo FCONEX para
#                                    análise de conexidade (opção i), conforme
#                                    pseudocódigo do Prof. Ivan Carlos.
#                                    Implementação do grafo reduzido e
#                                    classificação C0/C1/C2/C3.
#   2026-03-31 | Daniela Pereira   | Adição da flag carregado para controle
#                                    de fluxo do menu. Proteção de todas as
#                                    opções contra uso antes da leitura (a).
#                                    Tratamento de arquivo não encontrado.
# =============================================================================


import sys

class Grafo:
    TAM_MAX_DEFAULT = 100  # qtde de vértices máxima default

    # construtor da classe grafo
    def __init__(self, n=TAM_MAX_DEFAULT):
        self.n = n       # número de vértices
        self.m = 0       # número de arestas
        # lista de adjacência
        self.listaAdj = [[] for i in range(self.n)]

    # Insere uma aresta no Grafo tal que v é adjacente a w
    def insereA(self, v, w):
        self.listaAdj[v].append(w)
        self.m += 1

    # remove uma aresta v->w do Grafo
    def removeA(self, v, w):
        self.listaAdj[v].remove(w)
        self.m -= 1

    # Apresenta o Grafo contendo número de vértices, arestas
    # e a LISTA de adjacência obtida
    def show(self):
        print(f"\n n: {self.n:2d} ", end="")
        print(f"m: {self.m:2d}")
        for i in range(self.n):
            print(f"\n{i:2d}: ", end="")
            for w in range(len(self.listaAdj[i])):
                val = self.listaAdj[i][w]
                print(f"{val:2d}", end="")
        print("\n\nfim da impressao do grafo.")

class GrafoCarona(Grafo):

    def __init__(self, n=Grafo.TAM_MAX_DEFAULT):
        # Chama o construtor da classe base (Prof. Ivan)
        super().__init__(n)
        self.tipo      = 6     # orientado com peso na aresta
        self.rotulos   = []    # lista de strings: nome de cada cruzamento
        self.carregado = False # indica se o arquivo foi lido ao menos 1x


    def _checar_carregado(self):
        """
        Verifica se o grafo foi carregado do arquivo.
        Retorna True se ok, False se não foi carregado ainda.
        """
        if not self.carregado:
            print("  ⚠️  Grafo não carregado. Use a opção (a) primeiro.")
            return False
        return True

    def insereA(self, v, w, peso=1.0):
        # Verifica se aresta já existe
        for (viz, _) in self.listaAdj[v]:
            if viz == w:
                return  # já existe, não duplica
        self.listaAdj[v].append((w, peso))
        self.m += 1

    def removeA(self, v, w):
        for item in self.listaAdj[v]:
            if item[0] == w:
                self.listaAdj[v].remove(item)
                self.m -= 1
                return

    def show(self):
        if not self._checar_carregado(): return
        print("\n" + "=" * 65)
        print("  LISTA DE ADJACÊNCIA")
        print(f"  n: {self.n}  m: {self.m}")
        print("=" * 65)
        for i in range(self.n):
            rotulo = self.rotulos[i] if i < len(self.rotulos) else f"Vértice {i}"
            print(f"\n  [{i:>2}] {rotulo}")
            if self.listaAdj[i]:
                for (w, peso) in self.listaAdj[i]:
                    rot_w = self.rotulos[w] if w < len(self.rotulos) else f"Vértice {w}"
                    print(f"        → [{w:>2}] {rot_w}  ({peso:.1f} km)")
            else:
                print("        (sem arestas de saída)")
        print("\nfim da impressao do grafo.")
        print("=" * 65)

    # OPÇÃO A
    def carregar(self, arquivo="grafo.txt"):
        try:
            arq = open(arquivo, "r", encoding="utf-8")
        except FileNotFoundError:
            print(f"  ❌ Arquivo '{arquivo}' não encontrado.")
            return
        with arq as f:
            self.tipo = int(f.readline().strip())
            self.n    = int(f.readline().strip())

            # Reinicia estruturas
            self.listaAdj = [[] for _ in range(self.n)]
            self.rotulos  = []
            self.m        = 0

            # Lê vértices: id "rotulo" peso_vertice
            for _ in range(self.n):
                linha = f.readline().strip()
                parts = linha.split('"')
                # parts[0] = "id ", parts[1] = rótulo, parts[2] = " peso"
                rotulo = parts[1]
                self.rotulos.append(rotulo)

            # Lê arestas: u v peso
            qtd_arestas = int(f.readline().strip())
            for _ in range(qtd_arestas):
                linha = f.readline().strip()
                u, v, p = map(float, linha.split())
                u, v = int(u), int(v)
                self.insereA(u, v, p)  # usa o insereA sobrescrito

        self.carregado = True
        print(f"✅ Grafo carregado com sucesso! {self.n} vértices e {self.m} arestas.")

    # OPÇÃO B — Gravar dados no arquivo grafo.txt

    def salvar(self, arquivo="grafo.txt"):
        """
        Salva o estado atual do grafo no arquivo.
        O formato de gravação é idêntico ao de leitura.
        """
        if not self._checar_carregado(): return
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(f"{self.tipo}\n")
            f.write(f"{self.n}\n")
            # Grava vértices
            for i in range(self.n):
                rotulo = self.rotulos[i] if i < len(self.rotulos) else f"Vertice {i}"
                f.write(f'{i} "{rotulo}" 0\n')
            # Grava arestas
            f.write(f"{self.m}\n")
            for u in range(self.n):
                for (v, peso) in self.listaAdj[u]:
                    f.write(f"{u} {v} {peso}\n")
        print("✅ Arquivo grafo.txt salvo com sucesso!")

    # OPÇÃO C — Inserir vértice

    def inserirVertice(self):
        """
        Adiciona novo vértice com ID automático (n atual)
        e rótulo informado pelo usuário.
        Expande listaAdj e rotulos mantendo consistência.
        """
        if not self._checar_carregado(): return
        nome = input("  Nome do novo cruzamento: ").strip()
        if not nome:
            print("  ❌ Nome não pode ser vazio.")
            return
        self.listaAdj.append([])   # nova lista de adjacência vazia
        self.rotulos.append(nome)  # novo rótulo
        novo_id = self.n
        self.n += 1
        print(f"  ✅ Vértice {novo_id} inserido!")

    # OPÇÃO D — Inserir aresta

    def inserirAresta(self):

        if not self._checar_carregado(): return
        try:
            u = int(input("  Origem (número do vértice): "))
            v = int(input("  Destino (número do vértice): "))
            p = float(input("  Distância em km: "))
            if 0 <= u < self.n and 0 <= v < self.n:
                # Verifica se já existe
                for (viz, _) in self.listaAdj[u]:
                    if viz == v:
                        print(f"  ⚠️  Aresta {u}→{v} já existe.")
                        return
                self.insereA(u, v, p)
                print("  ✅ Aresta inserida!")
            else:
                print("  ❌ Vértice inválido!")
        except ValueError:
            print("  ❌ Entrada inválida. Digite apenas números.")
            
    # OPÇÃO E — Remover vértice

    def removerVertice(self):
        """
        Remove um vértice e todas as arestas que o envolvem.
        Reajusta os índices de listaAdj e rotulos para manter
        sequência contínua (0, 1, 2, ...).
        """
        if not self._checar_carregado(): return
        try:
            u = int(input("  Vértice a remover: "))
            if 0 <= u < self.n:
                # Remove lista de adjacência e rótulo do vértice u
                del self.listaAdj[u]
                del self.rotulos[u]

                # Para cada vértice restante:
                # remove arestas que apontavam para u
                # e reajusta índices dos destinos (k > u → k-1)
                nova_lista = []
                for i in range(len(self.listaAdj)):
                    nova_adj_i = []
                    for (k, peso) in self.listaAdj[i]:
                        if k == u:
                            self.m -= 1  # aresta removida
                            continue     # descarta essa aresta
                        novo_k = k - 1 if k > u else k
                        nova_adj_i.append((novo_k, peso))
                    nova_lista.append(nova_adj_i)
                self.listaAdj = nova_lista

                # Remove as arestas que saíam de u do contador
                # (já foram descartadas ao deletar listaAdj[u])
                self.n -= 1
                print("  ✅ Vértice removido!")
            else:
                print("  ❌ Vértice inválido!")
        except ValueError:
            print("  ❌ Entrada inválida.")

    # OPÇÃO F — Remover aresta

    def removerAresta(self):

        if not self._checar_carregado(): return
        try:
            u = int(input("  Origem: "))
            v = int(input("  Destino: "))
            if 0 <= u < self.n:
                for (viz, _) in self.listaAdj[u]:
                    if viz == v:
                        self.removeA(u, v)
                        print("  ✅ Aresta removida!")
                        return
                print("  ❌ Aresta não encontrada!")
            else:
                print("  ❌ Vértice inválido!")
        except ValueError:
            print("  ❌ Entrada inválida.")


    # OPÇÃO G — Mostrar conteúdo do arquivo

    def mostrarArquivo(self):
        """
        Exibe tipo, vértices com rótulos e total de arestas
        de forma visualmente organizada.
        """
        if not self._checar_carregado(): return
        print("\n" + "=" * 65)
        print("  CONTEÚDO DO GRAFO")
        print("=" * 65)
        print(f"  Tipo do Grafo : {self.tipo} (orientado com peso na aresta)")
        print(f"  Vértices      : {self.n}")
        print(f"  Arestas       : {self.m}")
        print("-" * 65)
        print("  VÉRTICES:")
        for i in range(self.n):
            rotulo = self.rotulos[i] if i < len(self.rotulos) else f"Vértice {i}"
            print(f"  [{i:>2}] {rotulo}")
        print("=" * 65)

    # OPÇÃO I — Conexidade e grafo reduzido (Algoritmo FCONEX)


    def _n_pos(self, conjunto):
        """
        Corresponde a N+[R+(v)] no pseudocódigo FCONEX
        """
        vizinhos = set()
        for u in conjunto:
            for (v, _) in self.listaAdj[u]:
                vizinhos.add(v)
        return vizinhos

    def _n_neg(self, conjunto, adj_inv):

        vizinhos = set()
        for u in conjunto:
            for v in adj_inv.get(u, set()):
                vizinhos.add(v)
        return vizinhos

    def _fconex(self, V_restante, adj_inv, sccs):
        """
        Pseudocódigo (slide da aula):
        -------------------------------------------------------
        Início FCONEX(s0 | s0 pertence V)  <dados G=(V,A)>
          v <- s0
          R+(v) = R-(v) <- {v};  W <- vazio

          enquanto N+[R+(v)] - R+(v) != vazio faça
            W <- N+[R+(v)] - R+(v)
            R+(v) <- R+(v) U W

          enquanto N-[R-(v)] - R-(v) != vazio faça
            W <- N-[R-(v)] - R-(v)
            R-(v) <- R-(v) U W

          W <- R+(v) ∩ R-(v)      <- componente f-conexa
          V <- V - W
          Se V != vazio: FCONEX(si | si pertence V)
        Fim.
        -------------------------------------------------------
        Complexidade: O(n²) no pior caso.
        """
        if not V_restante:
            return

        # s0 = primeiro vértice disponível
        s0 = min(V_restante)

        # Inicialização: R+(s0) = R-(s0) = {s0}
        R_pos = {s0}  # Fecho transitivo direto
        R_neg = {s0}  # Fecho transitivo inverso

        # Monta Fecho Transitivo Direto R+(v)
        while True:
            W = self._n_pos(R_pos) & V_restante - R_pos
            if not W:
                break
            R_pos |= W

        # Monta Fecho Transitivo Inverso R-(v)
        while True:
            W = self._n_neg(R_neg, adj_inv) & V_restante - R_neg
            if not W:
                break
            R_neg |= W

        # Componente f-conexa = R+(v) ∩ R-(v)
        W = R_pos & R_neg
        sccs.append(W)

        # Remove componente e continua recursivamente
        V_restante -= W
        if V_restante:
            self._fconex(V_restante, adj_inv, sccs)

    def mostrarConexidade(self):
        """
        Executa o algoritmo FCONEX e exibe:
        - As componentes fortemente conexas (SCCs)
        - A categoria de conexidade (C0, C1, C2 ou C3)
        - O grafo reduzido
        """
        if not self._checar_carregado(): return
        if self.n == 0:
            print("  ⚠️  Grafo vazio.")
            return

        # Constrói grafo transposto: adj_inv[v] = {u | existe aresta u→v}
        adj_inv = {}
        for u in range(self.n):
            for (v, _) in self.listaAdj[u]:
                adj_inv.setdefault(v, set()).add(u)

        # Executa FCONEX
        sys.setrecursionlimit(10000)
        V_restante = set(range(self.n))
        sccs = []
        self._fconex(V_restante, adj_inv, sccs)
        num_sccs = len(sccs)

        print("\n" + "=" * 65)
        print("  CONEXIDADE DO GRAFO — ALGORITMO FCONEX")
        print("=" * 65)
        print(f"\n  Componentes Fortemente Conexas (SCCs): {num_sccs}")
        print("-" * 65)

        # Exibe cada SCC
        for i, scc in enumerate(sccs):
            if len(scc) == 1:
                v = list(scc)[0]
                rot = self.rotulos[v] if v < len(self.rotulos) else f"Vértice {v}"
                print(f"  S{i+1}: [{v}] {rot}")
            else:
                print(f"  S{i+1} ({len(scc)} vértices):")
                for v in sorted(scc):
                    rot = self.rotulos[v] if v < len(self.rotulos) else f"Vértice {v}"
                    print(f"    • [{v:>2}] {rot}")

        print("\n" + "-" * 65)

        # Determina categoria de conexidade
        if num_sccs == 1:
            categoria  = "C3"
            descricao  = "Fortemente Conexo"
            explicacao = ("Existe caminho direcionado entre qualquer par de "
                          "vértices. Todos os cruzamentos são mutuamente "
                          "alcançáveis — ideal para um sistema de caronas.")
        else:
            # Verifica conexidade no grafo não-direcionado subjacente
            visitado = [False] * self.n
            pilha = [0]
            visitado[0] = True
            while pilha:
                u = pilha.pop()
                for (v, _) in self.listaAdj[u]:
                    if not visitado[v]:
                        visitado[v] = True
                        pilha.append(v)
                for v in adj_inv.get(u, set()):
                    if not visitado[v]:
                        visitado[v] = True
                        pilha.append(v)
            conexo_nao_dir = all(visitado)

            if not conexo_nao_dir:
                categoria  = "C0"
                descricao  = "Desconexo"
                explicacao = ("Existem vértices sem nenhum caminho entre si, "
                              "mesmo ignorando as direções das arestas.")
            else:
                # Monta mapa vértice → índice da SCC
                mapa_scc = {}
                for i, scc in enumerate(sccs):
                    for v in scc:
                        mapa_scc[v] = i

                # Arestas do grafo reduzido
                arestas_red = set()
                for u in range(self.n):
                    for (v, _) in self.listaAdj[u]:
                        if mapa_scc[u] != mapa_scc[v]:
                            arestas_red.add((mapa_scc[u], mapa_scc[v]))

                # C2 se DAG reduzido tem exatamente 1 fonte
                grau_entrada = [0] * num_sccs
                for (a, b) in arestas_red:
                    grau_entrada[b] += 1
                fontes = sum(1 for g in grau_entrada if g == 0)

                if fontes == 1:
                    categoria  = "C2"
                    descricao  = "Unilateralmente Conexo"
                    explicacao = ("Para qualquer par de vértices existe caminho "
                                  "em pelo menos uma direção.")
                else:
                    categoria  = "C1"
                    descricao  = "Fracamente Conexo"
                    explicacao = ("O grafo é conexo apenas ignorando as "
                                  "direções das arestas.")

        print(f"  Categoria : {categoria} — {descricao}")
        print(f"  Explicação: {explicacao}")

        # Grafo Reduzido
        print("\n" + "-" * 65)
        print(f"  GRAFO REDUZIDO ({num_sccs} supervértice(s)):")

        if num_sccs == 1:
            print("  Uma única SCC — grafo reduzido tem 1 nó (DAG trivial).")
        else:
            mapa_scc = {}
            for i, scc in enumerate(sccs):
                for v in scc:
                    mapa_scc[v] = i
            arestas_red = set()
            for u in range(self.n):
                for (v, _) in self.listaAdj[u]:
                    if mapa_scc[u] != mapa_scc[v]:
                        arestas_red.add((mapa_scc[u], mapa_scc[v]))
            if arestas_red:
                print("  Arestas entre SCCs:")
                for (a, b) in sorted(arestas_red):
                    print(f"    S{a+1} → S{b+1}")
            else:
                print("  Nenhuma aresta entre SCCs.")

        print("=" * 65)



# MENU PRINCIPAL

g = GrafoCarona()
# O grafo é carregado pelo usuário através da op (a)

while True:
    print("\n" + "=" * 65)
    print("   CARONAS MACKENZIE – OTIMIZAÇÃO DE ROTAS NA MALHA VIÁRIA SP")
    print("   Teoria dos Grafos – Turma 6G – Prof. Ivan Carlos")
    print("=" * 65)
    print("  a) Ler dados do arquivo grafo.txt")
    print("  b) Gravar dados no arquivo grafo.txt")
    print("  c) Inserir vértice")
    print("  d) Inserir aresta")
    print("  e) Remover vértice")
    print("  f) Remover aresta")
    print("  g) Mostrar conteúdo do arquivo")
    print("  h) Mostrar grafo (lista de adjacência)")
    print("  i) Apresentar conexidade e grafo reduzido")
    print("  j) Encerrar a aplicação")
    print("-" * 65)

    op = input("  Digite a opção (a-j): ").strip().lower()

    if op == "a":
        g.carregar()
    elif op == "b":
        g.salvar()
    elif op == "c":
        g.inserirVertice()
    elif op == "d":
        g.inserirAresta()
    elif op == "e":
        g.removerVertice()
    elif op == "f":
        g.removerAresta()
    elif op == "g":
        g.mostrarArquivo()
    elif op == "h":
        g.show()
    elif op == "i":
        g.mostrarConexidade()
    elif op == "j":
        print("\n  ✅ Aplicação encerrada.")
        break
    else:
        print("  ❌ Opção inválida! Digite uma letra de a a j.")
