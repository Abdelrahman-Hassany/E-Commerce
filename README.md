# E-Commerce Backend Project

This repository is part of my hands-on learning journey. It contains my first e-commerce project built with Django, which I continuously improve to enhance performance, code quality, and scalability.

## Current Status

- The project uses Django views and templates.
- Still in progress and actively being improved.
- The login page has **not been implemented yet**.

## Planned Improvements

- Create a shared `context` file to centralize the logic for getting the total number of items in the cart.
  - This will replace repeated logic in multiple view functions.
- Use Django’s `@login_required` decorator instead of checking if `user == anonymous`.
  - This will improve security and prevent console spoofing by guests.
- Ensure guests can see items and interact with the cart, but cannot perform restricted actions.

## Security Goals

- Apply Django’s standard authentication and access control.
- Add CSRF protection where needed.
- Define more granular permissions.

## Technologies Used

- Python
- Django
- HTML & CSS (Django Templates)

##  To-Do

- [ ] Implement login & registration pages
- [ ] Build shared context file for cart items
- [ ] Replace `user == anonymous` checks with `@login_required`
- [ ] Build RESTful API version using Django REST Framework
- [ ] Deploy on cloud 

---

Feel free to explore, and I welcome feedback!
