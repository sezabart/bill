from data import bills, materials, categories

import datetime
import os
import json
from jinja2 import Environment, FileSystemLoader

def fill_template(bill, template_path: str, output_path: str):
    if not os.path.exists(template_path):
        raise FileExistsError(f'Cannot find template at {template_path}')
    
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    
    template_data = {
        'user': bill.user,
        'bill_id': bill.id,
        'lines': [{
            'nice_name': materials[m].nice_name, 
            'system_name': materials[m].system_name,
            'quantity': f'{q}{categories[materials[m].category].unit}', 
            'cost_per_unit': f'{materials[m].cost_per_unit}€/{categories[materials[m].category].unit}', 
            'cost': f'{q * materials[m].cost_per_unit:.2f}',
            } for m, q in json.loads(bill.data).items()],
        'total': f'{bill.total:.2f}',
        'print_timestamp': datetime.datetime.now().strftime('%Y-%m-%d - %H:%M:%S'),
    }
    
    with open(output_path, 'w') as f:
        f.write(template.render(template_data))
    
    return output_path

def print_file(file: str):
    if not os.path.exists(file):
        raise FileExistsError(f'Cannot find file at {file}')
    os.system(f'lp {file}')
    return 'Printed'

