import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime
import pandas as pd
from io import BytesIO
from tkinter.filedialog import asksaveasfilename

# --- LISTAS PARA GERAÇÃO DE NOMES ---
LISTA_PRIMEIROS_NOMES = [
    # Nomes masculinos
    "Miguel", "Arthur", "Bernardo", "Heitor", "Davi", "Lorenzo", "Théo", "Pedro", "Gabriel", "Enzo",
    "Matheus", "Lucas", "Benjamin", "Nicolas", "Guilherme", "Rafael", "Joaquim", "Samuel", "Enzo Gabriel",
    "João Miguel", "Henrique", "Gustavo", "Murilo", "Pedro Henrique", "João Pedro", "João Lucas", "Felipe",
    "João Gabriel", "Leonardo", "Fernando", "Tomás", "Antônio", "Daniel", "Vicente", "Eduardo", "Caio",
    "Vitor", "Isaac", "Lucca", "João", "Benício", "Augusto", "João Paulo", "Otávio", "Ricardo", "Carlos",
    # Nomes femininos
    "Helena", "Alice", "Laura", "Manuela", "Sophia", "Isabella", "Luísa", "Heloísa", "Cecília", "Maitê",
    "Maria Clara", "Elisa", "Liz", "Júlia", "Maria Luiza", "Valentina", "Maria Alice", "Beatriz", "Maria",
    "Lívia", "Antonella", "Mariana", "Luna", "Ana Clara", "Ana Júlia", "Ana Laura", "Maria Júlia", "Sofia",
    "Clara", "Maria Eduarda", "Ana", "Melissa", "Yasmin", "Maria Cecília", "Maria Helena", "Stella", "Ana Beatriz",
    "Aurora", "Ana Luísa", "Ana Sophia", "Gabriela", "Lorena", "Isabel", "Amanda", "Catarina", "Vitória"
]

LISTA_SOBRENOMES = [
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes",
    "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida", "Lopes", "Soares", "Fernandes", "Vieira", "Barbosa",
    "Rocha", "Dias", "Nascimento", "Andrade", "Moreira", "Nunes", "Marques", "Machado", "Mendes", "Freitas",
    "Cardoso", "Ramos", "Gonçalves", "Monteiro", "Pinto", "Cruz", "Correia", "Cunha", "Azevedo", "Cavalcanti",
    "Peixoto", "Miranda", "Reis", "Campos", "Aragão", "Barros", "Moraes", "Melo", "Neto", "Nogueira"
]
INICIAIS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# --- CONFIGURAÇÕES DE CARTÕES (IIN/BIN) ---
CONFIG_CARTOES = {
    # Cartões Genéricos
    "Visa (Genérico)": {
        "prefixos": ["4"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Genérico"
    },
    "Mastercard (Genérico)": {
        "prefixos": ["51", "52", "53", "54", "55"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Genérico"
    },
    "American Express (Genérico)": {
        "prefixos": ["34", "37"],
        "comprimento": 15,
        "bandeira": "American Express",
        "banco": "Genérico"
    },
    "Elo (Genérico)": {
        "prefixos": ["636368", "504175", "5067", "509", "627780"],
        "comprimento": 16,
        "bandeira": "Elo",
        "banco": "Genérico"
    },
    
    # Banco do Brasil
    "BB Visa Gold": {
        "prefixos": ["498407"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Banco do Brasil"
    },
    "BB Visa Infinite": {
        "prefixos": ["498408"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Banco do Brasil"
    },
    "BB Mastercard Gold": {
        "prefixos": ["546452"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Banco do Brasil"
    },
    "BB Mastercard Black": {
        "prefixos": ["552289"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Banco do Brasil"
    },
    "BB Elo Mais": {
        "prefixos": ["650487"],
        "comprimento": 16,
        "bandeira": "Elo",
        "banco": "Banco do Brasil"
    },

    # Itaú
    "Itaú Mastercard Gold": {
        "prefixos": ["511258"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Itaú"
    },
    "Itaú Visa Gold": {
        "prefixos": ["418049"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Itaú"
    },

    # Bradesco
    "Bradesco Visa Gold": {
        "prefixos": ["407941"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Bradesco"
    },
    "Bradesco Mastercard Gold": {
        "prefixos": ["516988"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Bradesco"
    },
    "Bradesco Elo Grafite": {
        "prefixos": ["636297"],
        "comprimento": 16,
        "bandeira": "Elo",
        "banco": "Bradesco"
    },

    # Santander
    "Santander Visa Infinite": {
        "prefixos": ["422642"],
        "comprimento": 16,
        "bandeira": "Visa",
        "banco": "Santander"
    },
    "Santander Mastercard Black": {
        "prefixos": ["525741"],
        "comprimento": 16,
        "bandeira": "Mastercard",
        "banco": "Santander"
    }
}

def gerar_nome_ficticio():
    """Gera um nome com inicial do meio, ex: Marcos C. Leon"""
    primeiro = random.choice(LISTA_PRIMEIROS_NOMES)
    sobrenome = random.choice(LISTA_SOBRENOMES)
    inicial = random.choice(INICIAIS)
    return f"{primeiro} {inicial}. {sobrenome}"

def calcular_luhn_dv(base_numero):
    """Calcula o dígito verificador usando o Algoritmo de Luhn (Módulo 10)"""
    pesos = [2, 1]
    soma_produtos = 0
    base_invertida = base_numero[::-1]
    
    for i, digito_str in enumerate(base_invertida):
        peso = pesos[i % len(pesos)]
        produto = int(digito_str) * peso
        soma_produtos += (produto // 10) + (produto % 10)
        
    resto = soma_produtos % 10
    dv = 0 if resto == 0 else (10 - resto)
    return str(dv)

def gerar_cartao_credito(config_cartao):
    """Gera um conjunto completo de dados de cartão de crédito."""
    # 1. Número do Cartão (com Luhn)
    prefixo = random.choice(config_cartao["prefixos"])
    comprimento = config_cartao["comprimento"]
    
    # Gera o "meio" do cartão
    comprimento_meio = comprimento - len(prefixo) - 1
    meio_cartao = ''.join([str(random.randint(0, 9)) for _ in range(comprimento_meio)])
    
    # Base para cálculo do DV
    base_calculo = prefixo + meio_cartao
    dv = calcular_luhn_dv(base_calculo)
    
    numero_cartao = base_calculo + dv
    
    # 2. Nome Fictício
    nome_cartao = gerar_nome_ficticio()
    
    # 3. Data de Validade (MM/AA)
    hoje = datetime.now()
    ano_futuro = hoje.year + random.randint(1, 5)
    mes_futuro = random.randint(1, 12)
    validade = f"{mes_futuro:02d}/{ano_futuro % 100:02d}"
    
    # 4. CVV
    if config_cartao["bandeira"] == "American Express":
        cvv = f"{random.randint(1000, 9999):04d}"
    else:
        cvv = f"{random.randint(0, 999):03d}"
        
    return (
        nome_cartao, 
        config_cartao["banco"], 
        config_cartao["bandeira"], 
        numero_cartao, 
        validade, 
        cvv
    )

class GeradorCartaoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Cartões de Crédito")
        self.root.geometry("1000x700")
        
        # Configurar tema escuro
        self.root.configure(bg='#1e1e1e')
        style = ttk.Style()
        style.theme_use('default')
        
        # Configurações de cores do tema escuro
        style.configure('TFrame', background='#1e1e1e')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('TButton', background='#2d2d2d', foreground='#ffffff')
        style.configure('Treeview', 
                      background='#2d2d2d', 
                      fieldbackground='#2d2d2d', 
                      foreground='#ffffff')
        style.configure('TCombobox', 
                      background='#2d2d2d', 
                      fieldbackground='#2d2d2d', 
                      foreground='#ffffff')
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansão da janela
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        # Título e Aviso
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0,20))
        
        ttk.Label(title_frame, 
                 text="💳 Gerador de Cartões de Crédito (para Testes)", 
                 font=('Helvetica', 16, 'bold'),
                 foreground='#00ff00').grid(row=0, column=0, pady=10)
        
        ttk.Label(title_frame, 
                 text="Estes dados são 100% FALSOS e devem ser usados APENAS em ambientes de teste",
                 foreground="#ff6b6b",
                 font=('Helvetica', 10, 'bold')).grid(row=1, column=0, pady=5)
        
        # Frame de controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, pady=(0,20))
        
        # Organizar cartões por banco
        bancos = sorted(list(set(config["banco"] for config in CONFIG_CARTOES.values())))
        cartoes_por_banco = {banco: [] for banco in bancos}
        for nome, config in CONFIG_CARTOES.items():
            cartoes_por_banco[config["banco"]].append(nome)
        
        # Seleção do banco
        ttk.Label(controls_frame, text="Banco:").grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        self.banco_combo = ttk.Combobox(controls_frame, values=bancos, width=30)
        self.banco_combo.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)
        self.banco_combo.set(bancos[0])
        self.banco_combo.bind('<<ComboboxSelected>>', self.atualizar_cartoes)
        
        # Seleção do tipo de cartão
        ttk.Label(controls_frame, text="Cartão:").grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)
        self.tipo_cartao = ttk.Combobox(controls_frame, width=40)
        self.tipo_cartao.grid(row=0, column=3, pady=5, padx=5, sticky=tk.W)
        
        # Quantidade
        ttk.Label(controls_frame, text="Quantidade:").grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        self.quantidade = ttk.Spinbox(controls_frame, from_=1, to=1000, width=10)
        self.quantidade.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)
        self.quantidade.set(10)
        
        # Botões
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=2, columnspan=2, pady=10)
        
        ttk.Button(button_frame, 
                  text="🔄 Gerar Cartões", 
                  command=self.gerar_cartoes,
                  style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, 
                  text="📥 Exportar Excel", 
                  command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        
        # Frame para resultados
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Área de resultados com estilo escuro
        self.resultado = ttk.Treeview(results_frame, 
                                    columns=("Nome", "Banco", "Bandeira", "Número", "Validade", "CVV"),
                                    show="headings", 
                                    style='Treeview')
        
        # Configurar colunas
        self.resultado.heading("Nome", text="Nome no Cartão")
        self.resultado.heading("Banco", text="Banco Emissor")
        self.resultado.heading("Bandeira", text="Bandeira")
        self.resultado.heading("Número", text="Número do Cartão")
        self.resultado.heading("Validade", text="Validade")
        self.resultado.heading("CVV", text="CVV")
        
        # Ajustar largura das colunas
        self.resultado.column("Nome", width=200)
        self.resultado.column("Banco", width=150)
        self.resultado.column("Bandeira", width=100)
        self.resultado.column("Número", width=160)
        self.resultado.column("Validade", width=80)
        self.resultado.column("CVV", width=60)
        
        # Configurar grid com scrollbar
        self.resultado.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.resultado.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.resultado.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansão da área de resultados
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
        
        # Inicializar lista de cartões
        self.atualizar_cartoes(None)

    def atualizar_cartoes(self, event):
        """Atualiza a lista de cartões baseado no banco selecionado"""
        banco_selecionado = self.banco_combo.get()
        cartoes_banco = [nome for nome, config in CONFIG_CARTOES.items() 
                        if config["banco"] == banco_selecionado]
        self.tipo_cartao['values'] = cartoes_banco
        if cartoes_banco:
            self.tipo_cartao.set(cartoes_banco[0])
            
    def gerar_cartoes(self):
        # Limpar tabela
        for item in self.resultado.get_children():
            self.resultado.delete(item)
            
        try:
            quantidade = int(self.quantidade.get())
            if quantidade < 1 or quantidade > 1000:
                raise ValueError("Quantidade deve ser entre 1 e 1000")
                
            tipo_cartao = self.tipo_cartao.get()
            if not tipo_cartao:
                raise ValueError("Selecione um tipo de cartão")
                
            config = CONFIG_CARTOES[tipo_cartao]
            
            # Gerar e mostrar cartões com tags alternadas para melhor visualização
            for i in range(quantidade):
                cartao = gerar_cartao_credito(config)
                tag = 'par' if i % 2 == 0 else 'impar'
                self.resultado.insert("", tk.END, values=cartao, tags=(tag,))
                
            messagebox.showinfo("Sucesso", f"{quantidade} cartões gerados com sucesso!")
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
    
    def exportar_excel(self):
        if not self.resultado.get_children():
            messagebox.showwarning("Aviso", "Gere alguns cartões primeiro!")
            return
            
        try:
            # Preparar dados
            dados = []
            for item in self.resultado.get_children():
                dados.append(self.resultado.item(item)["values"])
                
            df = pd.DataFrame(dados, columns=["Nome no Cartão", "Banco Emissor", 
                                            "Bandeira", "Número do Cartão",
                                            "Validade (MM/AA)", "CVV"])
            
            # Pedir local para salvar
            filename = asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Salvar cartões como"
            )
            
            if filename:
                df.to_excel(filename, index=False)
                messagebox.showinfo("Sucesso", f"Arquivo salvo com sucesso em:\n{filename}")
                
        except Exception as e:
            messagebox.showerror("Erro ao exportar", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorCartaoApp(root)
    root.mainloop()