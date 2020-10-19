# Government Identity Verification Engine

## Transaction Logging Service

### Pre-requisites
- [Git Bash](https://git-scm.com/downloads)
- [CF CLI](https://easydynamics.atlassian.net/wiki/spaces/GSATTS/pages/1252032607/Cloud.gov+CF+CLI+Setup)
- Cloud.gov account (Contact [Will Shah](mailto:wshah@easydynamics.com?subject=GSA%20Cloud.gov%20Account) to get one).
- [Maven](https://maven.apache.org/) 
- [OpenJDK 8](https://developers.redhat.com/products/openjdk/download)

This project was created with [Spring Boot Initializr](https://start.spring.io/)

### Getting started

This project is configured to work in the cloud.gov environment with a MySQL db.

To run the project locally with an in memory h2 database, uncomment the code in the application.properties files and comment the cloud configuration.

Once you have changed it to h2, run `mvnw spring-boot:run` to build and run the application.

### Accessing Content Locally

If you are running locally, open `http://localhost:8080/swagger-ui.html` in your browser

You will be presented with the Swagger UI, and have different options for the various requests.

### Build/Deployment

The building and deploying of the project is automated using AWS Codebuild with linked GitHub repository.

The resulting REST API is hosted on cloud.gov and can be accessed through the following route:
`https://give-transaction-logging-cheerful-wolverine-ne.app.cloud.gov/swagger-ui.html`

### Available Scripts

`mvnw clean install`

Builds the .jar files (including aws .jar file for lambda usage)

`mvnw clean install`

Runs the application.