FROM python:latest

RUN pip install pymemgpt[local,postgres]
RUN pip install simplematrixbotlib
RUN pip install -e .
RUN pip install wmill

ENTRYPOINT []
CMD ["memgpt", "server", "--type matrix"]