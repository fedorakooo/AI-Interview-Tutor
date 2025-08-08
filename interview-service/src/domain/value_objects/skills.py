from enum import StrEnum


class BackendTechSkill(StrEnum):
    # Languages & Frameworks
    PYTHON = "Python"
    FASTAPI = "FastAPI"
    DJANGO = "Django"

    # Databases
    SQL = "SQL"
    MONGODB = "MongoDB"
    DYNAMODB = "DynamoDB"
    REDIS = "Redis"
    ELASTICSEARCH = "ElasticSearch"

    # Message Brokers
    RABBITMQ = "RabbitMQ"
    KAFKA = "Kafka"

    # Cloud Platforms
    AWS = "AWS"
    GOOGLE_CLOUD = "Google Cloud"
    AZURE = "Azure"

    # DevOps
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
    TERRAFORM = "Terraform"

    # Architecture
    MICROSERVICES = "Microservices"
