from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging
from app.models.member_model import Member


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger('MemberSeeder')

def seed_members(db: Session):
    existing_count = db.query(Member).count()
    if existing_count > 0:
        logger.info(f"Database already contains {existing_count} members, skipping seeding.")
        return
    
    logger.info("Seeding database with sample members...")
    
    for i in range(4):
        db.add(Member(
            organization_id=1,
            first_name=f"John {i}",
            last_name=f"Doe {i}",
            login=f"john123_{i}",
            avatar_url=f"https://example.com/avatar{i}.jpg",
            followers=120 + i,
            following=35 + i,
            title=f"Software Engineer {i}",
            email=f"john{i}@example.com"
        ))
    
    db.commit()

    logger.info(f"Successfully seeded database with 4 members")