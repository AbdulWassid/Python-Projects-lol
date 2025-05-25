import pygame
import level1
import level2
import level3
import level4

def game():
    pygame.init()
    
    #level 1
    lvl1_completed = level1()
    
    #level 2
    if lvl1_completed:
        lvl2_completed = level2()
        
    #level 3
    if lvl2_completed:
        level3_completed = level3()
    #level 4
    if level3_completed:
        level4 = level4()

if __name__ == "__main__":
    game()