from flask import Blueprint, request, jsonify, render_template
from app.services.general_service import GeneralService

general_bp = Blueprint('general', __name__)

def create_crud_routes(endpoint):
    # Unique function for `GET` and `POST`
    def get_and_create():
        if request.method == 'GET':
            try:
                result = GeneralService.get_all(endpoint)
                return jsonify(result), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        elif request.method == 'POST':
            try:
                data = request.json or request.form
                result = GeneralService.create(endpoint, data)
                return jsonify(result), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        else:
            return jsonify({"error": "Method Not Allowed"}), 405

    # Dynamically assign unique endpoint names
    general_bp.add_url_rule(
        f'/{endpoint}', 
        view_func=get_and_create, 
        methods=['GET', 'POST'], 
        endpoint=f'{endpoint}_list'
    )

    # Unique function for `GET`, `PUT`, and `DELETE` with ID
    def manage_by_id(id):
        if request.method == 'GET':
            try:
                result = GeneralService.get_by_id(endpoint, id)
                return jsonify(result), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        elif request.method == 'PUT':
            try:
                data = request.json or request.form
                result = GeneralService.update_by_id(endpoint, id, data)
                return jsonify(result), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        elif request.method == 'DELETE':
            try:
                result = GeneralService.delete_by_id(endpoint, id)
                return jsonify(result), 200
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        return jsonify({"error": "Method not allowed"}), 405

    # Dynamically assign unique endpoint names for ID-based operations
    general_bp.add_url_rule(
        f'/{endpoint}/<int:id>', 
        view_func=manage_by_id, 
        methods=['GET', 'PUT', 'DELETE'], 
        endpoint=f'{endpoint}_detail'
    )

# Add routes for all specified endpoints
ENDPOINTS = [
    "level", "section", "question", "questionChoice"
]

# Register all CRUD routes
for route in ENDPOINTS:
    create_crud_routes(route)


@general_bp.route('/items/<endpoint>', methods=['GET'])
def items_page(endpoint):
    try:
        # Validate the endpoint
        if endpoint not in ENDPOINTS:
            return jsonify({"message": f"Invalid endpoint: {endpoint}", "status": "error"}), 400
        
        # Fetch all items dynamically based on the endpoint
        items = GeneralService.get_all(endpoint)
        return render_template('items.html', items=items, endpoint=endpoint)
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "status": "error"}), 500    


# UPLOAD ENDPOINT
@general_bp.route('/upload', methods=['POST'])
def upload():
    try:
        result = GeneralService.upload_file()
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "status": "error"}), 500