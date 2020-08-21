import re


def normalise(s):
    """
    Tokenize on parenthesis, punctuation, spaces and American units followed by a slash.

    We sometimes give American units and metric units for baking recipes. For example:
        * 2 tablespoons/30 mililiters milk or cream
        * 2 1/2 cups/300 grams all-purpose flour

    The recipe database only allows for one unit, and we want to use the American one.
    But we must split the text on "cups/" etc. in order to pick it up.
    """

    # handle abbreviation like "100g" by treating it as "100 grams"
    s = s.lower()
    s = re.sub(r"(\d+)\s*g", r"\1 grams", s, flags=re.IGNORECASE)
    s = re.sub(r"(\d+)\s*oz", r"\1 ounces", s, flags=re.IGNORECASE)
    s = re.sub(r"(\d+)\s*ml", r"\1 milliliters", s, flags=re.IGNORECASE)
    s = re.sub(r"(\d+)\s*tbsp\.?", r"\1 tablespoons", s, flags=re.IGNORECASE)
    s = re.sub(r"(\d+)\s*tsp\.?", r"\1 teaspoons", s, flags=re.IGNORECASE)
    s = re.sub(r"\(optional\)", r"", s, flags=re.IGNORECASE)

    american_units = ["cup", "tablespoon", "teaspoon", "pound", "ounce", "quart", "pint"]
    for unit in american_units:
        s = s.replace(unit + "/", unit + " ")
        s = s.replace(unit + "s/", unit + "s ")

    return s


def tokenize(s):
    """
    Tokenize on parenthesis, punctuation, spaces and American units followed by a slash.

    We sometimes give American units and metric units for baking recipes. For example:
        * 2 tablespoons/30 mililiters milk or cream
        * 2 1/2 cups/300 grams all-purpose flour

    The recipe database only allows for one unit, and we want to use the American one.
    But we must split the text on "cups/" etc. in order to pick it up.
    """

    return filter(None, re.split(r"([,()])?\s+", clump_fractions(normalise(s))))


def clump_fractions(s):
    """
    Replaces the whitespace between the integer and fractional part of a quantity
    with a dollar sign, so it's interpreted as a single token. The rest of the
    string is left alone.

        clump_fractions("aaa 1 2/3 bbb")
        # => "aaa 1$2/3 bbb"
    """
    return re.sub(r"(\d+)\s+(\d)/(\d)", r"\1$\2/\3", s)
