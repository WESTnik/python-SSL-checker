## Python SSL checker

---
This project validate SSL certificate external site. If the certificate has expired then it is sent notification message on you Telegram bot otherwise the script shows the number of days before the expiration date.

---

### Requirements

The code is written in Python 3.10.0.

Before starting you must install the following Python-libraries:
1. All requirements
```bash
pip install -r requirements.txt
```
In the next step, you must create a telegram bot using @BotFather which will give you token to access the HTTP API looks like string 34334543534:DFTNMGFDdfddfadjkkmWfg.
To connect telegram_send library to you Telegram bot you must run the following command in terminal:
```bash
telegram-send --configure
```
After that you must enter you Telegram token in terminal and press "Enter". The terminal code will appear in you Telegram bot.

See more [Documentation](https://pythonhosted.org/telegram-send/#telegram-send)

---

### Usage

---
For the program to work, you need to pass two arguments - the domain name and the number of days


To start on Windows:
```bash
 python.exe .\ssl_checker.py dev.by 40
```

To start on Linux-based:
```bash
python3 ./ssl_checker.py dev.by 40
```
---

### License
BSD

### Author information
Author's email : [Lisenok.p@gmail.com](Lisenok.p@gmail.com)