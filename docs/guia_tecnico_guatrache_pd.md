# Aunrood för de Täkneker — Kooperaatiw Njiaje Eswauna

## 📅 Plaan för de Johrszoit

| Daaje | Aktiwithait | Woarkjaijch |
|-------|--------------|-------------|
| 55–65 | Ihra droage (Rendimiento) | `nuevaesperanza rendimiento ...` |
| 70 | Ääaste Foto met Druhn/Smartfoon | `nuevaesperanza estres ...` |
| 90 | Twaiete Ihra + Wota anpoossa | Zonifisierjung + `irrigation_optimizer` |
| 120 | Läste Kiek | Foto + aanlijche Analyse |

## 📸 So moakt jie Foto för Strees-Analyse

1. **Tied**: 10:00–14:00 (jeschta Licht, keen swoare Wulke)  
2. **Höchde**:  
   - Druhn: 30–40 m (≈4 ha pro Foto)  
   - Smartfoon: von Kjara ut, 2–3 m hoog  
3. **Beld**:  
   - Dreejpunkt in de Midda haa  
   - Keen loange Schoade (mit de Sun im Röjjen fotjografiere)  
4. **Noome**: `campoX_datum.jpg` (bispill: `campo5_20250615.jpg`)

## 📊 So moakt jie NDVI uutrechne

1. **Sentinel-2** bruke (kjoastelos) vun USB:  
   - Opp de Kjoompjuuta met Internet:  
     ```bash
     python scripts/download_sentinel_offline.py --campo 5 --fecha 2025-06-15
     ```  
   - Datei `sentinel_guatrache_5_*.zip` opp USB speichere  
   - Opp de Feld-Kjoompjuuta:  
     ```bash
     nuevaesperanza rendimiento "Campo 5" --ndvi $(nuevaesperanza-ndvi-from-usb D:/)
     ```

## 🖨️ So deelt jie de Ihrgenisse

- PDF drucke (in `reports/`)  
- Opp de Tofel in de Maschiene-Saal plaake  
- In de weekentliche Besprechung von de Owaitea bespreeke

> ✅ **Wichtich**: All Dateie bleaft in de Kooperaatiw. Nix jeiht opp Internet.
