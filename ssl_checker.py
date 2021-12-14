import socket
import ssl
from datetime import datetime, timedelta
from typing import Dict, Union

import telegram_send

DAYS_TO_EXPIRATION = 50
SHOW = True


def check_cert_validity(cert: Dict) -> bool:
    not_after = str_to_date(cert['notAfter'])
    current_time = datetime.utcnow()
    return current_time + timedelta(days=DAYS_TO_EXPIRATION) <= not_after


def str_to_date(date_string: str) -> datetime:
    return datetime.strptime(date_string.rstrip(' GMT'), "%b %d %H:%M:%S %Y")


def get_days_to_expiration(cert: Dict) -> int:
    not_after = str_to_date(cert['notAfter'])
    current_date = datetime.utcnow()
    diff = not_after - current_date
    return diff.days


def send_telegram_notification(days: int, domain: str) -> None:
    if days >= 0:
        telegram_send.send(messages=[f'SSL certificate for domain {domain} expires in {days} days'])
    else:
        telegram_send.send(messages=[f'SSL certificate for domain {domain} has been expired {abs(days)} days ago'])


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


if __name__ == "__main__":
    main()
