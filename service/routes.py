"""
Product Store Service with REST API
"""
from flask import jsonify, request, abort, url_for
from service.models import Product
from service.common import status
from . import app, db


######################################################################
# H E A L T H   C H E C K
######################################################################
@app.route("/health", methods=["GET"])
def healthcheck():
    """Let them know our heart is still beating"""
    app.logger.info("Health check request")
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# H O M E   P A G E
######################################################################
@app.route("/", methods=["GET"])
def index():
    """Base URL for our service"""
    app.logger.info("Request for Root URL")
    # Serve simple HTML for Behave UI tests
    return (
        "<html><head><title>Product Catalog Administration</title></head>"
        "<body><h1>Welcome to Product Catalog Administration</h1></body></html>"
    )


######################################################################
# U T I L I T Y   F U N C T I O N S
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.warning("Missing Content-Type header")
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")

    if request.headers["Content-Type"] != content_type:
        app.logger.warning("Invalid Content-Type: %s", request.headers["Content-Type"])
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {content_type}")


######################################################################
# R E S E T   D A T A B A S E
######################################################################
@app.route("/api/products/reset", methods=["DELETE"])
def reset_products():
    """Removes all products (used for testing)"""
    app.logger.info("Request to reset all products")
    db.session.query(Product).delete()
    db.session.commit()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# C R E A T E   A   P R O D U C T
######################################################################
@app.route("/api/products", methods=["POST"])
def create_products():
    """Creates a Product"""
    app.logger.info("Request to create a new product")
    check_content_type("application/json")

    data = request.get_json()
    if not data:
        abort(status.HTTP_400_BAD_REQUEST, "Invalid JSON data")

    product = Product()
    product.deserialize(data)
    product.create()

    location_url = url_for("get_products", product_id=product.id, _external=True)
    app.logger.info("Product created with id [%s]", product.id)

    return jsonify(product.serialize()), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# R E A D   A   P R O D U C T
######################################################################
@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """Reads a Product by ID"""
    app.logger.info("Request for product with id [%s]", product_id)
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# U P D A T E   A   P R O D U C T
######################################################################
@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """Updates a Product"""
    app.logger.info("Request to update product with id [%s]", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' not found")

    data = request.get_json()
    if not data:
        abort(status.HTTP_400_BAD_REQUEST, "Invalid JSON data")

    product.deserialize(data)
    product.id = product_id
    product.update()

    app.logger.info("Product [%s] updated successfully", product_id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# D E L E T E   A   P R O D U C T
######################################################################
@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """Deletes a Product"""
    app.logger.info("Request to delete product with id [%s]", product_id)
    product = Product.find(product_id)

    if product:
        product.delete()
        app.logger.info("Product [%s] deleted", product_id)
    else:
        app.logger.warning("Product [%s] not found for deletion", product_id)

    return "", status.HTTP_204_NO_CONTENT


######################################################################
# L I S T   A L L   P R O D U C T S
######################################################################
@app.route("/api/products", methods=["GET"])
def list_products():
    """List all Products with optional filters"""
    app.logger.info("Request for product list")

    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    products = []

    if name:
        app.logger.info("Filtering by name: %s", name)
        products = Product.find_by_name(name)
    elif category:
        app.logger.info("Filtering by category: %s", category)
        products = Product.find_by_category(category)
    elif available is not None:
        app.logger.info("Filtering by availability: %s", available)
        available = available.lower() in ["true", "1", "yes"]
        products = Product.find_by_availability(available)
    else:
        app.logger.info("Returning all products")
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK
