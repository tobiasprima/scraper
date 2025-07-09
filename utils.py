import logging

'''Function for initializing logging'''
def setup_logger(name, log_file, level):
    """To setup as many loggers as you want"""
    
    # date_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    # default_formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    
    log_format = '[%(asctime)s]:%(levelname)-7s:%(message)s'
    time_format = '%b-%d-%a:%H:%M:%S'
    color_formatter = logging.Formatter(log_format, datefmt=time_format)
    
    handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')        
    handler.setFormatter(color_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    
    return logger
    # logging.basicConfig(filename=f'{self.case_number}_{self.site_name}.log', filemode='w', encoding='utf-8', level=logging.DEBUG)
    # self.logger = logging.getLogger(__name__)
