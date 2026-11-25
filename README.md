# Speed Cube Timer
Timer til speedcubere. Den virker på telefonen uden internet.

## Sådan bruger du den
- Hold fingeren på skærmen, til tallet bliver grønt, og slip for at starte.
- Tryk hvor som helst på skærmen for at stoppe.
- Tryk på en tid i listen for at give +2, DNF eller slette den.
- Under **Menu** kan du slå 15 sekunders inspektion til.
- **På computer:** hold en vilkårlig tast nede, til tallet bliver grønt, og slip for at starte.
  Tryk på en vilkårlig tast (eller klik) for at stoppe.

## Placering i verden
Under statistikken vises, hvor din bedste tid og dit bedste gennemsnit ville ligge på WCA's
verdensrangliste og i dit land (vælg land i **Menu**, Danmark er standard). Det er et skøn ud
fra officielle konkurrenceresultater, ikke en officiel placering. 6x6, 7x7 og 3x3 Blind
sammenlignes med Mo3, de andre med Ao5, ligesom WCA gør.

Tallene ligger i `ranks/` og laves af `tools/build_ranks.py`, som henter WCA's offentlige
eksport. GitHub Action'en `.github/workflows/ranks.yml` kører den hver mandag.

> This information is based on competition results owned and maintained by the World Cube
> Association, published at https://worldcubeassociation.org/results.

## Puslespil og sessioner
- Vælg puslespil i menuen øverst til venstre: 2x2–7x7, 3x3 OH, 3x3 Blind, Pyraminx,
  Skewb, Megaminx, Square-1 eller Clock. Scramblet passer til det valgte puslespil,
  og der vises et billede af, hvordan puslespillet skal se ud (kan slås fra i **Menu**).
- Hvert puslespil har sine egne sessioner. Vælg en session i menuen ved siden af,
  eller vælg "＋ Ny session" for at lave en ny.
- Under **Menu** kan du omdøbe eller slette den aktuelle session.
- Tider fra før sessioner fandtes, ligger i 3x3 → "Session 1".

## Installér på telefonen
Åbn siden én gang, mens du har net:
- **iPhone (Safari):** Del-knappen → "Føj til hjemmeskærm"
- **Android (Chrome):** ⋮-menuen → "Installer app" / "Føj til startskærm"

Derefter virker appen uden internet.

## Scrambles og licens
Scrambles og billeder laves af [csTimer](https://github.com/cs0x7f/cstimer)s modul
`cstimer_module.js` (version 0.1.5, af cs0x7f), som er GPL-3.0. Derfor er hele denne app
også udgivet under GPL-3.0. Se `LICENSE`.
