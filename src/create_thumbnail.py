from PIL import Image, ImageFont, ImageDraw 

def make_thumbnail(white, black):
    # Open an Image
    img = Image.open('data/thumbnails/template.jpeg')
    
    # Call draw Method to add 2D graphics in an image
    d = ImageDraw.Draw(img)
    
    # Custom font style and font size
    font = '/Users/francesc/Desktop/Francesc/No_UNI/Programació/py_projects/py_dailyChess/data/arial.TTF'
    
    selected_size = 1
    for size in range(1, 400):
        song_ifont = ImageFont.truetype(font, size)
        left, top, right, bottom = song_ifont.getbbox(white)
        w = right - left
        h = bottom - top
        if w > 1000 or h > 300:
            break
        selected_size = size
    
    selected_size2 = 1
    for size in range(1, 400):
        author_ifont = ImageFont.truetype(font, size)
        left, top, right, bottom = author_ifont.getbbox(black)
        w = right - left
        h = bottom - top
        if w > 1000 or h > 300:
            break
        selected_size2 = size
    selected_size = min(selected_size, selected_size2)

    song_ifont = ImageFont.truetype(font, selected_size)
    author_ifont = ImageFont.truetype(font, selected_size)


    # Add Text to an image
    d.text((640, 720//2 - selected_size), white, font=song_ifont, stroke_width=selected_size//15, stroke_fill="#000000", fill="#FFE415", anchor="mm")
    d.text((640, 720//2), "vs", font=song_ifont, stroke_width=selected_size//15, stroke_fill="#000000", fill="#FFE415", anchor="mm")
    d.text((640,  720//2 + selected_size), black, font=author_ifont, stroke_width=selected_size//15, stroke_fill="#000000", fill="#FFE415", anchor="mm")
    
    # Display edited image
    #img.show()

    # Save the edited image
    img.save("data/thumbnails/thumbnail.jpg")

