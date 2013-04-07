import Image, ImageDraw, ImageFont

def watermark(img_src, text, pos):
    try:
        img = Image.open(img_src)
        draw = ImageDraw.Draw(img)
        
        draw_pos = (30, 10)
        if pos == 'top-left':
            draw_pos = (30, 30)
        elif pos == 'top-right':
            draw_pos = (img.size[0] - len(text) * 30, 10)
        elif pos == 'bottom-left':
            draw_pos = (30, img.size[1] - 80)
        else:
            draw_pos = (img.size[0] - len(text) * 30, img.size[1] - 80)
        
        font = ImageFont.truetype('summary.ttf', 50)
        draw.text(draw_pos, text, font=font)
        del draw
        img.save(img_src + '.jpg')
    except Exception, e:
        print 'watermark' + e