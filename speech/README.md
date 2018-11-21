# speech

## Prerequisitos

Para ejecutar el script *speech.py* e necesario instalar las siguientes dependencias

```bash
sudo apt-get install python3 python3-pip code
sudo pip3 install -r requirements.txt
```

## Ejecución

```
./speech.py -h
usage: speech.py [-h] [-t TEXT] [-r] [-w WHAT] [-g] [-l] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to reproduce
  -r, --random          Reproduce random sentence from files in ./topics
  -w WHAT, --what WHAT  Specify topic to reproduce random sentence
  -g, --generate        Generate mp3 files for precharged sentences
  -l, --list            List available topics
  -c, --clean_cache     Clean mp3 files in /tmp
```
