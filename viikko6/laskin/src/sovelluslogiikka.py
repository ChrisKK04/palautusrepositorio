class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._edelliset_arvot = [0]

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def aseta_edelliset_arvot(self, arvot):
        self._edelliset_arvot = arvot

    def arvo(self):
        return self._arvo
    
    def edelliset_arvot(self):
        return self._edelliset_arvot

class Summa:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        nykyinen = self._sovelluslogiikka.arvo()
        uusi = nykyinen + self._syote()

        arvot = self._sovelluslogiikka.edelliset_arvot()
        arvot.append(uusi)
        self._sovelluslogiikka.aseta_edelliset_arvot(arvot)

        self._sovelluslogiikka.aseta_arvo(uusi)

class Erotus:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        nykyinen = self._sovelluslogiikka.arvo()
        uusi = nykyinen - self._syote()

        arvot = self._sovelluslogiikka.edelliset_arvot()
        arvot.append(uusi)
        self._sovelluslogiikka.aseta_edelliset_arvot(arvot)

        self._sovelluslogiikka.aseta_arvo(uusi)

class Nollaus:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        self._sovelluslogiikka.aseta_edelliset_arvot([0])
        self._sovelluslogiikka.aseta_arvo(0)

class Kumoa:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote

    def suorita(self):
        arvot = self._sovelluslogiikka.edelliset_arvot()
        if len(arvot) > 1:
            arvot.pop()
            self._sovelluslogiikka.aseta_edelliset_arvot(arvot)
            self._sovelluslogiikka.aseta_arvo(self._sovelluslogiikka.edelliset_arvot()[-1])