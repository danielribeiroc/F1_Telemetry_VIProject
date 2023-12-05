FROM python:3.10-alpine

WORKDIR /app
COPY . /app

RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev jpeg-dev zlib-dev
RUN pip install -r requirements.txt

EXPOSE 8082

ENV NAME World

CMD ["python", "./DashF1_Comparaison_v3.py"]
