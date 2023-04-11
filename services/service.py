from fuzzywuzzy import fuzz

def compare(s1,s2 : str) -> bool:
    crs1 = []
    crs2 = []
    for c in s1:
        if c.isdigit():
            crs1.append(int(c))
    for c in s2:
        if c.isdigit():
            crs2.append(int(c))
    if len(crs1) != 0 and crs1 != crs2:
        return False
    line1 = "".join(c for c in s1 if c.isalpha())
    line2 = "".join(c for c in s2 if c.isalpha())
    return True if fuzz.ratio(line1.lower(),line2.lower()) >= 62 else False