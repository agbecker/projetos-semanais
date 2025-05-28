import random
# Classe do jogo, armazena estado das portas

class Game(object):
    def __init__(self, door_count=9):
        self.door_count = door_count
        self.number_closed = door_count
        self.doors = {i:False for i in range(1,door_count+1)}
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
    
    def get_closed(self):
        return [i for i in self.doors if not self.doors[i]]
    
    def close_door(self, index):
        doors = self.doors

        if doors[index]:
            return False
        
        doors[index] = True
        return True
    
    def input_loop(self):
        
        while True:
            num = input('Porta a fechar: ')
            try:
                num = int(num)
            except:
                print('Entrada inválida')
                continue

            if num>self.door_count:
                print(f'Há apenas portas de 1 a {self.door_count}. Tente novamente.')
                continue

            if num > self.current_score:
                print(f"Este valor é maior que os pontos disponíveis. Você tem {self.current_score} pontos.")
                continue

            if num not in self.get_closed():
                print('Esta porta já está aberta')
                continue

            return num            
            

    def game_over(self):
        closed = self.get_closed()
        if 0 < self.current_score < min(closed):
            return True
        
        if len(closed)==0:
            return True

        return False

    def game_loop(self):
        while True:
            dice = self.roll_dice()
            self.current_score = sum(dice)
            print(f'Valor dos dados: {dice}.')

            while not self.game_over() and self.current_score > 0:
                print(self)
                print(f"Pontos disponíveis: {self.current_score}")

                choice = self.input_loop()
                self.doors[choice] = True
                self.current_score -= choice


            if self.game_over():
                if len(self.get_closed()) == 0:
                    print('Você ganhou! Que lacre')

                else:
                    print("Perdeu seu perdedor >:(")

                return




if __name__ == "__main__":
    game = Game()
    game.game_loop()
    