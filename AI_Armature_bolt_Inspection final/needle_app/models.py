from django.db import models

class Configuration(models.Model):
    # Logging
    log_folder = models.CharField(max_length=255, default="logs")
    log_file = models.CharField(max_length=255, default="main.log")

    # Debug
    debug_mode = models.BooleanField(default=False)

    # Logo
    logo_name = models.CharField(max_length=255, default="logo.png")

    # Image saving
    save_folder_name = models.CharField(max_length=255, default="savedImages")
    save_mode = models.BooleanField(default=True)

    # Camera config
    number_of_camera = models.IntegerField(default=1)
    camera_ids = models.CharField(max_length=255, default="40649607")
    exposure = models.IntegerField(default=10000)

    # AI model
    classification_model = models.CharField(max_length=255)

    # Display settings
    resize_width = models.IntegerField(default=960)
    resize_height = models.IntegerField(default=600)
    bounding_box_thickness = models.IntegerField(default=10)
    header_height = models.IntegerField(default=50)

    # PLC configs
    plc_ip = models.GenericIPAddressField(default="192.168.0.1")
    rack = models.IntegerField(default=0)
    slot = models.IntegerField(default=1)
    db_number = models.IntegerField(default=1)
    byte_index = models.IntegerField(default=0)
    bitindex_dict = models.JSONField(default=dict)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuration {self.id} ({self.plc_ip})"
