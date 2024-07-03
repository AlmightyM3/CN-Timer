import pygame
import pygame_gui
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

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    pygame.display.set_caption("CN-Timer")
    pygame.display.set_icon(pygame.image.load(dirPath+"/icon.png"))
    DT = 1
    run = True

    with open(dirPath+"/data.json", "r") as file:
        data = json.load(file)
    
    bgImage = pygame.transform.scale(pygame.image.load(dirPath+data["BGImagePath"][5:] if "-dir-" in data["BGImagePath"] else data["BGImagePath"]), pygame.display.get_window_size()).convert()
    font = pygame.font.Font(data["Font"], data["FontSize"])
    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])

    GUImanager = pygame_gui.UIManager(pygame.display.get_window_size())
    GUIactive = False
    GUIback = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((75, 75), (275, 550)), manager=GUImanager)
    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((25, 25), (225, 50)), text="{Amanda is so cool}" if random.random() < 0.03 else "The Cool Menu", manager=GUImanager, container = GUIback)

    backgroundButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((138-80, 100), (160, 50)), text='Change Background', manager=GUImanager, container = GUIback)
    colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((138-85, 175), (170, 50)), text='Change Text Color', manager=GUImanager, container = GUIback)
    fontSizeLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((138-115, 250), (170, 50)), text="Change Font Size:", manager=GUImanager, container = GUIback)
    fontSizeEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((138+40, 255), (60, 40)), initial_text='', manager=GUImanager, container = GUIback)
    fontLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((138-100, 325), (130, 50)), text="Change Font:", manager=GUImanager, container = GUIback)
    fontEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((138+20, 330), (80, 40)), initial_text='', manager=GUImanager, container = GUIback)

    backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((138-35, 400), (70, 50)), text='Back', manager=GUImanager, container = GUIback)
    exitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((138-35, 475), (70, 50)), text='Quit', manager=GUImanager, container = GUIback)

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

        if GUIactive:
            GUImanager.update(DT)
            GUImanager.draw_ui(window)
        
        pygame.display.flip()
        DT = clock.tick(30)/1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if GUIactive:
                    GUIactive = False
                else:
                    GUIactive = True
            
            GUImanager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exitButton:
                    run = False
                elif event.ui_element == backButton:
                    newFont = fontEntery.get_text()
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
                    
                    newFontSize = fontSizeEntery.get_text()
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
                    
                    with open(dirPath+"/data.json", "r") as file:
                        data = json.load(file)
                    
                    bgImage = pygame.transform.scale(pygame.image.load(dirPath+data["BGImagePath"][5:] if "-dir-" in data["BGImagePath"] else data["BGImagePath"]), pygame.display.get_window_size()).convert()
                    font = pygame.font.Font(data["Font"], data["FontSize"])
                    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])
                    GUIactive = False
                
                elif event.ui_element == colorButton:
                    colour_picker = pygame_gui.windows.UIColourPickerDialog(pygame.Rect(160, 50, 420, 400), GUImanager, window_title='Change Colour...')
                elif event.ui_element == backgroundButton:
                    file_dialog = pygame_gui.windows.UIFileDialog(pygame.Rect(160, 50, 440, 500), GUImanager, window_title='Load Image...', initial_file_path=dirPath, allow_picking_directories=False, allow_existing_files_only=True, allowed_suffixes={".png",".jpg"})

            if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                try:
                    image_path = pygame_gui.core.utility.create_resource_path(event.text)
                    image_path  = image_path.lower()
                    if "\\" in image_path:
                        image_path = image_path.replace("\\", "/")
                    if dirPath in image_path:
                        image_path = image_path.replace(dirPath, "-dir-")
                    
                    with open(dirPath+"/data.json", 'r+') as f:
                        data = json.load(f)
                        data['BGImagePath'] = image_path 
                        f.seek(0) 
                        json.dump(data, f, indent=4)
                        f.truncate() 
                except pygame.error:
                    pass
            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                color = event.colour
                with open(dirPath+"/data.json", 'r+') as f:
                    data = json.load(f)
                    data['FontColor']['r'] = color[0]
                    data['FontColor']['g'] = color[1]
                    data['FontColor']['b'] = color[2]
                    f.seek(0) 
                    json.dump(data, f, indent=4)
                    f.truncate() 
    pygame.quit()