import csv
import tkinter as tk
import pygame
import random
from PIL import Image
#from PIL import EpsImagePlugin

#EpsImagePlugin.gs_windows_binary = r"C:\Users\Sam I guess\Documents\python projects\PokemonGame\gs\gs9.55.0\bin\gswin64.exe"

def main():
    run = False
    poke_dict =load_pokemon()
    print("Welcome! I hope you enjoy this short demo. I aquired the pokeball and character sprites from bulbapedia.com, and the pokemon\
        are from https://www.pokencyclopedia.info/en/index.php. The background used for the enocunter is from pokemon essentials. \n ")
    while run == False:
        print("The game will load in a seperate screen, so pull that up. The green is grass meaning that wild pokemon will appear! \nThere are two sets of controls\
used to play this game: WASD to move and ENTER to throw a pokeball. Keep pressing enter until you get the message that you \ncaught the pokemon.\
When you are finished playing press the red x on the top right of the screen. \n")
        ready = input("Do you understand? (Y or N) \n")
        
        #create_map() #DO NOT UNCOMMENT! FIND OUT BELOW
        
        if ready.lower() == "y" or ready.lower() == "yes":
            print("Good Luck and Have Fun!")
            run = True
            create_pygame(poke_dict)
    
    
def create_pygame(dict):
    #initalizes and set the window size, caption for the window as well as the images that are being loaded in
    pygame.init()
    win =pygame.display.set_mode((600,600))
    pygame.display.set_caption("Samantha Jenkins Pokemon Demo")
    bg = pygame.image.load('pokemon_background.png')
    char = pygame.image.load(r'sprites\Red_OD1.png')
    
    #Sets the placement of the character, how far they will move as well as their size
    x=32
    y=32
    #the next two values are used to later to determine how far the character has moved 
    x_relative = x
    y_relative = y
    width = 40
    height = 60
    vel = 5
    run = True

    #used to redraw the window after each key press to make the character have a walkling animation.
    def redraw_window():
        win.blit(bg, (0,0))

        win.blit(char,(x,y))

        pygame.display.update()


    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #gets the key presses from the users keyboard
        keys = pygame.key.get_pressed()
        #checks if they pressed a to move left and moves the character left
        if keys[pygame.K_a] and x > vel:
            x-= vel
            win.blit(char,(x,y))
        #same for right
        elif keys[pygame.K_d] and x < 600 - vel - width:
            x+= vel
        #same for up
        elif keys[pygame.K_w] and y> vel:
            y-= vel
        #same for down
        elif keys[pygame.K_s] and y < 600 - vel - height:
            y+= vel
        
        #checks to see if the character has moved 50 pixels in any one direction
        if x_relative== x+50 or x_relative == x-50 or y_relative == y-50 or y_relative == y+50:
            #calls the locate color function to see if the color is green
            locate_color(x,y,dict)
            #resets the values for x_relative and y_relative 
            x_relative = x
            y_relative = y
        
        redraw_window()
    
    pygame.QUIT

def locate_color(x, y,dict):
    #opens the background image
    background = Image.open("pokemon_background.png")
    background_load = background.load()
    #finds the r g and b values of the top left corner of the background which is green
    r, g, b, c = background_load[0,0]
    #locates the red green blue values of the middle pixel of the character
    red, green, blue, free_value = background_load[x,y]
    #Sees if the greens are the same if so it calls the encounter function
    if r==red and green == g and blue ==b:
        encounter(dict)

def encounter(dict):
    #randomly generates an int which is checked to see if an encounter will happen
    encounter_rate = random.randint(0,100)
    if encounter_rate >= 50:
        #randomly generates the pokemon's number
        pokemon = random.randint(1,151)
        #calls the find_pokemon function which gets the name and image name from the dictionary
        name, file = find_pokemon(dict, pokemon)
        #initalises a second game for the encounter
        pygame.init()
        win =pygame.display.set_mode((600,600))
        #background color
        color = (139,237,126)
        #fills in the background
        win.fill(color)
        #sets the caption and includes the pokemon's name
        pygame.display.set_caption(f"ENCOUNTER:{name}")
        #loads the background, back of the character, and the pokemon
        background = pygame.image.load(r"encounter_background\grass_base1.png")
        pokemon = pygame.image.load(rf"sprites\{file}")
        char = pygame.image.load(r"sprites\RGB_Red_Back.png")
        
        #used for success and name text
        white = (255,255,255)
        black = (0,0,0)
        success_font = pygame.font.Font('encounter_background\TIMES.TTF', 24)
        success_text = success_font.render(f'Success! You caught {name}', False, black, white )
        success_text_Rect = success_text.get_rect()
        success_text_Rect.center= (300, 300)

        pokemon_font = pygame.font.Font('encounter_background\TIMES.TTF', 16)
        pokemon_text = pokemon_font.render(f"{name}", False, black, white)
        pokemon_text_rect = pokemon_text.get_rect()
        pokemon_text_rect.center=(350,300)
        
        #places the images for the characters and images
        char_x = 175
        char_y = 350
        pokemon_x = 350
        pokemon_y = 200
        
        run = True

        #redraws the window
        def redraw_window():
            win.blit(background, (250,200))
            win.blit(pokemon,(pokemon_x,pokemon_y))
            win.blit(char,(char_x,char_y))
            win.blit(pokemon_text, pokemon_text_rect)

            pygame.display.update()

        while run:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            redraw_window()

            keys = pygame.key.get_pressed()
            #If enter key pressed laods the pokeball and finds the catch chance which is randomly generated
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                pokeball = pygame.image.load(r"sprites\pokeball.png")
                win.blit(pokeball,(pokemon_x,pokemon_y))
                pygame.display.update()

                catch_chance = random.randint(0,100)
                #if catch_chance is over 60 (so 40% chance of a catch) if prints the successful capture screen and closes the window.
                if catch_chance > 60:
                    print(f"You caught {name}")
                    win.blit(success_text,success_text_Rect)
                    pygame.display.update()
                    pygame.time.delay(1600)
                    run = False
                else:
                    redraw_window()

        pygame.QUIT

#uses the csv for the specific gen of pokemon wanted (for this case only gen 1 sprites have been been available) and creates a dictionary that is used in find pokemon
def load_pokemon():
    
    pokemon_dict = {}
    with open("gen01.csv", "rt") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            key = int(row[0])
            pokemon_dict[key] = row
    
    return pokemon_dict

#sees if the pokemon number is in the dictionary then return its name and the name.lower() + .png
def find_pokemon(dict,key):
    if key in dict:
        values = dict[key]
        name = values[1]
        pokemon_sprite = name + ".png"
        pokemon_sprite_file = pokemon_sprite.lower()
        return name, pokemon_sprite_file
    else:
        print("could not find")

                
#Creaes the map using tkinter
#I left this code here to demonstrate that I used tkinter in order to create my map, but in order to save the background as a png file there would be an additional series of 
#downloads that I do not feel comfortable making you do in order for you to run the program as it was fully intend. I have instead added the background in with the folder. 
def create_map():
    #Size of window
    width = 610
    height = 610

    # Create the Tk root object.
    root = tk.Tk()
    root.geometry(f"{width}x{height}")

    # Create a Frame object.
    frame = tk.Frame(root)
    frame.master.title("Scene")
    frame.pack(fill=tk.BOTH, expand=1)

    # Create a canvas object that will draw into the frame.
    canvas = tk.Canvas(frame)
    canvas.pack(fill=tk.BOTH, expand=1)
    
    #draws the background and the grass.
    def draw_scene (canvas, scene_left, scene_top, scene_right, scene_bottom):
        canvas.create_rectangle(scene_left, scene_top, scene_right, scene_bottom, fill='wheat1', outline='grey1')

        #Places the grass onto the background
        def draw_grass(canvas, left, top, right, bottom):
            canvas.create_rectangle(left, top, right, bottom, fill="OliveDrab3", outline= "OliveDrab3")
        draw_grass(canvas, scene_left, scene_top, 150, scene_bottom)
        draw_grass(canvas, scene_left, scene_top, 375, 175)
        draw_grass(canvas, 250, 250, 500, scene_bottom)
        draw_grass(canvas, 500, scene_top, scene_right, 300)

     # Call the draw_scene function.
    draw_scene(canvas, 10, 10, width-1, height-1)
    def save_as_png(canvas,fileName):
        # save postscipt image 
        canvas.postscript(file = fileName + '.ps') 
        # use PIL to convert to PNG 
        img = Image.open(fileName + '.ps') 
        img.save(fileName + '.png', 'png') 

    save_as_png(canvas, "pokemon_background")

    root.mainloop()

main()

