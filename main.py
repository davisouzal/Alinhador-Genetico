# Programa com PySide2 para mostrar uma lista pré-definida de caracteres cada um com uma cor diferente

import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from tkinter import *

dict_cores = {
    'A': 'red',
    'C': 'blue',
    'G': 'green',
    'T': 'yellow',
    '-': 'white'
}


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole:
            return QtGui.QColor(dict_cores[self._data[index.row()][index.column()]])

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data):
        super().__init__()

        self.table = QtWidgets.QTableView()

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

def addSeq():
    seq = novaSeq.get(1.0, "end").upper()
    lbSeq.insert(END, seq[:-1])
    sequencias.append(seq[:-1])
    novaSeq.delete(1.0, END)

def printSeqs():
    print(sequencias)

def alinharSeqs():
    app.destroy()

def removeSeqs():
    label = str(lbSeq.get(ACTIVE))
    idx = lbSeq.get(0, END).index(label)
    del sequencias[idx]
    lbSeq.delete(idx)

def editSeqs():
    label = str(lbSeq.get(ACTIVE))
    idx = lbSeq.get(0, END).index(label)
    def editSeq():
        del sequencias[idx]
        lbSeq.delete(idx)

        seq = editEntry.get(1.0, END).upper()
        lbSeq.insert(idx, seq[:-1])
        sequencias.insert(idx, seq[:-1])
        edit.destroy()
    def editDestroy():
        edit.destroy()

    edit = Tk()
    edit.title("Edição de Sequência")
    edit.configure(background='#dde')
    edit.geometry("400x170")

    editLabel = Label(edit, text="Digite abaixo a sequência correta", background='#dde')
    editLabel.pack()

    editEntry = Text(edit, width=150)
    editEntry.insert('1.0', label)
    editEntry.place(x=30, y=50, width=230, height=80)

    editBtn = Button(edit, text="Editar", command=editSeq)
    editBtn.place(x=265, y=50, width=100, height=40)
    cancelBtn = Button(edit, text="Cancelar", command=editDestroy)
    cancelBtn.place(x=265, y=90, width=100, height=40)

app = Tk()
app.title("Alinhador Genético")
app.configure(background='#dde')

app.geometry("600x300+0+0")

sequencias = []

labSeq = Label(app,text="Sequências para alinhar: ", background="#dde")
labSeq.place(x=335, y=10, width=200, height=20)

lbSeq = Listbox(app)
for sequencia in sequencias:
    lbSeq.insert(END, sequencia)
lbSeq.place(x=350, y=30, width=200)
btnAlinhar = Button(app, text="Alinhar", command=alinharSeqs)
btnAlinhar.place(x=350, y = 215, width=200)
btnEditSeq = Button(app, text="Editar", command=editSeqs)
btnEditSeq.place(x=350, y = 250, width=100)
btnRmSeq = Button(app, text="Deletar", command=removeSeqs)
btnRmSeq.place(x=450, y = 250, width=100)

labInsert = Label(app, text="Digite a sequência a ser alinhada: ", background="#dde")
labInsert.place(x=10, y = 100)
novaSeq = Text(app)
novaSeq.place(x=10, y = 120, width=230, height=50)
btnNovaSeq = Button(app, text="Inserir", command=addSeq)
btnNovaSeq.place(x=10, y = 175)

#btnPrint = Button(app, text='print', command=printSeqs)
#btnPrint.place(x=10, y=205)

app.mainloop()


def cria_matriz(linhas, colunas):
    matriz = [
        [0 for i in range(colunas)] for j in range(linhas)
    ]
    
    return matriz


def alinhar(sequencia_1, sequencia_2):
    # Cria as matrizes
    principal_matriz = cria_matriz(len(sequencia_1)+1,len(sequencia_2)+1)
    matriz_verificacao_correspondencia = cria_matriz(len(sequencia_1),len(sequencia_2))

    # Provendos os scores de match, mismatch e gap
    igual = 1
    diferente = 0
    gap = -1

    # Preenchendo a matriz de verificação de correspondência de acordo com o match ou mismatch
    for i in range(len(sequencia_1)):
        for j in range(len(sequencia_2)):
            if sequencia_1[i] == sequencia_2[j]:
                matriz_verificacao_correspondencia[i][j] = igual
            else:
                matriz_verificacao_correspondencia[i][j] = diferente


    # Preenchendo a matriz principal usando o algoritmo Needleman Wunsch
    # Passo 1: Inicialização
    for i in range(len(sequencia_1)+1):
        principal_matriz[i][0] = i*gap
        
    for j in range(len(sequencia_2)+1):
        principal_matriz[0][j] = j * gap


    # Passo 2: Preenchendo a matriz
    for i in range(1,len(sequencia_1)+1):
        for j in range(1,len(sequencia_2)+1):
            principal_matriz[i][j] = max(
                principal_matriz[i-1][j-1] + matriz_verificacao_correspondencia[i-1][j-1],
                principal_matriz[i-1][j] + gap,
                principal_matriz[i][j-1] + gap
            )

    # STEP 3 : Traceback

    alinhamento_1 = ""
    alinhamento_2 = ""

    ti = len(sequencia_1)
    tj = len(sequencia_2)

    while(ti >0 and tj > 0):

        if (ti >0 and tj > 0 and principal_matriz[ti][tj] == principal_matriz[ti-1][tj-1]+ matriz_verificacao_correspondencia[ti-1][tj-1]):

            alinhamento_1 = sequencia_1[ti-1] + alinhamento_1
            alinhamento_2 = sequencia_2[tj-1] + alinhamento_2

            ti = ti - 1
            tj = tj - 1
        
        elif(ti > 0 and principal_matriz[ti][tj] == principal_matriz[ti-1][tj] + gap):
            alinhamento_1 = sequencia_1[ti-1] + alinhamento_1
            alinhamento_2 = "-" + alinhamento_2

            ti = ti -1
        else:
            alinhamento_1 = "-" + alinhamento_1
            alinhamento_2 = sequencia_2[tj-1] + alinhamento_2

            tj = tj - 1
    
    return alinhamento_1, alinhamento_2



alinhamento_1, alinhamento_2 = alinhar(sequencias[0], sequencias[1])

alinhamentos = [alinhamento_1, alinhamento_2]

for i in range(2, len(sequencias)):
    alinhamentos.append(alinhar(alinhamentos[i-2], sequencias[i])[1])


for i in range(len(alinhamentos)):
    alinhamentos[i] = list(alinhamentos[i])


#Calcula Score das colunas
listScore = []

for i in range(0,len(alinhamentos[0])):
    currentyScore = 0
    base1 = alinhamentos[0][i]
    for j in range(1,len(alinhamentos)):
        try:
            base2 = alinhamentos[j][i]
            if(base2 == '-' or base1 == '-'):
                currentyScore -= 1
            elif(base2 == base1):
                currentyScore += 1
            
        except:
            pass
        base1 = base2
    
    listScore.append(currentyScore)
#END
# print(listScore)
totalScore = sum(listScore)

alinhamentos.append(listScore)
alinhamentos.append(['Valor total: ',totalScore])

app=QtWidgets.QApplication(sys.argv)
window=MainWindow(alinhamentos)
window.show()
app.exec_()