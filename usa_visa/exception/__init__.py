import os
import sys

def error_message_detail(error, error_detail: sys): # type: ignore
    """
    Creates a detailed error message with the filename, line number, and error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename # type: ignore
    error_message = (
        f"Error occurred in python script [{file_name}] "
        f"at line [{exc_tb.tb_lineno}] " # type: ignore
        f"with error message: [{str(error)}]"
    )
    return error_message

class USVisaException(Exception):
    def __init__(self, error, error_detail: sys): # type: ignore
        """
        :param error: Exception object
        :param error_detail: sys module to extract traceback
        """
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self):
        return self.error_message
