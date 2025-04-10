def bionic_word(word):
    if len(word) <= 1:
        return word
    elif len(word) <= 3:
        return f"<b>{word[:1]}</b>{word[1:]}"
    else:
        midpoint = len(word) // 2
        return f"<b>{word[:midpoint]}</b>{word[midpoint:]}"

def process_text(text):
    word_pattern = regex.compile(r'\b[\p{L}\p{M}]+\b', regex.UNICODE)
    
    def replace_word(match):
        word = match.group(0)
        return bionic_word(word)
    
    return word_pattern.sub(replace_word, text)