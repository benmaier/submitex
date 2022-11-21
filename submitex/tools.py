
def match_is_comment(text,match):
    """
    Check if a match of a pattern is a commented out on its line.

    Parameters
    ==========
    text : str
        The text (latex source) that is being scanned
    match : re.Match
        The current match

    Returns
    =======
    is_commented_out : bool
        Whether or not the match is actually just in a comment
    """

    if match is None:
        return False

    pointer = match.span()[0]
    while pointer >=0 and text[pointer] not in ['\n', '%']:
        pointer -= 1
        if text[pointer] == '%' and pointer > 0 and text[pointer-1] == '\\':
            pointer -= 1


    return text[pointer] == '%'

def iterate_matches(text,pattern,skip_comments=True):
    """
    Iterate through all matches of a text, given a pattern.

    Parameters
    ==========
    text : str
        The text (latex source) that is being scanned
    pattern : re.Pattern
        Search the text for all occurences of this pattern
    skip_comments : bool, default = True
        Whether or not to skip matches that are commented out

    Yields
    ======
    match : re.Match
        The next match
    """

    pos = 0
    while True:

        match = pattern.search(text,pos=pos)

        if match is None:
            break

        pos = match.span()[-1]

        if skip_comments and match_is_comment(text, match):
            continue

        yield match

def search_pattern_and_replace(text,pattern,replacement,skip_comments=True):
    pos = 0
    while True:
        match = pattern.search(text,pos=pos)
        if match is None:
            break
        pos = match.span()[1]
        if skip_comments match_is_comment(newtex,match):
            continue
        start, end = match.span()
        before = newtex[:start]
        after = newtex[end:]
        newtex = before + after

    return newtex


if __name__=="__main__":
    import re

    pattern = re.compile(r'\\test')
    test = r"""
        This is a \test
        this is a %\test
        %\test
    """
    test2 = r"""This is a \test
    """
    test3 = r"""%This is a \test
    """
    test4 = r"""\%This is a \test
    """
    test5 = r"""
    \%This is a \test
    """

    for skip_comments in [False, True]:
        print("====== skip_comments:", skip_comments)
        for text in [test, test2, test3, test4, test5]:
            print("\n","===")
            print(text)
            for match in iterate_matches(text, pattern,skip_comments=skip_comments):
                print(match)
                print("is match comment?", match_is_comment(text, match))
