from fastapi import HTTPException
from app.repository.package_repository import PackageRepository
from app.schema.package import PackageCreate


class PackageService:
    def __init__(self, package_repository: PackageRepository):
        self.package_repository = package_repository
        
    def get_all_packages(self):
        return self.package_repository.get_all_packages()
    
    def get_package_by_id(self, package_id: int):
        package = self.package_repository.get_package_by_id(package_id)
        if not package or not package.active:
            raise HTTPException(status_code=404, detail="Package not found")
        return package
    
    def create_package(self, package: PackageCreate):
        print(f"Package received in Service: {package}")
        return self.package_repository.create_package(package)

    def delete_package_by_id(self, package_id: int):
        package = self.package_repository.get_package_by_id(package_id)
        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        package.active = False
        
        return self.package_repository.update_package(package)

    def update_package_by_id(self, package_id: int, package_data: PackageCreate,):
        package = self.package_repository.get_package_by_id(package_id)

        if not package:
            raise HTTPException(status_code=404, detail="Package not found")

        package.title = package_data.title
        package.description = package_data.description
        package.price = package_data.price  
        package.ticket_quantity = package_data.ticket_quantity

        return self.package_repository.update_package(package)
