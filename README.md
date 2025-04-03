# About
This is a simple CRUD application designed to streamline the process of registering appointments in a veterinary clinic. It performs a check against a MySQL database, to see if there are any available veterinarians for the specified appointment type and date. Below are some sample screenshots, taken from an admin account.
<br>
# REST API
This application has a fully implemented REST API for handling various requests. Authentication is done via api keys, assigned to users after they get registered. You can browse the api.py for more information, as the documentation will be posted here at a later date.
<br>
An example request would be: GET /api/appointments/<int:app_id>?key=<insert_your_api_key_here>
# Screenshots
![image](https://github.com/user-attachments/assets/bc179aa7-eb7d-466d-8c2f-d5c03ba7146d)
![image](https://github.com/user-attachments/assets/9da96096-3518-402d-af50-a704297c3033)
