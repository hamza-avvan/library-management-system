# DB service
FROM mysql:5.7
ADD db/lms.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

# app service
FROM python:3.9-slim

ARG USER=webmin
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USER 2>&1 \
    && useradd --uid $USER_UID --gid $USER_GID -m $USER 2>&1; exit 0

USER $USER
ENV PATH=$PATH":/home/$USER/.local/bin"

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]