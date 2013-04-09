import Image, ImageDraw, ImageFont

def watermark(img_src, text, pos):
    try:
        img = Image.open(img_src)
        draw = ImageDraw.Draw(img)
        size = draw.textsize(text)
        
        draw_pos = (30, 30)
        if pos == 'top-left':
            draw_pos = (30, 30)
        elif pos == 'top-right':
            draw_pos = (img.size[0] - size[0] - 30, 30)
        elif pos == 'bottom-left':
            draw_pos = (30, img.size[1] - size[1] - 30)
        else:
            draw_pos = (img.size[0] - size[0] - 30, img.size[1] - size[1] - 30)
        
        font = ImageFont.truetype('summary.ttf', 50)
        draw.text(draw_pos, text, font=font)
        del draw
        img.save(img_src + '.jpg')
    except Exception, e:
        print 'watermark' + e