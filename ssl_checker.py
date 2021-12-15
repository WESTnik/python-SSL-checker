import socket
import ssl
from datetime import datetime, timedelta
from typing import Dict, Union
import logging
import telegram_send
import argparse

SHOW = True


def check_cert_validity(cert: Dict[str, str], days_to_exp: int) -> bool:
    """
        The function check if SSL certificate valid/expired

        :param cert: takes the value of the certificate
        :param days_to_exp: takes the value of the number of days
        :return: TRUE/FALSE result if SSL certificate valid/expired
        """
    not_after = str_to_date(cert['notAfter'])
    current_time = datetime.utcnow()
    return current_time + timedelta(days=days_to_exp) <= not_after


def str_to_date(date_string: str) -> datetime:
    """
        The function convert string to date format

        :param date_string: takes the value from certificate string parameter which contain expired date
        :return: takes truncated and formatted copy of the string of date
        """
    return datetime.strptime(date_string.rstrip(' GMT'), "%b %d %H:%M:%S %Y")


def get_days_to_expiration(cert: Dict[str, str]) -> int:
    """
        The function get number of days until the end of the certificate

        :param cert: takes the value of the certificate
        :return: number of days until the end of the certificate
        """
    not_after = str_to_date(cert['notAfter'])
    current_date = datetime.utcnow()
    diff = not_after - current_date
    return diff.days


def send_telegram_notification(days: int, domain: str) -> None:
    """
        The function sent notification on you Telegram bot about status SSL certificate

        :param days: takes the value of days which is left until the expiration date SSL certificate
        :param domain: domain name
        :return: None
        """
    if days >= 0:
        telegram_send.send(messages=["SSL certificate for domain {0} expires in {1} days".format(domain, days)])
    else:
        telegram_send.send(messages=["SSL certificate for domain {0} has been expired {1} days ago".format(domain, abs(days))])
    logging.info("Notification has been sent via Telegram")


def get_ssl_cert(target_url: str) -> Union[Dict, None]:
    """
        The function install network connection with target domain and get SSL certificate for analyze

        :param target_url: takes the value domain name
        :return: cert: Contain the dictionary parameter values of SSL certificate
        """
    try:
        ctx = ssl.create_default_context()
        socks = socket.socket()
        sock = ctx.wrap_socket(socks, server_hostname=target_url)
        sock.connect((target_url, 443))
        cert = sock.getpeercert(binary_form=False)

    except socket.error:
        logging.error("Unknown host: {}".format(target_url))
        return None
    except KeyError as e:
        logging.error("No or invalid SSL cert: {}".format(e))
        return None
    return cert


def main(domain: str, days_to_exp: int) -> None:
    """
        The function main contains general business logic

        :param domain: takes the certificate from domain
        :param days_to_exp: number of days for notification
        :return: None
        """

    certificate = get_ssl_cert(args.domain_name)
    if certificate:
        validity = check_cert_validity(certificate, days_to_exp)
        logging.info(validity)
        logging.info(certificate)
        if not validity and SHOW:
            days = get_days_to_expiration(certificate)
            print(days)
            send_telegram_notification(days, domain)
        else:
            logging.debug("The certificate is valid")


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Get the hostname and number of days to expired")
    parser.add_argument("domain_name", type=str, help="Input domain name for check")
    parser.add_argument("days_to_expiration", type=int, help="Days to expiration")
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = parse_args()
    main(args.domain_name, args.days_to_expiration)
