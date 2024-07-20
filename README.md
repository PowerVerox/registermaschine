# Registermaschine

## Implementation einer Registermaschine in Python

## Ablauf ausführen

1. textdatei speichern mit registermaschine befehlen
2. einlesen in list (man kann direkt mit den index zum befehl springen usw (instruction[5]))
3. wenn syntax_check kein fehler
4. programmcounter hoch, erste zeile lesen --> befehlsfunktion ausführen (switch case oder wie macht man das??)

## pyenv installieren

ausführen:

`curl https://pyenv.run | bash`

ganz unten in `~/.bashrc` einfügen:

`export PATH="$HOME/.pyenv/bin:$PATH"`

`eval "$(pyenv init --path)"`

`eval "$(pyenv virtualenv-init -)"`

python version installieren:
`pyenv install 3.12.4`

## Quellen

<https://link.springer.com/content/pdf/10.1007/978-3-322-82204-8.pdf>
