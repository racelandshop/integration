FROM ludeeus/container:racelandshop-action

RUN git clone https://github.com/racelandshop/default.git /default

COPY action.py /racelandshop/action.py

ENTRYPOINT ["python3", "/racelandshop/action.py"]