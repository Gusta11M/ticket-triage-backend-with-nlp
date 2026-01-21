# 🗂️ Ticket Triage Backend with NLP

RESTful backend developed in Python using **FastAPI** for ticket management and automatic triage. 
The system leverages pre-trained **NLP models** to classify tickets by category and priority, persisting the results in a relational database.

The project focuses on backend engineering best practices and is designed as a portfolio project for junior backend/software engineering roles.

---

## 🚀 Backend Features

* **Ticket Management (CRUD)**
    * Create ticket
    * Retrieve ticket by ID
    * List tickets with simple filters
    * Update ticket (e.g., status)
* **Automatic Ticket Classification using NLP**
    * Category classification
    * Priority classification
* **Persistence** of classification results in the database
* **Category and Priority Management (CRUD)**
* **Security:** Basic authentication using JWT
* **Testing:** Automated tests for core flows
* **Documentation:** Automatic API documentation (OpenAPI / Swagger)

---

## 🛠️ Technology Stack

### Backend
* **Python**
* **FastAPI**

### Database & Storage
* **PostgreSQL** (Relational Database)
* **SQLAlchemy** (ORM)

### Intelligence
* **NLP:** Pre-trained text classification models (Hugging Face / Spacy / Scikit-learn)

### DevOps & Tools
* **Authentication:** JWT (JSON Web Tokens)
* **Testing:** `pytest` & `httpx`
* **Deployment:** Docker

---

## 🎯 Project Goal

The goal of this project is to demonstrate practical backend engineering skills, including:
1.  **REST API Design**
2.  **Data Modeling**
3.  **NLP Integration** in a real-world context
4.  **Automated Testing**
5.  **Technical Documentation**

This is not a full-featured helpdesk product, but a portfolio project focused on software engineering quality and decision-making.

---

## 🚫 Out of Scope

* Graphical user interface (frontend)
* Training or fine-tuning NLP models from scratch
* Advanced helpdesk features (SLAs, comments, notifications)
* Complex authorization or role management

---

## 📊 Data Models

### User
* `id`: Primary Key
* `email`: String (Unique)
* `hashed_password`: String
* `is_active`: Boolean
* `created_at`: DateTime

### Category
* `id`: Primary Key
* `category_name`: String
* `created_at`: DateTime

### Priority
* `id`: Primary Key
* `priority_name`: String (e.g., Low, Medium, High)
* `level`: Integer (e.g., 1, 2, 3 — for ordering)
* `created_at`: DateTime

### Ticket
* `id`: Primary Key
* `title`: String
* `message`: Text
* `status`: Enum (OPEN, IN_PROGRESS, CLOSED)
* `category_id`: Foreign Key
* `priority_id`: Foreign Key
* `user_id`: Foreign Key
* `created_at`: DateTime
* `updated_at`: DateTime

---

## 🛣️ API Endpoints

### 🔑 Authentication
* **POST `/auth/login`**: Create Token
    * **Body:** `{"email": "user@example.com", "password": "password"}`
    * **Response:** `{"access_token": "token", "token_type": "bearer"}`

### 🎫 Ticket Endpoints
* **POST `/tickets`**: Create a new ticket (triggers NLP classification)
* **GET `/tickets/{id}`**: Get specific ticket details
* **GET `/tickets`**: List tickets with filters (`?status=OPEN&category_id=1`)
* **PUT `/tickets/{id}`**: Update ticket status or manual overrides

### 📁 Category & Priority Endpoints
* **GET/POST/PUT/DELETE `/categories`**
* **GET/POST/PUT/DELETE `/priorities`**

### 🩺 Health & Meta
* **GET `/health`**: System status check

---

## 🔄 System Flow

```mermaid
flowchart LR
    Client[Client]
    API[FastAPI Router]
    Auth[Auth & Dependencies]
    Controller[Controller Layer]
    Service[Service Layer]
    NLP[NLP Service]
    Repo[Repository Layer]
    DB[(PostgreSQL)]

    Client --> API
    API --> Auth
    Auth --> Controller
    Controller --> Service
    Service --> NLP
    Service --> Repo
    Repo --> DB
    DB --> Repo
    Repo --> Service
    Service --> Controller
    Controller --> Client