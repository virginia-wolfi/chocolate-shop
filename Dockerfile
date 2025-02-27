# Используем официальный образ Python
FROM python:3.13-alpine

# Устанавливаем рабочую директорию
WORKDIR /chocolate-shop


# install python dependencies
RUN pip install --upgrade pip
RUN pip install poetry


# copy project requirements
COPY poetry.lock pyproject.toml ./

# install project requirements,
RUN poetry install

COPY . ./

RUN chmod +x entrypoint.sh

# Запускаем entrypoint
ENTRYPOINT ["./entrypoint.sh"]

