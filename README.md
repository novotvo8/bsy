# BSY Bonus Stage 5

### 1. Download clone script and run it in the repo

```
curl -O https://vojtech-novotny.com/bsy/clone.sh.zip
unzip clone.sh.zip
chmod 755 clone.sh
./clone.sh
```

### 2. Run the bots

```
python bot<id>/bot.py
```

### 3. Run the controller

```
python controller/controller.py
```

### Controller commands:

`SH <command>` - execute any shell command by the current bot

`CP <path_to_remote_file>` - copy a file from the current bot

`CH <bot_id>` - change bot you are controlling

`SA` - show active bots

### Cool Cat GitHub channel:

https://gist.github.com/novotvo8/5f6e9ef9fe8a3a54b74dff0c94fd61e1
