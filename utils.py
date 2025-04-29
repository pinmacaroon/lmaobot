"""
**utils**

* **u**: usual
* **t**: things
* **i**: i (pin)
* **l**: like
* **s**: sometimes

---

the `utils.py` file every project has lmao.

---

:copyright: (c) 2025 by pin.
:license: MIT, see <https://pinmacaroon.github.io/> for more details.
"""
import re
import uuid

import discord

def is_float(element: any) -> bool:
    """
    check if a thingie is floating point convertible.
    
    ---
    
    **arguments**
    * `element` of type `any`: to be checked
    
    ---
    **returns**
    * `True` if convertible
    * `False` if `None` or conversion fails
    """
    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False
    
def boolean_maker(src: str) -> bool | None:
    """
    make a `str` into a `bool`.
    
    ---
    
    **arguments**
    * `src` of type `str`: to be converted
    
    ---
    **returns**
    * `True` if `src` stripped and lowered is 'true' or 'yes'
    * `False` if `src` stripped and lowered is 'false' or 'no'
    * `None` when both conditions aren't met
    """
    if src.strip().lower() == 'true' or src.strip().lower() == 'yes':
        return True
    elif src.strip().lower() == 'false' or src.strip().lower() == 'no':
        return False
    else: return None

def parse_command(raw: str) -> list:
    """
    parse a `str` (supposed to be a single line) into a `list` which can have
    `str`, `float` and `bool`.
    
    the string is broken into a list of words at every whitespace. to make a
    phrase, surround it with `"` characters.
    
    valid `float` items are converted into `float`, valid `bool` items are 
    converted into `bool`.
    
    ---
    
    **arguments**
    * `raw` of type `str`: to be parsed
    
    ---
    **returns**
    * `list` with items of type of `str`, `float` and `bool`.
    """
    parsed: list = []
    holder: str = ""
    capture = False
    for i in list(raw):
        if not re.match(r'[^"|^\s]', i) == None:
            holder += i
        elif i == '\'':
            if capture:
                capture = False
                parsed.append(holder)
                holder = ""
            else:
                parsed.append(holder)
                holder = ""
                capture = True
        elif i == ' ':
            if capture:
                holder += i
            else:
                parsed.append(holder)
                holder = ""
    parsed.append(holder)
    for i in parsed:
        if len(i) <= 0:
            del parsed[parsed.index(i)]
    for i in parsed:
        if is_float(i):
            parsed[parsed.index(i)] = float(i)
        if not boolean_maker(i) is None:
            parsed[parsed.index(i)] = boolean_maker(i)
        else:
            pass
    return parsed

def get_uuid() -> str:
    """
    get a uuid urn string
    
    ---
    
    **arguments**
    * none
    
    ---
    **returns**
    * `str` with a uuid urn string
    """
    return uuid.uuid4().urn.split(':')[2]

def get_member_from_mention_and_server(
    mention: str, server: discord.Guild
    ) -> discord.Member | None:
    return server.get_member(int(re.sub(r'\D', '', mention)))

if __name__ == '__main__':
    while True:
        inp = input('> ')
        print(parse_command(inp))