# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

from rasa_sdk.events import FollowupAction
from difflib import get_close_matches
import random


mysql_password="pnp@22022002"
 # please update your mysql password above.


class ResetSlotsAction(Action):
    def name(self) -> Text:
        return "action_reset_select_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        return [SlotSet(slot, None) for slot in tracker.slots.keys() if (slot != "f_login_type" and slot != "f_login_phno" and slot !="f_login_password")]


class CheckLoginStatusAction(Action):
    def name(self) -> Text:
        return "action_check_login_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        f_login_type = tracker.get_slot("f_login_type")

        if f_login_type == "1":
            message = "You are logged in as an admin."
        elif f_login_type == "2":
            message = "You are logged in as a customer."
        elif f_login_type == "3":
            message = "You are logged in as a delivery guy."
        else:
            message = "You are not logged in."
            
        print(f_login_type)
        dispatcher.utter_message(text=message)

        return []



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []



class ActionLogin(Action):
  def name(self):
    return "action_login"

  def run(self, dispatcher, tracker, domain):
   
    print("running action_login")
    user_type = tracker.get_slot("user_type")
    user_phno = tracker.get_slot("user_phno")
    user_password= tracker.get_slot("user_password")

    # Connect to the local instance of MySQL
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      password=mysql_password,
      database="myrasabot"
    )
    print("Connected to MySQL")

    # Create a cursor object to execute queries
    cursor = db.cursor()

    # Select the table based on the user type
    if user_type == "1":
      table = "admin"
      # Query the table with the user phone number and password
      query = f"SELECT * FROM {table} WHERE phno = %s AND password = %s"
      values = (user_phno, user_password)
      cursor.execute(query, values)
      result = cursor.fetchone()

      # Check if the result is not empty
      if result:
        # Login successful
        dispatcher.utter_message("Login successful.")
      else:
        # Incorrect credentials
        dispatcher.utter_message("Incorrect credentials. Please register first via any other admin , if u haven't done before.")

    elif user_type == "2":
      table = "customer"
      # Query the table with the user phone number and password
      query = f"SELECT * FROM {table} WHERE c_phno = %s AND c_password = %s"
      values = (user_phno, user_password)
      cursor.execute(query, values)
      result = cursor.fetchone()

      # Check if the result is not empty
      if result:
        # Login successful
        dispatcher.utter_message("Login successful.")
      else:
        # Incorrect credentials
        dispatcher.utter_message("Incorrect credentials. Please register first if u haven't done before.")


    elif user_type == "3":
      table = "delivery_guy"
      query = f"SELECT * FROM {table} WHERE phno = %s AND password = %s"
      values = (user_phno, user_password)
      cursor.execute(query, values)
      result = cursor.fetchone()

      # Check if the result is not empty
      if result:
        # Login successful
        dispatcher.utter_message("Login successful.")
      else:
        # Incorrect credentials
        dispatcher.utter_message("Incorrect credentials. Please register first via admin , if u haven't done before.")


    else:
      table = None
      dispatcher.utter_message("Invalid user type.")

    # Close the cursor and the database connection
    cursor.close()
    db.close()
    print("Disconnected from MySQL")
    
    # Set a slot with the user type and return 
    return [SlotSet("f_login_type", user_type),SlotSet("f_login_phno",user_phno),SlotSet("f_login_password",user_password)]

class LoginCheckAction(Action):
    def name(self) -> Text:
        return "action_logout"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="You are now logged out.")
        return [SlotSet("f_login_type", None),SlotSet("f_login_phno",None),SlotSet("f_login_password",None)]


# define the custom action class
class ActionRegisterCustomer (Action):
  # define the name of the action
  def name (self) -> Text:
    return "action_register_customer"

  # define the run method that executes the action logic
  def run (self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict [Text, Any]) -> List [Dict [Text, Any]]:
    # get the slot values from the tracker
    print("running action action_register_customer")
    name = tracker.get_slot ("name")
    user_phno = tracker.get_slot ("user_phno")
    user_password = tracker.get_slot ("user_password")
    city_name = tracker.get_slot ("city_name")
    address = tracker.get_slot ("address")

    # connect to the mysql database
    db = mysql.connector.connect (
      host="localhost",
      user="root",
      password=mysql_password,
      database="myrasabot"
    )
    print ("Connected to mysql")

    # create a cursor object to execute queries
    cursor = db.cursor ()

    # check if a customer with the same phone number already exists in the database
    query = "SELECT * FROM customer WHERE c_phno = %s"
    cursor.execute (query, (user_phno,))
    result = cursor.fetchone ()

    # if the result is not None, it means the customer already exists
    if result is not None:
      # get the existing customer details from the result
      c_id, c_name, c_phno, c_password, c_city_name, c_address = result

      # utter a message to inform the user that they are already registered
      dispatcher.utter_message (text=f"You are already registered as {c_name} with phone number {c_phno} and password {c_password}.")

    # otherwise, the customer is new and needs to be added to the database
    else:
      # generate a random id that is not in the database
      query = "SELECT c_id FROM customer"
      cursor.execute (query)
      ids = [row [0] for row in cursor.fetchall ()] # get a list of existing ids
      id = random.randint (1, 1000) # generate a random id between 1 and 1000
      while id in ids: # loop until the id is not in the list
        id = random.randint (1, 1000) # generate a new id

      # insert the new customer details into the database
      query = "INSERT INTO customer (c_id, c_name, c_phno, c_password, c_city_name, c_address) VALUES (%s, %s, %s, %s, %s, %s)"
      cursor.execute (query, (id, name, user_phno, user_password, city_name, address))
      db.commit () # commit the changes to the database

      # utter a message to confirm the registration of the new customer
      dispatcher.utter_message (text=f"Thank you for registering as {name} with phone number {user_phno} and password {user_password}. Your customer id is {id}.")

    # close the database connection
    db.close ()
    print ("Disconnected from mysql")

    # return an empty list of events
    return []



class ActionAddProduct(Action):
    def name(self):
        return "action_add_product"

    def run(self, dispatcher, tracker, domain):
        print("running action action_add_product")

        if tracker.get_slot("f_login_type") == "1":
            # connect to the SQL database
            # connect to the mysql database
            db = mysql.connector.connect (
                host="localhost",
                user="root",
                password=mysql_password,
                database="myrasabot"
             )
            print ("Connected to mysql")

            # create a cursor object to execute queries
            cursor = db.cursor ()
            # print connected to mysql
            print("Connected to mysql")
            # get the slot values for product details
            p_name = tracker.get_slot("p_name")
            p_quantity = tracker.get_slot("p_quantity")
            p_rating = tracker.get_slot("p_rating")
            p_price = tracker.get_slot("p_price")
            p_description = tracker.get_slot("p_description")
            p_image_links_text = tracker.get_slot("p_image_links_text")
           
            p_id = random.randint(1, 1000)
            cursor.execute("SELECT * FROM product WHERE p_id = %s", (p_id,))
            results=cursor.fetchone()
            while results:
                p_id = random.randint(1, 1000)
                cursor.execute("SELECT * FROM product WHERE p_id = %s", (p_id,))
                results=cursor.fetchone()
            cursor.execute("INSERT INTO product (p_id, p_name, p_quantity, p_rating, p_description, p_price) VALUES (%s, %s, %s, %s,%s, %s)", (p_id, p_name, p_quantity, p_rating, p_description, p_price))
            db.commit()

            image_links = p_image_links_text.split(",")
            for image_link in image_links:
                cursor.execute("INSERT INTO product_images (p_id, image_link) VALUES (%s, %s)", (p_id, image_link.strip()))
            db.commit()
            dispatcher.utter_message(f"Product {p_name} is now added to database in MYSQL.")
            db.close()
            print("Disconnected from mysql")
        else:
            dispatcher.utter_message("Sorry, you do not have the privileges of adding/removing a product. This feature is only available for the admin.")

        return []




class ActionRemoveCustomer(Action):
    
    def name(self) -> Text:
        return "action_remove_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to the local instance of MySQL
        db = mysql.connector.connect(
          host="localhost",
          user="root",
          password=mysql_password,
          database="myrasabot"
        )
        print("Connected to MySQL")
        
        # get customer_id from slots
        customer_id = tracker.get_slot("id")
        
        # delete customer with the given ID
        mycursor = db.cursor()
        sql = "DELETE FROM customer WHERE c_id = %s"
        val = (customer_id,)
        mycursor.execute(sql, val)
        db.commit()

        print(mycursor.rowcount, "record(s) deleted")
        dispatcher.utter_message("Deletion successful")

        # disconnect from MySQL
        db.close()
        print("Disconnected from MySQL")

        return []



class ActionTellCustomersName(Action):
    
    def name(self) -> Text:
        return "action_tell_customers_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # connect to MySQL
       # Connect to the local instance of MySQL
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          password=mysql_password,
          database="myrasabot"
        )
        print("Connected to MySQL")
        
        # retrieve all customer IDs and names
        mycursor = mydb.cursor()
        mycursor.execute("SELECT c_id, c_name FROM customer")
        result = mycursor.fetchall()
        
        # utter all customer IDs and names
        if result:
            for row in result:
                dispatcher.utter_message(f"ID: {row[0]}, Name: {row[1]}")
        else:
            dispatcher.utter_message("No customers found")

        # disconnect from MySQL
        mydb.close()
        print("Disconnected from MySQL")

        return []


class ActionAddAdminOrDeliveryGuy(Action):
    def name(self) -> Text:
        return "action_add_admin_or_delivery_guy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         
        login = tracker.get_slot("f_login_type")
        if login != "1": 
              dispatcher.utter_message("Sorry, you do not have the privileges of adding/removing a admin or delivery guy. This feature is only available for the admin.")
              return []
    
        # connect to mysql database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")
        

        # obtain values from form
        admin_or_delivery_guy = tracker.get_slot("admin_or_delivery_guy")
        new_name = tracker.get_slot("new_name")
        new_phno = tracker.get_slot("new_phno")
        new_password = tracker.get_slot("new_password")
        
        # insert new user into the appropriate table
        if admin_or_delivery_guy == "1":
            # generate a random unique ID for admin
            admin_id = random.randint(1000, 9999)
            while True:
                cursor.execute(f"SELECT * FROM admin WHERE id={admin_id}")
                result = cursor.fetchone()
                if not result:
                    break
                admin_id = random.randint(1000, 9999)
            
            # insert new admin into admin table
            query = f"INSERT INTO admin (id, name, password, phno) VALUES ({admin_id}, '{new_name}', '{new_password}', '{new_phno}')"
            cursor.execute(query)
            db.commit()
            dispatcher.utter_message(text="Successfully added a new admin")
        elif admin_or_delivery_guy == "2":
            # generate a random unique ID for delivery guy
            delivery_guy_id = random.randint(1000, 9999)
            while True:
                cursor.execute(f"SELECT * FROM delivery_guy WHERE id={delivery_guy_id}")
                result = cursor.fetchone()
                if not result:
                    break
                delivery_guy_id = random.randint(1000, 9999)
            
            # insert new delivery guy into delivery_guy table
            query = f"INSERT INTO delivery_guy (id, name, password, phno) VALUES ({delivery_guy_id}, '{new_name}', '{new_password}', '{new_phno}')"
            cursor.execute(query)
            db.commit()
            dispatcher.utter_message(text="Successfully added a new delivery guy")
        else:
            dispatcher.utter_message(text="Sorry, I didn't understand what you want to add.")
        
        # disconnect from mysql database
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")
        
        return []


class ViewProductByCallsForRemoval(Action):

    def name(self) -> Text:
        return "action_view_product_by_calls_for_removal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        login = tracker.get_slot("f_login_type")
        if login != "1": 
              dispatcher.utter_message("Sorry, you do not have the privileges of adding/removing a admin or delivery guy. This feature is only available for the admin.")
              return []
        
        # Connect to MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get columns to be displayed from slot
        cols_str = tracker.slots.get("cols")
        cols = []
        for col in cols_str.split(","):
            if col.isnumeric() and 1 <= int(col) <= 4:
                cols.append(int(col))


        # Define the columns to display
        cols_dict = {   
            1: "p_name",
            2: "p_quantity",
            3: "p_rating",
            4: "p_description"
        }
        cols_to_display = ", ".join([cols_dict[col] for col in cols])

        # Fetch and display the products with the specified columns
        cursor.execute("SELECT p_id, {} FROM product".format(cols_to_display))
        products = cursor.fetchall()
        cols_to_display = []
        for col in cols:
            cols_to_display.append(cols_dict[col])
        for product in products:
            product_str = "Product ID: {}  ".format(product[0])
            for i in range(len(cols_to_display)):
                product_str += "{}: {}  ".format(cols_to_display[i], product[i+1])
            product_str+="\n"
            dispatcher.utter_message(product_str)

        # Disconnect from MySQL
        db.close()
        print("Disconnected from MySQL")

        return []




class DeleteProduct(Action):

    def name(self) -> Text:
        return "action_delete_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get product ID from slot
        product_id = tracker.slots.get("id", "")

        # Connect to MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Delete the product from the database
        delete_query = "DELETE FROM product WHERE p_id = %s"
        cursor.execute(delete_query, (product_id,))
        db.commit()

        # Confirm deletion to the user
        num_rows_deleted = cursor.rowcount
        if num_rows_deleted > 0:
            message = "Product with ID {} has been deleted.".format(product_id)
        else:
            message = "Product with ID {} was not found in the database.".format(product_id)
        dispatcher.utter_message(message)

        # Disconnect from MySQL
        db.close()
        print("Disconnected from MySQL")

        return []


class ViewProductByCallsForRemoval(Action):

    def name(self) -> Text:
        return "action_show_all_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
                
        # Connect to MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get columns to be displayed from slot
        cols_str = tracker.slots.get("cols")
        cols = []
        for col in cols_str.split(","):
            if col.isnumeric() and 1 <= int(col) <= 4:
                cols.append(int(col))

        # Define the columns to display
        cols_dict = {   
            1: "p_name",
            2: "p_quantity",
            3: "p_rating",
            4: "p_description"
        }
        cols_to_display = []
        for col in cols:
            cols_to_display.append(cols_dict[col])

        # Check if there are columns to display
        if cols_to_display:
            # Fetch and display the products with the specified columns
            cursor.execute("SELECT p_id, {} FROM product".format(", ".join(cols_to_display)))
            products = cursor.fetchall()
            
        else:
            print("No columns specified to display.")
            dispatcher.utter_message("No columns specified to display")
            return[]
        
        for product in products:
            product_str = "Product ID: {}  ".format(product[0])
            for i in range(len(cols_to_display)):
                product_str += "{}: {}  ".format(cols_to_display[i], product[i+1])
            product_str+="\n"
            dispatcher.utter_message(product_str)

        # Disconnect from MySQL
        db.close()
        print("Disconnected from MySQL")

        return []




class ActionSearchProducts(Action):

    def name(self) -> Text:
        return "action_search_products"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get values from slots
        choice = tracker.get_slot("choice")
        value = tracker.get_slot("value")
        value= value.lower()
        # Connect to MySQL
    
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")
        f=0
        results = []

        if choice == "1":
            # Search by name
            cursor.execute("SELECT p_name FROM product")
            results = cursor.fetchall()
            if results:
                names = [result[0] for result in results]
                close_matches = get_close_matches(value, names)
                if close_matches:
                    cursor.execute("SELECT * FROM product WHERE p_name IN (%s)" % ','.join(['%s']*len(close_matches)), close_matches)                   
                    results = cursor.fetchall()
                    f=1
                    response = "Here are the closest matches for name '{}' in our database:\n{}".format(value, "\n".join(close_matches))
                else:
                    response = "Sorry, no products were found with a name similar to '{}'.".format(value)
            else:
                response = "Sorry, no products were found."

        elif choice == "2":
            # Search by price
            cursor.execute("SELECT p_price FROM product")
            results = cursor.fetchall()
            if results:
                prices = [str(result[0]) for result in results]
                close_matches = get_close_matches(value, prices)
                if close_matches:
                    cursor.execute("SELECT * FROM product WHERE p_price IN (%s)" % ','.join(['%s']*len(close_matches)), close_matches)
                    results=cursor.fetchall()
                    f=1
                    response = "Here are the closest matches for price '{}' in our database:\n{}".format(value, "\n".join(close_matches))
                else:
                    response = "Sorry, no products were found with a price of {}.".format(value)
            else:
                response = "Sorry, no products were found."

        elif choice == "3":
            # Search by rating
            cursor.execute("SELECT p_rating FROM product")
            results = cursor.fetchall()
            if results:
                ratings = [str(result[0]) for result in results]
                close_matches = get_close_matches(value, ratings)
                if close_matches:
                    cursor.execute("SELECT * FROM product WHERE p_rating IN (%s)" % ','.join(['%s']*len(close_matches)), close_matches)
                    results=cursor.fetchall()
                    f=1
                    response = "Here are the closest matches for rating '{}' in our database:\n{}".format(value, "\n".join(close_matches))
                else:
                    response = "Sorry, no products were found with a rating of {}.".format(value)
            else:
                response = "Sorry, no products were found."

        else:
            response = "Sorry, I didn't understand your search criteria. Please try again."

        dispatcher.utter_message(text=response)
        # Iterate over results and add image URLs to the response
        if results and f==1:
            for result in results:
                p_id = result[0]
                p_name = result[1]
                p_quantity = result[2]
                p_rating = result[3]
                p_description = result[4]
                p_price = result[5]
                cursor.execute("SELECT * FROM product_images WHERE p_id = %s", (p_id,))
                image_results = cursor.fetchall()
                image_links = []
                response = "\n\nProduct Name: {}\nPrice: ${}\nRating: {}\nDescription: {}\nquantity: {}\n".format(p_name, p_price, p_rating, p_description, p_quantity)
                dispatcher.utter_message(text=response)
                for image_result in image_results:
                    image_link = image_result[1]
                    image_links.append(image_link)
                    dispatcher.utter_image_url(image_link)

        

        # Close the database connection
        db.close()
        print("Disconnected from MySQL")

        return []




class ActionPlaceOrder(Action):
    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Retrieve slots
        login_type = tracker.get_slot("f_login_type")
        phno = tracker.get_slot("f_login_phno")
        password = tracker.get_slot("f_login_password")
        orders_str = tracker.get_slot("order")
        print(phno, password,orders_str)
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        mycursor = mydb.cursor()
        print("connected to mysql")
        # Check login type
        if login_type != "2":
            dispatcher.utter_message(text="Please login as customer to place order.")
            return []
        
        # Retrieve customer info from database
        mycursor.execute("SELECT c_id, c_address, c_city_name FROM customer WHERE c_phno = %s AND c_password = %s", (phno, password))
        customer = mycursor.fetchone()
        
        if not customer:
            dispatcher.utter_message(text="Incorrect phone number or password for customer have you logged in correctly. Please try again.")
            return []
        
        c_id, address, city_name = customer
        
        # Parse order string  orders =" maza:2,pepsi:3,7up:4" ex orders string
        orders = {}
        for order_str in orders_str.split(","):
            order_parts = order_str.split(":")
            p_name = order_parts[0].strip().lower()
            quantity = int(order_parts[1].strip())
            orders[p_name] = quantity
        
        # check o_id
        while True:
            o_id = random.randint(1, 1000)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM orders WHERE o_id = %s", (o_id,))
            result = mycursor.fetchone()
            if result is None:
                break

        # Check product availability and update order details
        total_cost = 0
        mycursor.execute("INSERT INTO orders (o_id, o_status, o_cost, o_date, o_city_name, o_address, o_c_id) VALUES (%s, 'Pending', %s, NOW(), %s, %s, %s)", (o_id, total_cost, city_name, address, c_id))
        for p_name, quantity in orders.items():
            mycursor.execute("SELECT p_id, p_price, p_quantity FROM product WHERE LOWER(p_name) = %s", (p_name,))
            product = mycursor.fetchone()
            
            if not product or product[2] < quantity:
                dispatcher.utter_message(text=f"Sorry, {p_name} is out of stock or not available in sufficient quantity.")
                return []
            
            p_id, p_price, p_quantity = product
            
            # Update product quantity
            mycursor.execute("UPDATE product SET p_quantity = %s WHERE p_id = %s", (p_quantity - quantity, p_id))

            # Calculate cost and add to order details
            cost = p_price * quantity
            total_cost += cost
            # Add order to database
            mycursor.execute("INSERT INTO orders_detail (o_id, p_id, quantity) VALUES (%s, %s, %s)", (o_id, p_id, quantity))
            
        mycursor.execute("UPDATE orders SET o_cost = %s WHERE o_id = %s", (total_cost, o_id))
        o_id = mycursor.lastrowid
        
        mydb.commit()
        
        dispatcher.utter_message(text=f"Your order with order id {o_id} has been placed. Total cost is Rs {total_cost} .It will be delivered within 2-3 working days. Please pay the total cost to delivery person.")
        dispatcher.utter_image_url("./robot_pics/modern-robot-with-shipping-boxes.png")
        mydb.close()
        print("Disconnected from MySQL")
        
        return []




class ActionShowRecentOrders(Action):
    def name(self) -> Text:
        return "action_show_my_orders"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # get values from slots f_login_type, f_login_phno, f_login_password
        login_type = tracker.get_slot("f_login_type")
        login_phno = tracker.get_slot("f_login_phno")
        login_password = tracker.get_slot("f_login_password")

        # check if the user is logged in as customer
        if login_type != "2":
            dispatcher.utter_message(text="Please login as a customer to view orders.")
            return []
        
        # connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # find the id of the customer using f_login_phno, f_login_password values
        cursor.execute("SELECT c_id FROM customer WHERE c_phno = %s AND c_password = %s", (login_phno, login_password))
        result = cursor.fetchone()

        if result is None:
            dispatcher.utter_message(text="Invalid login credentials.")
        else:
            # find the orders made by the customer from table orders, orders_detail
            c_id = result[0]
            cursor.execute("SELECT o_id, p_id, quantity FROM orders_detail WHERE o_id IN (SELECT o_id FROM orders WHERE o_c_id = %s)", (c_id,))
            results = cursor.fetchall()

            # utter the details of the recent orders made by the customer
            if len(results) > 0:
                message = "Here are your orders:\n"
                for row in results:
                    o_id = row[0]
                    p_id = row[1]
                    quantity = row[2]

                    # get the product name from table product
                    cursor.execute("SELECT p_name FROM product WHERE p_id = %s", (p_id,))
                    result = cursor.fetchone()
                    p_name = result[0]

                    # get the order date from table orders
                    cursor.execute("SELECT o_date FROM orders WHERE o_id = %s", (o_id,))
                    result = cursor.fetchone()
                    o_date = result[0]

                    message += f"- Order ID: {o_id}, Product ID: {p_id}, Product Name: {p_name}, Quantity: {quantity}, Order Date: {o_date}\n"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message(text="You have not made any orders yet.")

        # disconnect from MySQL database
        db.close()
        print("Disconnected from MySQL database")
        
        return []        



class ActionShowFeedbackProducts(Action):
    
    def name(self) -> Text:
        return "action_show_feedback_products"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # fetch user information from slots
        login_type = tracker.get_slot('f_login_type')
        login_phno = tracker.get_slot('f_login_phno')
        login_password = tracker.get_slot('f_login_password')
        
        # check if user is a customer
        if login_type != "2":
            dispatcher.utter_message("Please log in as a customer to give feedback.")
            return []
        
        # connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        # create cursor to execute queries
        cursor = db.cursor()
        print("Connected to MySQL database")

                
        # fetch customer id from database
        cursor.execute("SELECT c_id FROM customer WHERE c_phno=%s AND c_password=%s", (login_phno, login_password))
        result = cursor.fetchone()
        if result is None:
            dispatcher.utter_message("No customer found with the given phone number and password.")
            db.close()
            return []
        
        # fetch list of product ids and names purchased by customer
        cursor.execute("SELECT p.p_id, p.p_name FROM orders_detail od JOIN orders o ON od.o_id=o.o_id JOIN product p ON od.p_id=p.p_id WHERE o.o_c_id=%s", (result[0],))
        results = cursor.fetchall()
        
        # check if customer has made any purchases
        if len(results) == 0:
            dispatcher.utter_message("You have not purchased any products yet.")
        else:
            # display the list of purchased products
            message = "You have purchased the following products:\n"
            for r in results:
                message += f"Product ID: {r[0]}, Product Name: {r[1]}\n"
            dispatcher.utter_message(message)
        
        # disconnect from the MySQL database
        db.close()
        print("Disconnected from MySQL database")
        return []



class ActionShowRecentOrders(Action):

    def name(self) -> Text:
        return "action_feedback_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         # check if user is a customer
        login_type = tracker.get_slot("f_login_type")
        if login_type != "2":
            dispatcher.utter_message("Please login as a customer to give feedback")
            return []
        
        # connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # get values from slots
        login_phno = tracker.get_slot("f_login_phno")
        login_password = tracker.get_slot("f_login_password")
        p_ids = tracker.get_slot("p_ids")
        f_content = tracker.get_slot("f_content")
        f_p_rating = tracker.get_slot("f_p_rating")

        # get customer id using phone number and password
        cursor.execute("SELECT c_id FROM customer WHERE c_phno=%s AND c_password=%s", (login_phno, login_password))
        result = cursor.fetchone()
        if result is None:
            dispatcher.utter_message("Invalid phone number or password")
            return []
        c_id = result[0]

        # check if products were actually ordered by customer
        p_id_list = [int(p_id.strip()) for p_id in p_ids.split(",")]
        for p_id in p_id_list:
            cursor.execute("SELECT o_id FROM orders_detail WHERE o_id IN (SELECT o_id FROM orders WHERE o_c_id=%s) AND p_id=%s", (c_id, p_id))
            result = cursor.fetchone()
            if result is None:
                dispatcher.utter_message("Product with ID {} was not ordered by you".format(p_id))
                return []

        # insert feedback for products
        content_list = f_content.split(",")
        rating_list = [float(rating.strip()) for rating in f_p_rating.split(",")]
        for i in range(len(p_id_list)):
            cursor.execute("INSERT INTO feedback (f_content, f_p_rating, p_id, c_id) VALUES (%s, %s, %s, %s)",
                            (content_list[i], rating_list[i], p_id_list[i], c_id))
        db.commit()

        dispatcher.utter_message("Feedback submitted successfully")
        
        # disconnect from MySQL database
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")

        return []




class ActionShowFeedbacks(Action):
    def name(self) -> Text:
        return "action_show_all_feedbacks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get values from slots
        f_login_type = tracker.slots.get("f_login_type")

        # Check if the user is authorized to view feedbacks
        if f_login_type not in ["1", "2"]:
            dispatcher.utter_message(text="Only admins or customers can view feedbacks.")
            return []

        # Retrieve feedbacks for each product
        cursor.execute("SELECT p_id, p_name FROM product")
        products = cursor.fetchall()
        for product in products:
            p_id = product[0]
            p_name = product[1]

            cursor.execute("SELECT f_content, f_p_rating FROM feedback WHERE p_id = %s", (p_id,))
            feedbacks = cursor.fetchall()
            if feedbacks:
                feedback_text = "\n".join([f"Feedback: {f[0]}, Rating: {f[1]}" for f in feedbacks])
                dispatcher.utter_message(text=f"Product: id_{p_id}, name_{p_name}\n{feedback_text}")
            else:
                dispatcher.utter_message(text=f"No feedbacks for product: id_{p_id}, name_{p_name}")
        
        # Disconnect from MySQL database
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")
        return []



class ActionShowFeedbacks(Action):
    def name(self) -> Text:
        return "action_show_select_feedbacks"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get values from slots
        f_login_type = tracker.slots.get("f_login_type")

        # Check if the user is authorized to view feedbacks
        if f_login_type not in ["1", "2"]:
            dispatcher.utter_message(text="Only admins or customers can view feedbacks.")
            return []
        
        # get product name from slot 
        product_name= tracker.get_slot("f_p_name")

        # get closest product names from the database
        cursor.execute("SELECT p_name FROM product")
        results=cursor.fetchall()
        names = [result[0] for result in results]
        close_matches = get_close_matches(product_name.lower(), names)

        if not close_matches:
           response = "Sorry, no products were found with a name similar to '{}'.".format(product_name)
           dispatcher.utter_message(text=response)
           return []
        
        dispatcher.utter_message(text="Here are the feedbacks associated with the closest product names to your input")
        
        # get product ids of the closest product names
        p_ids = []  
        for name in close_matches:          
            cursor.execute("SELECT p_id FROM product WHERE p_name=%s", (name,))
            result = cursor.fetchone()
            p_ids.append(result[0])
        
        # print feedbacks for each product in p_ids
        for id in p_ids:
            cursor.execute("SELECT f_content, f_p_rating FROM feedback WHERE p_id=%s", (id,))
            feedbacks = cursor.fetchall()
            if feedbacks:
                feedback_text = "\n".join([f"Feedback: {f[0]}, Rating: {f[1]}" for f in feedbacks])
                dispatcher.utter_message(text=f"Product: id_{id}, name_{name}\n{feedback_text}")
            else:
                dispatcher.utter_message(text=f"No feedbacks for product: id_{id}, name_{name}")
    
        # Disconnect from MySQL database
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")
        return []
    


class ActionShowOrders(Action):
    
    def name(self) -> Text:
        return "action_show_orders"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get values from slots
        f_login_type = tracker.get_slot("f_login_type")
        o_choice = tracker.get_slot("o_choice")

        # Check if login type is admin or delivery_guy
        if f_login_type not in ["1", "3"]:
            dispatcher.utter_message(text="Only admin or delivery guy can view orders")
            return []

        # Check user's choice and retrieve orders accordingly
        if o_choice == "1":
            cursor.execute("""
                SELECT orders.o_id, orders.o_status, orders.o_date, orders.o_cost,
                GROUP_CONCAT(CONCAT(product.p_id, ' : ', product.p_name, ' : ', orders_detail.quantity) SEPARATOR '\n') AS products,
                orders.o_address
                FROM orders
                JOIN orders_detail ON orders.o_id = orders_detail.o_id
                JOIN product ON orders_detail.p_id = product.p_id
                GROUP BY orders.o_id
                ORDER BY orders.o_date DESC
            """)
            orders = cursor.fetchall()

            if not orders:
                dispatcher.utter_message(text="No orders found")
                return []

            # Format orders into a message
            message = "Here are all orders ever made:\n"
            for order in orders:
                message += f"Order ID: {order[0]}, Status: {order[1]}, Date: {order[2]}, Cost: {order[3]}\n"
                message += "Product_id : Product_name : Quantity\n"
                message += f"{order[4]}\n"
                message += f"Address: {order[5]}\n\n"
            dispatcher.utter_message(text=message)

        elif o_choice == "2":
            cursor.execute("""
                SELECT orders.o_id, orders.o_status, orders.o_date, orders.o_cost,
                GROUP_CONCAT(CONCAT(product.p_id, ' : ', product.p_name, ' : ', orders_detail.quantity) SEPARATOR '\n') AS products,
                orders.o_address
                FROM orders
                JOIN orders_detail ON orders.o_id = orders_detail.o_id
                JOIN product ON orders_detail.p_id = product.p_id
                WHERE orders.o_status = 'Pending'
                GROUP BY orders.o_id
                ORDER BY orders.o_date DESC
            """)
            orders = cursor.fetchall()

            if not orders:
                dispatcher.utter_message(text="No pending orders found")
                return []

            # Format pending orders into a message
            message = "Here are all pending orders:\n"
            for order in orders:
                message += f"Order ID: {order[0]}, Status: {order[1]}, Date: {order[2]}, Cost: {order[3]}\n"
                message += "Product_id : Product_name : Quantity\n"
                message += f"{order[4]}\n"
                message += f"Address: {order[5]}\n\n"
            dispatcher.utter_message(text=message)

        elif o_choice == "3":
            cursor.execute("""
                SELECT orders.o_id, orders.o_status, orders.o_date, orders.o_cost,
                GROUP_CONCAT(CONCAT(product.p_id, ' : ', product.p_name, ' : ', orders_detail.quantity) SEPARATOR '\n') AS products,
                orders.o_address
                FROM orders
                JOIN orders_detail ON orders.o_id = orders_detail.o_id
                JOIN product ON orders_detail.p_id = product.p_id
                WHERE orders.o_status = 'Completed'
                GROUP BY orders.o_id
                ORDER BY orders.o_date DESC
            """)
            orders = cursor.fetchall()

            if not orders:
                dispatcher.utter_message(text="No pending orders found")
                return []

            # Format pending orders into a message
            message = "Here are all pending orders:\n"
            for order in orders:
                message += f"Order ID: {order[0]}, Status: {order[1]}, Date: {order[2]}, Cost: {order[3]}\n"
                message += "Product_id : Product_name : Quantity\n"
                message += f"{order[4]}\n"
                message += f"Address: {order[5]}\n\n"
            dispatcher.utter_message(text=message)

            
        else:
          dispatcher.utter_message("Please enter a valid choice.\n")
            
        # Disconnect from MySQL database
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")
        return []


class ActionUpdateOrderStatus(Action):

    def name(self) -> Text:
        return "action_update_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get values from slots
        f_login_type = tracker.get_slot("f_login_type")
        o_ids = tracker.get_slot("o_ids")
 
        # Check if user is delivery guy or customer
        if f_login_type not in ["3"]:
            dispatcher.utter_message(text="Only delivery guy can update order status")
            return []

        # Separate all ids from o_ids
        ids = o_ids.split(",")
        ids = [int(id) for id in ids]
        

        # Update order status from pending to completed for each id
        for id in ids:
            sql = "UPDATE orders SET o_status='Completed' WHERE o_id=%s AND o_status='Pending'"
            val = (id,)
            cursor.execute(sql, val)
            db.commit()
            if cursor.rowcount > 0:
                dispatcher.utter_message(text=f"Order {id} status updated to Completed")
            else:
                dispatcher.utter_message(text=f"Order {id} not found or already completed")

        # Close database connection
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")
        
        return []




class ActionUpdateProductQuantity(Action):

    def name(self) -> Text:
        return "action_update_product_quantity"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")

        # Get values from slots
        f_login_type = tracker.get_slot("f_login_type")
        p_id_quantity = tracker.get_slot("p_id_quantity")
        print(p_id_quantity)

        # Check if user is admin
        if f_login_type != "1":
            dispatcher.utter_message(text="Only admin can increase product quantities")
            return []

        # Check if id_q is provided and is in the correct format
        if not p_id_quantity or ":" not in p_id_quantity:
            dispatcher.utter_message(text="Please provide the product id and quantity in the correct format")
            return []

        # Split id_q into a dictionary of id-quantity pairs
        id_quantities = {}
        for id_quantity in p_id_quantity.split(","):
            if ":" in id_quantity:
                id, quantity = id_quantity.split(":")
                id_quantities[id] = quantity

        # Check if all products should be updated
        if "all" in id_quantities.keys():
            new_quantity = int(id_quantities["all"])
            print("here")
            cursor.execute("UPDATE product SET p_quantity = p_quantity + %s", (new_quantity,))
            db.commit()
            dispatcher.utter_message(text=f"All products quantities increased by {new_quantity}")
            return []


        # Update quantities of individual products
        for id, quantity in id_quantities.items():
            cursor.execute("SELECT * FROM product WHERE p_id = %s", (id,))
            product = cursor.fetchone()
            if not product:
                dispatcher.utter_message(text=f"Product with id {id} not found")
            else:
                current_quantity = product[2]
                new_quantity = current_quantity + int(quantity)
                cursor.execute("UPDATE product SET p_quantity = %s WHERE p_id = %s", (new_quantity, id))
                db.commit()
                dispatcher.utter_message(text=f"Product with id {id} updated with new quantity {new_quantity}")

        # Close database connection
        cursor.close()
        db.close()
        print("Disconnected from MySQL database")

        return []





class ActionUpdateGraphs(Action):
    
    def name(self) -> Text:
        return "action_update_graphs"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Connect to MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysql_password,
            database="myrasabot"
        )
        cursor = db.cursor()
        print("Connected to MySQL database")
        
        # Retrieve product names and feedback ratings
        cursor.execute("SELECT p.p_name, AVG(f.f_p_rating) FROM product p LEFT JOIN feedback f ON p.p_id = f.p_id GROUP BY p.p_name")
        f1results = cursor.fetchall()
        if not f1results:
            dispatcher.utter_message(text="No data found!")
            return []
        
        # Plot graph and save image
        product_names = [result[0] for result in f1results]
        avg_ratings = [result[1] if result[1] is not None else 0 for result in f1results]

        plt.figure(figsize=(10,5))
        plt.bar(product_names, avg_ratings,color='blue')
        plt.title('Average Feedback Ratings by Product')
        plt.xlabel('Product')
        plt.ylabel('Average Feedback Rating')
        plt.savefig("./my_rasa_bot_front_end/view_graphical_stats/graphs_images/product_feedback_graph.png")
        plt.close()

        
        # Fetch product names and their order details
        cursor.execute("SELECT p_name, COALESCE(SUM(quantity), 0) FROM product LEFT JOIN orders_detail ON product.p_id = orders_detail.p_id GROUP BY p_name")
        data = cursor.fetchall()

        if not data:
            dispatcher.utter_message(text="No data found!")
            return []

        # Create bar graph
        product_names = [x[0] for x in data]
        orders = [x[1] for x in data]

        plt.bar(product_names, orders, color='blue')
        plt.title("Number of orders for each product")
        plt.xlabel("Product Name")
        plt.ylabel("Number of Orders")

        # Save the graph image
        graph_path = "./my_rasa_bot_front_end/view_graphical_stats/graphs_images/product_no_of_orders.png"
        plt.savefig(graph_path)
        plt.close()


        # Get the number of orders per month
        cursor.execute("SELECT MONTH(o_date) as month, COUNT(*) as num_orders FROM orders GROUP BY MONTH(o_date)")
        f2results = cursor.fetchall()
        if not f2results:
            dispatcher.utter_message(text="No data found!")
            return []

        # Extract the month and number of orders data from the results
        months = [result[0] for result in f2results]
        num_orders = [result[1] for result in f2results]
        # Define the month names
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Set the x-tick labels to be the month names
        plt.xticks(range(1, 13), month_names)

        # Set y-axis ticks to integer values
        plt.yticks(np.arange(min(num_orders), max(num_orders)+1, 1.0))
        # Draw the bar graph
        plt.title('Number of Orders per Month')
        plt.xlabel('Month')
        plt.ylabel('Number of Orders')
        plt.plot(months, num_orders, color='blue',marker='o')

        # Save the graph to a file
        plt.savefig('./my_rasa_bot_front_end/view_graphical_stats/graphs_images/orders_month.png')
        plt.close()


         # Get the total cost of orders per month
        cursor.execute("SELECT MONTH(o_date) as month, SUM(o_cost) as total_cost FROM orders GROUP BY MONTH(o_date)")
        f3results = cursor.fetchall()
        if not f3results:
            dispatcher.utter_message(text="No data found!")
            return []
        
        # Extract the month and total cost data from the results
        months = [result[0] for result in f3results]
        total_cost = [result[1] for result in f3results]
        cumulative_cost = np.cumsum(total_cost)

        # Draw the bar graph
        plt.title('Total Cost of Orders per Month')
        plt.xlabel('Month')
        plt.ylabel('Total Cost of Orders')
        
        plt.xticks(range(1, 13), month_names)

        plt.plot(months, cumulative_cost, color='blue', marker='o')

        # Save the graph to a file
        plt.savefig('./my_rasa_bot_front_end/view_graphical_stats/graphs_images/orders_month_cost.png')
        plt.close()

        dispatcher.utter_message(text="graphs have been updated. kindly refresh the page.")
        # Disconnect from MySQL database
        db.disconnect()
        print("Disconnected from MySQL database")
        
        return []




class ActionExecuteCustomMysqlQuery(Action):
    def name(self) -> Text:
        return "action_execute_custom_mysql_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Get the entity value at `mysql`
        mysql_value =  tracker.get_slot('mysql_cmd')
        print(mysql_value)
        

        # Check the value of the `mysql` slot
        if mysql_value.lower() == "help":
            # Display the help message
            message = "Welcome! In this terminal interface, you can execute any SQL query. "
            message += "Type 'initialize' to initialize the database at MySQL to its previous value. "
            message += "Type 'help' to get help."
            dispatcher.utter_message(text=message)
            print(message)
            return []
        elif mysql_value.lower() == "initialize":
            # Trigger the follow-up action `action_initialize_mysql`
            return [FollowupAction("action_initialize_mysql")]

        # Connect to MySQL database
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password=mysql_password,
                database="myrasabot"
            )
            cursor = db.cursor()
            print("Connected to MySQL database")
        except Error as e:
            dispatcher.utter_message(text=f"Error connecting to MySQL database: {e}")
            print("Error connecting to MySQL database: {e}")
            return []

        # Execute MySQL query
        try:
            cursor.execute(mysql_value)
            result = cursor.fetchall()

            # Display the result in a tabular format
            if len(result) > 0:
                headers = []
                for i in cursor.description:
                     headers.append(i[0])
                 
                
                rows = [list(row) for row in result]
                
                        
                message = "Here is the result of your query:\n"
                #message += tabulate(rows, headers=headers, tablefmt="fancy_grid")
                message+='['
                for s in headers :
                    message+=str(s)+'$'
                message+=']'
                
                for row in rows:
                    message+='['
                    for ele in row:
                     message+=str(ele)+'$'
                    message+="]"
                     
                message=message.replace("'","")
                dispatcher.utter_message(text=message)
            else:
                message = "done."
            dispatcher.utter_message(text=message)
            print(message)
        except Error as e:
            # Display the error message
            dispatcher.utter_message(text=f"MySQL Error: {e.msg}")
        finally:
            # Close the database connection
            db.commit()
            if db.is_connected():
                cursor.close()
                db.close()
                print("Disconnected from MySQL database")

        return []


class ActionExecuteCustomMysqlQuery(Action):
    def name(self) -> Text:
        return "action_initialize_mysql"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="mysql database has been initialized to its default value.")
        # Connect to MySQL database
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=mysql_password,
                database="myrasabot"
            )
            
            print("Connected to MySQL database")
        except Error as e:
            dispatcher.utter_message(text=f"Error connecting to MySQL database: {e}")
            print("Error connecting to MySQL database: {e}")
            return []
         # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        try:
            # Read SQL commands from the file
            with open("final_sql_cmds.sql", "r") as file:
                sql_commands = file.read().split(";")

            # Execute each SQL command
            for command in sql_commands:
                command = command.strip()
                if command:
                    cursor.execute(command)

            # Commit the changes to the database
            connection.commit()

            dispatcher.utter_message(text="MySQL database has been initialized with the SQL commands from 'final_sql_cmds.sql'.")

        except FileNotFoundError:
            dispatcher.utter_message(text="File 'final_sql_cmds.sql' not found.")

        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while executing the SQL commands: {str(e)}")

        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()

        return []