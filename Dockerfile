FROM python:3.9-alpine3.17

# install bash
RUN apk update \
    && apk add bash curl

#create/change working directory
WORKDIR /home/app

#install dependencies
RUN pip install boto3

#copy files
COPY ./app/app.py .

#inject image URL
ARG container
ENV CONTAINER $container

#inject repo url
ARG project
ENV PROJECT $project

EXPOSE 5000

CMD ["python", "app.py"]
