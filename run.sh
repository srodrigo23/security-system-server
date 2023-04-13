
clear
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd src
clear
echo 'Launch Server'
python main.py
# cd src/original_detectors
# python original_fire_detector.py