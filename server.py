from fasthtml.common import (
    # FastHTML's HTML tags
    A, AX, Button, Card, CheckboxX, Container, Div, Form, Grid, Group,P, H1, H2, H3, H4, H5, Hr, Hidden, Input, Li, Ul, Main, Script, Style, Textarea, Title, Titled, Select, Option, Table, Tr, Th, Td,
    # FastHTML's specific symbols
    Beforeware, FastHTML, fast_app, SortableJS, fill_form, picolink, serve, NotStr,
    # From Starlette, Fastlite, fastcore, and the Python standard library:
    FileResponse, NotFoundError, RedirectResponse, database, patch, dataclass, UploadFile
)
import os
import datetime
import requests


db = database('sqlite3.db')

bills, categories, materials = db.t.bills, db.t.categories, db.t.materials
if bills not in db.t:
    bills.create(
        id=int,
        lab_id=int,
        user=str,
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
    categories.insert(name='Laser Cutting', unit='mm²')

if materials not in db.t:
    materials.create(
        id=int,
        category=int,
        nice_name=str,
        system_name=str,
        cost_per_unit=float,
        pk='id'
    )
    materials.insert(category=1, nice_name='PLA', system_name='pla', cost_per_unit=0.05)
    materials.insert(category=1, nice_name='PETG', system_name='petg', cost_per_unit=0.05)
    materials.insert(category=2, nice_name='Acrylic', system_name='acrylic', cost_per_unit=0.05)
    materials.insert(category=2, nice_name='Plywood', system_name='plywood', cost_per_unit=0.05)

# Create a dataclass for the bills table entries
Bill, Category, Material = bills.dataclass(), categories.dataclass(), materials.dataclass()


# This will be our 404 handler, which will return a simple error page.
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))

# FastHTML includes the "HTMX" and "Surreal" libraries in headers, unless you pass `default_hdrs=False`.
app = FastHTML(exception_handlers={404: _not_found},
               # PicoCSS is a tiny CSS framework that we'll use for this project.
               # `picolink` is pre-defined with the header for the PicoCSS stylesheet.
               hdrs=(picolink,
                     # `Style` is an `FT` object, which are 3-element lists consisting of:
                     # (tag_name, children_list, attrs_dict).
                     Style(':root { --pico-font-size: 100%; }'),
                )
      )
# `app.route` (or `rt`) requires only the path, using the decorated function's name as the HTTP verb.
rt = app.route

@rt("/") # Index page
def get():
    frm = Form(
        H3('Create a material bill:'),
        Group(H5('User:'), Input(name='user', placeholder='First & Last Name', required=True, autocomplete="off", style='max-width: 200px;')),
        Group(H5('Category:'), 
            Select(
                Option('Select a category', value='', disabled=True, selected=True, ),
                *[Option(c.name, value=c.id) for c in categories()],
                name='category',
                required=True,
                autocomplete="off",
                style='max-width: 200px;',
                hx_get='/material_select_row', hx_trigger='change, click from:next button', hx_target='#material_select_rows', hx_swap='beforeend', hx_include='category'
            ),
            Button('+', type='button', style='max-width: 50px;')
            
        ),
        Table(
            Tr(
                Th('Material'),
                Th('Quantity'),
                Th('Unit'),
            ),
            id='material_select_rows'
        ),
        Button('Save & Print'),
        P('Printing...', id="printing", cls="htmx-indicator"),
        hx_post='/print', hx_swap='afterend', hx_indicator="#printing",
        name='material_bill'
    )

    return Titled("🛠️ FabLab's Bill 💶", frm)

@rt("/material_select_row")
def material_select_row(category: str=None):
    if category:
        cat = categories[category]
        search_arg = {'where': f"category='{cat.id}'"}
        category = cat.name
        unit = f' [{cat.unit}]'
    else:
        search_arg = {'order_by': 'category'}
        unit = ''
    
    return Tr(
                Td(
                    Select(
                        Option(f'Select {category} material', value='', disabled=True, selected=True),
                        *[Option(f"{m.nice_name}", value=m.id) for m in materials(**search_arg)],
                    name='material',
                    ),
                ),
                Td(
                    Input(type='number', name='quantity', autocomplete="off",),
                    style='max-width: 50px;'
                ),
                Td(unit),
            )

@rt("/save") # Make the Bill entry including calculated costs.

@rt("/print")
def post(user: str, material: list[int], quantity: list[int]):
    pass

serve() # Start the server