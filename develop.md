<p align="center">
  <img src="resources/img/retrobox_manager.png" alt="Retrobox Manager" width="480"/>
</p>

# retrobox-manager

Project to manage my Retrobox

## Packaging

```bash
raw_version=$(head -n 1 CHANGELOG | awk '{print $1}')
version="${raw_version#R}"
python3 -m PyInstaller --name "retrobox-manager" --onefile --noconsole --icon=resources/img/retrobox.ico retrobox-manager.py --add-data "libvlccore.dll:." --add-data "libvlc.dll:." --add-data "plugins:plugins" --add-data "resources:resources" --add-data "binaries:binaries" --add-data "CHANGELOG:." ; rm -Rf build ; rm retrobox-manager.spec
```

## Install

Install :
- **python3**
- **TKINTER** with following commands:
```bash
sudo apt update
sudo apt install python3-tk
```
- **requirements** using **pip3**:
```bash
pip3 install -r requirements
```

## Testing locally

To analyze your code, use command:

```bash
find . -iname "*.py" -not -path "./.venv/*" | xargs python3 -m pylint
```

To test the Scraper API:

```bash
curl -X GET "https://api.screenscraper.fr/api2/systemesListe.php?devid=<dev_pseudo>&devpassword=<password>&softname=manager&output=json"
```

## Usage

Use the environment variable RETROBOX_MANAGER_PATH to define a specific path to work.

```bash
export RETROBOX_MANAGER_PATH='E:\\_Retro Box\\retrobox-manager'
```

To start the application, type following command:

```bash
python3 retrobox-manager.py
```
