from PIL import Image
import sys

def light(pic):
    pic = pic.convert('L')
    w, h = pic.size
    for y in range(h):
        for x in range(w):
            l = (pic.getpixel( (x, y) ) >> 1) + 128
            pic.putpixel( (x, y), (l) )
    return pic

def dark(pic):
    pic = pic.convert('L')
    w, h = pic.size
    for y in range(h):
        for x in range(w):
            l = pic.getpixel( (x, y) ) >> 1
            pic.putpixel( (x, y), (l) )
    return pic

def samesize(pic1, pic2):
    w1, h1 = pic1.size
    w2, h2 = pic2.size
    w, h = max(w1, w2), max(h1, h2)
    wm, hm = abs(w1 - w2) >> 1, abs(h1 - h2) >> 1
    sspic1 = Image.new('L', (w, h), 0xFF)
    sspic2 = Image.new('L', (w, h), 0x0)
    if w == w1 and h == h1:
        sspic1.paste(pic1, (0, 0, w1, h1) )
        sspic2.paste(pic2, (wm, hm, wm + w2, hm + h2) )
    elif w == w1 and h == h2:
        sspic1.paste(pic1, (0, hm, w1, hm + h1) )
        sspic2.paste(pic2, (wm, 0, wm + w2, h2) )
    elif w == w2 and h == h1:
        sspic1.paste(pic1, (wm, 0, wm + w1, h1) )
        sspic2.paste(pic2, (0, hm, w2, hm + h2) )
    else:
        sspic1.paste(pic1, (wm, hm, wm + w1, hm + h1) )
        sspic2.paste(pic2, (0, 0, w2, h2) )
    return sspic1, sspic2

def tank(outpic, inpic):
    w, h = outpic.size
    newpic = Image.new('LA', inpic.size)
    for y in range(h):
        for x in range(w):
            outl, inl = outpic.getpixel( (x, y) ), inpic.getpixel( (x, y) )
            newa = 255 - (outl - inl)
            if newa == 0:
                newl = 0
            else:
                newl = int(inl / newa * 255)
            newpic.putpixel( (x, y), (newl, newa) )
    return newpic

if __name__ == '__main__':
    arg = sys.argv
    if len(arg) == 3:
        outp, inp = Image.open(arg[1]), Image.open(arg[2])
        light(outp).show
        dark(inp).show
        newp1, newp2 = samesize(light(outp), dark(inp) )
        newp = tank(newp1, newp2)
        newp.save('tank_out.png')
        inp.close()
        outp.close()
        newp.close()
    else:
        print('Please read "README.md" first!')
