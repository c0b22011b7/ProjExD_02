import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0)
    }  # 移動量の辞書

accs = [a for a in range(1, 11)]  # 加速度のリスト


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し、真理値タプルを消す関数
    引数 rct:　こうかとんor爆弾SurfaceのRect
    戻り値:横方向、縦方向判定結果 (画面内：True/画面外：False)
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向
        tate = False
    return yoko, tate
        

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_imgf = pg.transform.flip(kk_img, True, False)
    roto = {
        (0,-5):pg.transform.rotozoom(kk_imgf, 90, 1.0),
        (+5,-5):pg.transform.rotozoom(kk_imgf, 45, 1.0),
        (+5,0):pg.transform.rotozoom(kk_imgf, 0, 1.0),
        (+5,+5):pg.transform.rotozoom(kk_imgf, -45, 1.0),
        (0,+5):pg.transform.rotozoom(kk_imgf, -90, 1.0),
        (-5,+5):pg.transform.rotozoom(kk_img, 45, 1.0),
        (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
        (-5,-5):pg.transform.rotozoom(kk_img, -45, 1.0)
    }  # 押下キーに対応するSurfaceの辞書
    kk_rct = kk_img.get_rect()  # こうかとんSurfaceのrect
    kk_rct.center = 900, 400        
    bb_img = pg.Surface((20, 20))  # 練習1：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 黒い部分の透明化
    pg.draw.circle(bb_img, (255, 0, 0),(10, 10), 10)  # 半径10の赤い円
    bb_rct = bb_img.get_rect()  # 練習2：rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT) 
    vx ,vy = +5, +5  # 爆弾の速度
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct):
            kk_img = pg.image.load("ex02/fig/8.png")
            kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)  # 切り替え画像の用意
            screen.blit(bg_img,[0, 0])  # 背景の再描画
            screen.blit(kk_img,kk_rct)  # 切り替え後の画像をblit
            pg.display.update()
            clock.tick(1)
            print("Game Over")
            return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]: 
                sum_mv[0] += tpl[0]  # 押されたキーに応じて計算
                sum_mv[1] += tpl[1]
        
        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        x,y = sum_mv[0], sum_mv[1]
        if event.type == pg.KEYDOWN:
            kk_img = roto[(x, y)]  # 押下キーに応じた画像を参照しkk_imgに代入
        screen.blit(kk_img, kk_rct)
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)  # 練習2 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]  # 値の更新
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()