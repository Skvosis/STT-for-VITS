from pypinyin import lazy_pinyin, Style

def Character_to_Pinyin(texts):
    style = Style.TONE3
    text_pinyin = []

    for text in texts:
        pinyins = lazy_pinyin(text, style=style)
        out = ''
        for pinyin in pinyins:
            out += pinyin+' '
        text_pinyin.append(out)
    return text_pinyin

def Character_to_Phoneme(texts):
    pass

def Character_to_IPA(texts):
    pass

def No_Cleaner(text):
    return text