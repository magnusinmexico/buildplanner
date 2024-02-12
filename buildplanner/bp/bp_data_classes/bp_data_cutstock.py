# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_data_cutstock.py
# Author: Magnus Pettersson
#
# This module defines the BPDataCutStock class, a data class for representing
# cut stock data in a build planner application. The class encapsulates
# information about the length of the stock, the width of cuts made from the
# stock, and the pieces of stock remaining after cutting. It provides
# properties and methods to calculate the remaining stock, the total number of
# cuts, and to validate the cut stock data.
#
# The BPDataCutStock class serves as a fundamental data structure for managing
# and analyzing stock pieces used in cutting operations. It enables users to
# track the usage of stock materials, calculate the amount of waste generated
# during cutting, and verify the integrity of cut stock data. With its
# properties and methods, the class facilitates efficient management of stock
# inventory and optimization of cutting processes within the build planner
# system.
#
#------------------------------------------------------------------------------


from dataclasses import dataclass
from bp.bp_type_check import type_check_class
from bp.bp_data_classes import BPDataStockPieces

@type_check_class
@dataclass
class BPDataCutStock:
    """Data class for representing cut stock data."""

    # Properties
    stock_length: float
    cut_width: float
    stock_pieces: BPDataStockPieces

    @property
    def remaining_stock(self) -> float:
        """Calculate the remaining stock after cuts."""
        precision = max(len(str(length).split(".")[1]) for length in self.stock_pieces)
        return round(max(0.0, self.stock_length - sum(self.stock_pieces) - self.number_of_cuts * self.cut_width), precision)
    
    @property
    def number_of_cuts(self) -> int:
        """Calculate the total number of cuts."""
        length = 0.0
        cuts = 0
        for piece in self.stock_pieces:
            length += piece + self.cut_width
            cuts += 1
        if length > self.stock_length: 
            cuts -= 1
        return cuts
    
    @property 
    def is_valid(self) -> bool:
        """Check if the cut stock data is valid."""
        return (sum(self.stock_pieces) + self.number_of_cuts * self.cut_width) <= self.stock_length

    # Constructor
    def __init__(self, stock_length: float, cut_width: float, stock_pieces: BPDataStockPieces) -> None:
        """Initialize a BPDataCutStock object."""
        self.stock_length = stock_length
        self.cut_width = cut_width
        self.stock_pieces = stock_pieces.copy()

    # String representation
    def __repr__(self):
        """Return a string representation of the object."""
        return str(dict(zip(self.keys(), self.values())))
    
    def __str__(self):
        """Return a string representation of the object."""
        return str(dict(zip(self.keys(), self.values())))
    
    # Copy method
    def copy(self):
        """Create a copy of the object."""
        return BPDataCutStock(self.stock_length, self.cut_width, self.stock_pieces.copy())
    
    # Key and value methods
    def keys(self):
        """Return the keys of the object."""
        return ["stock_length", "cut_width", "number_of_cuts", "stock_pieces", "remaining_stock", "is_valid"]
    
    def values(self):
        """Return the values of the object."""
        return [self.stock_length, self.cut_width, self.number_of_cuts, self.stock_pieces, self.remaining_stock, self.is_valid]
    
    # Hash method
    def __hash__(self):
        """Return the hash value of the object."""
        return hash(str(self))
    
    # Items method
    def items(self):
        """Return the items of the object."""
        return dict(zip(self.keys(), self.values())).items()
    
    # Getitem method
    def __getitem__(self, key):
        """Get an item from the object."""
        if not key in self.keys(): 
            raise KeyError(f"The key '{key}' does not exist in this instance of BPDataCutStock")
        return dict(zip(self.keys(), self.values()))[key]