import string


def sanitize_name(value: str):
    result = ' '.join(value.split())

    return result.strip(string.punctuation).strip().lower()
