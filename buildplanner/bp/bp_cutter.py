# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_cutter.py
# Author: Magnus Pettersson
#
# This module provides a class for cutting stock pieces to fulfill demand. 
# It's commonly used in manufacturing and logistics to optimize the use of 
# available stock material while meeting the requirements of customer demand.
#
# The BPCutter class includes methods for performing cutting operations using 
# different algorithms such as optimal, greedy, and experimental. These algorithms 
# determine the most efficient way to cut stock pieces to minimize waste and 
# fulfill demand.
#
# The cutting process involves taking a set of available stock pieces and a 
# corresponding demand for stock pieces. The goal is to find the optimal way 
# to cut the available stock pieces to meet the demand, considering factors 
# such as stock dimensions, demand quantities, and cutting width.
#
# The module includes the following classes and enums:
# - BPCutter: The main class for performing cutting operations.
# - METHOD Enum: An enumeration of available cutting methods (OPT, GREEDY, EXPERIMENTAL).
# - BPDataStockPieces: A class representing a collection of stock pieces.
# - BPDataCutStock: A class representing a cut piece of stock material.
# - BPDataCutterResult: A class representing the result of a cutting operation.
#
#------------------------------------------------------------------------------

from enum import Enum, auto

from bp.bp_data_classes import (
    BPDataStockPieces,
    BPDataCutStock,
    BPDataCutterResult,
)

from bp.bp_log import BPLog

from bp.bp_type_check import type_check_class

@type_check_class
class BPCutter:
    """
    Class for cutting stock pieces to fulfill demand.
    """

    class METHOD(Enum):
        OPT = auto()
        GREEDY = auto()
        EXPERIMENTAL = auto()

    @property
    def result(self) -> BPDataCutterResult:
        return self.__result

    def __init__(
            self, 
            stock: BPDataStockPieces, 
            demand: BPDataStockPieces, 
            cut_width: float = 0.0, 
            method: METHOD = METHOD.OPT, 
            length_unit: str = "NONE", 
            original_length_unit: str = "NONE",
            precision: int = 0
            ) -> None:
        """
        Initializes the BPCutter instance.

        Args:
            stock (BPDataStockPieces): The available stock pieces.
            demand (BPDataStockPieces): The demand for stock pieces.
            cut_width (float, optional): The width to be cut from stock pieces. Defaults to 0.0.
            method (METHOD, optional): The cutting method to be used. Defaults to METHOD.OPT.
            length_unit (str, optional): The unit of length for stock pieces. Defaults to "NONE".
            original_length_unit (str, optional): The original unit of length for stock pieces. Defaults to "NONE".
            precision (int, optional): The precision for calculations. Defaults to 0.
        """
        self.__stock = stock.copy()
        self.__demand = demand.copy()
        self.__cut_width = cut_width
        self.__result = BPDataCutterResult(
            precision=precision,
            length_unit=length_unit,
            original_length_unit=original_length_unit,
            available_stock=stock.copy()
        )
        self.__method = method
        self.__log = BPLog()

    def cut(self, method: METHOD = None) -> None:
        """
        Performs the cutting operation based on the specified method, which can be
        one of the following:
        - BPCutter.METHOD.GREEDY
        - BPCutter.METHOD.EXPERIMENTAL
        - BPCutter.METHOD.OPT - Which uses both the methods above, returning the 
          best result based on minimized waste

        Args:
            method (METHOD, optional): The cutting method to be used. Defaults to None.
            
        """
        self.__log.debug("Stock: " + str(self.__stock))
        self.__log.debug("Demand: " + str(self.__demand))
        if len(self.__demand) == 0:
            return None
        if len(self.__stock) == 0:
            self.__result.remaining_demand = self.__demand
            return None
        method = self.__method if method == None else method
        if method == self.METHOD.OPT:
            results = []
            results.append(self.__greedy_cut())
            results.append(self.__experimental_cut())
            min_waste = None
            for result in results:
                if result != None:
                    self.__log.debug("Waste from " + result.method + ": " + str(result.total_waste))
                    if min_waste == None or result.total_waste < min_waste:
                        min_waste = result.total_waste
                        self.__result = result
        elif method == self.METHOD.GREEDY:
            self.__result = self.__greedy_cut()
        elif method == self.METHOD.EXPERIMENTAL:
            self.__result = self.__experimental_cut()
        return None
    
    def cut_iter(self, method: METHOD = None) -> None:
        """
        Performs the cutting operation iteratively based on the specified method.

        Args:
            method (METHOD, optional): The cutting method to be used. Defaults to None.
        """
        self.__log.debug("Stock: " + str(self.__stock))
        self.__log.debug("Demand: " + str(self.__demand))
        if len(self.__demand) == 0:
            return None
        if len(self.__stock) == 0:
            self.__result.set_remaining_demand(self.__demand)
            return None
        method = self.__method if method == None else method
        if method == self.METHOD.OPT:
            results = []
            for step in self.__greedy_cut_iter():
                yield step
            results.append(step[2])
            for step in self.__experimental_cut_iter():
                yield step
            results.append(step[2])
            min_waste = None
            for result in results:
                if result != None:
                    self.__log.debug("Waste from " + result.method + ": " + str(result.total_waste))
                    if min_waste == None or result.total_waste < min_waste:
                        min_waste = result.total_waste
                        self.__result = result
        elif method == self.METHOD.GREEDY:
            for step in self.__greedy_cut_iter():
                yield step
            self.__result = step[2]
        elif method == self.METHOD.EXPERIMENTAL:
            for step in self.__experimental_cut_iter():
                yield step
            self.__result = step[2]

    # ******** Experimental Cut ******** 

    def __experimental_cut_iteration(self, stock, demand, stock_in_use) -> bool:
        """
        Perform one iteration of the experimental cutting algorithm.

        Args:
            stock ([type]): [description]
            demand ([type]): [description]
            stock_in_use ([type]): [description]

        Returns:
            bool: [description]
        """
        min_waste = max(self.__stock)
        demand.clean()
        result = None
        for piece in demand.keys():
            for i in range(len(stock_in_use)):
                if piece <= stock_in_use[i][1]:
                    waste = stock_in_use[i][1] - (self.__cut_width + piece)
                    if waste < min_waste:
                        result = (piece, i)
                        min_waste = waste
        if result != None:
            original_stock_length = stock_in_use[result[1]][0]
            if not stock_in_use[result[1]][3]:
                if stock[original_stock_length] > 0:
                    stock_in_use.append([original_stock_length, original_stock_length, [], False])
                    stock[original_stock_length] -= 1
            stock_in_use[result[1]][1] = max(0.0, stock_in_use[result[1]][1] - (result[0] + self.__cut_width))
            stock_in_use[result[1]][2].append(result[0])
            stock_in_use[result[1]][3] = True
            demand[result[0]] -= 1
            return True
        else:
            return False

    def __experimental_cut_add_stock(self, stock, stock_in_use) -> bool:
        """
        Add available stock to the stock in use for experimental cutting.

        Args:
            stock ([type]): [description]
            stock_in_use ([type]): [description]

        Returns:
            bool: [description]
        """
        is_available = False
        for key, value in stock.items():
            if value > 0:
                is_available = True 
                stock[key] -= 1
                stock_in_use.append([key, key, [], False])
        return is_available
            
    def __experimental_cut(self) -> BPDataCutterResult:
        """
        Perform the experimental cutting operation.

        Returns:
            BPDataCutterResult: [description]
        """
        return max(self.__experimental_cut_iter())[2]

    def __experimental_cut_iter(self) -> BPDataCutterResult:
        """
        Perform the experimental cutting operation iteratively.

        Yields:
            BPDataCutterResult: [description]
        """
        demand = self.__demand.copy()
        stock = self.__stock.copy()
        experimental_result = BPDataCutterResult(
            precision=self.__result.precision,
            length_unit=self.__result.length_unit,
            original_length_unit=self.__result.original_length_unit,
            available_stock=self.__stock
        )
        stock_in_use = []
        self.__experimental_cut_add_stock(stock, stock_in_use)
        while True:
            yield (False, "Experimental Cut", None, len(demand))
            if not self.__experimental_cut_iteration(stock, demand, stock_in_use):
                break

        for stock_to_use in stock_in_use:
            if stock_to_use[3]:
                experimental_result.append(
                    BPDataCutStock(
                        stock_to_use[0],
                        self.__cut_width,
                        BPDataStockPieces(stock_to_use[2])
                    )
                )

        experimental_result.remaining_demand = demand
        experimental_result.method = "Experimental"

        yield (True, "Experimental Cut", experimental_result, len(demand))

    # ******** Greedy Cut ******** 

    def __greedy_cut_iteration(self, stock: float, demand: BPDataStockPieces, cut: float):
        """
        Perform one iteration of the greedy cutting algorithm.

        Args:
            stock (float): [description]
            demand (BPDataStockPieces): [description]
            cut (float): [description]

        Returns:
            [type]: [description]
        """
        result = BPDataStockPieces()
        cut_waste = 0.0
        number_of_cuts = 0
        remaining_demand = demand.copy()
        remanining_stock = stock
        for length in remaining_demand.keys():
            while True:
                if remaining_demand[length] > 0:
                    if remanining_stock >= length:
                        remanining_stock = remanining_stock - length - min(cut, (remanining_stock - length))
                        remaining_demand[length] -= 1
                        result.append(length)
                        cut_waste += cut
                        number_of_cuts += 1
                    else:
                        break
                else:
                    break
        return {
            "result": result,
            "waste": remanining_stock,
            "remaining_demand": remaining_demand,
            "tot_waste": remanining_stock + cut_waste,
            "number_of_cuts": number_of_cuts
        }

    def __greedy_cut(self) -> BPDataCutterResult:
        """
        Perform the greedy cutting operation.

        Returns:
            BPDataCutterResult: [description]
        """
        return max(self.__greedy_cut_iter())[2]

    def __greedy_cut_iter(self) -> BPDataCutterResult:
        """
        Perform the greedy cutting operation iteratively.

        Yields:
            BPDataCutterResult: [description]
        """
        demand = self.__demand.copy()
        stock = self.__stock.copy()
        greedy_result = BPDataCutterResult(
            precision=self.__result.precision,
            length_unit=self.__result.length_unit,
            original_length_unit=self.__result.original_length_unit,
            available_stock=self.__stock
        )

        while True:
            if len(stock) <= 0:
                break
            result = {}
            min_waste = max(stock)
            optimal_length = None
            for stock_length in stock.keys():
                if stock[stock_length] > 0:
                    result[stock_length] = self.__greedy_cut_iteration(stock_length, demand, self.__cut_width)
                    if result[stock_length]["tot_waste"] < min_waste: 
                        min_waste = result[stock_length]["tot_waste"]
                        optimal_length = stock_length
                yield (False, "Greedy Cut", None, len(demand))
            if optimal_length == None:
                break
            if len(result[optimal_length]["result"]) == 0:
                break
            demand = result[optimal_length]["remaining_demand"]
            cut_stock = BPDataCutStock(
                optimal_length,
                self.__cut_width,
                result[optimal_length]["result"]
            )
            greedy_result.append(cut_stock)
            stock[optimal_length] -= 1

        remaining_demand = BPDataStockPieces()
        for key in demand.keys():
            if demand[key] > 0:
                remaining_demand[key] = demand[key]
        greedy_result.remaining_demand = remaining_demand
        
        greedy_result.method = "Greedy Cut"
        yield (True, "Greedy Cut", greedy_result, len(demand))