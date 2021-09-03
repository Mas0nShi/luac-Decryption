# luac-Decryption
⛔For xxtea only, nothing can be done with bytecode⛔

✈If you encounter **luajit**, try using [luajit-decompiler](https://github.com/Mas0nShi/luajit-decompiler) ✈

⚡This is a script that decrypts the coco2dx-luac .luac file⚡

🌈The core process is the decryption of **`XXTEA`**.🌈

### Usage :
        python main.py [-d] [xxteaKey] [sign] [jscDir/zipFile]
### Example :
        python main.py -d e73c83539f2e65ab159 b4d6f1b968 C:\DecJsc-master\src
        python main.py -d e73c83539f2e65ab159 b4d6f1b968 C:\DecJsc-master\game.zip
### Tips :
        -d or -decrypt [decrypt]
        If the TEA is 16 bytes of \x00, please fill in NONE
        Supports folders and individual LUAC or ZIP files
### Outputs :
        The output folder is located in the same directory as the LUAC folder.

### ❗Waiting for repair and Known errors :

 -[x] zip files decompress

 Welcome to submit issue.

![example](https://github.com/Mas0nShi/luac-Decryption/blob/master/example.png)

If you have any questions, please contact [ MasonShi@88.com ]
