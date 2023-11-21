from agents import Pacman
from agents import Ghost
from colorama import Fore

class Display:
    def __init__(self, pacmanPos, inkyPos, blinkyPos, dotPoses, wallPoses):
        self.pacman = Pacman(pacmanPos, inkyPos, blinkyPos, dotPoses, wallPoses, 5)
        self.inky = Ghost(inkyPos, pacmanPos, blinkyPos, wallPoses)
        self.blinky = Ghost(blinkyPos, pacmanPos, inkyPos, wallPoses)
        self.food = dotPoses
        self.wall = wallPoses
        self.turn = "pacman"

    def play_ground(self):
        for i in range(10, -1, -1):
            for j in range(0, 20):
                if (j, i) == self.pacman.position: 
                    print(f"{Fore.YELLOW}P{Fore.WHITE}", end="  " ) 
                    continue
                elif (j, i) == self.inky.position: 
                    print(f"{Fore.RED}I{Fore.WHITE}", end="  " )
                    continue 
                elif (j, i) == self.blinky.position: 
                    print(f"{Fore.CYAN}B{Fore.WHITE}", end="  " )
                    continue
                elif (j, i) in self.food: 
                    print(f"{Fore.GREEN}.{Fore.WHITE}", end="  " )
                    continue
                elif (j, i) in self.wall: 
                    print('#',end="  ")
                    continue
                else: 
                    print(' ',end="  ")
                    continue
            print('\n')
        
        print(f"                       ", "SCORE : ", self.pacman.update_score(), f"                       ")

    def lose(self):
        print(f"{Fore.RED} GAME OVER! {Fore.WHITE}")
    
    def win(self):
        print(f"{Fore.YELLOW} YOU WON!! {Fore.WHITE}")

    def change_turn(self, turn):
        self.turn = turn
    
    def update_foods(self):
        if self.pacman.position == self.food:
            self.food.remove(self.pacman.position)
