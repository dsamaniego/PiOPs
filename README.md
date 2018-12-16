# speech.py

## Prerequisitos

### Ubuntu/Debian

Para ejecutar el script *speech.py* e necesario instalar las siguientes dependencias

```bash
sudo apt-get install python3 python3-pip python3-pyaudio vlc
sudo pip3 install -r requirements.txt
```

### Fedora

```bash
sudo dnf -y install python3 python3-pip python3-pyaudio python3-devel redhat-rpm-config portaudio-devel portaudio vlc
sudo pip3 install -r requirements.txt
```


## Ejecución

```
usage: speech.py [-h] [-t TEXT] [-r [RANDOM]] [-l] [-m MP3]

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Text to reproduce
  -r [RANDOM], --random [RANDOM]
                        Reproduce random sentence from ./topics/RANDOM.
                        Without argument, reproduce random sentence from
                        random topic
  -l, --list            List available topics
  -m MP3, --mp3 MP3     MP3 file of list. User -l to see available mp3
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
  "admin": [
    "1111111",
    "4444444"
  ],
  "authorized_ids": [
    "1111111",
    "2222222",
    "3333333",
    "4444444",
    "5555555",
    "6666666"
  ]
}
```

## Instalación

```bash
nohup /usr/local/bin/datiops_bot.py -c /home/pi/PIOPS/secrets.json &
```

## Ejecución

```
usage: datiops_bot.py [-h] -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Define el fichero json de configuracion del script
```