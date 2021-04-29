# TPW_P1

Website Developped using Django Framework for TPW's Course **Tecnologias e Programação Web** (3rd Year - 2nd Semester)

Theme : Shopping Store

### Development Team:
      > Fábio Carmelino
      > Maria Rocha
      > Pedro Souto

### Main features - General:
      > Search by a product's Category or Name (Results are presented using pagination(*) in case there are more than 12)
      > Tabs for: Hot Deals(Most sold products) / Newly Arrived(Most recent products) / Shops(List of Shops)  
      > (*) Pagination can be tested by selecting on the 'Browse Categories' menu the option 'Phones (14)'

### Main Features - Authenticated Customer:
      > External Authentication by Google
      > Internal Sign Up and Login 
      > Edit a user account details
      > Edit a user account address
      > Add and/or Remove Products to Cart
      > Add and/or Remove Products to Wishlist
      > Purchase Products in Cart 
      
### Main Features - Shop Account:
      > Create a Shop Account and Login
      > Create a New Product (Products may be shared by all shops)
      > Edit a Product (Only it's creater can edit it and only has long as no other shop as created items for the said product.)
      > Delete a Product (With the same restrictions as 'Edit Product')
      > Create a New Item for a Product that already exists (Only necessary to select an existent product and fill a form with the stock and price) 

### Testing accounts:
      normal account:
      > username: UserDemo
      > password: userdemo

      shop account1:
      username: tech4U
      password: secret

      shop account3:
      > username: MiStore
      > password: mistore1234online

      django admin:
      > username: Admin
      > password: ADMIN

### Site online:
      http://mariarocha.pythonanywhere.com/
      
      Note: Google Authentication is not working on pythonanywhere site because Google has some security measures that don't allow redirect the login to an insecure domain.
      
### Configurations:
      if running requirements.txt fails try this:
            python3 -m pip install django-allauth
            
      
- Licenciatura em Engenharia Informática, Universidade de Aveiro   (2020/2021)
