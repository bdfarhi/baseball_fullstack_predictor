FROM eclipse-temurin:17-jdk AS build

WORKDIR /app

# Copy and build with Maven
COPY . .
RUN ./mvnw package -DskipTests

# Run from JAR
FROM eclipse-temurin:17-jdk
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]