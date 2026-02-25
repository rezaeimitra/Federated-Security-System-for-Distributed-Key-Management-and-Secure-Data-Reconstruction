FROM python:3.10-slim
WORKDIR /app

COPY app.py /app
COPY share.txt /app/share.txt

RUN pip install flask requests cryptography
EXPOSE 5000
CMD ["python", "app.py"]
