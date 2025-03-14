from fastapi import APIRouter, Depends
from typing import List
from app.schema.package import PackageResponse, PackageCreate
from app.service.package_service import PackageService
from app.repository.package_repository import PackageRepository
from app.auth.auth import verify_admin, verify_user

router = APIRouter()
package_repository = PackageRepository()  
package_service = PackageService(package_repository)  

@router.get("/getPackages", dependencies=[Depends(verify_user)], response_model=List[PackageResponse])
def get_packages():
    return package_service.get_all_packages()

@router.get("/getPackageById/{package_id}", dependencies=[Depends(verify_user)], response_model=PackageResponse)
def get_package_by_id(package_id: int):
    package = package_service.get_package_by_id(package_id)
    return package

@router.post("/createPackage", dependencies=[Depends(verify_admin)], response_model=PackageResponse)
def create_package(package: PackageCreate):
    return package_service.create_package(package)

@router.post("/deletePackageByID/{package_id}", dependencies=[Depends(verify_admin)], response_model=PackageResponse)
def delete_package_by_id(package_id: int):
    package = package_service.delete_package_by_id(package_id)
    return package

@router.put("/updatePackageByID/{package_id}", dependencies=[Depends(verify_admin)], response_model=PackageResponse)
def update_package_by_id(package_id: int, package_data: PackageCreate):
    updated_package = package_service.update_package_by_id(package_id, package_data)
    return updated_package