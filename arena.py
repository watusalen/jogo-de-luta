import threading
import time
from rich.console import Console
from rich.table import Table
from personagem import Personagem

class Arena:
    """
    Classe que representa a arena onde ocorre a batalha entre os personagens.
    Cada personagem é uma thread separada que realiza ataques até que reste um único vencedor.
    """

    def __init__(self, nomes):
        """
        Inicializa a arena e cria os personagens que irão batalhar.

        :param nomes: Lista de nomes dos personagens que irão lutar.
        """
        self.console = Console()  # Console do rich para exibição formatada no terminal
        self.personagens = [Personagem(nome, 100, self) for nome in nomes]  # Cria os personagens com 100 de vida
        self.lock = threading.Lock()  # Lock para evitar condições de corrida ao acessar recursos compartilhados
        self.jogo_ativo = True  # Variável que indica se a batalha ainda está em andamento
        self.log = []  # Lista para armazenar as últimas ações dos personagens

    def registrar_acao(self, acao):
        """
        Registra uma ação no log da arena.
        Mantém um histórico das últimas 10 ações.

        :param acao: Texto descrevendo a ação realizada por um personagem.
        """
        with self.lock:  # Garante que múltiplas threads não modifiquem a lista simultaneamente
            self.log.append(acao)
            if len(self.log) > 10:  # Mantém apenas as últimas 10 ações visíveis
                self.log.pop(0)

    def exibir_estado(self):
        """
        Exibe no terminal o status dos personagens e o log das últimas ações.
        """
        self.console.clear()  # Limpa o terminal antes de exibir o novo estado

        # Criação da tabela de status dos personagens
        tabela = Table(title="Status da Batalha", style="bold magenta")
        tabela.add_column("Personagem", justify="left", style="cyan", no_wrap=True)
        tabela.add_column("Vida", justify="center", style="red")

        for p in self.personagens:
            # Exibe a vida restante com uma barra visual ou "Eliminado" caso o personagem esteja fora da batalha
            barra_vida = "█" * (p.vida // 5) if p.vida > 0 else "X"
            vida_texto = f"[red]{barra_vida} ({p.vida} HP)[/red]" if p.vida > 0 else "[red]Eliminado[/red]"
            tabela.add_row(p.nome, vida_texto)

        self.console.print(tabela)  # Exibe a tabela no terminal

        # Exibe o log das últimas ações realizadas pelos personagens
        self.console.print("\n[b]Últimas Ações:[/b]", style="bold yellow")
        for acao in self.log:
            self.console.print(acao, style="white")

    def iniciar_batalha(self):
        """
        Inicia a batalha entre os personagens.
        Cada personagem executa sua lógica de ataque em threads separadas até restar apenas um vencedor.
        """
        # Inicia as threads de cada personagem, permitindo que ataquem simultaneamente
        for p in self.personagens:
            p.start()

        # Loop principal do jogo, continua enquanto houver mais de um personagem vivo
        while True:
            with self.lock:
                vivos = [p for p in self.personagens if p.vida > 0]  # Obtém personagens ainda vivos
                if len(vivos) <= 1:
                    break  # Se restar apenas um personagem ou nenhum, a batalha termina
            
            self.exibir_estado()  # Atualiza o status no terminal
            time.sleep(0.5)  # Pequena pausa para suavizar a atualização da interface

        # Marca o jogo como encerrado
        self.jogo_ativo = False
        self.exibir_estado()  # Atualiza o estado final antes de declarar o vencedor

        # Determina o vencedor da batalha
        vencedor = next((p for p in self.personagens if p.vida > 0), None)
        if vencedor:
            self.console.print(f"\n[bold green]O grande vencedor é {vencedor.nome} com {vencedor.vida} HP![/bold green]\n")
        else:
            self.console.print("\n[bold red]Todos os personagens foram eliminados. Não há vencedor![/bold red]\n")

        # Aguarda um tempo antes de finalizar o programa para permitir leitura do resultado
        time.sleep(3)

        # Garante que todas as threads finalizem corretamente antes de encerrar o programa
        for p in self.personagens:
            p.join()