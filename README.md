
# Cole's Grocery Shop- Fruit And Grocery Management System

This project is a shop inventory management system. It allows you to track your stock levels, manage orders, manage products and users.
## Features
* Add, edit, and delete products from inventory
* Track stock levels for each product
* Manage incoming and outgoing orders
* Dynamic decentralization of accounts
* Add multiple products at the same time using excel file

## Installation
1. Clone this repository:

```bash
git clone https://github.com/mathlover1998/fruit_shop
```

2. Open project and create virtual environment:
```bash
python -m venv venv
```

3. Activate venv:
```bash
source venv/Scripts/activate
```

4. Navigate to main project:
```bash
cd fruit_shop
```

5. Install requirement packages:
```bash
pip install -r requirements.txt
```

6. Create .env file
(sample variables in .env.example file)
or you can contact [https://www.facebook.com/ColeTran87645/](https://www.facebook.com/ColeTran87645/) to get actual variables.

## Usage
1. Run the application:
```bash
python manage.py runserver
```

2. Follow the on-screen instructions to manage your fruit inventory.

3. To access the admin page, go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) or [https://fruit-shop-qi40.onrender.com/admin/](https://fruit-shop-qi40.onrender.com/admin/) (Using admin account (username: admin, password: 123))

4. To allow account to CRUD product, that account needed to add relationship with Employee table and give it Inventory Manager Permission.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
