# speech

## Prerequisitos

Para ejecutar el script *speech.py* e necesario instalar las siguientes dependencias

```bash
sudo apt-get install python3 python3-pip
sudo pip3 install -r requirements.txt
```

## Ejecución

```
./speech.py -h
usage: speech.py [-h] [-t TEXT] [-f] [-g]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to reproduce
  -f, --file            File to take random line and reproduce it
  -g, --generate        Generate mp3 files for precharged sentences
```
