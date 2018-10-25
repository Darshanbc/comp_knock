from PIL import Image

im=Image.open("testfig.png")
px=im.load()


width, height = im.size
r=g=b=0
for x in range(width):
    for y in range(height):
    	(tr,tg,tb,k)=im.getpixel((x,y))
    	r=tr+r
    	b=tb+b
    	g=tg+g

print r/(width*height)
print g/(width*height)
print b/(width*height)


