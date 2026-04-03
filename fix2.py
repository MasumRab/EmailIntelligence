with open("setup/services.py", "r") as f:
    text = f.read()

text = text.replace('frontend_config = config.get_service_config("frontend")\n            frontend_path = config.get_service_path("frontend")', 'frontend_path = config.get_service_path("frontend")')

with open("setup/services.py", "w") as f:
    f.write(text)
