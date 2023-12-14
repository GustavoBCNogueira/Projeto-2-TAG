import networkx as nx
import matplotlib.pyplot as plt


# Função para tratar a entrada
# Não retorna nenhum tipo
def treatInput() -> None:

    # Declaração de variáveis globais
    global projects
    global students

    # Tratamento do arquivo
    f = open("entrada.txt", 'r')
    for l in f:
        if l[0] == '(':
            if ':' not in l:
                l = l[1:-2]
                l = l.split(", ")
                l[1] = int(l[1])
                l[2] = int(l[2])
                l.append([])
                projects[l[0]] = tuple(l[1:])
            else:
                student, studentInfo = l.split(':')
                student = student[1:-1]
                studentProjects = studentInfo[:-4]
                studentProjects = studentProjects[1:-2]
                studentProjects = studentProjects.split(", ")
                studentGrade = studentInfo[-4:]
                studentGrade = studentGrade[1:-2]
                studentGrade = int(studentGrade)
                l = [student, studentProjects, studentGrade]
                students.append(tuple(l))
    
    f.close()


# Função para inscrever um aluno em um de seus projetos de preferência, ou não, caso não seja possível
# Recebe uma tupla com dados do estudante e o seu índice, que o identifica
# Retorna True se a inscrição for possível e False caso contrário
def handleStudent(student: tuple, idx: int) -> bool:
    
    # Declaração de variáveis globais utilizadas
    global projects
    global students
    global stdFree
    global freeStdCount

    # Tentativa de inscrever o estudante em um dos projetos de preferência
    for project in student[1]:
        # Se ainda há vaga no projeto, basta ter a nota mínima para se inscrever
        if len(projects[project][2]) < projects[project][0]:
            if student[2] >= projects[project][1]:
                projects[project][2].append((student[2], idx))
                projects[project][2].sort()
                stdFree[idx] = False
                freeStdCount -= 1
                return True
        else:
            # Caso não haja vagas, é necessário ter uma nota maior do que a pior nota de um estudante inscrito no momento
            if student[2] > projects[project][2][0][0]:
                std = projects[project][2][0][1]
                projects[project][2].pop(0)
                projects[project][2].append((student[2], idx))
                projects[project][2].sort()
                students[std][1].remove(project)
                stdFree[idx] = False
                stdFree[std] = True
                return True
    return False


# Função que exeuta o algoritmo Gale-Shapley
# Não retorna nenhum tipo
def GaleShapley() -> None:

    # Declaração de váriaveis globais utilizadas
    global projects
    global students
    global stdFree
    global freeStdCount

    # Trata todos os estudantes
    i = 0    
    while i < len(students):
        if stdFree[i]:
            if handleStudent(students[i], i):
                stdFree[i] = False
        i += 1


# Função que executa uma iteração e mostra o grafo bipartido após a execução do algoritmo Gale-Shapley
# Recebe o número da iteração
# Não retorna nenhum tipo
def executeIteration(n: int) -> None:

    # Declaração de variáveis globais utilizadas
    global students
    global projects
    global stdFree
    global freeStdCount

    # Execução do algoritmo para a determinada iteração
    GaleShapley()
    
    print(f"Número de estudantes livres na iteração {n+1} : {freeStdCount}")
    print(f"Número de estudantes com projetos na iteração {n+1} : {len(students)-freeStdCount}")

    # Inicialização do grafo e inserção dos projetos e estudantes
    graph = nx.Graph()
    studentSet = ["S"+str(i) for i in range(len(students))]
    projectSet = list(projects.keys())
    graph.add_nodes_from(list(projects.keys()))
    graph.add_nodes_from(["S"+str(i) for i in range(len(students))])

    # Inserção das arestas no grafo, representando a vaga de um aluno em um projeto 
    for p in projectSet:
        for s in projects[p][2]:
            graph.add_edge(p, "S"+str(s[1]))

    # Desenho do grafo
    pos = {}
    pos.update((n, (1, i)) for i, n in enumerate(studentSet)) 
    pos.update((n, (2, i)) for i, n in enumerate(projectSet))
    plt.title(f"Iteração {n+1}") 
    nx.draw(graph, pos=pos, with_labels=True)
    plt.show()


# Função principal
if __name__ == "__main__":
    
    # Inicialização dos projetos e estudantes
    projects = {}       # Projetos: dicionário tendo a string identificadora do projeto 
                        # como chave e uma tupla com o número de vagas, o requisito 
                        # mínimo de notas para vagas e uma lista contendo
                        # os alunos inscritos no projeto no momento.
    
    students = []       # Estudantes: lista contendo tuplas uma string, 
                        # uma lista com os projetos de preferência e a nota.
                        # Os estudantes são identificados pelo seu índice na lista.

    # Tratamento da entrada
    treatInput()

    # Inicialização de um vetor de alunos livres e contador de alunos livres, utilizados no algoritmo Gale-Shapley
    stdFree = [True for i in range(len(students))]
    freeStdCount = len(students)

    # 10 iterações do algoritmo Gale-Shapley
    for n in range(10):
        executeIteration(n)
