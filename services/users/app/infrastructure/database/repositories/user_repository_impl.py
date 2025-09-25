from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

# Domain imports (business rules)
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User

# Infrastructure imports (technical details)  
from infrastructure.database.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    """PostgreSQL implementation of UserRepository using SQLAlchemy"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email in PostgreSQL database"""
        try:
            user_model = self.session.query(UserModel).filter(
                UserModel.email == email
            ).first()
            
            if user_model:
                return self._model_to_entity(user_model)
            return None
            
        except SQLAlchemyError as e:
            raise e
    
    def find_by_id(self, id: int) -> Optional[User]:
        """Find user by ID in PostgreSQL database"""
        try:
            user_model = self.session.query(UserModel).filter(
                UserModel.id == id
            ).first()
            
            if user_model:
                return self._model_to_entity(user_model)
            return None
            
        except SQLAlchemyError as e:
            raise e
    
    def save(self, user: User) -> User:
        """Save user to PostgreSQL database"""
        try:
            if user.id:
                # Update existing user
                user_model = self.session.query(UserModel).filter(
                    UserModel.id == user.id
                ).first()
                
                if not user_model:
                    raise ValueError(f"User with ID {user.id} not found")
                
                # Update fields
                user_model.email = user.email
                user_model.password_hash = user.password_hash
                user_model.level = user.level
                user_model.xp = user.xp
                user_model.is_active = user.is_active
                user_model.updated_at = datetime.now(timezone.utc)
            else:
                # Create new user
                user_model = UserModel(
                    email=user.email,
                    password_hash=user.password_hash,
                    level=user.level,
                    xp=user.xp,
                    is_active=user.is_active
                )
                self.session.add(user_model)
            
            self.session.commit()
            self.session.refresh(user_model)
            
            return self._model_to_entity(user_model)
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email"""
        try:
            count = self.session.query(UserModel).filter(
                UserModel.email == email
            ).count()
            return count > 0
        except SQLAlchemyError as e:
            raise e
    
    def delete(self, id: int) -> bool:
        """Delete user by ID"""
        try:
            user_model = self.session.query(UserModel).filter(
                UserModel.id == id
            ).first()
            
            if user_model:
                self.session.delete(user_model)
                self.session.commit()
                return True
            return False
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def find_all_active(self) -> List[User]:
        """Find all active users"""
        try:
            user_models = self.session.query(UserModel).filter(
                UserModel.is_active == True
            ).all()
            
            return [self._model_to_entity(model) for model in user_models]
            
        except SQLAlchemyError as e:
            raise e
    
    def update_last_login(self, id: int) -> bool:
        """Update user's last login timestamp"""
        try:
            user_model = self.session.query(UserModel).filter(
                UserModel.id == id
            ).first()
            
            if user_model:
                # Asumiendo que tienes un campo last_login en UserModel
                # Si no lo tienes, puedes usar updated_at
                if hasattr(user_model, 'last_login'):
                    user_model.last_login = datetime.now(timezone.utc)
                else:
                    user_model.updated_at = datetime.now(timezone.utc)
                
                self.session.commit()
                return True
            return False
            
        except SQLAlchemyError as e:
            self.session.rollback()
            raise e
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            level=model.level,
            xp=model.xp,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )