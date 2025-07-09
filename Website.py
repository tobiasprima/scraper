import asyncio
import json
import logging
import os
from exceptions import *
from datetime import datetime
from utils import *

import aiofiles
from playwright.async_api import Browser

from exceptions import PlaywrightException


class Website:
    """
    Base class for all website scraping classes.
    Handles browser setup, structured JSON output, and error logging.
    """

    client_data_dir = "client_data"
    default_timeout = 60000

    def __init__(self):
        self.case_number = ""
        self.browser: Browser = None
        self.context = None
        self.site_name = ""
        self.exception = None
        self.JSON_FILE = {
            "Site Name": "",
            "Case Number": "",
            "start_time": "",
            "end_time": "",
            "run_time": "",
            "message": "",
        }
        
        try:
            self.logger = setup_logger(name=f"{self.site_name}_logger", log_file=f"{self.case_number}_{self.site_name}.log", level=logging.DEBUG)
        except Exception as e:
            raise RuntimeError(f"Failed to set up logger for {self.site_name}. Error: {str(e)}")
        

    async def async_init(self, browser):
        """Initialize Playwright browser context"""
        self.browser = browser
        try:
            self.context = await self.browser.new_context()
            await self.context.grant_permissions(['geolocation'])
        except Exception as e:
            await self.exception_execution(PlaywrightException, e, "Error starting context")
            raise

    async def exception_execution(self, exception_type: Exception, exc: Exception, message: str):
        """
        Logs exception and writes failure details to the JSON file.
        """
        if not self.JSON_FILE["message"]:
            full_message = f"[{self.site_name}] {message}"
            self.exception = exception_type(full_message)
            self.JSON_FILE["message"] = f"{type(self.exception).__name__}: {str(self.exception)}"
            self.logger.exception(exc)
            self.logger.error(self.JSON_FILE["message"])

        async with aiofiles.open(f"{self.JSON_FILE['Case Number']}_{self.site_name}.json", 'w', encoding='utf-8') as f:
            await f.write(json.dumps(self.JSON_FILE, indent=4, ensure_ascii=False))

    def warning_execution(self, exc: Exception, message: str):
        """Log a non-fatal warning"""
        self.logger.warning(f"[{self.site_name}] {message}\nError: {exc}")

    async def save_JSON_FILE(self):
        """Write final JSON result after scrape ends"""
        try:
            self.JSON_FILE["end_time"] = str(datetime.now())
            start = datetime.strptime(self.JSON_FILE["start_time"], '%Y-%m-%d %H:%M:%S.%f')
            end = datetime.strptime(self.JSON_FILE["end_time"], '%Y-%m-%d %H:%M:%S.%f')
            self.JSON_FILE["run_time"] = str(end - start)
            self.JSON_FILE["message"] = "Success!"
            self.logger.info(self.JSON_FILE)

            async with aiofiles.open(f"{self.JSON_FILE['Case Number']}_{self.site_name}.json", 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self.JSON_FILE, indent=4, ensure_ascii=False))

        except Exception as e:
            await self.exception_execution(Exception, e, "Error saving data to JSON")
            raise

    async def scrape(self):
        """To be implemented by subclasses"""
        pass
