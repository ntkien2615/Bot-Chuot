FROM python:3.10
RUN pip install poetry
WORKDIR /code
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD python bot.py