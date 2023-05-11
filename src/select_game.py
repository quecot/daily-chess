
def select_code():
    codes    = open("data/codes.txt")
    uploaded = open("data/uploaded.txt")
    uploaded_s = uploaded.read()

    for code in codes:
        if code in uploaded_s:
            pass
        else:
            return code
    

def update_uploaded(code):
    with open("data/uploaded.txt", "r+") as f:
        old = f.read()
        f.seek(0)
        f.write(old + code)