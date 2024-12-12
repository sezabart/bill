from fasthtml.common import (
    A, AX, Button, Card, CheckboxX, Container, Div, Form, Grid, Group, P, H1, H2, H3, H4, H5, Hr, Hidden, Input, Li, Ul, Style, Textarea, Title, Titled, Select, Option, Table, Tr, Th, Td,
    FastHTML, picolink, serve,
)

# Simple 404 handler, which will return a  error page.
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))

# FastHTML includes the "HTMX" library in the header by default.
app = FastHTML(exception_handlers={404: _not_found},
               # PicoCSS is a tiny CSS framework that we'll use for this project.
               # `picolink` is pre-defined with the header for the PicoCSS stylesheet.
               hdrs=(picolink)
      )
# Decorator for url routing
rt = app.route

@rt("/") # Index page
def get():
    return Titled(
        "🛠️ FabLab's Bill 💶", 
        material_form(), 
        Hr(),
        A('Made by Bart Smits, 2024', href='https://github.com/sezabart/bill', cls='secondary'),
        style='text-align:center; max-width: 600px;'
    )

@rt("/material_form")
def material_form():
    return Form(
        H3('Create a material bill:'),
        Div(
            H5('User:', style='display: inline-block; vertical-align: middle; margin-right: 10px;'),
            Input(name='user', placeholder='First & Last Name', required=True, autocomplete="off", style='display: inline-block; vertical-align: middle; max-width: 200px;'),
            style='text-align: center; margin-bottom: 20px;'
        ),
        Table(
            Tr(
                Th('Material'),
                Th('Quantity'),
            ),
            material_select_row(required=True),
            id='material_select_rows'
        ),
        Button('Save & Print'),

        P('Saving & Printing...', id="indicator", cls="htmx-indicator", style="margin-top: 10px;"),

        hx_indicator="#indicator",
        hx_post='/save_print_bill', 
        name='material_form',
    )

from data import materials, categories

@rt("/material_select_row")
def material_select_row(required: bool = False):
    
    options = [Option('Select a material', hidden=True, disabled=True, selected=True)]
    for c in categories():
        options.append(Option(f'--{c.name}--', disabled=True))
        for m in materials(where=f"category='{c.id}'"):
            options.append(Option(f'{m.nice_name} [{c.unit}]', value=m.id))

    return Tr(
                Td(
                    Select(
                        *options,
                    name='material', autocomplete="off", required=required,
                    #hx_trigger='change once', hx_get='/material_select_row', hx_target='#material_select_rows', hx_swap='beforeend',
                    ),
                ),
                Td(
                    Input(type='number', name='quantity', autocomplete="off", max=99999, min=0, required=required),
                    style='max-width: 50px;'
                ),
                Td(
                    P('-', type='button', onclick='this.closest("tr").remove();', style='border: 1px solid grey; padding: 5px; background: none;') if not required else 
                    P('+', type='button', hx_trigger='click', hx_get='/material_select_row', hx_target='#material_select_rows', hx_swap='beforeend', hx_indicator="none",
                       style='border: 1px solid grey; padding: 5px; background: none;')
                )
            )

from data import save_bill
from print import fill_template, print_file

@rt("/save_print_bill")
def post(user: str, material: list[int], quantity: list[int]):
    bill = save_bill(user, zip(material, quantity))
    print(f'{bill=} {type(bill)=}')
    if not bill:
        return message({'Error occurred while saving the bill, contact the administrator.': True})
    
    file = fill_template(bill, 'template_en_fablab.odt', 'filled_en_fablab.odt')
    if not file:
        return message({'Error occurred while filling the template, contact the administrator.': True})
    
    return message(print_file('filled_en_fablab.odt'))
    

def message(messages: dict[str, bool]):
    return Div(
        *[P(msg, style=f'color: {"red" if err else "green"};',
             hx_trigger=f"load delay:{5 if err else 1}s", hx_get='/material_form', hx_swap='outerHTML'
             ) for msg, err in messages.items()],
    )


serve() # Start the server