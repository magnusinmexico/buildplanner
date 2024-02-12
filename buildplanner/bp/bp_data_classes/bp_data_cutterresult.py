# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_data_cutterresult.py
# Author: Magnus Pettersson
#
# This module defines the BPDataCutterResult class, which represents the result
# of a cutting operation in a build planner application. The class encapsulates 
# information about the stock pieces used, remaining demand, available stock, 
# waste generated, and cutting instructions. It provides methods to manipulate
# and access this data, as well as generate reports and visual representations
# of the cutting instructions.
#
# The BPDataCutterResult class is a fundamental component of the build planner
# system, facilitating efficient planning and optimization of cutting 
# operations. It enables users to track the usage of stock materials, manage
# remaining demand, and minimize waste generation during cutting processes.
# With its comprehensive set of attributes and methods, the class empowers
# users to analyze cutting results, generate detailed reports, and visualize
# cutting instructions in various formats, including HTML and SVG.
#
#------------------------------------------------------------------------------

from bp.bp_data_classes import BPDataStockPieces, BPDataCutStock
from bp.bp_type_check import type_check_class
from bp.bp_defs import *

from bp import bp_svg

@type_check_class
class BPDataCutterResult:

    __cut_stock_list : list
    __used_stock : BPDataStockPieces
    __remaining_demand : BPDataStockPieces
    __available_stock : BPDataStockPieces
    __total_waste : float
    __precision: int
    __length_unit: str
    __original_length_unit:str
    __stock_height: float
    __stock_width: float
    method : str

    @property
    def stock_height(self):
        return self.__stock_height if self.__stock_height > 0.0 else (0.0 if len(self.__used_stock)==0 else self.__used_stock.max_length()*0.005)

    @stock_height.setter
    def stock_height(self,value):
        self.__stock_height = value

    @property
    def stock_width(self):
        return self.__stock_width if self.__stock_width > 0.0 else (0.0 if len(self.__used_stock)==0 else self.__used_stock.max_length()*0.05)

    @stock_width.setter
    def stock_width(self,value):
        self.__stock_width = value

    @property
    def precision(self) -> int:
        return self.__precision
    
    @precision.setter
    def precision(self,value:int):
        self.__precision = value

    @property 
    def length_unit(self) -> str:
        return self.__length_unit
    
    @length_unit.setter
    def length_unit(self,value:str):
        if value not in length_unit_suffix:
            scale_values = ",".join(length_unit_suffix.keys())
            raise ValueError(f"{value} is an invalid scale value. Must be one of {scale_values}")
        self.__scale = value

    @property 
    def original_length_unit(self) -> str:
        return self.__original_length_unit
    
    @original_length_unit.setter
    def original_length_unit(self,value:str):
        if value not in length_unit_suffix:
            scale_values = ",".join(length_unit_suffix.keys())
            raise ValueError(f"{value} is an invalid scale value. Must be one of {scale_values}")
        self.__scale = value
    
    @property
    def messages(self) -> str:
        return "\n".join(self.__messages)

    @property
    def used_stock(self) -> BPDataStockPieces:
        return self.__scale_stock_pieces(self.__used_stock)

    @property
    def remaining_demand(self) -> BPDataStockPieces:
        return self.__scale_stock_pieces(self.__remaining_demand)
    
    @remaining_demand.setter
    def remaining_demand(self,value : BPDataStockPieces) -> BPDataStockPieces:
        self.__remaining_demand = value

    @property
    def available_stock(self):
        return self.__scale_stock_pieces(self.__available_stock)

    @available_stock.setter
    def available_stock(self,value: BPDataStockPieces):
        self.__available_stock = value

    @property
    def remaining_stock(self) -> BPDataStockPieces:
        return self.__scale_stock_pieces((self.__available_stock - self.__used_stock).clean())

    @property
    def total_waste(self) -> float:
        return float(self.__scale_float(self.__total_waste))

    @property
    def completed(self) -> bool:
        return len(self.remaining_demand) == 0
    
    @property
    def cut_stock_list(self) -> list:
        cut_stock_dict = {}
        max_width = 0
        for cut_stock in self.__cut_stock_list:
            cut_stock_scaled = self.__scale_cut_stock(cut_stock)
            key = str(hash(str(cut_stock_scaled)))
            if (key in cut_stock_dict):
                cut_stock_dict[key]["amount"] += 1
            else:
                cut_stock_dict[key] = {"amount":1, "cut_stock" : cut_stock_scaled}
                if cut_stock_scaled.stock_length > max_width: max_width = cut_stock_scaled.stock_length
        cut_stock_list = [inner_dict for outer_dict in cut_stock_dict.values() for inner_dict in [outer_dict]]
        return sorted(cut_stock_list, key=lambda x: (-x['cut_stock']['stock_length'], -x['amount'], x['cut_stock']['remaining_stock']))

    def __init__(self, precision : int = 0, length_unit : str = "NONE", original_length_unit : str = "NONE", available_stock : BPDataStockPieces = BPDataStockPieces() ) -> None:
        self.__cut_stock_list = []
        self.__used_stock = BPDataStockPieces()
        self.__remaining_demand = BPDataStockPieces()
        self.__available_stock = available_stock.copy()
        self.__total_waste = 0.0
        self.__precision = precision
        if length_unit not in length_unit_suffix:
            scale_values = ",".join(length_unit_suffix.keys())
            raise ValueError(f"{length_unit} is an invalid length_unit value. Must be one of {scale_values}")
        self.__length_unit = length_unit
        if original_length_unit not in length_unit_suffix:
            scale_values = ",".join(length_unit_suffix.keys())
            raise ValueError(f"{original_length_unit} is an invalid original_length_unit value. Must be one of {scale_values}")
        self.__original_length_unit = original_length_unit
        self.__stock_width = 0.0
        self.__stock_height = 0.0
        self.method = ""

    def __scale_stock_pieces(self, stock_pieces:BPDataStockPieces) -> BPDataStockPieces:
        stock_pieces_scaled = BPDataStockPieces()
        scale_factor = length_unit_scale_factor[self.__length_unit]/length_unit_scale_factor[self.__original_length_unit]
        precision = self.precision 
        for key,value in stock_pieces.items():
            stock_pieces_scaled[float(round(key*scale_factor,precision))] = value
        return stock_pieces_scaled
    
    def __scale_cut_stock(self, cut_stock:BPDataCutStock) -> BPDataCutStock:
        cut_stock_scaled = BPDataCutStock(
            self.__scale_float(float(cut_stock.stock_length)),
            self.__scale_float(float(cut_stock.cut_width)),
            self.__scale_stock_pieces(cut_stock.stock_pieces))
        return cut_stock_scaled
    
    def __scale_float(self, f:float) -> float:
        scale_factor = length_unit_scale_factor[self.__length_unit]/length_unit_scale_factor[self.__original_length_unit]
        precision = self.precision 
        return float(round(f*scale_factor,precision))
    
    def keys(self):
        return ["cut_stock_list",
                "used_stock",
                "remaining_demand",
                "total_waste",
                "completed"]
    
    def values(self): 
        return [self.cut_stock_list,
                self.used_stock,
                self.remaining_demand,
                self.total_waste,
                self.completed]
    
    def items(self):
        return dict(zip(self.keys(),self.values())).items()

    def append(self,cut_stock : BPDataCutStock) -> 'BPDataCutterResult':
        assert(cut_stock.is_valid), f"The BPDataCutStock object is not valid:\n{cut_stock}"
        self.__cut_stock_list.append(cut_stock)
        self.__used_stock.append(cut_stock["stock_length"])
        self.__total_waste += cut_stock["remaining_stock"]+cut_stock["number_of_cuts"]*cut_stock["cut_width"]
        return self

    def __repr__(self):
        return str(dict(zip(self.keys(),self.values())))
    
    def __getitem__(self, key):
        if not key in self.keys(): 
            raise KeyError(f"The key '{key}' does not exists in an instance of BPDataCutterResult")
        return dict(zip(self.keys(),self.values()))[key]
    
    def __str__(self) -> str:

        count = 0 
        str_amount_arr = []
        str_stock_length_arr = []
        str_stock_pieces_arr = []
        str_cut_with_arr = []
        str_waste_arr = []
        str_length_unit= length_unit_suffix[self.length_unit]
        str_length_unit_brackets = "" if self.length_unit == "NONE" else f" ({length_unit_suffix[self.length_unit]})" 
        str_report_title = "Build Planner - Cutter Result"
        str_amount_header = "Amount:"
        str_stock_length_header = "Stock length:"
        str_stock_pieces_header= f"Stock cut pieces{str_length_unit_brackets}:"
        str_cut_width_header = "Cut width:"
        str_waste_header = "Waste:"
        str_needed_stock_title = "Needed stock"
        str_cutting_instruction_title = "Cutting instruction"
        str_padding = "  "
        str_total_waste = "Total waste:"
        str_remaining_demand = "Remaining demand:"
        str_remaining_stock = "Remaining stock:"
        
        for cut_stock in self.cut_stock_list:
            str_amount_arr.append(str(cut_stock["amount"]))
            str_stock_length_arr.append(str(cut_stock["cut_stock"]["stock_length"])+str_length_unit)
            str_stock_pieces_arr.append("| "+" | ".join(f"{num}" for num in list(cut_stock["cut_stock"]["stock_pieces"]))+" |")
            str_cut_with_arr.append(str(cut_stock["cut_stock"]["cut_width"])+str_length_unit)
            str_waste_arr.append(str(cut_stock["cut_stock"]["remaining_stock"])+str_length_unit)
            count += 1
        len_amount = max(len(max(str_amount_arr, key=len)),len(str_amount_header)) if len(str_amount_arr)>0 else len(str_amount_header)
        len_stock_length = max(len(max(str_stock_length_arr, key=len)),len(str_stock_length_header)) if len(str_stock_length_arr)>0 else len(str_stock_length_header)
        len_stock_pieces = max(len(max(str_stock_pieces_arr, key=len)),len(str_stock_pieces_header)) if len(str_stock_pieces_arr)>0 else len(str_stock_pieces_header)
        len_cut_width = max(len(max(str_cut_with_arr, key=len)),len(str_cut_width_header)) if len(str_cut_with_arr)>0 else len(str_cut_width_header)
        len_waste = max(len(max(str_waste_arr, key=len)),len(str_waste_header)) if len(str_waste_arr)>0 else len(str_waste_header)
        len_total = len_amount+len_stock_length+len_stock_pieces+len_cut_width+len_waste+4*len(str_padding)

        # Report title
        str_result = "\n"+"*"*len_total+"\n"+"*"+" "*(len_total-2)+"*\n"+"*"+f"{str(str_report_title).center(len_total-2)}"+"*\n"+"*"+" "*(len_total-2)+"*\n"+"*"*len_total+"\n\n"
        
        #Needed stock and waste title
        str_result += str_needed_stock_title.upper()+"\n\n"

        #Needed stock and waste
        str_result += str_stock_length_header+str_padding+str_amount_header+"\n"
        str_result += "="*len(str_stock_length_header)+str_padding+"="*len(str_amount_header)+"\n"
        for item in self.used_stock.items():
            str_result+=(str(item[0])+str_length_unit).rjust(len(str_stock_length_header))+str_padding
            str_result+=str(item[1]).rjust(len(str_amount_header))+"\n"
        str_result += "\n"+str_total_waste+" "+str(self.total_waste)+str_length_unit+"\n"
        str_result += "\n"+str_remaining_demand+" "+str(self.remaining_demand)+"\n"
        str_result += "\n"+str_remaining_stock+" "+str(self.remaining_stock)+"\n\n"

        # Cutting instrction title
        str_result += str_cutting_instruction_title.upper()+"\n\n"

        # Cutting instructions headers
        str_result += str_amount_header.ljust(len_amount)+str_padding
        str_result += str_stock_length_header.ljust(len_stock_length)+str_padding
        str_result += str_stock_pieces_header.ljust(len_stock_pieces)+str_padding
        str_result += str_cut_width_header.ljust(len_cut_width)+str_padding
        str_result += str_waste_header.ljust(len_waste)+"\n"
        str_result += "="*len_amount+str_padding+"="*len_stock_length+str_padding+"="*len_stock_pieces+str_padding+"="*len_cut_width+str_padding+"="*len_waste+str_padding+"\n"

        # Cutting instructions data
        for i in range(count):
            str_result += str_amount_arr[i].rjust(len_amount)+str_padding
            str_result += str_stock_length_arr[i].rjust(len_stock_length)+str_padding
            str_result += str_stock_pieces_arr[i].ljust(len_stock_pieces)+str_padding
            str_result += str_cut_with_arr[i].rjust(len_cut_width)+str_padding
            str_result += str_waste_arr[i].rjust(len_waste)+"\n"

        return str_result
    
    def to_html(self) -> str:
        svg_cutting_instruction = self.to_svg()
        html_cut_stock = ""

        # Needed stock data
        html_stock = ""
        for stock in self.used_stock.items():
            html_stock += self.__html_stock.format(
                stock_length = str(round(stock[0],self.__precision if self.__precision != 0 else None)), 
                stock_amount = str(stock[1])
                )
            
        # Cutting instruction list 
        for cut_stock in self.cut_stock_list:
            html_cut_stock += self.__html_cut_stock.format(
                repeat = cut_stock["amount"],
                stock_length = str(round(cut_stock["cut_stock"].stock_length,self.__precision if self.__precision != 0 else None)),
                cut_list = ", ".join(map(lambda x: str(round(x,self.__precision if self.__precision != 0 else None)),cut_stock["cut_stock"].stock_pieces)),
                cut_width = str(round(cut_stock["cut_stock"].cut_width,self.__precision if self.__precision != 0 else None)),
                waste = str(round(cut_stock["cut_stock"].remaining_stock,self.__precision if self.__precision != 0 else None))
            )

        # Remaining demand (only shown if remaining demand..)
        html_remaining_demand = ""
        if not self.completed:
            html_remaining_list = ""
            for remaining in self.remaining_demand.items():
                html_remaining_list += self.__html_stock.format(
                    stock_length = self.__html_warning_icon + str(remaining[0]),
                    stock_amount = remaining[1]
                )
            html_remaining_demand = self.__html_remaining_demand.format(
                html_remaining_list = html_remaining_list
            )

        # The compiled page
        return self.__html.format(
                svg_fav_icon = bp_svg.svg_icon(),
                html_stock = html_stock,
                html_cut_stock = html_cut_stock,
                svg_cutting_instruction = svg_cutting_instruction,
                svg_bp_logo = bp_svg.svg_logo(),
                html_remaining_demand = html_remaining_demand,
                method = self.method,
                scale = "" if self.__length_unit == "None" else length_unit_suffix[self.__length_unit] 
            )
    
    def to_svg(self, svg_width: float = 1600.0) -> str:
        
        if len(self.used_stock) == 0: return self.__empty_svg

        scale = svg_width/self.used_stock.max_length()
        svg_height = 0.0
        y_pos = 0.0

        stock_width = svg_width*0.02
        label_font_size = round(stock_width * 0.6)
        row_margin = label_font_size
        
        svg_body = ""
        for item in self.cut_stock_list:
            y_pos += row_margin
            svg_body += self.__svg_wood_label.format(
                x = 0.0,
                y = y_pos,
                str_amount = str(item["amount"])+" X ",
                stock_length = round(item["cut_stock"].stock_length,self.__precision if self.__precision != 0 else None)
            )
            y_pos += row_margin

            # Add waste if there is waste
            if (item["cut_stock"].remaining_stock>0):
                cut_stock_list = [("demand", x) for x in list(item["cut_stock"].stock_pieces)] + [("waste", item["cut_stock"].remaining_stock)]
            else:
                cut_stock_list = [("demand", x) for x in list(item["cut_stock"].stock_pieces)] 

            # Insert cuts
            result_list = []
            n = item["cut_stock"].number_of_cuts
            cut_element = ("cut",item["cut_stock"].cut_width)
            for i, item in enumerate(cut_stock_list):
                result_list.append(item)
                if i + 1 < len(cut_stock_list) and i + 1 <= n:
                    result_list.append(cut_element)

            cut_stock_list = result_list

            x_pos = 0.0

            for piece in cut_stock_list:
                font_size_spec = stock_width * 0.75
                font_size_calc = piece[1] * scale / len(str(piece[1])) * 3 / 2
                font_size = min(font_size_spec, font_size_calc)
                svg_body += self.__svg_wood.format(
                    cls = piece[0],
                    x = round(x_pos),
                    y = round(y_pos),
                    w = round(piece[1] * scale),
                    h = round(stock_width),
                    cx = round(piece[1] * scale/2),
                    cy = round(stock_width * 0.6),
                    txt_w = str(round(piece[1],self.__precision if self.__precision != 0 else None)),
                    font_size = round(font_size)
                )
                x_pos += piece[1]*scale

            y_pos += stock_width * 0.6 + row_margin

            svg_height = y_pos

        return self.__svg.format(
            document_width=round(svg_width),
            document_height=round(svg_height),
            pattern_size=round(svg_width/200),
            label_font_size=label_font_size,
            svg_body=svg_body
            )
        
    __empty_svg = """<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0">
  <!-- Empty SVG document -->
</svg>"""    

    __svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg id="bp_cutter" xmlns="http://www.w3.org/2000/svg" width="{document_width}" height="{document_height}" viewBox="0 0 {document_width} {document_height}">
    <defs>
        <pattern id="diagonal-lines" width="{pattern_size}" height="{pattern_size}" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="{pattern_size}" style="stroke: black; stroke-width: 1;" />
        </pattern>
        <style>
            .stock {{fill: none;stroke:#000}}
            .demand {{fill: rgba(249,249,249,1);stroke:none}}
            .cut {{fill: #000;stroke:none}}
            .waste {{fill: url(#diagonal-lines);stroke:none}}
            .textinside {{fill: #000;font-family: Arial, Helvetica, sans-serifs;text-anchor:middle;dominant-baseline: middle; font-weight:bold;}}
            .label {{fill: #000;font-family: Arial, Helvetica, sans-serifs;font-size:{label_font_size}px;text-anchor:left;dominant-baseline: middle; font-weight:bold;}}
        </style>
    </defs>
    {svg_body}
</svg>"""

    __svg_wood = """    <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}"/>
    <svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
        <text style="font-size:{font_size}px;" class="textinside" x="{cx}" y="{cy}">{txt_w}</text>
    </svg>    
    <rect class="stock" x="{x}" y="{y}" width="{w}" height="{h}"/>              
"""

    __svg_wood_label = """   <text class="label" x="{x}" y="{y}">{str_amount}{stock_length}</text>'
"""

    __html_stock = """<tr>
                        <td>{stock_length}</td>
                        <td>{stock_amount}</td>
                    </tr>
"""


    __html_cut_stock = """<tr>
                        <td>{repeat}</td>
                        <td>{stock_length}</td>
                        <td>{cut_list}</td>
                        <td>{cut_width}</td>
                        <td>{waste}</td>
                    </tr>
"""

    __html_remaining_demand = """<div class="container">
            <h2 class="sub-header" style="color:#900;"><span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;Warning - Remaining Demand!</h2>
            <div class="table-responsive">
                <table class="table table-striped" style="color:#900;">
                    <thead>
                        <tr>
                            <th>Demand</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_remaining_list}
                    </tbody>
                </table>
            </div>
        </div>"""

    __html_warning_icon = """<span class="glyphicon glyphicon-exclamation-sign"></span>&nbsp;"""


    __html = """<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Build Planner - Cutter Result</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css"
        integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    <link rel="icon"
        href="data:image/svg+xml,{svg_fav_icon}"
        type="image/svg+xml">
    <style>
        .container svg {{
            width: 100%;
            height: auto;
        }}
    </style>
</head>

<body>
    <div class="jumbotron">
        <div class="container">
            <h1>Build Planner</h1>
            <p>This page contains the Build Planner cutter result, using method {method}.</p>
        </div>
        {html_remaining_demand}
        <div class="container">
            <h2 class="sub-header">Needed Stock</h2>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Stock Length ({scale})</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_stock}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="container">
            <h2 class="sub-header">Cutting instruction</h2>
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Repeat</th>
                            <th>Stock Length ({scale})</th>
                            <th>Cuts ({scale})</th>
                            <th>Cut width ({scale})</th>
                            <th>Waste ({scale})</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_cut_stock}
                    </tbody>
                </table>
            </div>
        </div>
        <div class="container">
            <h2 class="sub-header">Cutting instruction</h2>
            {svg_cutting_instruction}
        </div>
        <div class="container" style="text-align: right;">  
            <hr>
            <div style="width: 20%; margin-left: auto;">
                {svg_bp_logo}
            </div>
        </div>
    </div>
</body>

</html>"""
