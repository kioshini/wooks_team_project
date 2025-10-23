"""
Space Shooter (Galaga Style) - Mini Game
"""

# Анимация огня для корабля игрока
image playerShip1:
    "PlayerShipStill1.png"
    0.1
    "PlayerShipStill2.png"
    0.1
    "PlayerShipStill3.png"
    repeat

# === ПЕРЕМЕННЫЕ ИГРЫ ===
default shipPos = [0.5, 0.9]
default moveStep = 0.015
default shipBounds = { "xmin": 0.25, "xmax": 0.75, "ymin": 0.7, "ymax": 0.95 }
default play_area = { "xmin": 0.25, "xmax": 0.75, "ymin": 0.05, "ymax": 0.95 }
default shipMuzzleOffsetX = 0.03
default shipMuzzleForwardY = -0.03

default bullets = []
default bullet_step = 0.025
default enemies = []
default enemy_size = { "hw": 0.015, "hh": 0.02 }
default show_enemy_hitboxes = False
default enemy_bullets = []
default enemy_bullet_step = 0.015
default player_lives = 3
default player_score = 0
default current_wave = 1
default game_over = False
default formation_x_offset = 0.0
default formation_direction = 1
default formation_speed = 0.002

# === ЛОГИКА ИГРЫ ===
init python:
    import pygame
    import random

    def MoveShip(dx, dy):
        shipPos[0] = max(shipBounds["xmin"], min(shipBounds["xmax"], shipPos[0] + dx))
        shipPos[1] = max(0.0, min(1.0, shipPos[1] + dy))

    def FireBulletUp(side):
        if game_over:
            return
        offset_x = shipMuzzleOffsetX if side == "right" else -shipMuzzleOffsetX
        spawn_x = max(0.0, min(1.0, shipPos[0] + offset_x))
        spawn_y = max(0.0, min(1.0, shipPos[1] + shipMuzzleForwardY))
        bullets.append({ "x": spawn_x, "y": spawn_y, "vx": 0.0, "vy": -bullet_step })

    def _rect_contains_point(ex, ey, hw, hh, px, py):
        return (ex - hw) <= px <= (ex + hw) and (ey - hh) <= py <= (ey + hh)

    def ResetGame():
        global player_lives, player_score, current_wave, game_over, formation_x_offset, formation_direction
        shipPos[0] = 0.5
        shipPos[1] = 0.9
        player_lives = 3
        player_score = 0
        current_wave = 1
        game_over = False
        formation_x_offset = 0.0
        formation_direction = 1
        bullets[:] = []
        enemies[:] = []
        enemy_bullets[:] = []
        SpawnEnemyFormation(current_wave)
        renpy.restart_interaction()

    def SpawnEnemyFormation(wave):
        enemies[:] = []
        rows = min(3 + wave // 2, 5)
        cols = 8
        start_y = 0.15
        spacing_x = 0.08
        spacing_y = 0.08
        center_x = 0.5
        
        for row in range(rows):
            for col in range(cols):
                x = center_x + (col - cols/2.0 + 0.5) * spacing_x
                y = start_y + row * spacing_y
                x = max(play_area["xmin"] + 0.02, min(play_area["xmax"] - 0.02, x))
                y = max(play_area["ymin"] + 0.02, min(play_area["ymax"] - 0.02, y))
                hw = enemy_size["hw"]
                hh = enemy_size["hh"]
                sw = renpy.config.screen_width
                sh = renpy.config.screen_height
                hb_px_w = int(hw * sw * 2)
                hb_px_h = int(hh * sh * 2)
                enemies.append({
                    "x": x, "y": y, "hw": hw, "hh": hh,
                    "alive": True, "hb_px_w": hb_px_w, "hb_px_h": hb_px_h,
                    "in_formation": True, "formation_x": x, "formation_y": y,
                    "dive_timer": 0, "dive_state": None
                })

    def EnemyShoot(enemy):
        if not enemy["alive"]:
            return
        enemy_bullets.append({
            "x": enemy["x"], "y": enemy["y"],
            "vx": 0.0, "vy": enemy_bullet_step
        })

    def UpdateEnemies():
        global formation_x_offset, formation_direction
        if not enemies or game_over:
            return
        
        formation_x_offset += formation_direction * formation_speed
        if formation_x_offset > 0.08 or formation_x_offset < -0.08:
            formation_direction *= -1
        
        for e in enemies:
            if not e["alive"]:
                continue
            
            if e["in_formation"]:
                e["x"] = max(play_area["xmin"], min(play_area["xmax"], e["formation_x"] + formation_x_offset))
                e["dive_timer"] -= 1
                if e["dive_timer"] <= 0:
                    if random.random() < 0.001:
                        e["in_formation"] = False
                        e["dive_state"] = "diving"
                        e["dive_target_x"] = shipPos[0]
                    else:
                        e["dive_timer"] = 60
                if random.random() < 0.002:
                    EnemyShoot(e)
            else:
                if e["dive_state"] == "diving":
                    dx = (e["dive_target_x"] - e["x"]) * 0.02
                    dy = 0.015
                    e["x"] = max(play_area["xmin"], min(play_area["xmax"], e["x"] + dx))
                    e["y"] += dy
                    if random.random() < 0.05:
                        EnemyShoot(e)
                    if e["y"] > play_area["ymax"]:
                        e["dive_state"] = "returning"
                elif e["dive_state"] == "returning":
                    target_x = max(play_area["xmin"], min(play_area["xmax"], e["formation_x"] + formation_x_offset))
                    dx = (target_x - e["x"]) * 0.03
                    dy = (e["formation_y"] - e["y"]) * 0.03
                    e["x"] = max(play_area["xmin"], min(play_area["xmax"], e["x"] + dx))
                    e["y"] = max(play_area["ymin"], min(play_area["ymax"], e["y"] + dy))
                    if abs(e["x"] - target_x) < 0.02 and abs(e["y"] - e["formation_y"]) < 0.02:
                        e["in_formation"] = True
                        e["dive_state"] = None
                        e["dive_timer"] = 120

    def UpdateEnemyBullets():
        global player_lives, game_over
        if not enemy_bullets or game_over:
            return
        remaining = []
        for b in enemy_bullets:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
            if not (-0.1 <= b["x"] <= 1.1 and -0.1 <= b["y"] <= 1.1):
                continue
            ship_hw = 0.03
            ship_hh = 0.04
            if _rect_contains_point(shipPos[0], shipPos[1], ship_hw, ship_hh, b["x"], b["y"]):
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                continue
            remaining.append(b)
        enemy_bullets[:] = remaining

    def UpdateBullets():
        global player_score, current_wave
        if game_over:
            return
        for b in bullets:
            b["x"] += b["vx"]
            b["y"] += b["vy"]
        remaining_bullets = []
        for b in bullets:
            if not (-0.1 <= b["x"] <= 1.1 and -0.1 <= b["y"] <= 1.1):
                continue
            hit = False
            for e in enemies:
                if e["alive"] and _rect_contains_point(e["x"], e["y"], e["hw"], e["hh"], b["x"], b["y"]):
                    e["alive"] = False
                    hit = True
                    player_score += 100
                    break
            if not hit:
                remaining_bullets.append(b)
        bullets[:] = remaining_bullets
        enemies[:] = [e for e in enemies if e["alive"]]
        if not enemies and not game_over:
            current_wave += 1
            SpawnEnemyFormation(current_wave)

    def ProcessInput():
        if game_over:
            return
        keys = pygame.key.get_pressed()
        dx, dy = 0.0, 0.0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= moveStep
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += moveStep
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= moveStep
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += moveStep
        if dx != 0.0 or dy != 0.0:
            MoveShip(dx, dy)

    def HideGameScreens():
        renpy.hide_screen("play_area_screen")
        renpy.hide_screen("ship_screen")
        renpy.hide_screen("keymap_screen")
        renpy.hide_screen("bullets_screen")
        renpy.hide_screen("enemy_bullets_screen")
        renpy.hide_screen("enemies_screen")
        renpy.hide_screen("hud_screen")
        renpy.hide_screen("game_over_screen")
        renpy.restart_interaction()

# === ЭКРАНЫ ===
screen keymap_screen():
    key "K_e" action [Function(FireBulletUp, "right"), Function(FireBulletUp, "left")]
    key "K_SPACE" action [Function(FireBulletUp, "right"), Function(FireBulletUp, "left")]
    key "K_q" action Function(FireBulletUp, "left")
    timer 0.02 repeat True action Function(ProcessInput)

screen ship_screen():
    zorder 100
    add "playerShip1" xalign shipPos[0] yalign shipPos[1]

screen bullets_screen():
    zorder 110
    for b in bullets:
        add Solid("#00ff00") xysize (3, 10) xalign b["x"] yalign b["y"]
    timer 0.02 repeat True action Function(UpdateBullets)

screen enemy_bullets_screen():
    zorder 110
    for b in enemy_bullets:
        add Solid("#ff0000") xysize (3, 10) xalign b["x"] yalign b["y"]
    timer 0.02 repeat True action Function(UpdateEnemyBullets)

screen enemies_screen():
    zorder 105
    for e in enemies:
        add Transform("virus-36904.png", xysize=(e["hb_px_w"], e["hb_px_h"])) xalign e["x"] yalign e["y"]
        if show_enemy_hitboxes:
            add Solid("#00ff0080") xysize (e["hb_px_w"], e["hb_px_h"]) xalign e["x"] yalign e["y"]
    timer 0.02 repeat True action Function(UpdateEnemies)

screen hud_screen():
    zorder 200
    frame:
        xalign 0.5 yalign 0.0
        padding (20, 10)
        background "#00000080"
        hbox:
            spacing 40
            text "LIVES: [player_lives]" size 24 color "#ffffff"
            text "SCORE: [player_score]" size 24 color "#ffff00"
            text "WAVE: [current_wave]" size 24 color "#00ff00"

screen game_over_screen():
    if game_over:
        zorder 300
        modal True
        frame:
            xalign 0.5 yalign 0.5
            padding (40, 30)
            background "#000000e0"
            vbox:
                spacing 20
                text "GAME OVER" size 48 color "#ff0000" xalign 0.5
                text "Final Score: [player_score]" size 32 color "#ffff00" xalign 0.5
                text "Wave Reached: [current_wave]" size 24 color "#00ff00" xalign 0.5
                textbutton "Restart" action Function(ResetGame) xalign 0.5
                textbutton "Return to Menu" action [Function(HideGameScreens), Jump("main_menu")] xalign 0.5

screen play_area_screen():
    zorder 50
    frame:
        xalign 0.5 yalign 0.5
        xysize (int((play_area["xmax"] - play_area["xmin"]) * config.screen_width), 
                int((play_area["ymax"] - play_area["ymin"]) * config.screen_height))
        background None
        padding (0, 0)
        add Solid("#ffffff20")
        add Solid("#00ff00") xysize (int((play_area["xmax"] - play_area["xmin"]) * config.screen_width), 2) yalign 0.0
        add Solid("#00ff00") xysize (int((play_area["xmax"] - play_area["xmin"]) * config.screen_width), 2) yalign 1.0
        add Solid("#00ff00") xysize (2, int((play_area["ymax"] - play_area["ymin"]) * config.screen_height)) xalign 0.0
        add Solid("#00ff00") xysize (2, int((play_area["ymax"] - play_area["ymin"]) * config.screen_height)) xalign 1.0

# === ТОЧКА ВХОДА В ИГРУ ===
label game_space_shooter:
    hide screen main_menu_screen
    $ ResetGame()
    scene bgBlack
    show bgSpaceBackground
    show screen play_area_screen
    show screen ship_screen
    show screen keymap_screen
    show screen bullets_screen
    show screen enemy_bullets_screen
    show screen enemies_screen
    show screen hud_screen
    show screen game_over_screen
    $ renpy.pause(hard=True)
