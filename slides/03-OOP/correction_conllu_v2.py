import argparse
from collections import Counter

import pathlib


class Word:
    """Word : a word in conllu format"""

    def __init__(
        self,
        identifier,
        form,
        lemma,
        upos,
        xpos,
        feats,
        head,
        deprel,
        deps,
        misc,
    ):
        self.identifier = identifier
        self.form = form
        self.lemma = lemma
        self.upos = upos
        self.xpos = xpos
        self.feats = feats
        self.head = head
        self.deprel = deprel
        self.deps = deps
        self.misc = misc


class Sentence:
    """
    A sentence is composed of a list of Word objects, an id and a text string
    """

    def __init__(self):
        self.words = []
        self.id = ""
        self.text = ""

    def add_word(self, line):
        """
        Add a Word to the words list
        """
        features = line.split("\t")
        if features:
            self.words.append(Word(*features))

    def __len__(self):
        return len(self.words)


def main():
    parser = argparse.ArgumentParser(description="Exo conllu")
    parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
    parser.add_argument("dir", help="le dossier de fichiers conllu")
    parser.add_argument("type", help="'form' ou 'pos'")
    parser.add_argument("n", help="taille des n-grammes", type=int)
    args = parser.parse_args()

    files = pathlib.Path(args.dir).glob("*.conllu")
    counter = Counter()
    for f in files:
        with open(f) as conllu:
            sents = []
            sent = Sentence()
            for line in conllu:
                line = line.rstrip()
                if not line:
                    if len(sent) > 0:
                        sents.append(sent)
                        sent = Sentence()
                elif line.startswith("# sent_id"):
                    sent.id = line[len("# send_id = ") :]
                elif line.startswith("# text"):
                    sent.text = line[len("# text = ") :]
                elif line[0].isdigit():
                    sent.add_word(line)
            # En cas de fichier qui ne termine pas par une ligne vide
            if len(sent) > 0:
                sents.append(sent)
        for s in sents:
            for i in range(len(s) - args.n):
                wngram = s.words[i : i + args.n]
                if args.type == "form":
                    cngram = tuple(w.form for w in wngram)
                elif args.type == "pos":
                    cngram = tuple(w.upos for w in wngram)
                counter[cngram] += 1
    for k, v in counter.most_common():
        print(f"{' '.join(k)}: {v}")


if __name__ == "__main__":
    main()
