"""Tile real rendered screenshots for layout review."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
files=sorted((root/'.screenshots').glob('[0-9][0-9].png'))
for group in range(0,len(files),12):
    canvas=Image.new('RGB',(1280,3*265),'#d9ded7')
    d=ImageDraw.Draw(canvas)
    for j,path in enumerate(files[group:group+12]):
        img=Image.open(path);img.thumbnail((310,230))
        x=(j%4)*320;y=(j//4)*265
        canvas.paste(img,(x,y+24));d.text((x+10,y+5),str(int(path.stem)),fill='#163c43')
    canvas.save(root/'.screenshots'/f'contact-{group//12+1}.png')
