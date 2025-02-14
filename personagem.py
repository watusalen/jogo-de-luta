import threading
import random
import time

class Personagem(threading.Thread):
    """
    Classe que representa um personagem no jogo de luta.
    Cada personagem é executado como uma thread separada e pode atacar outros personagens.
    """
    
    def __init__(self, nome, vida, arena):
        """
        Inicializa um personagem com nome, vida inicial e referência à arena onde a batalha ocorre.

        :param nome: Nome do personagem.
        :param vida: Quantidade inicial de vida do personagem.
        :param arena: Referência à arena onde a batalha ocorre.
        """
        super().__init__()  # Inicializa a thread
        self.nome = nome  # Nome do personagem
        self.vida = vida  # Vida inicial do personagem
        self.arena = arena  # Referência à arena para interagir com outros personagens
        self.lock = threading.Lock()  # Lock para evitar condições de corrida ao modificar a vida
    
    def atacar(self):
        """
        Escolhe aleatoriamente um oponente vivo na arena e o ataca,
        reduzindo sua vida em um valor aleatório entre 5 e 20.
        """
        with self.arena.lock:
            # Seleciona apenas personagens vivos (excluindo ele mesmo)
            oponentes_vivos = [p for p in self.arena.personagens if p != self and p.vida > 0]
            
            if not oponentes_vivos:
                return  # Nenhum oponente disponível para atacar, encerra a ação
            
            # Escolhe um oponente aleatório
            oponente = random.choice(oponentes_vivos)
        
        # Define um valor de dano aleatório entre 5 e 20
        dano = random.randint(5, 20)  
        
        with oponente.lock:
            if oponente.vida > 0:
                # Garante que o dano não reduza a vida abaixo de 0
                dano_real = min(dano, oponente.vida)  
                oponente.vida -= dano_real  # Aplica o dano ao oponente
                
                # Registra a ação na arena
                self.arena.registrar_acao(f"{self.nome} atacou {oponente.nome} causando {dano_real} de dano!")

                # Se o oponente for eliminado (vida chegar a 0), registrar a eliminação
                if oponente.vida == 0:
                    self.arena.registrar_acao(f"{oponente.nome} foi eliminado!")
    
    def run(self):
        """
        Método principal da thread. Enquanto o jogo estiver ativo e o personagem tiver vida,
        ele continuará atacando outros personagens até que reste apenas um sobrevivente.
        """
        while self.arena.jogo_ativo:
            with self.arena.lock:
                # Verifica quantos personagens ainda estão vivos
                vivos = [p for p in self.arena.personagens if p.vida > 0]
                
                # Se houver apenas um sobrevivente ou o próprio personagem foi eliminado, sair do loop
                if len(vivos) <= 1 or self.vida <= 0:
                    break  
            
            # Realiza um ataque contra um oponente vivo
            self.atacar()
            
            # Aguarda um tempo aleatório antes de realizar outro ataque (entre 0.5 e 1.5 segundos)
            time.sleep(random.uniform(0.5, 1.5))
