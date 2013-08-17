import string
import random
from md5 import md5

import requests


class TempMail(object):
    """
    Wrapper for online service which provides temporary email address.
    """

    def __init__(self, login=None, domain=None, api_domain='api.temp-mail.ru'):
        self.login = login
        self.domain = domain
        self.api_domain = api_domain

    @property
    def available_domains(self):
        """
        Return list of available domains for use in email address.
        """
        url = 'http://{0}/request/domains/format/json/'.format(self.api_domain)
        req = requests.get(url)
        return req.json()

    def generate_login(self, min_length=6, max_length=10, digits=True):
        """
        Generate string for email address login with defined length and
        alphabet.
        """
        chars = string.ascii_lowercase
        if digits:
            chars += string.digits
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(chars) for x in range(length))

    def get_email_address(self):
        """
        Use login and domain from class initialization or generate new
        and return full email address.
        """
        if self.login is None:
            self.login = self.generate_login()

        available_domains = self.available_domains
        if self.domain is None:
            self.domain = random.choice(available_domains)
        elif self.domain not in available_domains:
            raise ValueError('Domain not found in available domains!')
        return u'{0}{1}'.format(self.login, self.domain)

    def get_hash(self, email):
        """
        Return md5 hash for given email address.
        """
        return md5(email).hexdigest()

    def get_mailbox(self, email=None, email_hash=None):
        """
        Return list of emails in given email address
        or dict with `error` key if mail box is empty.
        """
        if email_hash is None:
            email_hash = self.get_hash(email)

        url = 'http://{0}/request/mail/id/{1}/format/json/'.format(
            self.api_domain, email_hash)
        req = requests.get(url)
        return req.json()
