from locations.request import delete_location
from employees.request import create_employee, delete_employee
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animals_by_location_id, get_animals_by_status
from employees import get_all_employees, get_single_employee, create_employee, delete_employee, update_employee, get_employees_by_location_id
from locations import get_all_locations, get_single_location, create_location, delete_location, update_location
from customers import get_all_customers, get_single_customer, create_customer, delete_customer, update_customer, get_customers_by_email

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        if "?" in resource:
            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)
        else:
            id = None

        # Try to get the item at index 2
            try:
                # Convert the string "1" to the integer 1
                # This is the new parseInt()
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {}  # Default response
        # Your new console.log() that outputs to the terminal
        print(self.path)

        parsed = self.parse_url(self.path)
        if len(parsed) == 2:
            (resource, id) = parsed
        # It's an if..else statement
            if resource == "animals":
                # In Python, this is a list of dictionaries
                # In JavaScript, you would call it an array of objects
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"

            elif resource == "employees":
                if id is None:
                    response = f"{get_all_employees()}"
                else:
                    response = f"{get_single_employee(id)}"

            elif resource == "locations":
                if id is None:
                    response = f"{get_all_locations()}"
                else:
                    response = f"{get_single_location(id)}"

            elif resource == "customers":
                if id is None:
                    response = f"{get_all_customers()}"
                else:
                    response = f"{get_single_customer(id)}"
            else:
                response = []

        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)
            elif key == "location_id" and resource == "animals":
                response = get_animals_by_location_id(value)
            elif key == "status" and resource == "animals":
                response = get_animals_by_status(value)
            elif key == "location_id" and resource == "employees":
                response = get_employees_by_location_id(value)
            # This weird code sends a response back to the client
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None
        new_employee = None
        new_locations = None
        new_customers = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)
            self.wfile.write(f"{new_animal}".encode())
        elif resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(f"{new_employee}".encode())
        elif resource == "locations":
            new_locations = create_location(post_body)
            self.wfile.write(f"{new_locations}".encode())
        elif resource == "customers":
            new_customers = create_customer(post_body)
            self.wfile.write(f"{new_customers}".encode())
        # Encode the new animal and send in response

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "locations":
            delete_location(id)
        elif resource == "customers":
            delete_customer(id)

    # Encode the new animal and send in response
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
