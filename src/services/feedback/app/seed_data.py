from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from .models.feedback_model import Feedback

logger = logging.getLogger('DatabaseSeeder')

def seed_feedbacks(db: Session):
    existing_count = db.query(Feedback).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} feedbacks, skipping seeding.")
        return
    
    print("Seeding database with sample feedbacks...")
    
    sample_data = [
        {
            "organization_id": 1,
            "feedback": "Feedback 1 for organization 1",
        },
        {
            "organization_id": 1,
            "feedback": "Feedback 2 for organization 1",
        },
        {
            "organization_id": 1,
            "feedback": "Feedback 3 for organization 1",
        },
        {
            "organization_id": 1,
            "feedback": "Feedback 4 for organization 1",
        },
        
        {
            "organization_id": 2,
            "feedback": "Feedback 1 for organization 2",
        },
        {
            "organization_id": 2,
            "feedback": "Feedback 2 for organization 2",
        },
        {
            "organization_id": 2,
            "feedback": "Feedback 3 for organization 2",
        },
    ]
    
    for feedback_data in sample_data:
        feedback = Feedback(**feedback_data)
        db.add(feedback)
    
    db.commit()
    print(f"Successfully seeded database with {len(sample_data)} feedbacks")