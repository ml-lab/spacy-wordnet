from spacy.tokens.doc import Doc
from spacy.tokens.token import Token

from spacy_wordnet.wordnet_domains import Wordnet, _WordnetDomains


class WordnetAnnotator(object):
    __FIELD = 'wordnet'

    def __init__(self, lang: str = 'es'):
        Token.set_extension(WordnetAnnotator.__FIELD, default=None, force=True)
        self.__wn_domains = _WordnetDomains()
        self.__lang = lang

    def __call__(self, doc: Doc):
        for token in doc:
            wordnet = Wordnet(token=token, wn_domains=self.__wn_domains, lang=self.__lang)
            token._.set(WordnetAnnotator.__FIELD, wordnet)

        return doc
