# E-Commerce

A simple e-commerce web application built with Django that allows both Customers and Sellers to interact with products, manage their carts, and handle authentication and orders.

## Features Implemented

### User Authentication
- Login / Register Pages: Users can sign up as either Customer or Seller, and get access to role-based features.
- Cart for Guests: Cart is stored in cookies for users who are not logged in.

### Shopping Cart
- Add Products to Cart: Users can add products directly from the store page.
- Navbar Cart Count: Displays the total number of items in the cart.

### Cart Page Functionalities
- Increase or decrease product quantity
- Remove products from the cart
- View all added products in the cart

### Checkout and Order Tracking
- Checkout Page integrated with PayPal
- On successful payment, the order appears in the Track Shipment page

### Seller Features
- Upload Product: Sellers can upload new products via a dedicated page
- Product Detail & Order Handling: Sellers can view incoming orders and mark them as Prepared or Rejected

## Features in Progress
- User Profile Page
- User Dashboard
- Enhanced Order Tracking for Customers

## Tech Stack
- Django (Backend Framework)
- HTML & CSS (Frontend Structure and Styling)
- JavaScript (Cart updates and interactivity)
- PostgreSQL (Database)

## Notes
- This project supports both guest users and registered users.
- Still under development, more features will be added soon.

## Links
- GitHub Repository: [https://github.com/Abdelrahman-Hassany/E-Commerce](https://github.com/Abdelrahman-Hassany/E-Commerce)
- Live Version on Railway (may have issues with media/static files): [http://e-commerce-production-305d.up.railway.app](http://e-commerce-production-305d.up.railway.app)

Feel free to explore the code, and I welcome feedback or contributions.