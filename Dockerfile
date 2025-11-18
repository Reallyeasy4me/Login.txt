FROM python:3.10
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
CMD ["pytest", "-v"]