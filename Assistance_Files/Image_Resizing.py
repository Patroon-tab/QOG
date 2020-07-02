from PIL import Image, ImageTk



def resize(input,output,x,y):
    img = Image.open(input)
    img = img.resize((x, y))
    img.save(output)


def main():
    resize("pic.png", "pic2.png", 208, 183)
if __name__ == "__main__":
    main()



