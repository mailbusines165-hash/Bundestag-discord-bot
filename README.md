# Landtag/Bundestag Discord Bot – Simulation

Ein einfacher Discord-Bot mit Slash-Commands, der eine Auszahlungskarte als **Simulation** erzeugt.

## Befehle

- `/auszahlung betrag:2500` – erzeugt ein PNG
- `/ping` – Bot-Test
- `/hilfe` – Hilfe

## Zugriff beschränken

In den Umgebungsvariablen kannst du festlegen:

- `ALLOWED_CHANNEL_ID` – nur dieser Channel darf `/auszahlung` verwenden
- `ALLOWED_ROLE_ID` – nur Mitglieder mit dieser Rolle dürfen den Befehl verwenden

Wenn du beide leer lässt, gibt es keine zusätzliche Einschränkung.

## Discord-Token

Den Bot-Token niemals in `bot.py` oder GitHub eintragen.
Er wird als Umgebungsvariable `DISCORD_TOKEN` beim Hosting gespeichert.

## GitHub + Hosting

1. Dateien in ein GitHub-Repository hochladen.
2. Das Repository mit einem Python-Worker-Hostingdienst verbinden.
3. Die Umgebungsvariablen setzen.
4. Den Bot starten.
5. Den Bot über das Discord Developer Portal mit den benötigten Bot-/Application-Scopes einladen.

Die erzeugten Karten sind absichtlich mit
"SIMULATION – NICHT AMTLICH / KEIN ZAHLUNGSBELEG"
gekennzeichnet.
