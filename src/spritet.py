# Kiersin vähän tehtävän antoa ja tein omista kuvista koodia.
# Sitähän ei kielletty.
# Tämä on erillinen ohjelma, millä tehdään kuvista listoja ja tallennetaan txt-tiedostoihin
# Itse peliin tätä ei tarvita, mutta jos haluat muuttaa renderöitäviä kuvia,
# niin tee tällä uudet matriisit ja copypastaa ne kuvat.py alta löytyvien funktioiden
# palautusarvoiksi
# HUOM!! tätä käyttääksesi sinulla pitää olla asennettuna erillinen Python Imaging Library (PIL)
# Voit asentaa sen suorittamalla komentokehoitteessa pip install Pillow -käskyn
# skaala_px = 10 ja se kannattaa olla 10 jos ei halua muuttaa itse ohjelmassa spritejen renderöintiä
# isomilla kuin 10*10 pikselimäärillä ohjelman suoritus hidastuu huomattavasti

from PIL import Image
def rgb_matriisin_tekija(skaala_px: int, avattava_kuva_ja_polku: str, tallennettava_tiedosto: str) -> None:
    img = Image.open(avattava_kuva_ja_polku)
    img = img.resize((skaala_px, skaala_px))

    pikselit = img.load()
    matriisi = [[0 for j in range(skaala_px)] for i in range(skaala_px)]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = pikselit[i, j]
            matriisi[i][j] = (int(r), int(g), int(b))
    with open(tallennettava_tiedosto, "w") as f:
        f.write(str(matriisi))

if __name__ == "__main__":   
    rgb_matriisin_tekija(10, "conv\coin.jpg", "coin.txt")
    rgb_matriisin_tekija(10, "conv\ovi.jpg", "ovi.txt")
    rgb_matriisin_tekija(10, "conv\lohikaarme3.jpg", "lohikaarme.txt")
    rgb_matriisin_tekija(10, "conv\hero2.jpg", "hero.txt")
    rgb_matriisin_tekija(10, "conv\stone.jpg", "stone.txt")
