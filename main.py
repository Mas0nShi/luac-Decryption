import xxtea
import os
from traveDir import depthIteratePath
import sys
import random
from loguru import logger
from io import BytesIO
import zipfile

dIP = depthIteratePath([".luac"])

"""1.Print Log"""
try:
    from shutil import get_terminal_size as get_terminal_size
except:
    try:
        from backports.shutil_get_terminal_size import get_terminal_size as get_terminal_size
    except:
        pass
try:
    import click

except:
    class click:

        @staticmethod
        def secho(message=None, **kwargs):
            print(message)

        @staticmethod
        def style(**kwargs):
            raise Exception("unsupported style")

banner = """
 ooo        ooooo                      .oooo.              
 `88.       .888'                     d8P'`Y8b             
  888b     d'888   .oooo.    .oooo.o 888    888 ooo. .oo.  
  8 Y88. .P  888  `P  )88b  d88(  "8 888    888 `888P"Y88b 
  8  `888'   888   .oP"888  `"Y88b.  888    888  888   888 
  8    Y     888  d8(  888  o.  )88b `88b  d88'  888   888 
  o8o        o888o `Y888""8o 8""888P'  `Y8bd8P'  o888o o888o 

                     Running Start                           
\n"""


def show_banner():
    colors = ['bright_red', 'bright_green', 'bright_blue', 'cyan', 'magenta']
    try:
        click.style('color test', fg='bright_red')
    except:
        colors = ['red', 'green', 'blue', 'cyan', 'magenta']
    try:
        columns = get_terminal_size().columns
        if columns >= len(banner.splitlines()[1]):
            for line in banner.splitlines():
                if line:
                    fill = int((columns - len(line)) / 2)
                    line = line[0] * fill + line
                    line += line[-1] * fill
                click.secho(line, fg=random.choice(colors))
    except:
        pass


class ColorPrinter:
    @staticmethod
    def print_red_text(content, end="\n"):
        print("\033[1;31m %s \033[0m" % content, end=end),

    @staticmethod
    def print_green_text(content, end="\n"):
        print("\033[1;32m %s \033[0m" % content, end=end),

    @staticmethod
    def print_blue_text(content, end="\n"):
        print("\033[1;34m %s \033[0m" % content, end=end),

    @staticmethod
    def print_cyan_text(content, end="\n"):
        print("\033[1;36m %s \033[0m" % content, end=end),

    @staticmethod
    def print_white_text(content, end="\n"):
        print("\033[1;37m %s \033[0m" % content, end=end),


def readJscFile(path):
    """Read .jsc file in this path."""
    f = open(path, "rb")
    data = f.read()
    f.close()
    return data


def saveFile(saveData, fileDir):
    """Save the decrypted data on the same relative path."""
    rootPath = os.path.split(fileDir)[0]
    if not os.path.exists(rootPath):
        try:
            os.makedirs(rootPath)
        except OSError:
            if not os.path.exists(rootPath):
                raise Exception("Error: create directory %s failed." % rootPath)

    if fileDir.endswith("c"):
        file = fileDir[:-1]
    else:
        file = fileDir
    with open(file, "wb") as fd:
        fd.write(saveData)
    fd.close()


def decrypt(filePath, key, sign):
    """The main process to decryption."""
    data = readJscFile(path=filePath)
    # 1.xxtea decrypt
    if len(key) < 16:
        key += "\0" * (16 - len(key))  # padding \0

    dec_data = xxtea.decrypt(data=data[len(sign):], key=key[:16], padding=False, rounds=0)
    # 2.determine file type
    dec_data = bytes(dec_data)
    return dec_data


def batchDecrypt(srcDir, xxteaKey, sign):
    if not os.path.exists(srcDir):  # path exist
        logger.error("FileNotFound")
        exit(-1)
    isFile = os.path.isfile(srcDir)  # is files or dirs

    dirPath = os.path.dirname(srcDir)  # dir name ...xx/a.luac =>  ...xx/
    outPath = os.path.join(dirPath, "out")  # out path xx/out
    if isFile:
        filePathArr = [srcDir]  # get single file
    else:
        filePathArr = dIP.getDepthDir(srcDir)  # get fileTrees

    for filePath in filePathArr:
        decData = decrypt(filePath, xxteaKey, sign)  # decrypt core
        fileBaseName = os.path.basename(filePath)  # xxx/game.zip => game.zip
        zipDirName = os.path.splitext(fileBaseName)[0]  # game.zip => game

        if decData[:2] == b"PK":
            logger.info("decrypt file is ZIP, decompressing...")

            decompressPath = os.path.join(outPath, zipDirName)  # zip decompress path
            if not os.path.exists(outPath):
                os.mkdir(outPath)  # make dir
            if not os.path.exists(decompressPath):
                os.mkdir(decompressPath)  # make dir

            fio = BytesIO(decData)  # read bytesIO
            fzip = zipfile.ZipFile(file=fio)  # func zip
            for fileName in fzip.namelist():
                fzip.extract(fileName, decompressPath)  # save file in zip
                logger.success("Save flie:{0}".format(os.path.join(decompressPath, fileName)))

        else:

            saveFilePath = outPath + filePath.split(srcDir)[1]  # save path
            saveFile(decData, saveFilePath)  # save file
            logger.success("Save flie:{0}".format(saveFilePath))


def main():
    if len(sys.argv) != 5:
        print("\nThis is decrypt for Coco2d-luac .luac.")
        ColorPrinter.print_white_text("Usage : ")
        print("        python {0} [-d] [xxteaKey] [sign] [jscDir]".format(sys.argv[0]))
        ColorPrinter.print_white_text("Example : ")
        print(r"        python {0} -d e73c83539f2e65ab159 b4d6f1b968 C:\DecJsc-master\src".format(sys.argv[0]))
        ColorPrinter.print_white_text("Tips : ")
        print("        -d or -decrypt [decrypt]")
        print("        Supports folders and individual LUAC or ZIP files")
        print("        If you have any questions, please contact [ MasonShi@88.com ]\n")
        exit(1)

    instruct = sys.argv[1]
    xxtea_key = sys.argv[2]
    sign = sys.argv[3]
    srcDir = sys.argv[4]
    if instruct[1:2] == "d":
        show_banner()
        batchDecrypt(srcDir=srcDir, xxteaKey=xxtea_key, sign=sign)
        ColorPrinter.print_white_text("        Running exit...\n")


if __name__ == "__main__":
    main()
