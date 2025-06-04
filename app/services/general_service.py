from app.models import Level, Section, Question, QuestionChoice  # Import models
from app import db  # Import the database instance

class GeneralService:
    MODELS = {
        "level": Level,
        "section": Section,
        "question": Question,
        "questionChoice": QuestionChoice
    }

    @staticmethod
    def get_all(endpoint):
        model = GeneralService.MODELS.get(endpoint)
        if not model:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        return [item.to_dict() for item in model.query.all()]

    @staticmethod
    def create(endpoint, data):
        model = GeneralService.MODELS.get(endpoint)
        if not model:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        item = model(**data)
        db.session.add(item)
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def get_by_id(endpoint, id):
        model = GeneralService.MODELS.get(endpoint)
        if not model:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        item = model.query.get(id)
        if not item:
            raise ValueError(f"Item with ID {id} not found")
        return item.to_dict()

    @staticmethod
    def update_by_id(endpoint, id, data):
        model = GeneralService.MODELS.get(endpoint)
        if not model:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        item = model.query.get(id)
        if not item:
            raise ValueError(f"Item with ID {id} not found")
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return item.to_dict()

    @staticmethod
    def delete_by_id(endpoint, id):
        model = GeneralService.MODELS.get(endpoint)
        if not model:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        item = model.query.get(id)
        if not item:
            raise ValueError(f"Item with ID {id} not found")
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}

    @staticmethod
    def upload_file():
        # Example implementation for file upload
        file = request.files.get('file')
        if not file:
            raise ValueError("No file provided")
        # Save the file and return the result
        file.save(f"/path/to/upload/directory/{file.filename}")
        return {"message": "File uploaded successfully", "filename": file.filename}