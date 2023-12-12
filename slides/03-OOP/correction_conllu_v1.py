import argparse


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
    parser = argparse.ArgumentParser(description="Exo conllu 1")
    parser.add_argument("file", help="le fichier conllu")
    args = parser.parse_args()

    sents = []
    sent = Sentence()
    with open(args.file) as conllu:
        for line in conllu:
            # on enlève les espaces en fin de ligne (y compris \n)
            line = line.rstrip()
            # ligne vide ou uniquement composée d'espacespour une fin de phrase
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

    print(f"Le fichier contient {len(sents)} phrases.")


if __name__ == "__main__":
    main()
