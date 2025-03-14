from app.model.package import Package
from app.schema.package import PackageCreate
from sqlalchemy.orm import Session
from app.database.database import db_instance

class PackageRepository:
    def __init__(self):
        self.db: Session = db_instance.get_session()

    def get_all_packages(self):
        return self.db.query(Package).filter(Package.active == True).all()
    
    def get_package_by_id(self, id: int):
        package = self.db.query(Package).filter(Package.package_id == id).one_or_none()
        return package

    def create_package(self, package: PackageCreate):
        try:
            new_package = Package(**package.dict())
            self.db.add(new_package)
            self.db.commit()
            return new_package
        except Exception as e:
            self.db.rollback()
            raise e
    
    def update_package(self, package: Package):  
        self.db.commit()
        self.db.refresh(package)
        return package