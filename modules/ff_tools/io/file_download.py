# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from typing import Optional
from pathlib import Path
import requests
import os
import time
import logging

logger = logging.getLogger(__name__)


def download_file_cached(
        url: str,
        output_path: str,
        *,
        force: bool = False,
        expiration_days: int = 14,
        bearer_token: Optional[str] = None,
    ):
    """
    Download a file from a HTTP server using GET request with bearer token authentication.
    If the file already exists locally, and force is false, and the file is not older than
    `expiration_days`, it will not be downloaded again.
    
    Args:
        url (str): The URL of the file to download
        output_path (str): Local path where the file should be saved
        bearer_token (str): The bearer token for authorization
    """
    if not force:
        if os.path.exists(output_path):
            # check if file is older than expiration_days
            file_age = os.path.getmtime(output_path)
            current_time = time.time()
            age_days = (current_time - file_age) / (60 * 60 * 24)

            if age_days < expiration_days:
                logger.debug(f"File in local cache, skipping: {output_path}")
                return True
            else:
                logger.debug(f"File in local cache is expired: {output_path}")
                os.remove(output_path)

    else:
        logger.debug(f"Forcing download: {output_path}")

    download_file(url, output_path, bearer_token)


def download_file(url: str, output_path: str, bearer_token: Optional[str] = None):
    """
    Download a file from a HTTP server using GET request with bearer token authentication.
    
    Args:
        url (str): The URL of the file to download
        output_path (str): Local path where the file should be saved
        bearer_token (str): The bearer token for authorization
    """
    logger.debug(f"Downloading file from: {url}")
    
    try:
        # Set up headers with authorization
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        } if bearer_token else {}
        
        # Send GET request with stream=True to handle large files efficiently
        response = requests.get(url, headers=headers, stream=True)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
       
        # Open file in binary write mode
        logger.debug(f"Writing file to: {output_path}")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'wb') as file:
            # Download the file in chunks to handle large files
            chunk_size = 8192
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:  # filter out keep-alive chunks
                    file.write(chunk)
        
    except Exception as e:
        logger.error(f"Error while downloading file: {e}")

        # Clean up partial download if it exists
        if os.path.exists(output_path):
            os.remove(output_path)

        raise Exception(f"Download failed: {e}")
