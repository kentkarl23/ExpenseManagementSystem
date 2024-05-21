import xml.etree.ElementTree as ET
import hashlib

def create_users_xml():
    root = ET.Element("users")
    tree = ET.ElementTree(root)
    tree.write("users.xml")

def create_transactions_xml():
    root = ET.Element("transactions")
    tree = ET.ElementTree(root)
    tree.write("transactions.xml")

def read_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return root

def add_user_to_xml(user):
    root = read_xml('users.xml')
    user_element = ET.SubElement(root, "user")
    for key, value in user.items():
        child = ET.SubElement(user_element, key)
        child.text = str(value)
    save_xml('users.xml', root)

def add_transaction_to_xml(xml_data, transaction, transaction_hash):
    """
    Add a transaction to the XML data.
    """
    transaction_element = ET.Element("transaction")

    # Add keys and values from the transaction dictionary to the XML element
    for key, value in transaction.items():
        if key != 'id':
            child = ET.Element(key)
            child.text = str(value)
            transaction_element.append(child)

    # Add the transaction hash as an attribute
    transaction_element.set('hash', transaction_hash)

    # Add the transaction element to the XML data
    xml_data.append(transaction_element)

def save_xml(filename, root):
    tree = ET.ElementTree(root)
    tree.write(filename)

def read_users_from_xml():
    try:
        tree = ET.parse('users.xml')
        root = tree.getroot()
        users = []
        for user_elem in root.findall('user'):
            user = {}
            for child in user_elem:
                user[child.tag] = child.text
            users.append(user)
        return users
    except FileNotFoundError:
        print("Error: users.xml file not found.")
        return []

def read_transactions_from_xml():
    try:
        tree = ET.parse('transactions.xml')
        root = tree.getroot()
        transactions = []
        for transaction_elem in root.findall('transaction'):
            transaction = {}
            for child in transaction_elem:
                transaction[child.tag] = child.text
            transactions.append(transaction)
        return transactions
    except FileNotFoundError:
        print("Error: transactions.xml file not found.")
        return []

def generate_transaction_hash(description, amount, date):
    """
    Generate a unique hash for a transaction based on its description, amount, and date.
    """
    transaction_data = f"{description}{amount}{date}"
    return hashlib.sha256(transaction_data.encode()).hexdigest()
    
# In xml_utils.py
class XMLUser:
    # class definition remains the same:
    def __init__(self, id, email, password, first_name):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name

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

# Existing code...

def read_transactions_from_xml():
    try:
        tree = ET.parse('transactions.xml')
        root = tree.getroot()
        transactions = []
        for transaction in root.findall('transaction'):
            transaction_data = {}
            for elem in transaction:
                transaction_data[elem.tag] = elem.text
            transactions.append(transaction_data)
        return transactions
    except FileNotFoundError:
        print("Error: transactions.xml file not found.")
        return None               