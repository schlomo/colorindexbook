#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import csv
import datetime
import glob
import os

import fpdf
from colorutils import Color

fpdf.fpdf.PAGE_FORMATS["a5wirmachendruck"] = (436.5, 612.283)

def rgbFromColor(color):
    if color[0] == "#":
        pass

class PDF(fpdf.FPDF):
    def __init__(self, orientation = 'P', unit = 'pt', format = 'a5wirmachendruck'):
        super().__init__(orientation, unit, format)
        self.alias_nb_pages()
        self.set_margins(0,0)
        self.set_display_mode("fullpage","continuous")
        self.add_font("Liberation Serif", "", "LiberationSerif-Regular.ttf", uni=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def footer(self):
        self.set_y(-57)
        self.set_font("Liberation Serif", '', 10)
        self.cell(0, 0, str(self.page_no()) + ' / {nb}', 0, 0, 'C')

    def add_title_page(self, title=""):
        self.add_page()
        self.set_font("Liberation Serif", "", 60)
        self.set_y(200)
        self.multi_cell(0,60,title,0,"C",ln=2)
        self.set_font("Liberation Serif", "", 20)
        self.ln()
        self.cell(0,20,datetime.date.today().strftime("%d.%m.%Y"),0,2,"C")

    def add_back_page(self,):
        self.add_page()
        self.set_font("Liberation Serif", "", 10)
        self.set_y(400)
        self.multi_cell(0,12,"© Schlomo Schapiro\nLicense: CC-BY-SA",0,"C",ln=2)

    def add_color_page(self, name, color):
        self.add_page()
        self.set_font("Liberation Serif", "", 16)
        background_color = Color(hex=color)
        self.set_fill_color(background_color.red, background_color.green, background_color.blue)
        #self.cell(0, 510, "", 0, 2, "C", True)
        self.cell(218, 510, "", 0, 2, "C", True) # 218pt is half width of the WirMachenDruck A5 page
        self.cell(0,25, name + "  " + color, 0, 1, "C")

def convert_csv_to_pdf(csv_file_name, title=None):
    basename, _ = os.path.splitext(csv_file_name)
    pdf_file_name = basename + ".pdf"
    if title is None:
        title = basename.replace("-", "\n").title()

    with PDF() as pdf:
        pdf.add_title_page(title)
        pdf.add_page() # inside cover should be blank
        colors = {}
        with open("web-colors.csv", newline="") as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, dialect=dialect, fieldnames=["name", "color"])
            content_pages = 0
            for row in reader:
                color = row["color"].strip()
                name = row["name"].strip()
                if color in colors:
                    print(f"Skipping duplicate color {name} {color} (have already {colors[color]}) ")
                    continue
                colors[color] = name

                content_pages += 1
                if content_pages > 148:
                    raise Exception(f"Too many content pages ({content_pages}) while adding {name} {color}")

                pdf.add_color_page(name, color)

        fill_pages = content_pages % 4
        if fill_pages != 0:
            fill_pages = 4 - fill_pages
        print(f"Content Pages: {content_pages} Fill Pages: {fill_pages}")
        for x in range(0,fill_pages):
            pdf.add_page()
        pdf.add_page() # inside back cover should be blank
        pdf.add_back_page()
        total_pages = pdf.page_no()
        pdf.output(pdf_file_name)
        print(f"Converted {csv_file_name} to {pdf_file_name} ({total_pages} pages)")
    
if __name__ == "__main__":
    for file in glob.glob("*.csv"):
        convert_csv_to_pdf(file)