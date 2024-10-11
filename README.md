# Cosmic Server 7  

Cosmic Server 7 is a backend system designed to manage solar products, buyers, sellers, and administrative actions. The project is built using Django and Django Rest Framework (DRF).  

## Table of Contents  
- [Installation](#installation)  
- [Features](#features)  
- [API Endpoints](#api-endpoints)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgments](#acknowledgments)  

## Installation  

1. Clone the repository:  

   ```bash  
   git clone https://github.com/your-repo/cosmic_server7.git  
   cd cosmic_server7


2. Set up and activate a virtual environment:
   ```bash
    python3 -m venv venv source venv/bin/activate # On Windows use \`venv\\Scripts\\activate\

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
    

API Endpoints
-------------

### Authentication

*   POST : Login endpoint.
    
*   POST : Logout endpoint.
    

### Solar Solutions

*   GET /solar-solutions/: Retrieve solar solutions.
    
*   POST /solar-solutions/: Create a new solar solution.
    
*   GET /solar-solutions/{id}/: Retrieve details of a specific solar solution.
    

### Buyer OTP

*   POST : Send OTP to the buyer.
    
*   POST : Confirm OTP and track buyer interaction.
    

### Analytics

*   GET : View all seller reports (Admin only).
    
*   GET /: View seller's product interactions (Seller only).
    

Project Structure
-----------------

cosmic_server7/  
│  
├── accounts/  
│   ├── models.py           # UserProfile, Company, CustomUser models.  
│   ├── views.py            # User management and authentication views.  
│   └── serializers.py      # User-related serializers.  
│  
├── solar/  
│   ├── models.py           # Solar solutions, buyer interactions, and related models.  
│   ├── views.py            # Solar product views and APIs.  
│   └── serializers.py      # Solar solution serializers.  
│  
├── analytics/  
│   ├── models.py           # BuyerInteraction model.  
│   ├── views.py            # Admin and seller analytics viewsets.  
│   └── serializers.py      # Analytics serializers.


Contributing
------------    

License
-------

Acknowledgments
---------------
