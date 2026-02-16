# ML Betygsprediktor 🎓

En Streamlit-app som predikterar betyg för Machine Learning-kursen baserat på ditt studieintyg från YH Akademin.

## Installation

1. Klona detta repo eller ladda ner filerna
2. Installera nödvändiga paket:
```bash
pip install -r requirements.txt
```

## Användning

Kör appen:
```bash
streamlit run betygsprediktor.py
```

Ladda sedan upp ditt studieintyg (PDF) och få din betygsprediktion!

## Prediktionslogik

- **VG**: ≥70% VG-poäng (starkt) eller ≥50% (med få/inga IG)
- **G**: 30-70% VG-poäng, eller balanserat mellan VG/IG
- **IG**: >50% IG-poäng

Systemet väger in både VG- och IG-procent för en nyanserad prediktion.
Enstaka IG-kurser påverkar inte prediktionen negativt om övriga prestationer är starka.

## Baserat på ditt studieintyg

Med 8 kurser och 200 poäng med 100% VG blir prediktionen: **VG** 🌟
