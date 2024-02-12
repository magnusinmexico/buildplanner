# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_log.py
# Author: Magnus Pettersson
#
# This module provides a logging class with severity levels for Python programs.
# It allows logging messages with different severity levels such as ERROR, WARNING,
# INFO, and DEBUG. The severity levels help in categorizing and prioritizing 
# log messages based on their importance and criticality.
#
#------------------------------------------------------------------------------

import inspect

from bp.bp_type_check import type_check_class

@type_check_class
class BPLog:
    """
    Class for logging messages with severity levels.
    """

    class SEVERITY:
        NONE = 0
        ERROR = 1
        WARNING = 2
        INFO = 3
        DEBUG = 4

    __log = None

    __calling_class: str = None
    __severity: int = SEVERITY.ERROR

    def __init__(self):
        """
        Initializes the BPLog instance.
        """
        if BPLog.__log is None:
            BPLog.__log = []
        self.__calling_class = inspect.currentframe().f_back.f_back.f_locals.get('self').__class__.__name__
        if self.__severity >= BPLog.SEVERITY.DEBUG:
            self.__add_to_log(self.__calling_class, BPLog.SEVERITY.DEBUG, f"BPLog activated for class '{self.__calling_class}'")

    def __add_to_log(self, calling_class: str, severity: int, message: str):
        """
        Adds a log entry to the log list.
        
        Args:
            calling_class (str): The name of the calling class.
            severity (int): The severity level of the log message.
            message (str): The log message.
        """
        assert calling_class == self.__calling_class, f"{calling_class} is not allowed to call BPLog for {self.__calling_class}"
        BPLog.__log.append((calling_class, severity, message))

    def debug(self, message: str = ""):
        """
        Logs a debug message.
        
        Args:
            message (str, optional): The debug message. Defaults to "".
        """
        if self.__severity >= BPLog.SEVERITY.DEBUG:
            calling_class = inspect.currentframe().f_back.f_back.f_locals.get('self').__class__
            self.__add_to_log(calling_class.__name__, BPLog.SEVERITY.DEBUG, message)

    def info(self, message: str = ""):
        """
        Logs an info message.
        
        Args:
            message (str, optional): The info message. Defaults to "".
        """
        if self.__severity >= BPLog.SEVERITY.INFO:
            calling_class = inspect.currentframe().f_back.f_back.f_locals.get('self').__class__
            self.__add_to_log(calling_class.__name__, BPLog.SEVERITY.INFO, message)

    def warning(self, message: str = ""):
        """
        Logs a warning message.
        
        Args:
            message (str, optional): The warning message. Defaults to "".
        """
        if self.__severity >= BPLog.SEVERITY.WARNING:
            calling_class = inspect.currentframe().f_back.f_back.f_locals.get('self').__class__
            self.__add_to_log(calling_class.__name__, BPLog.SEVERITY.WARNING, message)

    def error(self, message: str = ""):
        """
        Logs an error message.
        
        Args:
            message (str, optional): The error message. Defaults to "".
        """
        if self.__severity >= BPLog.SEVERITY.ERROR:
            calling_class = inspect.currentframe().f_back.f_back.f_locals.get('self').__class__
            self.__add_to_log(calling_class.__name__, BPLog.SEVERITY.ERROR, message)

    def clear(self=None):
        """
        Clears the log.
        
        Args:
            self: The instance of BPLog. Defaults to None.
        """
        if (self != None):
            BPLog.__log = [item for item in BPLog.__log if item[0] != self.__calling_class]
        else:
            BPLog.__log = []

    def dump(self=None):
        """
        Returns the log entries.
        
        Args:
            self: The instance of BPLog. Defaults to None.
        
        Returns:
            list: List of log entries.
        """
        if (self != None):
            return [(item[0], item[1], item[2]) for item in BPLog.__log if item[0] == self.__calling_class]
        return BPLog.__log
    
    def to_str(self=None):
        """
        Returns the log entries as a string.
        
        Args:
            self: The instance of BPLog. Defaults to None.
        
        Returns:
            str: String representation of log entries.
        """
        str_response = ""
        if (self != None):
            logitems = [(item[0], item[1], item[2]) for item in BPLog.__log if item[0] == self.__calling_class]
        else:
            logitems = BPLog.__log
        for line in logitems:
            str_response += ["","ERROR","WARNING","INFO","DEBUG"][line[1]]+" : "+line[0]+" : "+line[2]+"\n"
        return str_response
    
    def __iter__(self):
        """
        Iterator method to iterate through log entries.
        """
        for i in [(item[0], item[1], item[2]) for item in BPLog.__log if item[0] == self.__calling_class]:
            yield i
    
    def __str__(self):
        """
        String representation of log entries.
        """
        return self.to_str()
    
    def set_severity(severity: int):
        """
        Sets the severity level for logging.
        
        Args:
            severity (int): The severity level to be set.
        """
        BPLog.__severity = severity
