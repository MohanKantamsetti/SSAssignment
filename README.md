# eCommerce Microservices Application
This repository contains an eCommerce application built using a microservices architecture. The application is designed to be scalable, resilient, and flexible, employing modern technologies like Docker, RabbitMQ, and Kong API Gateway.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Services](#services)
   - [Checkout Service](#checkout-service)
   - [Email Service](#email-service)
4. [Technologies Used](#technologies-used)
5. [Setup and Installation](#setup-and-installation)
6. [Usage](#usage)
7. [API Gateway Configuration](#api-gateway-configuration)
8. [Contributing](#contributing)
9. [License](#license)

## Overview

This project implements a basic eCommerce application using microservices. The application is composed of independent services for user management, inventory, reviews, and checkout, each with its own database. The services communicate asynchronously using RabbitMQ, and the system is secured and managed via Kong API Gateway.

## Architecture

The architecture consists of the following components:
- **Client Devices**: Interfaces for users to interact with the eCommerce application.
- **API Gateway**: Manages and routes incoming requests to the appropriate microservices.
- **Microservices**: Independent services for user, inventory, review, and checkout functionalities, each communicating with its own database.
- **RabbitMQ**: Facilitates communication between services, particularly between order creation and email notifications.
- **Databases**: Each service has a dedicated MongoDB instance for data storage.

## Services

### Checkout Service
- **Functionality**: Manages orders, processing payments, and communicating with RabbitMQ to trigger email notifications.
- **Database**: Utilizes MongoDB for storing order information.

### Email Service
- **Functionality**: Listens for order messages from RabbitMQ and sends confirmation emails using Gmail SMTP.
- **Dependencies**: Requires SMTP credentials to be configured for email sending.

## Technologies Used

- **Docker & Docker Compose**: Containerization and orchestration of services.
- **Kong API Gateway**: Manages API traffic and provides authentication and security.
- **RabbitMQ**: Message broker for asynchronous communication between services.
- **MongoDB**: Database for storing service-specific data.
- **Python**: Used for implementing the services, utilizing libraries such as Flask (for API handling) and Pika (for RabbitMQ integration).

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone <url>
   cd <dir>
   ```

2. **Configure Environment Variables**:
   - Set up `.env` files or environment variables for RabbitMQ, MongoDB, and SMTP credentials.

3. **Build and Start Services**:
   - Use Podman Compose to build and start all services:
   ```bash
   podman-compose up --build
   ```

4. **Initialize Kong**:
   - Run migrations for Kong:
   ```bash
   podman-compose exec kong kong migrations bootstrap
   ```

## Usage

- **Access the API**: Interact with the application via the API Gateway at `http://localhost:8000`.
- **Administer Kong**: Use Kong's Admin API at `http://localhost:8001` to manage services and routes.

## API Gateway Configuration

- **Kong Setup**: Use the Kong Admin API to configure services, routes, and JWT authentication.
- **Example Commands**:
  ```bash
  curl -i -X POST http://localhost:8001/services/ --data "name=checkoutservice" --data "url=http://backend:5000"
  ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
