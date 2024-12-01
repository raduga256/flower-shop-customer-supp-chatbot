"""
        # Creating Tools for the Lanngraph ###
        
        the LLM will be creating their own queries but while generating response,
        
        The LLM will have to base on the tools sometimes to answer the queries.
        
        we will use these tools to fetch data from our knowledge base.
        
    """

# Importing required libraries
from langchain_core.tools import tool
from typing import List, Dict
from vector_store import FlowerShopVectorStore 


# Instantiate VectorStore
vector_store = FlowerShopVectorStore()    

# DATABASE Access for Customer Details processes
customers_database = [
    {"name": "John Doe", "postcode": "SW1A 1AA", "dob": "1990-01-01", "customer_id": "CUST001", "first_line_address": "123 Main St", "phone_number": "07712345678", "email": "john.doe@example.com"},
    {"name": "Jane Smith", "postcode": "E1 6AN", "dob": "1985-05-15", "customer_id": "CUST002", "first_line_address": "456 High St", "phone_number": "07723456789", "email": "jane.smith@example.com"},
    {"name": "Alice Johnson", "postcode": "W1D 3QE", "dob": "1992-07-24", "customer_id": "CUST003", "first_line_address": "789 Elm St", "phone_number": "07734567890", "email": "alice.johnson@example.com"},
    {"name": "Bob Brown", "postcode": "M1 2AB", "dob": "1988-11-11", "customer_id": "CUST004", "first_line_address": "101 Oak St", "phone_number": "07745678901", "email": "bob.brown@example.com"},
    {"name": "Clara Green", "postcode": "B1 1TT", "dob": "1975-03-08", "customer_id": "CUST005", "first_line_address": "202 Pine St", "phone_number": "07756789012", "email": "clara.green@example.com"},
    {"name": "David Wilson", "postcode": "EC1A 1BB", "dob": "1983-06-20", "customer_id": "CUST006", "first_line_address": "303 Maple St", "phone_number": "07767890123", "email": "david.wilson@example.com"},
    {"name": "Emma White", "postcode": "SE1 2AA", "dob": "1995-09-13", "customer_id": "CUST007", "first_line_address": "404 Cedar St", "phone_number": "07778901234", "email": "emma.white@example.com"},
    {"name": "Frank Harris", "postcode": "N1 3ED", "dob": "1982-02-02", "customer_id": "CUST008", "first_line_address": "505 Birch St", "phone_number": "07789012345", "email": "frank.harris@example.com"},
    {"name": "Grace King", "postcode": "LS1 4BA", "dob": "1998-12-25", "customer_id": "CUST009", "first_line_address": "606 Fir St", "phone_number": "07790123456", "email": "grace.king@example.com"},
    {"name": "Henry Lee", "postcode": "EH1 3AT", "dob": "1979-08-15", "customer_id": "CUST010", "first_line_address": "707 Willow St", "phone_number": "07701234567", "email": "henry.lee@example.com"},

]

# store all the data protection checks so that we store user_input text and check against out Database
data_protection_checks = []


# Two Tools are created to check if 1. It's an exting customer , 2. If its a New customer, create.

@tool
def data_protection_check(name: str, postcode: str, year_of_birth: int, month_of_birth: int, day_of_birth: int) -> Dict:
    """
    Perform a data protection check against a customer to retrieve customer details.

    Args:
        name (str): Customer first and last name
        postcode (str): Customer registered address
        year_of_birth (int): The year the customer was born
        month_of_birth (int): The month the customer was born
        day_of_birth (int): The day the customer was born

    Returns:
        Dict: Customer details (name, postcode, dob, customer_id, first_line_address, email)
    """
    
    # validate customer details against the DB data protection safety
    for customer in customers_database:
        if (customer['name'].lower() == name.lower() and
            customer['postcode'].lower() == postcode.lower() and
            int(customer['dob'][0:4]) == year_of_birth and
            int(customer["dob"][5:7]) == month_of_birth and
            int(customer["dob"][8:10]) == day_of_birth):
            return f"DPA check passed - Retrieved customer details:\n{customer}"
    # store checks infor
    data_protection_checks.append(
        {
            'name': name,
            'postcode': postcode,
            'year_of_birth': year_of_birth,
            'month_of_birth': month_of_birth,
            'day_of_birth': day_of_birth
        }
    )
    
    # otherwise return check failed
    return "DPA check failed, no customer with these details found" 

@tool
def create_new_customer(first_name: str, surname: str, year_of_birth: int, month_of_birth: int, day_of_birth: int, postcode: str, first_line_of_address: str, phone_number: str, email: str) -> str:
    """
    Creates a customer profile, so that they can place orders.

    Args:
        first_name (str): Customers first name
        surname (str): Customers surname
        year_of_birth (int): Year customer was born
        month_of_birth (int): Month customer was born
        day_of_birth (int): Day customer was born
        postcode (str): Customer's postcode
        first_line_address (str): Customer's first line of address
        phone_number (str): Customer's phone number
        email (str): Customer's email address

    Returns:
        str: Confirmation that the profile has been created or any issues with the inputs
    """
    if len(phone_number) != 11:     # validate phone number
        return "Phone number must be 11 digits"
    
    # Add customer Details to the Database
    customer_id = len(customers_database) + 1
    customers_database.append({
        'name': first_name + ' ' + surname,
        'dob': f'{year_of_birth}-{month_of_birth:02}-{day_of_birth:02}',
        'postcode': postcode,
        'first_line_address': first_line_of_address,
        'phone_number': phone_number,
        'email': email,
        'customer_id': f'CUST{customer_id}'
    })
    return f"Customer registered, with customer_id {f'CUST{customer_id}'}"


# LLM will have a choice of when to use which tool.
@tool
def query_knowledge_base(query: str) -> List[Dict[str, str]]:
    """
    Looks up information in a knowledge base to help with answering customer questions and getting information on business processes.

    Args:
        query (str): Question to ask the knowledge base

    Return:
        List[Dict[str, str]]: Potentially relevant question and answer pairs from the knowledge base
    """
    
    # Return a list of dictionaries containing -Question, -Answer messages
    return vector_store.query_faqs(query=query)

@tool
def search_for_product_recommendations(description: str):
    """
    Looks up information in a knowledge base to help with product recommendation for customers. For example:

    "Boquets suitable for birthdays, maybe with red flowers"
    "A large boquet for a wedding"
    "A cheap boquet with wildflowers"

    Args:
        query (str): Description of product features

    Return:
        List[Dict[str, str]]: Potentially relevant products
    """
    
    # Return a list of dictionaries containing -Product Name, -Product Description
    return vector_store.query_inventories(query=description)
