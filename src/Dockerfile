FROM huggingface/transformers-pytorch-gpu:4.29.2

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

CMD [ "gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8000", "--preload" ]
