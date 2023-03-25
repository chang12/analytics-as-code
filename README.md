```bash
pyenv virtualenv 3.10 analytics-as-code

# 혹은
pyenv activate analytics-as-code
```
```
pip3 install -r requirements.txt
```
config.py.sample 을 -> config.py 로 copy & paste 한 뒤에, 값을 적절히 적는다.
```
uvicorn app:app
```
