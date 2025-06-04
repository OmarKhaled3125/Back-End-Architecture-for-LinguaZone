"""
Base service module that provides common functionality for all services.
"""
from typing import Any, Dict, List, Optional, Type, TypeVar
from app import db

T = TypeVar('T')


class BaseService:
    """Base service class with common CRUD operations."""
    
    def __init__(self, model_class: Type[T]):
        """Initialize the service with a model class."""
        self.model_class = model_class
    
    def get_all(self) -> List[T]:
        """Get all records from the database."""
        return self.model_class.query.all()
    
    def get_by_id(self, id: int) -> Optional[T]:
        """Get a record by its ID."""
        return self.model_class.query.get(id)
    
    def create(self, data: Dict[str, Any]) -> T:
        """Create a new record."""
        instance = self.model_class(**data)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """Update a record by its ID."""
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            db.session.commit()
        return instance
    
    def delete(self, id: int) -> bool:
        """Delete a record by its ID."""
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False
    
    def query(self):
        """Get a query object for the model."""
        return self.model_class.query
