FROM continuumio/miniconda3:latest

RUN pip install pymemgpt[local,postgres]
RUN pip install simplematrixbotlib

RUN mkdir -p /memgpt
WORKDIR /memgpt
COPY . ./

RUN pip install -e .
RUN pip install wmill

ENTRYPOINT []
CMD ["python", "entry.py", "server", "--type", "matrix"]