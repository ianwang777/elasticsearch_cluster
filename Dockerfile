FROM python:3.9

WORKDIR /usr/src/app

RUN pip install requests

COPY generate_health_data.py .

COPY search_es.py .

# CMD ["python", "./generate_health_data.py"]
CMD ["sh", "-c", "python ./generate_health_data.py & python ./search_es.py"]
