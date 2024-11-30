import random
import os
import threading

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def timer(pokemon):
    pokemon.aumentar_fome()
    threading.Timer(5.0, timer, [pokemon]).start()

class Pokemon:
    def __init__(self, nome, hp, defesa, ataque):
        self.nome = nome 
        self.hp = hp
        self.hp_inicial = hp
        self.defesa = defesa
        self.ataque = ataque
        self.felicidade = 50
        self.fome = 50
        self.energia = 50
        self.nivel = 1
        self.expTotal = 0
        self.expProxNv = 10
  
    def atacar(self, oponente):
        dano = self.ataque - oponente.defesa
        dano = max(0, dano)
        oponente.hp -= dano
        return dano
        
    def esta_vivo(self):
        return self.hp > 0
    
    def curar(self):
        self.hp = self.hp_inicial
       
    def aumentar_fome(self):
        if self.fome < 100:
            self.fome = min(100, self.fome + 20)
       
    def alimentar(self):
        if self.fome > 0:
            self.fome = max(0, self.fome - 20)
            print(f"{self.nome} foi alimentado! Fome: {self.fome}/100")
        else:
            print(f"{self.nome} está sem fome.")
        
    def brincar(self):
        self.felicidade = min(100, self.felicidade + 25)
        print(f"{self.nome} brincou com você! Felicidade: {self.felicidade}/100")
        
    def descansar(self):
        self.energia = min(100, self.energia + 30)
        print(f"{self.nome} descansou! Energia: {self.energia}/100")
        
    def ganhar_exp(self, pontos):
        self.expTotal += pontos
        print(f"{self.nome} ganhou {pontos} pontos de experiência! Total: {self.expTotal}/{self.expProxNv}")
        if self.expTotal >= self.expProxNv:
            self.subir_nv()
    
    def subir_nv(self):
        self.nivel += 1
        self.expTotal -= self.expProxNv
        self.expProxNv += 10
        print(f"Seu {self.nome} subiu para o nível {self.nivel}!!!")
        self.distribuir_pontos()
    
    def distribuir_pontos(self):
        pontosAtributo = 1
        while pontosAtributo > 0:
            print(f"Você possui {pontosAtributo} pontos de atributo para distribuir.")
            escolha = input("Escolha um atributo para aumentar, (H)P, (A)taque, (D)efesa: ").upper()
            if escolha == 'H':
                self.hp += 3
            elif escolha == 'A':
                self.ataque += 1
            elif escolha == 'D':
                self.defesa += 1
            else:
                print("Escolha inválida.")
                continue
            pontosAtributo -= 1
            
    @staticmethod
    def luta(pokemon_jogador, pokemon_adversario, jogador):
        print(f"Você foi desafiado por um {pokemon_adversario.nome}!")
        
        
        turno_do_jogador = True
        
        while pokemon_jogador.esta_vivo() and pokemon_adversario.esta_vivo():
            limpar_tela()
            
            if turno_do_jogador:
                
                print(f"É o seu turno!\n{pokemon_jogador.nome}: {pokemon_jogador.hp} HP\n{pokemon_adversario.nome}: {pokemon_adversario.hp} HP")
                acao = input("Escolha uma ação: (A)tacar, (F)ugir: ").upper()
                
                if acao == 'A':
                    dano = pokemon_jogador.atacar(pokemon_adversario)
                    print(f"Seu {pokemon_jogador.nome} causou {dano} de dano ao oponente!")
                    
                elif acao == 'F':
                    print("Você fugiu!")
                    return
                
                else:
                    print("Ação inválida.")
                    continue
                
            else:
                
                print(f"É o turno do {pokemon_adversario.nome}!")
                dano = pokemon_adversario.atacar(pokemon_jogador)
                print(f"O {pokemon_adversario.nome} causou {dano} de dano ao seu {pokemon_jogador.nome}!")
            
            
            turno_do_jogador = not turno_do_jogador
        
        
        if pokemon_jogador.esta_vivo():
            print(f"Você e {pokemon_jogador.nome} venceram!")
            pokemon_jogador.ganhar_exp(10)
            jogador.drop_item()
        else:
            print(f"Você e {pokemon_jogador.nome} foram derrotados...")
        
        pokemon_adversario.curar()


class Jogador:
    def __init__(self):
        self.inventario = {"Poção": 3, "Revive": 1}
    
    def mostrar_inventario(self):
        print("Inventário:")
        for item, quantidade in self.inventario.items():
            print(f"{item}: {quantidade}")
            
    def usar_item(self, item, pokemon):
        if item in self.inventario and self.inventario[item] > 0:
            if item == "Poção":
                pokemon.hp = min(pokemon.hp_inicial, pokemon.hp + 20)
                print(f"{pokemon.nome} foi curado em 20 pontos! HP atual: {pokemon.hp}/{pokemon.hp_inicial}")
            
            self.inventario[item] -= 1
        else:
            print(f"Você não tem {item} no seu inventário ou a quantidade é insuficiente.")
    
    def drop_item(self):
        itens_possiveis = ["Poção", "Revive"]
        item_dropado = random.choice(itens_possiveis)
        self.inventario[item_dropado] = self.inventario.get(item_dropado, 0) + 1
        print(f"Você recebeu um {item_dropado}!")

def jogar():
    jogador = Jogador()
    eevee = Pokemon("Eevee", hp=70, defesa=5, ataque=10)
    
    pokemon_adversarios = [
        Pokemon("Squirtle", hp=40, defesa=4, ataque=8),
        Pokemon("Charmander", hp=45, defesa=3, ataque=9),
        Pokemon("Bulbasaur", hp=45, defesa=5, ataque=7),
        Pokemon("Pikachu", hp=40, defesa=3, ataque=9),
        Pokemon("Pidgey", hp=35, defesa=2, ataque=7)
    ]
    
    timer(eevee)
    
    while eevee.esta_vivo():
        print("O que você quer fazer?")
        print("(A)limentar, (B)rincar, (D)escansar, (L)utar, (I)nventário, (F)ortalecer, (S)air.")
        acao = input("Escolha uma ação: ").upper()
        
        limpar_tela()
        
        if acao == 'A':
            eevee.alimentar()
            
        elif acao == 'B':
            if eevee.energia >= 10 and eevee.fome < 100:    
                eevee.brincar()
                eevee.energia = max(0, eevee.energia - 10)
            else:
                print(f"{eevee.nome} não quer brincar agora.")
            
        elif acao == 'D':
            eevee.descansar()
            
        elif acao == 'L':
            if eevee.energia >= 25:
                adversario = random.choice(pokemon_adversarios)
                Pokemon.luta(eevee, adversario, jogador)
                eevee.energia = max(0, eevee.energia - 25)
            else:
                print(f"{eevee.nome} está muito cansado para lutar.")
  
        elif acao == 'I':
            jogador.mostrar_inventario()
            item = input("Escolha um item para usar (ou digite 'S' para sair): ").capitalize()
            if item != 'S':
                jogador.usar_item(item, eevee)
        
        elif acao == 'F':
            print(f"{eevee.nome} está no nível {eevee.nivel}. Pontos de experiência: {eevee.expTotal}/{eevee.expProxNv}.")
            if eevee.expTotal >= eevee.expProxNv:
                resposta = input(f"Seu {eevee.nome} possui pontos de experiência suficientes para aumentar de nível. Deseja prosseguir? (s/n)").upper()
                if resposta == 'S':
                    eevee.subir_nv()
                elif resposta == 'N':
                    print("Você escolheu por não subir de nível agora.")
        
        elif acao == 'S':
            break
        
        else:
            print("Ação inválida.")
    
    print("Fim de jogo!")

jogar()


