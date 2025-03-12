import pandas as pd
import os

url = "https://raw.githubusercontent.com/seung-m1nsong/Data698/refs/heads/main/product_info.csv"

df = pd.read_csv(url)

dict_origin = {
    "19-69": "Sweden", "54 Thrones": "USA", "ABBOTT": "USA", "Acqua di Parma": "Italy",
    "adwoa beauty": "USA", "AERIN": "USA", "Algenist": "USA", "Alpha-H": "Australia",
    "alpyn beauty": "USA", "ALTERNA Haircare": "USA", "Ami Cole": "USA", "amika": "USA",
    "Anastasia Beverly Hills": "USA", "Aquis": "USA", "Armani Beauty": "Italy",
    "Artist Couture": "USA", "Atelier Cologne": "France", "Augustinus Bader": "Germany",
    "Azzaro": "France", "bareMinerals": "USA", "BeautyBio": "USA", "beautyblender": "USA",
    "belif": "South Korea", "Benefit Cosmetics": "USA", "BERDOUES": "France",
    "Bio Ionic": "USA", "Biossance": "USA", "Blinc": "USA", "Bobbi Brown": "USA",
    "Bon Parfumeur": "France", "BondiBoost": "Australia", "Boy Smells": "USA",
    "BREAD BEAUTY SUPPLY": "Australia", "Briogeo": "USA", "Bumble and bumble": "USA",
    "BURBERRY": "UK", "Buxom": "USA", "By Rosie Jane": "Australia", "caliray": "USA",
    "Calvin Klein": "USA", "CANOPY": "USA", "Capri Blue": "USA", "Carolina Herrera": "Venezuela",
    "Caudalie": "France", "CAY SKIN": "USA", "Ceremonia": "USA", "CHANEL": "France",
    "Charlotte Tilbury": "UK", "Chloe": "France", "Christian Louboutin": "France",
    "Christophe Robin": "France", "Cinema Secrets": "USA", "Clarins": "France",
    "CLEAN RESERVE": "USA", "CLINIQUE": "USA", "COLOR WOW": "USA", "Commodity": "USA",
    "Community Sixty-Six": "USA", "COOLA": "USA", "Crown Affair": "USA",
    "Curlsmith": "USA", "dae": "USA", "DAMDAM": "Japan", "Dame": "USA",
    "Danessa Myricks Beauty": "USA", "Deborah Lippmann": "USA", "DedCool": "USA",
    "DEREK LAM 10 CROSBY": "USA", "DERMAFLASH": "USA", "Dermalogica": "USA",
    "Dior": "France", "Dolce&Gabbana": "Italy", "DOMINIQUE COSMETICS": "USA",
    "Donna Karan": "USA", "dpHUE": "USA", "Dr. Barbara Sturm": "Germany",
    "Dr. Brandt Skincare": "USA", "Dr. Dennis Gross Skincare": "USA", "Dr. Jart+": "South Korea",
    "Dr. Lara Devgan Scientific Beauty": "USA", "Dr. Zenovia Skincare": "USA",
    "Drunk Elephant": "USA", "Drybar": "USA", "DUO": "USA", "EADEM": "USA",
    "Eight & Bob": "France","Ellis Brooklyn": "USA","Erno Laszlo": "USA","Estée Lauder": "USA","Evian": "France",
    "Fable & Mane": "UK","FaceGym": "UK","Farmacy": "USA","Fashion Fair": "USA","Fenty Beauty by Rihanna": "USA",
    "Fenty Skin": "USA","First Aid Beauty": "USA","Flora + Bast": "USA","Floral Street": "UK",
    "FOREO": "Sweden","FORVR Mood": "USA","Freck Beauty": "USA","fresh": "USA",
    "ghd": "UK", "Gisou": "Netherlands", "Givenchy": "France", "Glamnetic": "USA",
    "GLO Science": "USA", "Glossier": "USA", "Glow Recipe": "South Korea",
    "Good Dye Young": "USA", "Google": "USA", "goop": "USA", "Grace Eleyae": "USA",
    "Grande Cosmetics": "USA", "Gucci": "Italy", "GUERLAIN": "France",
    "GXVE BY GWEN STEFANI": "USA", "HABIT": "USA", "Hanni": "USA", "HAUS LABS BY LADY GAGA": "USA",
    "Herbivore": "USA", "HERETIC": "USA", "HERMÈS": "France", "Hourglass": "USA",
    "House of Lashes": "USA", "HUDA BEAUTY": "UAE", "HUM Nutrition": "USA",
    "Hyper Skin": "USA", "Iconic London": "UK", "IGK": "USA", "ILIA": "USA",
    "iluminage": "USA", "INC.redible": "UK", "iNNBEAUTY PROJECT": "USA",
    "innisfree": "South Korea", "Isle of Paradise": "UK", "IT Cosmetics": "USA",
    "Jack Black": "USA", "Jillian Dempsey": "USA", "JIMMY CHOO": "UK", "JLo Beauty": "USA",
    "Jo Malone London": "UK", "Josie Maran": "USA", "Jouer Cosmetics": "USA",
    "Juicy Couture": "USA", "Juliette Has a Gun": "France", "JVN": "USA",
    "K18 Biomimetic Hairscience": "USA", "Kaja": "South Korea", "Kate McLeod": "USA",
    "Kate Somerville": "USA", "KAYALI": "UAE", "Kérastase": "France", "Kiehl's Since 1851": "USA", "KILIAN Paris": "France",
    "Koh Gen Do": "Japan", "Kopari": "USA","KORA Organics": "Australia","KORRES": "Greece","Kosas": "USA","Kulfi": "USA",
    "KVD Beauty": "USA","L'Occitane": "France","L'Oreal Professionnel": "France","La Mer": "USA","Lancôme": "France",
    "LANEIGE": "South Korea","Laura Mercier": "USA","LAWLESS": "USA","lilah b.": "USA","Lilly Lashes": "USA",
    "Living Proof": "USA","LYS Beauty": "USA","MACRENE actives": "USA","Maison Louis Marie": "France","Maison Margiela": "France","MAKE UP FOR EVER": "France",
    "MAKEUP BY MARIO": "USA","MARA": "USA","Marc Jacobs Fragrances": "USA","Mario Badescu": "USA","maude": "USA","Melanin Haircare": "USA",
    "Melt Cosmetics": "USA","MERIT": "USA","MILK MAKEUP": "USA","Mizani": "USA","Montblanc": "France","Moon Juice": "USA","Moroccanoil": "Israel",
    "Mount Lai": "USA","Mugler": "France","Murad": "USA","NAILS INC.": "UK","Narciso Rodriguez": "USA","NARS": "France","Natasha Denona": "USA",
    "Naturally Serious": "USA","Nécessaire": "USA","NEST New York": "USA","NUDESTIX": "Canada",
    "NuFACE": "USA","Nutrafol": "USA","Olaplex": "USA","OLEHENRIKSEN": "Denmark","ONE/SIZE by Patrick Starrr": "USA","Oribe": "USA",
    "Origins": "USA","OTHERLAND": "USA","OUAI": "USA","Overose": "France","Paco Rabanne": "Spain","PAT McGRATH LABS": "UK","PATRICK TA": "USA",
    "PATTERN by Tracee Ellis Ross": "USA","Paula's Choice": "USA","Peace Out": "USA","Peter Thomas Roth": "USA",
    "philosophy": "USA","PHLUR": "USA","PMD": "USA","Prada": "Italy","Prima": "USA","PROVEN Skincare": "USA","Pureology": "USA",
    "Rahua": "Ecuador","Ralph Lauren": "USA","RANAVAT": "USA","Rare Beauty by Selena Gomez": "USA","REFY": "UK",
    "REN Clean Skincare": "UK","RIES": "USA","rms beauty": "USA","ROSE INC": "USA",
    "ROSE Ingleton MD": "USA","Rosebud Perfume Co.": "USA","Rossano Ferretti Parma": "Italy", "Saie": "USA", "Saint Jane Beauty": "USA",
    "SEPHORA COLLECTION": "France","Sephora Favorites": "France","Shani Darden Skin Care": "USA","Shiseido": "Japan","shu uemura": "Japan","SIMIHAZE BEAUTY": "USA",
    "SK-II": "Japan","Skin Laundry": "USA","Skinfix": "USA", "SKYLAR": "USA","Slip": "Australia","Smashbox": "USA",
    "SOBEL SKIN Rx": "USA","Sol de Janeiro": "Brazil","Soleil Toujours": "USA","St. Tropez": "UK",
    "stila": "USA","StriVectin": "USA","Sulwhasoo": "South Korea","Summer Fridays": "USA",
    "SUNDAY II SUNDAY": "USA","Sunday Riley": "USA","Supergoop!": "USA","Susteau": "USA","T3": "USA","TAN-LUXE": "UK","tarte": "USA",
    "Tata Harper": "USA","Tatcha": "Japan","The 7 Virtues": "Canada","The INKEY List": "UK","The Maker": "USA","The Nue Co.": "USA","The Ordinary": "Canada",
    "The Original MakeUp Eraser": "USA","The Outset": "USA","The Phluid Project": "USA","TOCCA": "USA","TOM FORD": "USA",
    "Too Faced": "USA","Topicals": "USA","Touchland": "USA","Tower 28 Beauty": "USA","TULA Skincare": "USA","TWEEZERMAN": "USA",
    "Urban Decay": "USA","Valentino": "Italy","Vegamour": "USA","Velour Lashes": "Canada","Verb": "USA","Versace": "Italy",
    "Viktor&Rolf": "Netherlands","Violet Voss": "USA","Viori": "USA","Virtue": "USA","Viseart": "France","VOLUSPA": "USA","Wander Beauty": "USA",
    "WASO": "Japan","Westman Atelier": "USA","Wishful": "UAE","World of Chris Collins": "USA","Youth To The People": "USA","Yves Saint Laurent": "France"
}

df["origin"] = df["brand_name"].map(dict_origin)


#output_file_path = r"C:\Users\SeungminSong\Downloads\698_Research\product_info_with_origin.csv"
#df.to_csv(output_file_path, index=False)

#print(df.head())

origin_counts = df["origin"].value_counts()
print(origin_counts) 


unique_brands = df.drop_duplicates(subset=["brand_name"])
origin_counts_unique = unique_brands["origin"].value_counts()

print(origin_counts_unique) 

