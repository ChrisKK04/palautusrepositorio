class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def arvo(self):
        return self._arvo

class Summa:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        nykyinen = self._sovelluslogiikka.arvo()
        uusi = nykyinen + self._syote()

        self._sovelluslogiikka.aseta_arvo(uusi)

class Erotus:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        nykyinen = self._sovelluslogiikka.arvo()
        uusi = nykyinen - self._syote()

        self._sovelluslogiikka.aseta_arvo(uusi)

class Nollaus:
    def __init__(self, sovelluslogiikka, syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._syote = syote
    
    def suorita(self):
        self._sovelluslogiikka.aseta_arvo(0)

class Kumoa:
    def __init__(self, sovelluslogiikka, syote):
        pass
