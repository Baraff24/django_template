import os
import subprocess
from celery import shared_task


@shared_task
def renew_ssl_certificate():
    """
    Task for SSL certificate renewal.
    """
    try:
        # Retrieve the domain from the environment variable
        domain = os.getenv("DOMAIN")

        if domain:
            # Execute the Certbot certificate renewal command
            subprocess.run(["certbot", "renew", "--webroot", "--webroot-path", "/vol/www/"])
            print(f"SSL certificate for {domain} successfully renewed!")
        else:
            print("DOMAIN environment variable not set.")
    except Exception as e:
        print(f"Error during SSL certificate renewal: {e}")
