import ply.lex as lex
from ply import yacc
from cProfile import label
import tkinter as tk #Biblioteca para interfaces gráficas
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import filedialog as fd

reserved = {
    'IFSULDEMINAS': 'IFSULDEMINAS',
    'INICIO': 'INICIO',
    'COMPILADORES': 'COMPILADORES',
    'FIM': 'FIM',
    'se': 'se',
    'senao': 'senao',
    'enquanto': 'enquanto',
    'para': 'para',
    'interrompa': 'interrompa',
    'prossiga': 'prossiga',
    'retorne': 'retorne',
    'em': 'em',
    'define': 'define',
    'classe': 'classe',
    'leia': 'leia',
    'escreva': 'escreva',
    'verdadeiro': 'verdadeiro',
    'falso': 'falso'
}

tokens = [
    'OP_ARIT', #'+', '-', '/', '*'
    'OP_REL', #'<', '>', '<>', '<=', '>=', '=='
    'OP_ATRIBUI', #':='
    'OP_LOGICO',
    'OP_MOD',
    'ASPAS',
    'PONTO',
    'ABRE_CH', #'{'
    'FECHA_CH', #'}'
    'ABRE_CLT', #'['
    'FECHA_CLT', #']'
    'ABRE_P', #'('
    'FECHA_P', #')'
    'COMENT', #'**...'
    'COMENTS', #'***...***']
    'VIRGULA', #','
    'PONTO_E_VIRGULA', 
    'DOIS_PONTOS',
    'DELIMITADOR', #';'
    'tipo_var',
    'valor_numint',
    'valor_texto',
    'valor_letra',
    'valor_numdec',
    'booleano',
    
#Verificação de compatibilidade com o ply (biblioteca utilizada)
'ignore', #ignorar tabulação e espaços
'numero_mf', #número mal formado
'texto_mf', #string mal formada
'variavel_mf', #variável mal formada
] + list(reserved.values()) #Concatenação com as palavras reservadas

t_OP_ARIT = r'[\+\-\/\*]'
t_OP_MOD = r'\%'
t_PONTO_E_VIRGULA = r'\;'
t_VIRGULA = r'\,'
t_ASPAS = r'\"'
t_DOIS_PONTOS = r'\:'
t_PONTO = r'\.'
t_COMENT =  r'¨(.*)'
t_COMENTS = r'\*\*\*[\s\S]*?\*\*\*'
t_booleano = r'\b(verdadeiro|falso)\b'

t_IFSULDEMINAS = r'IFSULDEMINAS'
t_INICIO = r'INICIO'
t_COMPILADORES = r'COMPILADORES'
t_FIM = r'FIM'
t_se = r'se'
t_senao = r'senao'
t_enquanto = r'enquanto'
t_para = r'para'
t_interrompa = r'interrompa'
t_prossiga = r'prossiga'
t_retorne = r'retorne'
t_em = r'em'
t_define = r'define'
t_classe = r'classe'
t_escreva = r'escreva'
t_leia = r'leia'

t_OP_REL = r'[<>]=?|==|!='
t_OP_ATRIBUI = r'\:='
t_OP_LOGICO = r'\b(e|ou)\b'
t_ABRE_P = r'\('
t_FECHA_P = r'\)'
t_ABRE_CH = r'\{'
t_FECHA_CH = r'\}'
t_ABRE_CLT = r'\['
t_FECHA_CLT = r'\]'
t_ignore = ' \t' #Ignora espaços e tabulações

def t_valor_texto(t):
    r'("[^"]*")'
    return t

def t_texto_mf(t):
    r'("[^"]*)'
    return t

def t_variavel_mf(t):
    r'([0-9]+[a-z]+)|([@!#$%&*]+[a-z]+|[a-z]+\.[0-9]+|[a-z]+[@!#$%&*]+)'
    return t

def t_numero_mf(t):
    r'([0-9]+\.[a-z]+[0-9]+)|([0-9]+\.[a-z]+)|([0-9]+\.[0-9]+[a-z]+)'
    return t

def t_valor_numdec(t):
    r'([0-9]+\.[0-9]+)|([0-9]+\.[0-9]+)'
    return t

def t_valor_numint(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_tipo_var(t):
    r'[a-z][a-z_0-9]*'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_DELIMITADOR(t):
    r'\;'
    return t
    t.lexer.lineno += len(t.value)

erros = 0

def add_lista_saida(t, notificacao):
    saidas.append((t.lineno, t.lexpos, t.type, t.value, notificacao))
saidas = []

#Regras para tratamento de erros
erroslexicos = []
def t_error(t):
    erroslexicos.append(t)
    t.lexer.skip(1)

root = tk.Tk()

class Application():
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.botoes()
        self.Menus()
        root.mainloop()

    def limpa_telaentrada(self):
        self.codigo_entry.delete(1.0, END)
        for i in self.saida.get_children():
            self.saida.delete(i)
        saidas.clear()
        erroslexicos.clear()
        #errossintaticos.clear()
        global erros
        erros = 0
        self.frame_1.update()
        self.frame_2.update()
        root.update()

    def tela(self):
        
        self.root.title("Compilador Simlish")
        self.root.configure(background = "white")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.minsize(width = 500, height = 350)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg = "#DCDCDC", highlightbackground = "grey", highlightthickness = 3)
        self.frame_1.place(relx = 0.02, rely = 0.07, relwidth = 0.96, relheight = 0.55)
        self.frame_2 = Frame(self.root, bd = 4, bg = "#DCDCDC", highlightbackground = "grey", highlightthickness = 3)
        self.frame_2.place(relx = 0.02, rely = 0.70, relwidth = 0.96, relheight = 0.20)

    def chama_analisador(self):
        columns = ('linha', 'posicao', 'token', 'lexema', 'notificacao')
        self.saida = ttk.Treeview(self.frame_2, height = 5, columns = columns, show = 'headings')
        self.saida.heading("linha", text = 'Linha')
        self.saida.heading("posicao", text = 'Posição referente ao início da entrada')
        self.saida.heading("token", text = 'Token')
        self.saida.heading("lexema", text = 'Lexema')
        self.saida.heading("notificacao", text = 'Notificação')

        data = self.codigo_entry.get(1.0, "end-1c")
        data.lower()
        lexer = lex.lex()
        lexer.input(data)

        #Tokenizar a entrada para passar para o analisar léxico
        for tok in lexer:
            global erros
            if tok.type == "texto_mf":
                erros += 1
                add_lista_saida(tok, f"Ops... String mal formada!")
            elif tok.type == "variavel_mf":
                erros += 1
                add_lista_saida(tok, f"Ops... Variável mal formada!")
            elif tok.type == "numero_mf":
                erros += 1
                add_lista_saida(tok, f"Ops... Número mal formado!")
            elif tok.type == "valor_numint":
                max = (len(str(tok.value)))
                if (max > 15):
                    erros += 1
                    add_lista_saida(tok, f"Ops... Entrada maior que o limite suportado!")
                else:
                    add_lista_saida(tok, f"")
            elif tok.type == "se" or tok.type == "senao" or tok.type == "enquanto" or tok.type == "para" or tok.type == "interrompa" or tok.type == "prossiga" or tok.type == "retorne" or tok.type == "em" or tok.type == "define" or tok.type == "classe" or tok.type == "leia" or tok.type == "escreva" or tok.type == "verdadeiro" or tok.type == "falso" or tok.type == "IFSULDEMINAS" or tok.type == "COMPILADORES" or tok.type == "INICIO" or tok.type == "FIM":
                max = (len(tok.value))
                if (max < 20):
                    if tok.value in reserved:
                        tok.type = reserved[tok.value]
                        add_lista_saida(tok, f"Palavra reservada!") 
                    else:
                        add_lista_saida(tok, f"")

                else:
                    erros += 1
                    add_lista_saida(tok, f"Ops... Tamanho da variável maior que o limite suportado!")
            else:
                add_lista_saida(tok, f"")
        if (saidas[0][3] == "IFSULDEMINAS"):
            if (saidas[1][3] != ";"):
                erros += 1
                self.saida.insert('', tk.END, values = "Ops... É necessário a palavra IFSULDEMINAS no início do seu algoritmo!")
            else:
                pass
        else:
            erros += 1
            self.saida.insert('', tk.END, values = "Ops... É necessário a palavra IFSULDEMINAS no início do seu algoritmo!")
        for tok in erroslexicos:
            add_lista_saida(tok, f"Ops... Esta linguagem não aceita esse caracter.")
        
        tamerroslex = len(erroslexicos)
        if tamerroslex == 0 and erros == 0:
            self.saida.insert('', tk.END, values = "Legal! Análise Léxica efetuada sem erros!")
            #parser.pase(data)
        else:
            self.saida.insert('', tk.END, values = "Ops... Erro Léxico.") 
        for retorno in saidas:
            self.saida.insert('', tk.END, values = retorno)

        self.saida.place(relx = 0.001, rely = 0.01, relwidth = 0.999, relheight = 0.95)

        self.scrollAnalise = ttk.Scrollbar(self.frame_2, orient = 'vertical', command = self.saida.yview)
        self.scrollAnalise.place(relx = 0.979, rely = 0.0192, relwidth = 0.02, relheight = 0.92)
        self.saida['yscrollcommand'] = self.scrollAnalise 

    def botoes(self):
        #Botão para limpar
        self.bt_limpar = Button(text = "Limpar", bd = 2, bg = "#FF6347", font = ('', 11), command = self.limpa_telaentrada)
        self.bt_limpar.place(relx = 0.74, rely = 0.92, relwidth = 0.1, relheight = 0.05)

        #Botão para executar
        self.bt_executar = Button(text = "Executar", bd = 2, bg = "lightgreen", font = ('', 11), command = self.chama_analisador)
        self.bt_executar.place(relx = 0.85, rely = 0.92, relwidth = 0.1, relheight = 0.05)

        #Espaço (label) para a entrada do código
        self.lb_codigo = Label(text = "Código fonte", bg = "white", font = ('', 12))
        self.lb_codigo.place(relx = 0.001, rely = -0.001, relwidth = 0.2, relheight = 0.07)

        #Espaço (label) para a Análise Léxica
        self.lb_analise = Label(text = "Análise Léxica", bg = "white", font = ('', 12))
        self.lb_analise.place(relx = 0.001, rely = 0.62, relwidth = 0.2, relheight = 0.07)

        self.codigo_entry = tk.Text(self.frame_1)
        self.codigo_entry.place(relx = 0.001, rely = 0.001, relwidth = 0.995, relheight = 0.995)

        self.scroll_bar = ttk.Scrollbar(self.frame_1, orient = 'vertical', command = self.codigo_entry.yview)
        self.scroll_bar.place(relx = 0.982, rely = 0.0019, relwidth = 0.015, relheight = 0.99)
        self.codigo_entry['yscrollcommand'] = self.scroll_bar

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu = menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        def onOpen():
            tf = fd.askopenfilename(
                initialdir = "C:/Users/MainFrame/Desktop",
                title = "Abrir arquivo de texto",
                filetypes = (("Arquivos de texto", "*.txt"),)
            )
            tf = open(tf, 'r')
            entrada = tf.read()
            self.codigo_entry.insert(END, entrada)
            tf.close()
        
        def onSave():
            files = filedialog.asksaveasfile(mode = 'w', defaultextension = ".txt")
            t = self.codigo_entry.get(0.0, END)
            files.write(t.rstrip())
        
        def tokens():
            newWindow = Toplevel(root)
            newWindow.title("Tabela de Tokens")
            newWindow.configure(background = "white")
            newWindow.geometry("800x800")
            newWindow.resizable(True, True)
            newWindow.minsize(width = 550, height = 350)

            newWindow = ttk.Treeview(newWindow, height = 3, column = ('col1', 'col2', 'col3', 'col4'))
            newWindow.heading("#0", text='')
            newWindow.heading("#1", text='Tokens')
            newWindow.heading("#2", text='Lexemas')
            newWindow.heading("#3", text='Expressão Regular')
            newWindow.heading("#4", text='Descrição')

            newWindow.column("#0", width = 1, stretch = NO)
            newWindow.column("#1", width = 50,)
            newWindow.column("#2", width = 200)
            newWindow.column("#3", width = 125)
            newWindow.column("#4", width = 125)

            newWindow.place(relx = 0.001, rely = 0.01, relwidth = 0.999, relheight = 0.95)

            newWindow.insert("", 1, text = "", values = ("IFSULDEMINAS", "IFSULDEMINAS", "IFSULDEMINAS", "Palavra reservada 'IFSULDEMINAS'"))
            newWindow.insert("", 2, text = "", values = ("INICIO", "INICIO", "INICIO", "Palavra reservada 'INICIO'"))
            newWindow.insert("", 3, text = "", values = ("COMPILADORES", "COMPILADORES", "COMPILADORES", "Palavra reservada 'COMPILADORES'"))
            newWindow.insert("", 4, text = "", values = ("FIM", "FIM", "FIM", "Palavra reservada 'FIM'"))
            newWindow.insert("", 5, text = "", values = ("se", "se", "se", "Palavra reservada 'se'"))
            newWindow.insert("", 6, text = "", values = ("senao", "senao", "senao", "Palavra reservada 'senao'"))
            newWindow.insert("", 7, text = "", values = ("enquanto", "enquanto", "enquanto", "Palavra reservada 'enquanto'"))
            newWindow.insert("", 8, text = "", values = ("para", "para", "para", "Palavra reservada 'para'"))
            newWindow.insert("", 9, text = "", values = ("interrompa", "interrompa", "interrompa", "Palavra reservada 'interrmopa"))
            newWindow.insert("", 10, text = "", values = ("prossiga", "prossiga", "prossiga", "Palavra reservada 'prossiga"))
            newWindow.insert("", 11, text = "", values = ("retorne", "retorne", "retorne", "Palavra reservada 'retorne'"))
            newWindow.insert("", 12, text = "", values = ("em", "em", "em", "Palavra reservada 'em'"))
            newWindow.insert("", 13, text = "", values = ("define", "define", "define", "Palavra reservada 'define'"))
            newWindow.insert("", 14, text = "", values = ("classe", "classe", "classe", "Palavra reservada 'classe'"))
            newWindow.insert("", 15, text = "", values = ("leia", "leia", "leia", "Palavra reservada 'leia'"))
            newWindow.insert("", 16, text = "", values = ("escreva", "escreva", "escreva", "Palavra reservada 'escreva'"))
            newWindow.insert("", 17, text = "", values = ("booleano", "verdadeiro, falso", "verdadeiro | falso", "Palavra reservada 'booleano'"))

            newWindow.insert("", 19, text = "", values = ("OP_ARIT", "+, -, /, *", "+, -, /, *", "+, -, /, *", "+, -, /, *", "Operadores aritméticos"))
            newWindow.insert("", 20, text = "", values = ("OP_REL", "<, >, <>, <=, >=, ==", "<, >, <>, <=, >=, ==", "Operadores relacionais"))
            newWindow.insert("", 21, text = "", values = ("OP_ATRIBUI", ":=", ":=", "Operador de 'atribuição'"))
            newWindow.insert("", 22, text = "", values = ("ABRE_CH", "{", "{", "Operador de 'abre chaves'"))
            newWindow.insert("", 23, text = "", values = ("FECHA_CH", "}", "}", "Operador de 'fecha chaves'"))
            newWindow.insert("", 24, text = "", values = ("ABRE_CLT", "[", "[", "Operador de 'abre colchetes'"))
            newWindow.insert("", 25, text = "", values = ("FECHA_CLT", "]", "]", "Operaode de 'fecha colchetes'"))
            newWindow.insert("", 26, text = "", values = ("ABRE_P", "(", "(", "Operador de 'abre parênteses'"))
            newWindow.insert("", 27, text = "", values = ("FECHA_P", ")", ")", "Operador de 'fecha parênteses'"))
            newWindow.insert("", 28, text = "", values = ("COMENT", "¨", "¨", "Operador de 'comentário em linha'"))
            newWindow.insert("", 30, text = "", values = ("VIRGULA", ",", ",", "Operador de execução 'vírgula'"))
            newWindow.insert("", 31, text = "", values = ("PONTO_E_VIRGULA", ";", ";", "Operador de execução 'ponto e vírgula'"))
            newWindow.insert("", 32, text = "", values = ("DELIMITADOR", "$", "$", "Operador de 'delimitador (fim delinha)'"))
            newWindow.insert("", 33, text = "", values = ("tipo_var", "char, inteiro, decimal", "char, inteiro, decimal", "Variável"))
            newWindow.insert("", 34, text = "", values = ("valor_numint", "0, 1, 2, 3", "4, 5, 6", "Digito numérico 'INTEIRO'"))
            newWindow.insert("", 35, text = "", values = ("valor_texto", "Ciência da Computação", "Ciência da Computação", "Texto"))
            newWindow.insert("", 36, text = "", values = ("valor_letra", "C, I, E, c, i, e", "C, O, M, c, o, m", "Caracter único"))
            newWindow.insert("", 37, text = "", values = ("valor_numdec", "0.1, 0.01, 0.001", "3.14, 3.141", "Digito numérico 'DECIMAL'"))

            newWindow.insert("", 38, text = "", values = ("ASPAS", ",", ",", "Operador de execução 'aspas'"))
            newWindow.insert("", 38, text = "", values = ("OP_MOD", "%", "%", "Operador aritmético 'módulo'"))

            label.pack(pady = 10)
            mainloop()
        
        menubar.add_cascade(label = "Arquivo", menu = filemenu)
        menubar.add_cascade(label = "Tabela de Tokens", menu = filemenu2)

        filemenu.add_command(label = "Abrir Script", command = onOpen)
        filemenu.add_command(label = "Salvar como", command = onSave)
        filemenu.add_separator()
        filemenu.add_command(label = "Sair", command = Quit)
        filemenu2.add_command(label = "Tokens", command = tokens)

Application()
    







