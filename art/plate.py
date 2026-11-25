"""Drawing primitives for the six original spot illustrations, in design pixels."""
import math
import random
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

S = 3
INK = '#152e34'
PAPER = '#f7f1e1'
FONTS = Path('C:/Windows/Fonts')
FACES = {'display':'georgiab.ttf', 'serif':'georgia.ttf', 'italic':'georgiai.ttf',
         'sans':'arial.ttf', 'bold':'arialbd.ttf', 'narrow':'ARIALNB.TTF',
         'mono':'consolab.ttf'}

@lru_cache(None)
def font(face, size):
    return ImageFont.truetype(str(FONTS/FACES[face]),round(size*S))

class Plate:
    def __init__(self,w,h,color):
        self.w,self.h=w,h
        self.im=Image.new('RGB',(w*S,h*S),color)
        self.d=ImageDraw.Draw(self.im)

    def p(self,points): return [(round(x*S),round(y*S)) for x,y in points]
    def poly(self,col,*pts): self.d.polygon(self.p(pts),fill=col)
    def rect(self,col,x,y,u,v): self.d.rectangle(self.p([(x,y),(u,v)]),fill=col)
    def oval(self,col,x,y,u,v): self.d.ellipse(self.p([(x,y),(u,v)]),fill=col)
    def line(self,col,weight,*pts):
        self.d.line(self.p(pts),fill=col,width=max(1,round(S*weight)),joint='curve')
    def curve(self,start,*segments):
        pts=[start]
        for a,b,end in segments:
            x,y=pts[-1]
            for n in range(1,19):
                t=n/18; s=1-t
                pts.append((s**3*x+3*s*s*t*a[0]+3*s*t*t*b[0]+t**3*end[0],
                            s**3*y+3*s*s*t*a[1]+3*s*t*t*b[1]+t**3*end[1]))
        return pts
    def shape(self,col,start,*segments): self.poly(col,*self.curve(start,*segments))
    def stroke(self,col,width,start,*segments): self.line(col,width,*self.curve(start,*segments))
    def text(self,x,y,words,size,face='sans',color=INK,limit=None):
        """Top aligned to the cap line; optional modest horizontal typesetting."""
        f=font(face,size)
        cap=f.getbbox('H')[1]
        w=math.ceil(f.getlength(words))+S*4
        height=round(size*S*1.6)
        mask=Image.new('L',(w,height))
        ImageDraw.Draw(mask).text((S,-cap+round(size*S*.25)),words,font=f,fill=255)
        if limit and w>limit*S: mask=mask.resize((round(limit*S),height),Image.Resampling.LANCZOS)
        self.im.paste(color,(round(x*S)-S,round((y-size*.25)*S)),mask)
    def paste(self,other,x,y): self.im.paste(other.im,(int(x*S),int(y*S)))
    def tag(self,x,y,words):
        f=font('mono',16)
        width=math.ceil(f.getlength(words)/S)+20
        self.rect(INK,x,y,x+width,y+26)
        self.text(x+10,y+6,words,16,'mono',PAPER)
