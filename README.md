'bill' is a small, modular webapp for the purposes of creating bills.

It is intented as voluntary project to support the Center ROG. (but not directly sactioned by Center ROG)

When members at for example the FabLab use material of Center ROG, say 3D printing filament, this has to be payed for at the Center ROG shop.
To facilitate this a small paper bill is handwritten.

This project tries to make this easier by re-using an old phone as a kiosk-style portal where bill information can be filled in, after which the bill gets printed on thermal paper like a receipt.

Current setup is a Django server on a Raspberry Pi (3+ or Zero W) connected via a direct serial connection to an old-fashioned thermal printer (yet to be acquired) with an old Motorola smartphone running Android as the kiosk.

Future expansion could be done by having child printers connected via serial to an ESP8266 or ESP32 which gets the print data via (secured) web-socket API from the Raspberry Pi main server. 

[Useful code](https://github.com/trandi/esp32-thermal_printer)

[Inspiration](https://www.youtube.com/watch?v=MZT0gV6-M9w)

![Thermal printer](https://i5.walmartimages.com/seo/Thermal-Receipt-Printer-80mm-Desktop-Direct-Printing-USB-Connection-300mm-s-High-Speed-Auto-Cutter-Support-ESC-POS-Shipping-Business-Restaurant-Kitch_b1fb0bc1-5692-4c62-bcd1-e0f806bb529e.28fb62aa49f0b1d1524440c16d8c59c0.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF)

This is a Work In Progress by Bart Smits, being preformed in spare time in and around Ljubljana. Any help appreciated. 
