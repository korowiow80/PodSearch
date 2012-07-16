"""Decodes a given byte string to an unicode string."""
from mimetypes import knownfiles
from Util.LoggerFactory.LoggerFactory import LoggerFactory


class Decoder:
    
    _logger = LoggerFactory().getLogger('Decoder')
    
    knownEncodings = ["UTF-8", "ASCII", "UTF-16", "UTF-32", "Big5", "GB2312",
                      "EUC-TW", "HZ-GB-2312", "ISO-2022-CN", "EUC-JP",
                      "SHIFT_JIS", "ISO-2022-JP", "EUC-KR", "ISO-2022-KR",
                      "KOI8-R", "MacCyrillic", "IBM855", "IBM866",
                      "ISO-8859-5", "windows-1251", "ISO-8859-2",
                      "windows-1250", "ISO-8859-5", "windows-1251",
                      "windows-1252", "ISO-8859-7", "windows-1253",
                      "ISO-8859-8", "windows-1255", "TIS-620"]
    
    def __init__(self):
        pass

    def decode(self, byteString):
        #encoding = chardet.detect(byteString)

        for encoding in self.knownEncodings:
            try:
                utf8String = byteString.decode(encoding)
                return utf8String
            except Exception as e:
                msg = "Was not able to decode using encoding %s, got error %s" \
                       % (encoding, e)
                self._logger.debug(msg)
        
        self._logger.warning('Was not able to decode with any known decoding.')
