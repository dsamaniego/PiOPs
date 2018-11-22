# speech.py

## Prerequisitos

Para ejecutar el script *speech.py* e necesario instalar las siguientes dependencias

```bash
sudo apt-get install python3 python3-pip vlc
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

# datio_ops.py

## Prerequisitos

```bash
pip3 install -r requirements.txt
```

## configuración

Es necesario tener un fichero *json* con el token del bot de telegram y la lista de ids de telegram autorizados. El formato debe ser el siguiente:

```json
{
  "token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "authorized_ids": [
    1111111,
    2222222,
    3333333,
    4444444,
    5555555,
    6666666
  ]
}
```

## Instalación

```bash
sudo ln -s /home/pi/PIOPS/datiops_bot.py /usr/local/bin/
sudo cp datiops_bot.service /etc/systemd/system/
sudo systemctl enable datiops_bot
sudo systemctl start datiops_bot
```

## Ejecución

```
usage: datiops_bot.py [-h] -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Define el fichero json de configuracion del script
```