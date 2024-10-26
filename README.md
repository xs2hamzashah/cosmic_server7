# Cosmic Server 7  

Cosmic Server 7 is a backend system designed to manage solar products, buyers, sellers, and administrative actions. The project is built using Django and Django Rest Framework (DRF).  

## Table of Contents  
- [Installation](#installation)  
- [Features](#features)

## Installation  

1. Clone the repository:  

   ```bash  
   git clone https://github.com/your-repo/cosmic_server7.git  
   cd cosmic_server7

2. Set up and activate a virtual environment:
   ```bash
    python3 -m venv venv 
    source venv/bin/activate (BASH)
    On Windows use \`venv\\Scripts\\activate\ (CMD)
   
3. Install the dependencies:
   ```bash
    pip install -r requirements.txt

3. Create and Run database migrations:
    ```bash
   python manage.py makemigrations 
   python manage.py migrate

4.  Create a superuser:
    ```bash
    python manage.py createsuperuser
    
6.  Start the development server:
    ```bash
    python manage.py runserver

Features
--------

*   **Admin Analytics:** Admin can view seller performance, buyer interactions, and detailed reports of products.
    
*   **Seller Analytics:** Sellers can view interactions on their products and buyer details.
    
*   **OTP-based Buyer Interaction:** Secure OTP verification for buyer interactions.
    
*   **Dynamic Filtering:** Users can filter solar solutions based on city, system size, and price.
    
*   **Buyer Interaction Tracking:** Tracks buyer activity and interaction with solar solutions.
