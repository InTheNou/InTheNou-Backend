def processSearchString(searchstring):
    """
    Splits a string by its spaces, filters non-alpha-numeric symbols out,
    and joins the keywords by space-separated pipes.
    """
    if isinstance(searchstring, str):
        keyword_list = str.split(searchstring)
        filtered_words = []
        for word in keyword_list:
            filtered_string = ""
            for character in word:
                if character.isalnum():
                    filtered_string += character
            if not filtered_string.isspace() and filtered_string != "":
                filtered_words.append(filtered_string)
        keywords = " | ".join(filtered_words)
        return keywords
    raise ValueError("Invalid search string: " + str(searchstring))


def validate_offset_limit(offset, limit):
    if not isinstance(offset, int) or not offset >= 0:
        raise ValueError("Invalid Offset: " + str(offset))
    if not isinstance(limit, int) or not limit > 0:
        raise ValueError("Invalid limit: " + str(limit))