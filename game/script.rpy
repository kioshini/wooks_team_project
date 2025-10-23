image bgBlack = "bgBlack.jpg"
image bgSpaceBackground = "bgSpaceBackground.jpg"

# Отключаем систему сохранений для аркадной игры
define config.has_quicksave = False
define config.has_autosave = False
define config.autosave_on_quit = False
define config.autosave_on_choice = False

# Экран главного меню с выбором мини-игр
screen main_menu_screen():
    tag menu
    modal True
    zorder 400
    
    frame:
        xalign 0.5 yalign 0.5
        padding (50, 40)
        background "#000000e0"
        
        vbox:
            spacing 30
            text "MINI GAMES COLLECTION" size 52 color "#00ffff" xalign 0.5 bold True
            
            null height 20
            
            vbox:
                spacing 15
                xalign 0.5
                
                textbutton "Space Shooter (Galaga Style)" action Jump("game_space_shooter") xalign 0.5:
                    text_size 28
                    xminimum 400
                
                textbutton "Game 2 (Coming Soon)" action NullAction() xalign 0.5:
                    text_size 28
                    xminimum 400
                    text_color "#808080"
                
                textbutton "Game 3 (Coming Soon)" action NullAction() xalign 0.5:
                    text_size 28
                    xminimum 400
                    text_color "#808080"
                
                null height 20
                
                textbutton "Quit Game" action Quit() xalign 0.5:
                    text_size 24
                    xminimum 400

label start:
    jump main_menu

label main_menu:
    scene bgBlack
    show screen main_menu_screen
    $ renpy.pause(hard=True)