from app import db
from app.models.level import Level
from sqlalchemy.exc import SQLAlchemyError
import os
from app.utils.file_upload import save_file, delete_file


class LevelService:
    def get_all(self):
        levels = Level.query.all()
        return [level.to_dict() for level in levels]

    def get_by_id(self, level_id):
        level = Level.query.get(level_id)
        return level.to_dict() if level else None

    def create_level(self, data, file=None):
        try:
            # Handle file upload if provided
            image_url = None
            if file:
                try:
                    image_url = save_file(file, 'levels')
                except Exception as e:
                    raise Exception(f"Failed to save file: {str(e)}")

            level = Level(
                name=data['name'],
                description=data.get('description', ''),
                image_url=image_url
            )
            db.session.add(level)
            db.session.commit()
            return level.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    def update_level(self, level_id, data, file=None):
        try:
            level = Level.query.get(level_id)
            if not level:
                return None
            
            # Handle file upload if provided
            if file:
                try:
                    # Delete old image if exists
                    if level.image_url:
                        delete_file(level.image_url)
                       
                    # Save new image
                    image_url = save_file(file, 'levels')
                    data['image_url'] = image_url
                except Exception as e:
                    raise Exception(f"Failed to save new file: {str(e)}")
            
            # Update fields
            for key, value in data.items():
                setattr(level, key, value)
            
            db.session.commit()
            return level.to_dict()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    def delete_level(self, level_id):
        try:
            level = Level.query.get(level_id)
            if not level:
                return False
            
            # Delete associated image if exists
            if level.image_url:
                try:
                    delete_file(level.image_url)
                except Exception as e:
                    raise Exception(f"Failed to delete image for level {level_id}: {str(e)}")
            
            try:
                db.session.delete(level)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                raise Exception(f"Database error while deleting level: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to delete level: {str(e)}") 