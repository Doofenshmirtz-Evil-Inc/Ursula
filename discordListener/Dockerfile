FROM python:3.7-slim
ADD bot.py /
ADD cogs /cogs
ADD requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./bot.py"]