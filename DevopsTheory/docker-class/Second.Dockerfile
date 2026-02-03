FROM ubuntu:22.04

RUN apt update && apt install -y openjdk-17-jdk

WORKDIR /home/app

COPY Hello.java .

RUN javac Hello.java
ENTRYPOINT "echo 'Pulkit' &&";
CMD ["java", "Hello"]
