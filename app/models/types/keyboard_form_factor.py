import re
from enum import Enum
from utils.regex_dict import RegexDict


class KeyboardFormFactor(Enum):

    forty_percent = 0
    sixty_percent = 1
    sixtyfive_percent = 2
    seventyfive_percent = 3
    tenkeyless = 4
    frowless = 5
    full_size = 6

    @classmethod
    def get_from_literal(cls, literal):
        reg_dict = RegexDict()
        reg_dict[re.compile(r"4[0-9]|Forty", re.I)] = KeyboardFormFactor.forty_percent
        reg_dict[re.compile(r"60|Sixty", re.I)] = KeyboardFormFactor.sixty_percent
        reg_dict[re.compile(r"6[5-9]|Sixty-Five|Sixtyfive", re.I)] = KeyboardFormFactor.sixtyfive_percent
        reg_dict[re.compile(r"7[0-9]|Seventy-Five|Seventyfive", re.I)] = KeyboardFormFactor.seventyfive_percent
        reg_dict[re.compile(r"8[0-9]|TKL|Tenkeyless", re.I)] = KeyboardFormFactor.tenkeyless
        try:
            return reg_dict[literal]
        except KeyError:
            return None
