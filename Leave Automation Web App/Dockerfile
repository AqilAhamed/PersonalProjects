ARG PORT=443
FROM cypress/browsers:latest

RUN apt-get update

RUN apt-get install python3 -y

RUN echo $(python3 -m site --user-base)

COPY requirements.txt .

ENV PATH /home/root/.local/bin:${PATH}

RUN apt-get update && apt-get install python3-pip -y && pip install -r requirements.txt --break-system-packages

COPY . .

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
