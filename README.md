## Python SSL checker

---
This project validate SSL certificate external site. If the certificate has expired then it is sent notification message on you Telegram bot otherwise the script shows the number of days before the expiration date.

---

### Requirements

The code is written in Python 3.10.0.

Before starting you must install the following Python-libraries:
1. telegram_send
```bash
sudo pip3 install telegram-send
```
In the next step, you must create a telegram bot using @BotFather which will give you token to access the HTTP API looks like string 34334543534:DFTNMGFDdfddfadjkkmWfg.
To connect telegram_send library to you Telegram bot you must run the following command in terminal:
```bash
telegram-send --configure
```
After that you must enter you Telegram token in terminal and press "Enter". The terminal code will appear in you Telegram bot.

See more [Documentation](https://pythonhosted.org/telegram-send/#telegram-send)

---
### Description

---
The constant "DAYS_TO_EXPIRATION" contain number of days set manually. It is used to calculate the expiration date of the certificate.

The boolean constant "SHOW" used as switch for send notification. By default is "TRUE".

Function * *"def check_cert_validity()"* * used for validate SSL certificate on site. Required function argument is SSL certificate. Returned function value is "TRUE" or "FALSE" 
```python
def check_cert_validity(cert: Dict) -> bool:
    not_after = str_to_date(cert['notAfter'])
    current_time = datetime.utcnow()
    return current_time + timedelta(days=DAYS_TO_EXPIRATION) <= not_after
```

Function * *"def str_to_date()"* * used for convert expired date of SSL certificate to string.
```python
def str_to_date(date_string: str) -> datetime:
    return datetime.strptime(date_string.rstrip(' GMT'), "%b %d %H:%M:%S %Y")
```

Function * *"def get_days_to_expiration(cert)"* * used for to calculate the number of days.
```python
def get_days_to_expiration(cert: Dict) -> int:
    not_after = str_to_date(cert['notAfter'])
    current_date = datetime.utcnow()
    diff = not_after - current_date
    return diff.days
```

Function * *"send_telegram_notification()"* * used by send notification on Telegram bot.
```python
def send_telegram_notification(days: int, domain: str) -> None:
    if days >= 0:
        telegram_send.send(messages=[f'SSL certificate for domain {domain} expires in {days} days'])
    else:
        telegram_send.send(messages=[f'SSL certificate for domain {domain} has been expired {abs(days)} days ago'])
```

Function * *"def get_ssl_cert()"* * takes as parameter domain name for check. After that a certificate request connection is created.
```python
def get_ssl_cert(target_url: str) -> Union[Dict, None]:
    """Get the ssl cert of a website."""
    try:
        ctx = ssl.create_default_context()
        socks = socket.socket()
        sock = ctx.wrap_socket(socks, server_hostname=target_url)
        sock.connect((target_url, 443))
        cert = sock.getpeercert(binary_form=False)

    except socket.error:
        print(f'Unknown host: {target_url}')
        return None
    except KeyError as e:
        print(f'No or invalid SSL cert: {e}')
        return None
    return cert
```
See more [Documentation](https://docs.python.org/3/library/ssl.html)

Function * *"def main()"* *
```python
def main() -> None:
    url = input('Enter site name: ')
    certificate = get_ssl_cert(url)
    if certificate:
        validity = check_cert_validity(certificate)
        print(validity)
        print(certificate)
        if not validity and SHOW:
            days = get_days_to_expiration(certificate)
            print(days)
            send_telegram_notification(days, url)
```

### Usage

---

To start on Windows:
```bash
 python.exe .\ssl_checker.py
```

To start on Linux-based:
```bash
python3 ./ssl_checker.py
```
---

### License
BSD

### Author information
Author's email : [Lisenok.p@gmail.com](Lisenok.p@gmail.com)