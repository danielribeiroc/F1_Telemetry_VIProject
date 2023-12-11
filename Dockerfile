FROM python:3.10

WORKDIR /app
COPY . /app

RUN mkdir cache

RUN pip install --upgrade cython
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "./DashF1_Comparaison.py"]
