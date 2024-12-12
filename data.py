import datetime
from fasthtml.common import database

db = database('sqlite3.db')

bills, categories, materials = db.t.bills, db.t.categories, db.t.materials


if bills not in db.t:
    bills.create(
        id=int,
        lab_id=int,
        user=str,
        data=dict,
        total=float,
        created_at=datetime.datetime, 
        valid=bool,
        paid=bool,
        pk='id'
    )

if categories not in db.t:
    categories.create(
        id=int,
        name=str,
        unit=str,
        pk='id'
    )
    categories.insert(name='3D Filament', unit='g')
    categories.insert(name='3D Resin', unit='ml')
    categories.insert(name='PCB', unit='mm²')

if materials not in db.t:
    materials.create(
        id=int,
        category=int,
        nice_name=str,
        system_name=str,
        cost_per_unit=float,
        pk='id'
    )
    materials.insert(category=1, nice_name='PLA', system_name='STO3D-INT-FIL3', cost_per_unit=0.04)
    materials.insert(category=1, nice_name='PETG', system_name='STO3D-INT-FIL3', cost_per_unit=0.04)
    materials.insert(category=2, nice_name='Resin', system_name='STO3D-INT-SMOLA', cost_per_unit=0.06)
    materials.insert(category=2, nice_name='Fancy Resin', system_name='STO3D-INT-SMOLA2', cost_per_unit=0.72)
    materials.insert(category=3, nice_name='GFR4 blank', system_name='GFR4', cost_per_unit=0.05)

# Create a dataclass for the bills table entries
Bill, Category, Material = bills.dataclass(), categories.dataclass(), materials.dataclass()



def save_bill(user: str, data: zip) -> int:
    data = {m: q for m, q in data if m in materials and q > 0}
    bill = Bill(
        lab_id=1, # This is a placeholder the FabLab
        user=user,
        created_at=datetime.datetime.now(),
        valid=None, # TODO: implement validation via admin panel.
        paid=False, # TODO: implement payment validation via admin panel.
        data=data,
        total=sum(materials[m].cost_per_unit * q for m, q in data.items()),
    )
    return bills.insert(bill)
