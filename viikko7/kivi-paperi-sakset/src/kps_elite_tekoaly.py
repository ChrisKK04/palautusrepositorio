from tekoaly_elite import TekoalyElite
from kivi_paperi_sakset import KiviPaperiSakset


class KPSEliteTekoaly(KiviPaperiSakset):
    def __init__(self):
        self.tekoaly = TekoalyElite(100)

    def _toisen_siirto(self, ensimmaisen_siirto):
        tokan_siirto = self.tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")

        self.tekoaly.aseta_siirto(ensimmaisen_siirto)

        return tokan_siirto

