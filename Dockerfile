FROM maven:3.9.8-eclipse-temurin-17 AS build
WORKDIR /workspace
COPY . .
ARG SERVICE
RUN mvn -pl ${SERVICE} -am -DskipTests package
FROM eclipse-temurin:17-jre
WORKDIR /app
ARG SERVICE
COPY --from=build /workspace/${SERVICE}/target/*.jar app.jar
ENTRYPOINT ["java","-jar","/app/app.jar"]
