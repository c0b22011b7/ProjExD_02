import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {pg.K_UP:(0, -5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5, 0),
         pg.K_RIGHT:(+5, 0)}  # 移動量の辞書

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # こうかとんSurfaceのrect
    kk_rct.center = 900,400
    enn = pg.Surface((20,20))  # 練習1：透明のSurfaceを作る
    enn.set_colorkey((0, 0, 0))  # 黒い部分の透明化
    pg.draw.circle(enn, (255,0,0), (10,10), 10)  # 半径10の赤い円
    bb_rct = enn.get_rect()  # 練習2：rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT) 
    vx ,vy = +5, +5  # 爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]: 
                sum_mv[0] += tpl[0]  # 押されたキーに応じて計算
                sum_mv[1] += tpl[1]
        
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0],sum_mv[1])
        screen.blit(kk_img, kk_rct.center)
        bb_rct.move_ip(vx, vy)  # 練習2 爆弾の移動
        screen.blit(enn,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()