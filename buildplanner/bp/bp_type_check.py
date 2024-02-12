# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_type_check.py
# Author: Magnus Pettersson
#
# This code provides functionality for type checking function arguments and 
# class attributes in Python. It uses annotations to specify the expected types
# of arguments and attributes and raises TypeError exceptions if the actual
# types do not match the expected types.
#
# The type_check_func function is a decorator that wraps around functions. It 
# checks the types of function arguments against their annotations and raises 
# TypeError if the types do not match.
#
# The type_check_class function is a decorator for classes. It checks the types
# of class attributes against their annotations and raises TypeError if the 
# types do not match.
#
# If bp_debug is not imported, both type_check_func and type_check_class 
# functions return the original functions and classes, effectively disabling 
# type checking.
#
#------------------------------------------------------------------------------

# Import necessary modules
import sys

# Check if the `bp_debug` module is imported
typecheck = ("bp_debug" in sys.modules)

# Enable type checking if `bp_debug` is imported
if typecheck:
    from pathlib import Path
    from functools import wraps
    import inspect
    import traceback

#------------------------------------------------------------------------------
#
# type_check_func
# Decorator function for type checking function arguments
#
#------------------------------------------------------------------------------
        
    def type_check_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            annotations = func.__annotations__
            all_args = dict(zip(func.__code__.co_varnames, args))
            all_args.update(kwargs)
            for arg_name, arg_value in all_args.items():
                if arg_name != 'self':
                    if arg_name in annotations:
                        frame_record = traceback.extract_stack(limit=2)[:-1][0]
                        traceback_info = f"On line {frame_record.lineno} in {frame_record.name} located in file: '{Path(frame_record.filename).name}' Code: {frame_record.line}"
                        if isinstance(annotations[arg_name], type):
                            if not isinstance(arg_value, annotations[arg_name]):
                                if str(annotations[arg_name].__name__) != str(type(arg_value).__name__):
                                    raise TypeError(f"{traceback_info}Argument '{arg_name}' should be of type {annotations[arg_name].__name__} but was {type(arg_value).__name__}")
                        elif isinstance(annotations[arg_name], str):
                            if not annotations[arg_name] == type(arg_value).__name__:
                                if annotations[arg_name] != str(type(arg_value).__name__):
                                    raise TypeError(f"{traceback_info}Argument '{arg_name}' should be of type {annotations[arg_name]} but was {type(arg_value).__name__}")
                        else:
                            raise TypeError(f"{traceback_info}Unexpected type: {str(annotations[arg_name])}")

            result = func(*args, **kwargs)
            return result
        return wrapper
    
#------------------------------------------------------------------------------
#
# type_check_class
# Decorator function for type checking class attributes
#
#------------------------------------------------------------------------------

    def type_check_class(SourceClass):
        methods = [t[1] for t in inspect.getmembers(SourceClass, predicate=inspect.isfunction)]
        for name, method in SourceClass.__dict__.items():
            if method in methods and not isinstance(method, property):
                setattr(SourceClass, name, type_check_func(method))
            elif name[-2:] != "__":
                setattr(SourceClass, name, method)
        if len(SourceClass.__annotations__) > 0:
            def __setattr(self, attribute, value):
                if attribute in self.__annotations__:
                    if type(value) == self.__annotations__[attribute]:
                        self.__dict__[attribute] = value
                    elif str(type(value).__name__) == str(self.__annotations__[attribute].__name__):
                        self.__dict__[attribute] = value
                    else:
                        frame_record = traceback.extract_stack(limit=4)[:-3][0]
                        traceback_info = f"On line {frame_record.lineno} in {frame_record.name} located in file: '{Path(frame_record.filename).name}' Code: {frame_record.line}"
                        raise TypeError(f"{traceback_info}'{attribute}' should be of type {self.__annotations__[attribute].__name__}, not {type(value).__name__} as given.")
                elif attribute in type(self).__dict__.keys() and attribute[:2] != "__":
                    self.__setattr_orig(attribute, value)
                else:
                    frame_record = traceback.extract_stack(limit=3)[:-2][0]
                    traceback_info = f"On line {frame_record.lineno} in {frame_record.name} located in file: '{Path(frame_record.filename).name}' Code: {frame_record.line}"
                    raise Exception(f"{traceback_info}The class {type(self).__name__} has no assignable member {attribute}")
        try:
            type(__setattr)
        except:
            pass
        else:
            SourceClass.__setattr_orig = SourceClass.__setattr__
            SourceClass.__setattr__ = __setattr
        return SourceClass

else:
    # If `bp_debug` is not imported, do not perform any type checking
    def type_check_func(func):
        return func

    def type_check_class(SourceClass):
        return SourceClass