"""Typeset and render the illustrated front page. Run with Pillow and Windows fonts."""
from pathlib import Path
from art.plate import *
from art import hormuz, field, briefs

ROOT = Path(__file__).resolve().parent
VERMILION = '#ab4531'

def globe(p,x,y,r):
    # A globe in a square of ink, with a cut meridian offset from the equator.
    p.rect(INK,x-r-6,y-r-6,x+r+6,y+r+6)
    c='#f4e9cf'
    for arc in (1,.50):
        p.d.ellipse(p.p([(x-r*arc,y-r),(x+r*arc,y+r)]),outline=c,width=round(2.5*S))
    for a in [-.54,0,.54]:
        w=r*math.sqrt(1-a*a)
        p.line(c,2,(x-w,y+r*a),(x+w,y+r*a))
    p.line(c,1.9,(x,y-r),(x,y+r))
    p.oval('#e88755',x+r*.52-5,y-r*.54-5,x+r*.52+5,y-r*.54+5)

def section_text(p,x,head,lines,w,small=False):
    top=878 if small else 605
    p.text(x,top,head,32 if small else 35,'display',INK,w)
    start=927 if small else 652
    for i,line in enumerate(lines):
        p.text(x,start+i*(26 if small else 27),line,22 if small else 24,'sans',INK,w)

def render():
    p=Plate(1024,1024,PAPER)
    p.rect(INK,22,14,1002,18)
    globe(p,60,71,31)
    p.text(113,31,'THE ILLUSTRATED WORLD DAILY',15,'mono',VERMILION)
    p.text(111,50,'Day Atlas',72,'display',INK,417)
    p.line('#aaa791',1,(608,31),(608,108))
    p.text(635,39,'TUESDAY',21,'mono',VERMILION)
    p.text(632,58,'24 NOV 2026',58,'bold',INK,370)
    p.paste(hormuz.draw(),22,120)
    p.paste(field.ukraine(),22,416)
    p.paste(field.taiwan(),519,416)
    section_text(p,22,'Two killed in Zaporizhzhia',
                 ['An overnight Russian strike', 'damages homes in the city.'],482)
    section_text(p,519,'Taiwan stocks jump 9%',
                 ['Nvidia reinstated Jensen Huang','as CEO on Monday.'],482)
    p.line('#b4b1a1',1,(512,416),(512,699))
    p.rect(INK,22,706,1002,708)
    for x,draw in [(22,briefs.brooklyn),(354,briefs.senegal),(686,briefs.cartagena)]:p.paste(draw(),x,719)
    section_text(p,22,'Jury convicts Huawei',
                 ['Federal jury finds firm and three','subsidiaries guilty of bank fraud.'],316,True)
    # Give the cup its own line rather than squeezing five words into one column.
    p.text(354,878,'Senegal regains',32,'display',INK,316)
    p.text(354,912,'Africa Cup',32,'display',INK,316)
    p.text(354,953,'Court restores the 2025 title.',22,'sans',INK,316)
    section_text(p,686,'Hostages in Cartagena',
                 ['Armed men took hostages','inside a supermarket.'],316,True)
    for x in (346,678):p.line('#b4b1a1',1,(x,719),(x,975))
    p.rect(INK,22,987,1002,989)
    p.text(22,998,'DAY ATLAS',13,'bold',INK)
    p.text(119,998,'/   WORLD DESK',13,'mono',VERMILION)
    p.text(801,998,'24.XI.2026    /    01',14,'mono',INK)
    out=p.im.resize((1024,1024),Image.Resampling.LANCZOS)
    master = ROOT / 'assets' / 'entry.png'
    master.parent.mkdir(exist_ok=True)
    out.save(master,optimize=True)
    return out

if __name__=='__main__':render()
