FROM python:3

RUN apt-get update && apt-get install -y vim

# Create app directory
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .

CMD [ "python", "./main.py" ]


