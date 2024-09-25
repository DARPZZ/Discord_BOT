# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the locale
RUN apt-get update && apt-get install -y locales tzdata && rm -rf /var/lib/apt/lists/* \
    && localedef -i da_DK -c -f UTF-8 -A /usr/share/locale/locale.alias da_DK.UTF-8
ENV LANG da_DK.UTF-8
ENV LANGUAGE da_DK:en
ENV LC_ALL da_DK.UTF-8
ENV TZ Europe/Copenhagen

# Set the working directory in the container
WORKDIR /usr/src/app
# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot when the container launches
CMD ["python", "bot.py"]
