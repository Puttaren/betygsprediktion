# ML Betygsprediktor 🎓
En Streamlit-app som predikterar betyg för Machine Learning-kursen baserat på studieintyg från YH Akademin.


Ladda upp ditt studieintyg (PDF) och få din betygsprediktion!
** Observera - måste vara studieintyget som laddats ned från YH-akademin **

## Prediktionslogik
- **VG**: ≥70% VG-poäng (starkt) eller ≥50% (med få/inga IG)
- **G**: 30-70% VG-poäng, eller balanserat mellan VG/IG
- **IG**: >50% IG-poäng

Systemet väger in både VG- och IG-procent för en nyanserad prediktion.
En enskild IG-kurs påverkar inte prediktionen alltför negativt om övriga prestationer är starka.
