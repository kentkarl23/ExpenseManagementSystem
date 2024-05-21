import xml.etree.ElementTree as ET
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password, first_name):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name

    @staticmethod
    def get_by_id(user_id):
        # Load users from the XML file
        users_tree = ET.parse('users.xml')
        root = users_tree.getroot()

        # Search for the user with the given ID
        for user_elem in root.findall('user'):
            if user_elem.attrib['id'] == str(user_id):
                # Extract user data from XML
                email = user_elem.find('email').text
                password = user_elem.find('password').text
                first_name = user_elem.find('first_name').text
                # Return a User object
                return User(user_id, email, password, first_name)

        # Return None if user not found
        return None

    @staticmethod
    def get_by_email(email):
        # Load users from the XML file
        users_tree = ET.parse('users.xml')
        root = users_tree.getroot()

        # Search for the user with the given email
        for user_elem in root.findall('user'):
            if user_elem.find('email').text == email:
                # Extract user data from XML
                user_id = user_elem.attrib['id']
                password = user_elem.find('password').text
                first_name = user_elem.find('first_name').text
                # Return a User object
                return User(user_id, email, password, first_name)

        # Return None if user not found
        return None

    def is_active(self):
        return True  # Adjust based on your application's logic

    def save_to_xml(self):
        # Load users from the XML file
        users_tree = ET.parse('users.xml')
        root = users_tree.getroot()

        # Create a new user element
        user_elem = ET.Element("user", id=str(self.id))

        # Add user data as sub-elements
        email_elem = ET.SubElement(user_elem, "email")
        email_elem.text = self.email

        password_elem = ET.SubElement(user_elem, "password")
        password_elem.text = self.password

        first_name_elem = ET.SubElement(user_elem, "first_name")
        first_name_elem.text = self.first_name

        # Append the new user element to the root
        root.append(user_elem)

        # Write the updated XML back to the file
        users_tree.write('users.xml')

class Expense:
    def __init__(self, id, amount, description, category, date, user_id):
        self.id = id
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date
        self.user_id = user_id


class Income:
    def __init__(self, id, amount, description, category, date, user_id):
        self.id = id
        self.amount = amount
        self.description = description
        self.category = category
        self.date = date
        self.user_id = user_id