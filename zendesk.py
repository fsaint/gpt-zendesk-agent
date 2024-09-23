import requests
import base64
from settings import ZENDESK_TOKEN as api_key, ZENDESK_EMAIL, ZENDESK_DOMAIN as zendesk_domain
# Function 1: Read open Zendesk tickets with no response
def auth():
    auth_string =  base64.b64encode(f"{ZENDESK_EMAIL}/token:{api_key}".encode('utf-8')).decode('utf-8')
    return f"Basic {auth_string}"

def read_open_zendesk_tickets():
    """
    Fetches a list of open tickets from Zendesk.

    This function constructs a query to retrieve all tickets with the status 'open' from the
    Zendesk API. The authorization header is handled by the `auth()` function, and the domain
    is substituted dynamically in the URL. The results are returned in JSON format if the
    request is successful.

    Returns:
        list: A list of open Zendesk tickets in JSON format if successful.
        str: An error message indicating the HTTP status code in case of failure.

    Raises:
        Exception: If the response status code is not 200, the error response is printed
        and a custom error message is returned.
    """
    url = f'https://{zendesk_domain}.zendesk.com/api/v2/search.json'
    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }
    query = 'status:open type:ticket'
    params = {'query': query}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()['results'][:1]
    else:
        print(response.text)
        return f"Error fetching tickets: {response.status_code}"

# Function 2: Search Senders tickets that are closed with keywords
def search_tickets(keywords):
    """
    Searches for closed tickets in Zendesk by a given keyword.

    This function sends a request to the Zendesk API to search for tickets with a 'closed' status,
    where the description contains the specified keywords. The `auth()` function handles the
    authorization, and the domain is dynamically inserted into the URL. Results are returned in
    JSON format if the request is successful.

    Args:
        keywords (str): The keywords to search for in the ticket descriptions.

    Returns:
        list: A list of closed tickets matching the keyword search in JSON format if successful.
        str: An error message indicating the HTTP status code in case of failure.

    Raises:
        Exception: Returns a custom error message with the HTTP status code if the request fails.
    """
    url = f'https://{zendesk_domain}.zendesk.com/api/v2/search.json'
    headers = {
        'Authorization': auth(),
        'Content-Type': 'application/json'
    }
    query = f'status:closed type:ticket description:"{keywords}"'

    params = {'query': query}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()['results']
    else:
        return f"Error searching tickets: {response.status_code}"

# Function 3: Write a reply to a Senders ticket
def reply_to_senders_ticket(ticket_id, message):
    """
    Sends a reply to a specific ticket using the Senders API.

    This function sends a POST request to the Senders API to reply to a specific ticket.
    The function constructs the API endpoint using the provided `ticket_id` and sends the 
    `message` as part of the request payload. The authorization is handled via an API key.

    Args:
        ticket_id (str): The ID of the ticket to which the reply will be sent.
        message (str): The reply message to be sent to the ticket.

    Returns:
        dict: The response from the Senders API if the request is successful.
        str: An error message indicating the HTTP status code in case of failure.

    Raises:
        Exception: Returns a custom error message with the HTTP status code if the request fails.
    """
    url = f"https://api.senders.com/v1/tickets/{ticket_id}/reply"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'message': message
    }

    #response = requests.post(url, headers=headers, json=data)
    print(message)

    if response.status_code == 200:
        return response.json()
    else:
        return f"Error replying to ticket: {response.status_code}"

def get_zendesk_ticket_messages(ticket_id):
    """
    Fetches all messages (comments) associated with a specific Zendesk ticket.

    This function retrieves all the comments (messages) for the specified Zendesk ticket
    by making a GET request to the Zendesk API. The request is authenticated using an email/token
    combination and API key.

    Args:
        ticket_id (int): The ID of the Zendesk ticket whose comments are to be fetched.

    Returns:
        list: A list of comments (messages) related to the specified ticket if the request is successful.
        None: If there is an error in fetching the ticket messages, `None` is returned.

    Raises:
        requests.exceptions.RequestException: If the request fails, an exception is caught, 
        an error message is printed, and `None` is returned.
    """
    url = f"https://{zendesk_domain}.zendesk.com/api/v2/tickets/{ticket_id}/comments.json"
    auth = (f'{ZENDESK_EMAIL}/token', api_key)

    try:
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an exception if the request was not successful
        comments = response.json().get('comments', [])
        return comments
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ticket messages: {e}")
        return None

if __name__ == '__main__':
    '''
    for t in read_open_zendesk_tickets('seer'):
        print(t)
    '''
    for t in search_tickets('password'):
        ticket_id = t['id']
        r = get_zendesk_ticket_messages(ticket_id)
        print(ticket_id)
        print(r)
