import logging, os
from enum import Enum
class ErrorCategory(Enum):
    DBT = "dbt"
    DATABASE="database"
    VALIDATION="validation"
    GENERAL="general"
    
LOG_FILE_MAP = {
    ErrorCategory.DBT: "logs/DBT/dbt_error.log",
    ErrorCategory.DATABASE: "logs/DATABASE/database_error.log",
    ErrorCategory.VALIDATION: "logs/VALIDATION/validation_error.log",
    ErrorCategory.GENERAL: "logs/GENERAL/general.log"
}
    
FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

class ETL_Logger:
    def __init__(self,category: ErrorCategory = ErrorCategory.GENERAL):
        #checks if object belongs to a class 
        if not isinstance(category, ErrorCategory):
            try: 
                category=ErrorCategory(str(category).lower())
            except ValueError:
                category=ErrorCategory.GENERAL 
                
        self.category = category
        logger_name = f"ETL_Logger.{category.value}"
        self.logger = logging.getLogger(logger_name)
        self._setup(category)
                
    def _setup(self, category: ErrorCategory):
        
        if self.logger.handlers:
            return
        
        self.logger.setLevel(logging.DEBUG)
        
        log_path = LOG_FILE_MAP[category]
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(logging.Formatter(FORMAT))
        self.logger.addHandler(file_handler)
        
    def error(self, message:str):
        self.logger.error(message)
        
    def warning(self, message:str):
        self.logger.warning(message)
        
    def info(self, message:str):
        self.logger.info(message)
        
    def debug(self, message:str):
        self.logger.debug(message)
        