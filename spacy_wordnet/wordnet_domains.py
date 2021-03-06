from nltk.corpus import wordnet as wn
from spacy.tokens.token import Token

from spacy_wordnet.__utils__ import *

__WN_DOMAINS_PATH = os.path.join(get_package_basepath(), 'data/wordnet_domains.txt')

__WN_DOMAINS_BY_SSID = defaultdict(list)


def wordnet_domains_path() -> str:
    return __WN_DOMAINS_PATH


def load_wordnet_domains(path: str):
    if __WN_DOMAINS_BY_SSID:
        return

    for line in open(path, 'r'):
        ssid, domains = line.strip().split('\t')
        __WN_DOMAINS_BY_SSID[ssid] = domains.split(' ')


def get_domains_for_synset(synset: Synset) -> List[str]:
    ssid = '{}-{}'.format(str(synset.offset()).zfill(8), synset.pos())
    return __WN_DOMAINS_BY_SSID.get(ssid, [])


class _WordnetDomains(object):
    def __init__(self):
        load_wordnet_domains(wordnet_domains_path())

    def domains_for_synset(self, synset: Synset) -> List[str]:
        return get_domains_for_synset(synset)


class Wordnet(object):

    def __init__(self, token: Token, wn_domains: _WordnetDomains, lang: str = 'es'):
        self.__wn_domains = wn_domains
        self.__token = token
        self.__lang = fetch_wordnet_lang(lang)
        self.__synsets = self.__find_synsets(token, self.__lang)
        self.__lemmas = self.__find_lemmas()
        self.__wordnet_domains = self.__find_wordnet_domains()

    def synsets(self):
        return self.__synsets

    def lemmas(self):
        return self.__lemmas

    def wordnet_domains(self):
        return self.__wordnet_domains

    def wordnet_domains_for_synset(self, synset):
        return get_domains_for_synset(synset)

    @staticmethod
    def __find_synsets(token: Token, lang: str):
        word_variants = [token.text]
        if token.pos in [VERB, NOUN, ADJ]:
            # extend synset coverage using lemmas
            word_variants.append(token.lemma_)

        for word in word_variants:
            token_synsets = wn.synsets(word, pos=spacy2wordnet_pos(token.pos), lang=lang)
            if token_synsets:
                return token_synsets

        return []

    def __find_wordnet_domains(self):
        return [domain for synset in self.synsets() for domain in get_domains_for_synset(synset)]

    def __find_lemmas(self):
        return [lemma for synset in self.__synsets for lemma in synset.lemmas(lang=self.__lang)]
