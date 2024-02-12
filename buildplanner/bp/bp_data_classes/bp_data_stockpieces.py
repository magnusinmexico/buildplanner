# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_data_stockpieces.py
# Author: Magnus Pettersson
#
# This module defines the BPDataStockPieces class, a data class for
# representing pieces of stock in a build planner application. The class
# encapsulates information about the lengths and quantities of stock pieces,
# providing methods for manipulation and analysis of stock piece data.
#
# The BPDataStockPieces class allows for the representation and management of
# stock pieces in various formats, including dictionaries and lists. It
# provides methods for accessing, modifying, and analyzing stock piece data,
# such as retrieving keys and values, sorting pieces by length, cleaning the
# data, and performing arithmetic operations with other instances of
# BPDataStockPieces. Additionally, the class supports iteration over the
# stock pieces and provides functionality for calculating the maximum and
# minimum piece lengths.
#
# With its comprehensive set of methods, the BPDataStockPieces class serves as
# a versatile tool for handling stock piece data within the build planner
# system, facilitating efficient management of inventory and optimization of
# cutting operations.
#
#------------------------------------------------------------------------------

from dataclasses import dataclass

from bp.bp_type_check import *
from bp.bp_utils import *

@type_check_class
@dataclass
class BPDataStockPieces:

    __stock_pieces : list

    def __init__(self,stock_pieces={}):
        stock_pieces_data_ok = True
        if isinstance(stock_pieces,BPDataStockPieces):
            self.__init__(dict(stock_pieces))
        elif isinstance(stock_pieces,dict):
            if dict_contains_number_keys_and_int_values(stock_pieces):
                self.__stock_pieces=[]
                for key, value in stock_pieces.items():
                    self.__stock_pieces.append({float(key):value})
                self.__stock_pieces = sorted(self.__stock_pieces, key=lambda d: list(d.keys())[0],reverse=True)
            else:
                stock_pieces_data_ok = False
        elif isinstance(stock_pieces,list):
            if list_contains_numbers(stock_pieces):
                self.__init__(make_list_quantitative_dict(stock_pieces))
            elif list_contains_dicts(stock_pieces):
                if all(dict_contains_number_keys_and_int_values(dict(items)) for items in stock_pieces):
                    self.__stock_pieces=[]
                    for item in stock_pieces:
                        self.update(BPDataStockPieces(item))
            else:
                stock_pieces_data_ok = False
        elif isinstance(stock_pieces,float) or isinstance(stock_pieces,int):
            self.__init__({float(stock_pieces):1})
        else:
            stock_pieces_data_ok = False
        assert stock_pieces_data_ok, "Parameter 'stock_pieces' must be either a dict[float,int], a list[float], an int, or a float."

    def __repr__(self):
        return str(dict(self))
    
    def __str__(self):
        return str(dict(self))
    
    def keys(self):
        return [list(d.keys())[0] for d in self.__stock_pieces]
    
    def values(self):
        return [list(d.values())[0] for d in self.__stock_pieces]
    
    def items(self):
        return dict(zip(self.keys(),self.values())).items()
    
    def copy(self):
        return BPDataStockPieces(dict(zip(self.keys(),self.values())))

    def __getitem__(self, key) -> int: # As no annotation, the type check does not "kick in" 
        if isinstance(key,int):
            return list(self)[key]
        elif isinstance(key,slice):
            return list(self)[key]
        elif not isinstance(key,float):
            raise TypeError(f"Argument 'key' should be of type <class 'float'> but was {type(key)}")
        elif not key in self.keys(): 
            raise KeyError(f"The key '{key}' does not exists in this instance of BPDataStockPieces")
        return dict(zip(self.keys(),self.values()))[key]
    
    def __setitem__(self, key : float, value : int) -> None:
        for i in range(len(self.__stock_pieces)):
            if key in self.__stock_pieces[i].keys():
                self.__stock_pieces[i][key] = value
                return None
        new_item = {key:value}
        self.__stock_pieces.append(new_item)
        self.sort()

    def append(self, piece_length : float):
        if piece_length in self.keys(): self[piece_length] +=1
        else: self[piece_length] = 1

    def update(self, stock_pieces : 'BPDataStockPieces') -> 'BPDataStockPieces':
        for key in stock_pieces.keys():
            self.__setitem__(key,stock_pieces[key])
        return self

    def __len__(self):
        return sum(self.values())
    
    def __iter__(self):
        for key in self.keys():
            for i in range(self[key]):
                yield key

    def max_length(self):
        return max(self.keys()) if len(self)>0 else 0.0
    
    def min_length(self):
        return min(self.keys()) if len(self)>0 else 0.0
    
    def sort(self, reverse:bool=True) -> 'BPDataStockPieces':
        self.__stock_pieces = sorted(self.__stock_pieces, key=lambda d: list(d.keys())[0],reverse=reverse)
        return self
    
    def clean(self, min_value:float = 0.0) -> 'BPDataStockPieces':
        self.__stock_pieces = [d for d in self.__stock_pieces if list(d.values())[0] > 0]
        self.__stock_pieces = [d for d in self.__stock_pieces if list(d.keys())[0] >= min_value]
        return self
    
    def __iadd__(self, bp_data_stock_pieces : 'BPDataStockPieces') -> 'BPDataStockPieces':
        for key, value in bp_data_stock_pieces.items():
            if key in self.keys():
                self[key] += value
            else:
                self[key] = value
        return self

    def __add__(self, bp_data_stock_pieces : 'BPDataStockPieces') -> 'BPDataStockPieces':
        bp_data_stock_pieces_new = BPDataStockPieces(self)
        for key, value in bp_data_stock_pieces.items():
            if key in bp_data_stock_pieces_new.keys():
                bp_data_stock_pieces_new[key] += value
            else:
                bp_data_stock_pieces_new[key] = value
        return bp_data_stock_pieces_new
    
    def __isub__(self, bp_data_stock_pieces : 'BPDataStockPieces') -> 'BPDataStockPieces':
        for key, value in bp_data_stock_pieces.items():
            if key in self.keys():
                self[key] = max(0,self[key]-value)
        return self

    def __sub__(self, bp_data_stock_pieces : 'BPDataStockPieces') -> 'BPDataStockPieces':
        bp_data_stock_pieces_new = BPDataStockPieces(self)
        for key, value in bp_data_stock_pieces.items():
            if key in bp_data_stock_pieces_new.keys():
                bp_data_stock_pieces_new[key] = max(0,bp_data_stock_pieces_new[key]-value)
        return bp_data_stock_pieces_new

    def __hash__(self):
        return hash(str(self.__stock_pieces))


