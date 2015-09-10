import jautils

from unidecode import unidecode
from google.appengine.api import memcache

import re
import logging

def romanize_languages_by_unidecode(word):
    """
    Changes word to alphabet.
    This method should be called in translate_languages_to_roman().
    Args:
        word: should be script varianted
    Returns:
        script varianted word
    """
    if jautils.should_normalize(word):
        hiragana_word = jautils.normalize(word)
        return jautils.hiragana_to_romaji(hiragana_word)
    script_varianted_word = unidecode(word)
    return script_varianted_word


def romanize_japanese_name_by_name_dict(word):
    if not word:
        return word

    dict1 = memcache.get('dict1')
    dict2 = memcache.get('dict2')
    if word in dict1:
        yomigana = (dict1[word])
        return jautils.hiragana_to_romaji(yomigana)
    if word in dict2:
        yomigana = (dict2[word])
        return jautils.hiragana_to_romaji(yomigana)
    return word


def apply_script_variant(query_txt):
    """
    Applies to script variant to query_txt.
    Args:
        query_txt: Search query
    Returns:
        script varianted query_txt (except kanji)
    """
    query_words = query_txt.split(' ')
    return ' '.join([romanize_languages_by_unidecode(word)
                     for word in query_words])