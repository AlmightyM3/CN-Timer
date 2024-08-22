import pygame
import pygame_gui
#import asyncio
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

def main(): #async 
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
    countdownFont = pygame.font.Font(data["Font"], data["CountdownFontSize"])
    clockFont = pygame.font.Font(data["Font"], data["ClockFontSize"])
    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])
    clockOffset = data["ClockOffset"]

    GUImanager = pygame_gui.UIManager(pygame.display.get_window_size())
    GUIactive = False
    GUIback = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((75, 75), (300, 700)), manager=GUImanager)
    title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((300/2-225/2, 25), (225, 50)), text="{Amanda is so cool}" if random.random() < 0.05 else "The Cool Menu", manager=GUImanager, container = GUIback)

    backgroundButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150-80, 100), (160, 50)), text='Change Background', manager=GUImanager, container = GUIback)
    colorButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150-85, 175), (170, 50)), text='Change Text Color', manager=GUImanager, container = GUIback)
    countdownFontSizeLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150-125, 250), (170, 50)), text="Change Timer Font Size:", manager=GUImanager, container = GUIback)
    countdownFontSizeEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((150+50, 255), (90, 40)), initial_text='', manager=GUImanager, container = GUIback)
    clockFontSizeLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150-125, 325), (170, 50)), text="Change Clock Font Size:", manager=GUImanager, container = GUIback)#
    clockFontSizeEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((150+50, 330), (90, 40)), initial_text='', manager=GUImanager, container = GUIback)
    fontLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150-100, 400), (130, 50)), text="Change Font:", manager=GUImanager, container = GUIback)
    fontEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((150+20, 405), (80, 40)), initial_text='', manager=GUImanager, container = GUIback)
    offsetLable = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((150-120, 475), (140, 50)), text="Change Clock Offset:", manager=GUImanager, container = GUIback)
    offsetXEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((150+25, 480), (40, 40)), initial_text='', manager=GUImanager, container = GUIback)
    offsetYEntery = pygame_gui.elements.UITextEntryBox(relative_rect=pygame.Rect((150+70, 480), (40, 40)), initial_text='', manager=GUImanager, container = GUIback)

    backButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150-35, 550), (70, 50)), text='Back', manager=GUImanager, container = GUIback)
    exitButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150-35, 625), (70, 50)), text='Quit', manager=GUImanager, container = GUIback)

    while run:
        #await asyncio.sleep(0)
        window.blit(bgImage, (0,0))
        currentTime = time.localtime()
        currentMin = currentTime.tm_min % 60
        currentSec = currentTime.tm_sec % 60
        minLeft = (49-currentMin) % 50 if currentMin<50 else (59-currentMin) % 10
        secLeft = (60 - currentSec) % 59

        text = countdownFont.render(f"{minLeft}:{secLeft if secLeft>=10 else '0'+str(secLeft)}", True, fontColor)
        textPos = text.get_rect(center=(pygame.display.get_window_size()[0]/2, pygame.display.get_window_size()[1]/2))
        window.blit(text, textPos)

        text = clockFont.render(f"{currentTime.tm_hour%12}:{currentTime.tm_min if currentTime.tm_min>=10 else '0'+str(currentTime.tm_min)}:{currentTime.tm_sec if currentTime.tm_sec>=10 else '0'+str(currentTime.tm_sec)}", True, fontColor)
        s=text.get_bounding_rect().bottomright
        textPos = text.get_rect(center=(pygame.display.get_window_size()[0]-s[0]/2-clockOffset[0], s[1]/2+clockOffset[1]))
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
                    
                    newFontSize = countdownFontSizeEntery.get_text()
                    if newFontSize:
                        try: 
                            newFontSize = abs(int(newFontSize))
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['CountdownFontSize'] = newFontSize 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                        except: 
                            pass
                    
                    newFontSize = clockFontSizeEntery.get_text()
                    if newFontSize:
                        try: 
                            newFontSize = abs(int(newFontSize))
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['ClockFontSize'] = newFontSize 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                        except: 
                            pass
                    
                    newOffsetX = offsetXEntery.get_text()
                    if newOffsetX:
                        try: 
                            newOffsetX = abs(int(newOffsetX))
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['ClockOffset'][0] = newOffsetX 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                        except: 
                            pass
                    newOffsetY = offsetYEntery.get_text()
                    if newOffsetY:
                        try: 
                            newOffsetY = abs(int(newOffsetY))
                            with open(dirPath+"/data.json", 'r+') as f:
                                data = json.load(f)
                                data['ClockOffset'][1] = newOffsetY 
                                f.seek(0) 
                                json.dump(data, f, indent=4)
                                f.truncate() 
                        except: 
                            pass
                    
                    with open(dirPath+"/data.json", "r") as file:
                        data = json.load(file)
                    
                    bgImage = pygame.transform.scale(pygame.image.load(dirPath+data["BGImagePath"][5:] if "-dir-" in data["BGImagePath"] else data["BGImagePath"]), pygame.display.get_window_size()).convert()
                    countdownFont = pygame.font.Font(data["Font"], data["CountdownFontSize"])
                    clockFont = pygame.font.Font(data["Font"], data["ClockFontSize"])
                    fontColor = (data["FontColor"]["r"],data["FontColor"]["g"],data["FontColor"]["b"])
                    clockOffset = data["ClockOffset"]
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

if __name__ == "__main__":
    main()
    #asyncio.run(main())