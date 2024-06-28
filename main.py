from tkinter import *
from tkinter import ttk, filedialog, colorchooser

import pygame

import random
import time
import json
import os

myTuple= ("A", "M", "A", "N", "D", "A")

if not pygame.font:
    print("Pygame font module not found.")
    exit()
dirPath = os.path.dirname(os.path.abspath(__file__)).lower()
if "\\" in dirPath:
    dirPath = dirPath.replace("\\", "/")

def importImage():
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("PNG files", "*.png"), ("JPG files", "*.jpg"), ("All files", "*.*")]).lower()
    if file_path:
        if dirPath in file_path:
            file_path = file_path.replace(dirPath, "-dir-")
        return file_path
    return False

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("CN-Timer")
    pygame.display.set_icon(pygame.image.load(dirPath+"/icon.png"))
    run = True

    with open(dirPath+"/data.json", "r") as file:
        data = json.load(file)
    
    bgImage = pygame.transform.scale(pygame.image.load(dirPath+data["BGImagePath"][5:] if "-dir-" in data["BGImagePath"] else data["BGImagePath"]), pygame.display.get_window_size()).convert()
    font = pygame.font.Font(data["Font"], data["FontSize"])
    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])

    while run:
        window.blit(bgImage, (0,0))
        currentTime = time.localtime()
        currentMin = currentTime.tm_min % 60
        currentSec = currentTime.tm_sec % 60
        minLeft = (49-currentMin) % 50 if currentMin<50 else (59-currentMin) % 10
        secLeft = (59 - currentSec) % 60

        text = font.render(f"{minLeft}:{secLeft if secLeft>=10 else '0'+str(secLeft)}", True, fontColor)
        textPos = text.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2))
        window.blit(text, textPos)
        
        pygame.display.flip()
        clock.tick(30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                root = Tk()
                root.attributes("-topmost", True)
                root.iconbitmap(dirPath+"/Icon.ico")
                
                ttk.Label(root, text=" {Amanda is so cool} " if random.random() < 0.03 else "  The Cool Menu  ", font='Helvetica 14 bold').pack()

                def updateBGImage():
                    path = importImage()
                    if path:
                        with open(dirPath+"/data.json", 'r+') as f:
                            data = json.load(f)
                            data['BGImagePath'] = path 
                            f.seek(0) 
                            json.dump(data, f, indent=4)
                            f.truncate() 
                def updateColor():
                    color = colorchooser.askcolor()[0]
                    
                    with open(dirPath+"/data.json", 'r+') as f:
                        data = json.load(f)
                        data['FontColor']['r'] = color[0]
                        data['FontColor']['g'] = color[1]
                        data['FontColor']['b'] = color[2]
                        f.seek(0) 
                        json.dump(data, f, indent=4)
                        f.truncate() 
                    
                ttk.Button(root, text="Change background", command=updateBGImage).pack()
                ttk.Button(root, text="Change timer color", command=updateColor).pack()
                
                ttk.Label(root, text="Font: ").pack()
                FC = Entry(root, width=10)
                FC.pack()
                
                ttk.Label(root, text="Font size: ").pack()
                FS = Entry(root, width=5)
                FS.pack()
                
                def quit():
                    global run
                    root.destroy()
                    run = False
                def back():
                    global bgImage, font, fontColor

                    newFont = FC.get()
                    if newFont:
                        newFont = newFont.lower()
                        if newFont in pygame.font.get_fonts():
                            newFont = pygame.font.match_font(newFont)
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['Font'] = newFont 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                    
                    newFontSize = FS.get()
                    if newFontSize:
                        try: 
                            newFontSize = abs(int(newFontSize))
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['FontSize'] = newFontSize 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                        except: 
                            pass
                    
                    root.destroy()
                    with open(dirPath+"/data.json", "r") as file:
                        data = json.load(file)
                    
                    bgImage = pygame.transform.scale(pygame.image.load(dirPath+data["BGImagePath"][5:] if "-dir-" in data["BGImagePath"] else data["BGImagePath"]), pygame.display.get_window_size()).convert()
                    font = pygame.font.Font(data["Font"], data["FontSize"])
                    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])
                ttk.Button(root, text="Back", command=back).pack()
                ttk.Button(root, text="Quit", command=quit).pack()
                
                root.mainloop()
    pygame.quit()