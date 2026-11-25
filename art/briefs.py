"""Small plates: jury box; title ruling; people inside a Cartagena supermarket."""
from .plate import *

def brooklyn():
    p=Plate(316,145,'#c7b0a1')
    p.rect('#987e72',0,0,316,84)
    for x in range(-19,318,42):
        p.rect('#ae9381',x+2,0,x+38,70)
        p.line('#c8ac92',1.5,(x+5,64),(x+5,0))
    # A collective verdict: rows of jurors above a wooden box, rather than a judge.
    for row,positions in enumerate([[35,87,139,191,243,295],[14,66,118,170,222,274]]):
        base=60+row*30
        for i,x in enumerate(positions):
            head=['#bb8768','#d2a782','#996a50','#e0b38b'][(i+row)%4]
            collar=['#40565a','#65685e','#414c4b'][(i+row)%3]
            p.shape(collar,(x-21,base+7),((x-20,base-8),(x-10,base-12),(x-5,base-13)),((x,base-16),(x+11,base-12),(x+17,base-8)),((x+20,base-3),(x+21,base+2),(x+21,base+7)))
            p.oval('#424744',x-9,base-35,x+9,base-11)
            p.oval(head,x-7,base-31,x+8,base-13)
            p.poly('#474944',(x-8,base-26),(x-9,base-32),(x-4,base-36),(x+6,base-35),(x+9,base-30),(x,base-30))
        p.rect('#795e52',0,base+2,316,base+10)
        p.rect('#e0c2a1',0,base,316,base+2)
    p.rect('#95725f',0,96,316,145)
    for x in range(0,316,48):p.rect('#7c6053',x+4,101,x+44,142)
    # A case folder is a visual shorthand, not a facsimile of a court document.
    p.poly('#453f3c',(57,148),(72,71),(177,67),(184,61),(282,61),(269,146))
    p.poly('#d4ab79',(51,148),(65,65),(175,62),(183,56),(279,54),(264,146))
    p.poly('#f7e7c6',(55,147),(71,71),(273,62),(259,145))
    p.text(87,81,'HUAWEI',24,'bold','#493d35')
    p.rect('#a33d2f',128,106,250,138)
    p.text(137,113,'GUILTY',24,'bold','#fff0d4')
    for i in range(3):p.line('#bcaa8b',1.4,(77,112+i*7),(116-i*6,110+i*7))
    p.tag(10,8,'04  /  BROOKLYN')
    return p

def senegal():
    p=Plate(316,145,'#a7b6a1')
    p.poly('#8ba798',(0,110),(229,6),(316,0),(316,145),(0,145))
    p.poly('#54796d',(4,141),(171,114),(200,94),(294,86),(316,94),(316,145))
    p.poly('#627b6d',(15,141),(39,43),(178,35),(163,134))
    p.poly('#f4ebd1',(10,136),(33,38),(172,30),(150,126))
    p.line('#bca983',2,(20,128),(144,119),(163,38))
    p.text(43,53,'CAS',31,'display','#335a51')
    p.text(43,87,'RULING',15,'mono','#335a51')
    for i in range(3):p.line('#a5a58b',1.5,(39-i,108+i*5),(119-8*i,103+i*5))
    # A flowing Senegal tricolour behind the restored cup.
    p.poly('#29805e',(223,106),(259,89),(288,91),(317,77),(317,118),(285,129),(254,125),(221,142))
    p.poly('#efc454',(256,91),(285,91),(285,129),(254,125))
    p.poly('#b5503d',(285,91),(317,77),(317,118),(285,129))
    def star(x,y,r):
        pts=[]
        for j in range(10):
            a=-math.pi/2+j*math.pi/5;w=r if j%2==0 else .43*r
            pts.append((x+math.cos(a)*w,y+math.sin(a)*w))
        return pts
    p.poly('#347756',*star(270,109,9))
    # Africa Cup: globe of gold carried by tapered, upward-opening flutes.
    gold='#d8a039'; shine='#ffe09a';edge='#725736'
    p.oval(edge,164,130,247,141)
    p.poly('#4a5146',(171,125),(235,125),(240,136),(166,136))
    p.oval('#cab06e',170,121,236,132)
    p.shape(edge,(170,123),((187,114),(192,103),(185,83)),((180,68),(165,65),(167,41)),((170,30),(179,25),(185,22)),((180,38),(169,45),(190,57)),((203,66),(224,61),(231,42)),((234,35),(230,27),(229,25)),((251,44),(238,67),(225,79)),((208,98),(213,112),(235,123)),((216,130),(187,130),(170,123)))
    p.oval('#9b7138',177,16,232,69)
    p.oval(gold,178,16,229,65)
    p.oval('#eec05d',180,18,224,59)
    p.poly('#bd8739',(190,29),(195,24),(203,25),(208,23),(215,25),(216,30),(219,32),(224,33),(218,40),(216,48),(210,55),(207,52),(205,43),(202,39),(196,40),(191,36))
    p.stroke(shine,2.7,(182,38),((184,28),(192,21),(201,20)))
    p.shape(gold,(173,123),((202,107),(186,81),(178,72)),((168,61),(163,53),(169,39)),((169,59),(188,59),(200,76)),((211,92),(198,107),(210,120)),((220,122),(225,122),(230,124)),((207,129),(190,126),(173,123)))
    p.shape('#efbc59',(195,119),((207,97),(192,84),(209,67)),((219,58),(230,57),(235,43)),((234,65),(224,71),(216,82)),((203,101),(217,113),(222,119)))
    p.stroke(shine,2.2,(176,57),((180,65),(198,70),(199,88)),((204,102),(196,113),(185,120)))
    p.line('#f7d27e',2,(171,130),(234,130))
    p.tag(10,8,'05  /  SENEGAL')
    return p

def cartagena():
    p=Plate(316,145,'#b48061')
    p.rect('#dbb98a',0,0,316,24)
    p.rect('#3d5e5b',20,23,294,145)
    # A neighborhood grocery at street level: sign, awning, produce, glass doors.
    p.rect('#ead1a4',18,25,298,58)
    p.rect('#224847',22,29,294,54)
    p.text(67,33,'SUPERMERCADO',23,'narrow','#fff0c7',225)
    p.poly('#a94936',(17,55),(296,55),(305,72),(9,72))
    for i in range(9):
        x=19+i*32
        p.poly('#edcb93',(x,55),(x+13,55),(x+12+(i-4)*1.1,72),(x-2+(i-4)*1.1,72))
    p.rect('#1f3e40',14,73,302,79)
    p.rect('#88a29a',24,80,156,142)
    # Layered stock shapes in the shop, deliberately interrupted by people.
    for row in range(2):
        y=88+row*20
        for k in range(13):
            x=27+k*10
            p.rect(['#d7b677','#b27755','#567d76'][(k+row)%3],x,y-(k%3),x+6,y+8)
        p.rect('#476767',25,y+8,156,y+11)
    p.rect('#738e88',160,80,286,144)
    p.poly('#8ea497',(169,80),(197,80),(164,126),(160,126),(160,94))
    p.poly('#9dab96',(228,80),(239,80),(193,145),(183,145))
    # Two people, close to one another behind the glass, facing the street.
    def person(x,y,coat,face,hair):
        p.shape(coat,(x-16,y+45),((x-15,y+29),(x-19,y+19),(x-6,y+16)),((x-4,y+13),(x+2,y+14),(x+7,y+16)),((x+17,y+17),(x+16,y+31),(x+18,y+45)))
        p.rect(face,x-3,y+9,x+4,y+18)
        p.oval(hair,x-8,y-5,x+8,y+11)
        p.oval(face,x-6,y-2,x+6,y+13)
        p.poly(hair,(x-7,y+6),(x-8,y-2),(x-4,y-6),(x+4,y-6),(x+8,y-2),(x+6,y+4),(x,y),(x-5,y+1))
    person(187,101,'#ba8a66','#d5a078','#3e4541')
    person(219,98,'#364f52','#b4805d','#2c413f')
    # Raised open hands silhouette clearly against the lighter interior.
    p.poly('#ba8a66',(174,121),(168,116),(166,103),(170,101),(176,112),(182,116))
    p.poly('#e6b68b',(166,105),(162,97),(162,91),(164,92),(166,97),(165,89),(167,89),(169,96),(170,92),(172,93),(171,102))
    p.poly('#364f52',(226,117),(232,112),(234,102),(238,103),(238,117),(232,126))
    p.poly('#c28e6c',(234,104),(232,99),(232,93),(234,93),(235,98),(236,89),(238,89),(237,96),(239,90),(240,91),(240,99),(238,105))
    p.line('#263f40',4,(158,78),(158,145))
    p.line('#294648',4,(246,78),(246,145))
    p.line('#d4c3a7',2,(239,113),(239,126))
    # Slatted shutters at the right edge, not a depiction of a rescue.
    p.rect('#68807b',259,79,293,145)
    for y in range(81,146,7):p.line('#3d5d5d',1.5,(260,y),(292,y))
    for i in range(3):
        x=23+43*i
        p.poly('#414f48',(x,124),(x+39,124),(x+35,144),(x+3,144))
        for j in range(10):
            xx=x+2+j%5*7+(4 if j>4 else 0);yy=124-j//5*5
            p.oval(['#d5b362','#cb8554','#91a77a'][i],xx,yy,xx+7,yy+8)
        p.rect('#986d4e',x,129,x+39,143)
        p.line('#d4a477',2,(x+2,134),(x+37,134))
    p.tag(10,8,'06  /  COLOMBIA')
    return p
