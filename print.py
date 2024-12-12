from data import bills, materials, categories

import datetime
import os
import subprocess
import json

from relatorio.templates.opendocument import Template

def fill_template(bill, template_path: str, output_path: str):
    if not os.path.exists(template_path):
        return False
    template_data = {
        'user': bill.user,
        'bill_id': bill.id,
        'lines': [{
            'nice_name': materials[m].nice_name, 
            'system_name': materials[m].system_name,
            'quantity': f'{q}{categories[materials[m].category].unit}', 
            'cost_per_unit': f'{materials[m].cost_per_unit}/{categories[materials[m].category].unit}', 
            'cost': f'{q * materials[m].cost_per_unit:.2f}',
            } for m, q in json.loads(bill.data).items()],
        'total': f'{bill.total:.2f}',
        'print_timestamp': datetime.datetime.now().strftime('Printed %Y-%m-%d - %H:%M:%S'),
    }
    return open(output_path, 'wb').write(Template(source='', filepath=template_path).generate(o=template_data).render().getvalue())
    


def print_file(file: str):
    if not os.path.exists(file):
        print(f"File not found: {file}")
        return {'File not found.': True}
    if not file.endswith('.odt'):
        print(f"Invalid file type: {file}")
        return {'Invalid file type.': True}
    try:
        subprocess.run(['lowriter', '-p', f'{file}'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr.decode()}")
        return {'Error occurred while printing, contact the administrator.': True}
    
    return {'Successfully sent to printer.': False}

