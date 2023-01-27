# etesters

## Présentation

A partir des fichiers de production (Gerber RS-274X), le module permet de sélectionner les points d'intérêts à garder pour la construction d'un banc de test.


## Installation

Installer pip si ce n'est pas déjà fait
```
sudo apt-get install pip
```

Installer le module
```
git clone https://github.com/dxl0/etesters.git
cd etesters
pip install estesters
```

## Quick use

```
touch app.py
echo "import etesters" >> app.py
echo "etesters.App().display()
python3 app.py
```


## Doc

La doc se trouve au format html dans [/docs/build/html/index.html](/docs/build/html) .
