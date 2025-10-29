from behave import given, when, then
import requests
from urllib.parse import urljoin

# Base URL of your Flask API
BASE_URL = "http://localhost:8082"  # change to 8080 if that's your running port


##################################################################
# GIVEN: Test Data Setup
##################################################################
@given('the following products exist')
def step_impl(context):
    """Clear existing products and add new ones from table"""
    requests.delete(urljoin(BASE_URL, "/api/products/reset"))
    for row in context.table:
        data = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].lower() == "true",
            "category": row["category"]
        }
        requests.post(urljoin(BASE_URL, "/api/products"), json=data)


##################################################################
# WHEN: API or Page Interactions
##################################################################
@when('I visit the "Home Page"')
def step_impl(context):
    """Simulate visiting the home page"""
    response = requests.get(BASE_URL)
    context.response = response


@when('I set the "{field}" field to "{value}"')
def step_impl(context, field, value):
    """Set a field value before making an API request"""
    if not hasattr(context, "product"):
        context.product = {}
    if field.lower() == "price":
        context.product[field.lower()] = float(value)
    else:
        context.product[field.lower()] = value


@when('I select "{value}" from the "{field}" dropdown')
def step_impl(context, value, field):
    """Set dropdown field values like available/category"""
    if not hasattr(context, "product"):
        context.product = {}
    if field.lower() == "available":
        context.product["available"] = value.lower() == "true"
    elif field.lower() == "category":
        context.product["category"] = value


@when('I press the "Create" button')
def step_impl(context):
    """Send POST request to create a product"""
    context.response = requests.post(
        urljoin(BASE_URL, "/api/products"), json=context.product
    )
    if context.response.ok:
        context.product_id = context.response.json().get("id", None)


##################################################################
# THEN: Response Validations
##################################################################
@then('I should not see "404 Not Found"')
def step_impl(context):
    """Ensure 404 error is not in the response"""
    assert "404 Not Found" not in context.response.text


@then('I should see the message "Success"')
def step_impl(context):
    """Check that request succeeded"""
    assert context.response.status_code in [200, 201], \
        f"Expected 200 or 201, got {context.response.status_code}"
