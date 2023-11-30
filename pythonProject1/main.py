from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
        self.elerheto = True

    @abstractmethod
    def megjelenit(self):
        pass


class EgyagyasSzoba(Szoba):
    def megjelenit(self):
        return f"Egyágyas szoba {self.szobaszam}, ára: {self.ar}"


class KetagyasSzoba(Szoba):
    def megjelenit(self):
        return f"Kétágyas szoba {self.szobaszam}, ára: {self.ar}"


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def uj_szoba(self, szoba):
        self.szobak.append(szoba)

    def szoba_lista(self):
        return [szoba.megjelenit() for szoba in self.szobak]


class Foglalas:
    def __init__(self, szobaszam, datum):
        self.szobaszam = szobaszam
        self.datum = datetime.strptime(datum, "%Y-%m-%d")

    def __str__(self):
        return f"Foglalás a {self.datum.strftime('%Y-%m-%d')}-i napon a {self.szobaszam} számú szobára"

    def __repr__(self):
        return self.__str__()


class FoglalasKezelo:
    @staticmethod
    def foglalas(szalloda, szobaszam, datum):
        szoba = next((s for s in szalloda.szobak if s.szobaszam == szobaszam), None)
        if not szoba:
            return "Hiba: A megadott szobaszám nem létezik."

        if not szoba.elerheto:
            return "Hiba: A szoba már foglalt ezen a napon."

        foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
        today = datetime.now()

        if foglalas_datum <= today:
            return "Hiba: A foglalás dátuma érvénytelen."

        szoba.elerheto = False
        szalloda.foglalasok.append(Foglalas(szobaszam, datum))
        return f"Sikeres foglalás a {datum}-i napon a {szobaszam} számú szobára."

    @staticmethod
    def lemondas(szalloda, szobaszam, datum):
        foglalas_datum = datetime.strptime(datum, "%Y-%m-%d")
        foglalas = next((f for f in szalloda.foglalasok if f.szobaszam == szobaszam and f.datum == foglalas_datum),
                        None)

        if not foglalas:
            return "Hiba: A megadott foglalás nem létezik."

        foglalas_szoba = next((s for s in szalloda.szobak if s.szobaszam == szobaszam), None)
        foglalas_szoba.elerheto = True

        szalloda.foglalasok.remove(foglalas)
        return f"Sikeres lemondás a {datum}-i napon a {szobaszam} számú szobáról."

    @staticmethod
    def foglalasok_listazasa(szalloda):
        return [str(f) for f in szalloda.foglalasok]


# Teszt adatok
szalloda = Szalloda("Teszt Szálloda")

szalloda.uj_szoba(EgyagyasSzoba(101, 50))
szalloda.uj_szoba(KetagyasSzoba(201, 80))
szalloda.uj_szoba(KetagyasSzoba(202, 80))

szalloda.foglalasok.append(Foglalas(101, "2023-12-01"))
szalloda.foglalasok.append(Foglalas(201, "2023-12-05"))
szalloda.foglalasok.append(Foglalas(202, "2023-12-10"))
szalloda.foglalasok.append(Foglalas(101, "2023-12-15"))
szalloda.foglalasok.append(Foglalas(201, "2023-12-20"))

# Felhasználói interfész
while True:
    print("\nVálassz műveletet:")
    print("1. Szobák listázása")
    print("2. Foglalás")
    print("3. Lemondás")
    print("4. Foglalások listázása")
    print("0. Kilépés")

    valasztas = input("Választás: ")

    if valasztas == "1":
        print("\nSzobák:")
        print("\n".join(szalloda.szoba_lista()))

    elif valasztas == "2":
        szobaszam = input("Adja meg a szobaszámot: ")
        datum = input("Adja meg a foglalás dátumát (év-hónap-nap formátumban): ")
        print(FoglalasKezelo.foglalas(szalloda, szobaszam, datum))

    elif valasztas == "3":
        szobaszam = input("Adja meg a szobaszámot: ")
        datum = input("Adja meg a lemondás dátumát (év-hónap-nap formátumban): ")
        print(FoglalasKezelo.lemondas(szalloda, szobaszam, datum))

    elif valasztas == "4":
        print("\nFoglalások:")
        foglalasok = FoglalasKezelo.foglalasok_listazasa(szalloda)
        if foglalasok:
            print("\n".join(foglalasok))
        else:
            print("Nincsenek foglalások.")

    elif valasztas == "0":
        break

    else:
        print("Érvénytelen választás. Kérem, válasszon újra.")
