
FROM python:3.9-slim


RUN apt-get update && apt-get install -y locales tzdata && rm -rf /var/lib/apt/lists/* \
    && localedef -i da_DK -c -f UTF-8 -A /usr/share/locale/locale.alias da_DK.UTF-8
ENV LANG da_DK.UTF-8
ENV LANGUAGE da_DK:en
ENV LC_ALL da_DK.UTF-8
ENV TZ Europe/Copenhagen
restart: always
WORKDIR /usr/src/app
RUN touch /usr/src/app/discord.log

COPY . .


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
