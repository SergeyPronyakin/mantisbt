import string
import random

symbols = None


class GeneratorHelper:
    def random_str(self, prefix, maxlen, digits=None, spaces=None):
        global symbols
        if digits:
            symbols = string.ascii_letters + string.digits
        elif spaces:
            symbols = string.ascii_letters + " " * 10
        elif digits and spaces:
            symbols = string.ascii_letters + string.digits + " " * 10
        else:
            symbols = string.ascii_letters
        return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])

    def random_int(self, min, max):
        return "".join(random.choice("0123456789") for i in range(random.randint(min, max)))

    def random_phone(self):
        phone = []
        country_codes = [self.random_int(1, 2)]
        city_codes = [self.random_int(1, 4)]
        random_index = int(random.choice("01"))
        prefs = ["", "+"][random_index]
        parenthesis_open = ["", "("][random_index]
        phone_bodies = [self.random_int(4, 8)]
        for a, b, c, d, e in zip(prefs, country_codes, parenthesis_open, city_codes, phone_bodies):
            phone.append(a)
            phone.append(b)
            phone.append(c)
            phone.append(d)
            if c:
                phone.append(")")
            phone.append(e)

        return "".join(phone)