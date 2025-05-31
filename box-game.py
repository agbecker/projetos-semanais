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
            open = self.doors[door]
            if open:
                out.append(f'/{door}/')
            else:
                out.append(f'[{door}]')
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
    
    def input_loop(self):
        
        while True:
            entry = input('Portas a fechar: ')
            try:
                selection = list(map(int,entry.strip().split()))
            except:
                print('Entrada inválida')
                continue

            total = sum(selection)

            if any([door>self.door_count for door in selection]):
                print(f'Há apenas portas de 1 a {self.door_count}. Tente novamente.')
                continue

            if total > self.current_score:
                print(f"Este valor é maior que os pontos disponíveis. Você tem {self.current_score} pontos.")
                continue

            if any([door not in self.get_open() for door in selection]):
                print('Uma destas portas já está fechada')
                continue

            return selection          
        
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

    def game_over(self):
        open = self.get_open()
        if 0 < self.current_score < min(open):
            return True
        
        if len(open)==0:
            return True

        return False

    def game_loop(self):
        while True:
            dice = self.roll_dice()
            self.current_score = sum(dice)
            print(f'Valor dos dados: {dice}.')
            print(self)
            print(f"Pontos disponíveis: {self.current_score}")

            choice = self.input_loop()
            for door in choice:
                self.doors[door] = True

            if self.game_over():
                if len(self.get_open()) == 0:
                    print('Você ganhou! Que lacre')

                else:
                    print("Perdeu seu perdedor >:(")

                return




if __name__ == "__main__":
    game = Game()
    game.current_score = 5
    x = game.get_possibilities()
    print(x)
    # game.game_loop()
    