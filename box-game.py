import random
# Classe do jogo, armazena estado das portas

class Game(object):
    def __init__(self, door_count=9):
        self.door_count = door_count
        self.number_closed = door_count
        self.doors = {i:False for i in range(1,door_count+1)} # True = fechada
        self.current_score = 0

    def __str__(self):
        out = []
        for door in self.doors:
            closed = self.doors[door]
            if closed:
                out.append(f'[{door}]')
            else:
                out.append(f'/{door}/')
        return ' '.join(out)
    
    def roll_die(self):
        return random.randint(1,6)
    
    def roll_dice(self):
        roll1 = self.roll_die()
        roll2 = self.roll_die()

        return roll1, roll2
    
    def get_open(self):
        return [i for i in self.doors if not self.doors[i]]
    
    def close_door(self, index):
        doors = self.doors

        if doors[index]:
            return False
        
        doors[index] = True
        return True
        
    def get_possibilities(self):
        points = self.current_score
        possibilities = []
        available_doors = [i for i in self.doors if not self.doors[i] and i <= points]

        while len(available_doors) > 0:
            node = available_doors.pop() # Pega o maior nó como inicial
            frontier = []
            thread = [node]
            cost = node
            father = None

            while True:
                
                # Se atingiu a soma, essa é uma possibilidade
                if cost == points:
                    possibilities.append(list(thread))
                    thread.pop() # Remove último elemento da thread
                    if len(thread) == 0: # Se era uma thread unitária, acabou a exploração
                        break
                
                # Se não atingiu a soma, segue explorando
                # Obtém a fronteira do nodo atual
                # Está na fronteira todo nodo menor que não ultrapasse o total de pontos
                else:
                    frontier = frontier + [(node, i) for i in available_doors if i<node and cost+i <= points]

                if len(frontier) == 0:
                    break

                father, next = frontier.pop()
                while thread[-1] != father:
                    thread.pop()
                node = next
                thread.append(node)
                cost = sum(thread)
        return possibilities            
    
    def input_loop(self):        
        n = len(self.possibilities)
        print('Possíveis combinações de portas a fechar:')
        for i, comb in enumerate(self.possibilities):
            str_ints = map(str, comb[::-1])
            print(f'{i+1}) [{", ".join(str_ints)}]')
        print()
        
        while True:
            try:
                entry = input('Escolha uma opção: ')
                num = int(entry)
            except:
                if entry in ['quit','exit','^C']:
                    exit()
                print('Entrada inválida')
                continue

            if num > n or num < 1:
                print(f'Escolha uma opção de 1 a {n}')
                continue

            selection = self.possibilities[num-1]
            return selection          

    def game_loop(self):
        while True:
            dice = self.roll_dice()
            self.current_score = sum(dice)
            print(f'Valor dos dados: {dice}.')
            print(f"Pontos disponíveis: {self.current_score}")
            print(self)

            self.possibilities = self.get_possibilities()
            if len(self.possibilities) == 0:
                print("Perdeu seu perdedor >:(")
                return

            choice = self.input_loop()
            for door in choice:
                self.doors[door] = True

            if all([self.doors[i] for i in self.doors]):
                print('Você ganhou! Que lacre')
                return

if __name__ == "__main__":
    game = Game(22)
    game.game_loop()
    