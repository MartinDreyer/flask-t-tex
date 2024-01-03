FROM python:3.11

RUN apt-get update

RUN apt-get -y upgrade

RUN apt-get install -y ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt 

RUN pip install git+https://github.com/openai/whisper.git

COPY . . 

EXPOSE 8888

CMD ["flask", "--app", "t_tex", "run", "--host=0.0.0.0", "--port=8888"]
