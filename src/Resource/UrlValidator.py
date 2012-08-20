"""Validates URLs using a regular expression."""

import re


class UrlValidator():
    """Validates URLs using a regular expression."""
    
    url_re = (r"^(?:(?:https?|ftps?):\/\/)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,"
              r"3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!1"
              r"92\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1"
              r",3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2["
              r"0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|("
              r"?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:"
              r"[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z"
              r"\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:\/[^\s]*)?")
    
    url_re = re.compile(url_re, re.IGNORECASE)
    
    def __init__(self):
        pass
    
    def validate(self, url):
        """Validates a given URL using a regular expression. Returns True if
        the URL is matched, False otherwise.
        
        >>> from UrlValidator import UrlValidator
        >>> url_validator = UrlValidator()
        >>> url_validator.validate("http://example.com")
        True
        >>> url_validator.validate("https://example.com")
        True
        >>> url_validator.validate("ftp://example.com")
        True
        >>> url_validator.validate("ftps://example.com")
        True
        >>> url_validator.validate("sftp://example.com")
        False
        >>> url_validator.validate("http://subdomain.example.com")
        True
        >>> url_validator.validate("http://subsubdomain.subdomain.example.com")
        True
        >>> url_validator.validate("http://example.co.uk")
        True
        >>> url_validator.validate("http://example.com/path/to/somewhere/")
        True"""
        
        match = UrlValidator.url_re.match(url)
        if match:
            return True
        return False
