FROM python:3.9

WORKDIR /usr/src/app

RUN pip install requests

COPY generate_health_data.py .

CMD ["python", "./generate_health_data.py"]
