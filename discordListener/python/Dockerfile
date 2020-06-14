FROM python:3.7-slim

WORKDIR /python
ADD bot.py ./bot.py
ADD audioManager.py ./audioManager.py
ADD requirements.txt ./requirements.txt
ADD keys.env ./keys.env
RUN pip install --no-cache-dir -r /python/requirements.txt
CMD [ "python", "/python/bot.py"]