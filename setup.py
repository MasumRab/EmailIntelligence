from setuptools import setup, find_packages
import os

# Function to parse requirements.txt
def parse_requirements(filename="requirements.txt"):
    """Load requirements from a pip requirements file."""
    # Construct the full path to the requirements file
    req_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if not os.path.exists(req_file_path):
        print(f"Warning: {filename} not found at {req_file_path}. No dependencies will be installed via install_requires.")
        return []
    with open(req_file_path, 'r') as f:
        lineiter = (line.strip() for line in f)
        return [line for line in lineiter if line and not line.startswith("#")]

# Attempt to get the long description from a README.md file
long_description = 'A longer description of your project.' # Default
readme_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')
if os.path.exists(readme_path):
    try:
        with open(readme_path, encoding='utf-8') as f:
            long_description = f.read()
    except Exception as e:
        print(f"Warning: Could not read README.md: {e}")

setup(
    name='email_intelligence_project',  # TODO: Replace with your project's actual name
    version='0.1.0',                  # TODO: Replace with your project's version
    author='Your Name',               # TODO: Replace with your name
    author_email='your.email@example.com',  # TODO: Replace with your email
    description='An intelligent email processing application.',  # TODO: Replace with a short description
    long_description=long_description,
    long_description_content_type='text/markdown', # Assumes README.md is markdown
    url='https://github.com/yourusername/email_intelligence_project',  # TODO: Replace with your project's URL
    
    # If your Python packages are in the root directory (alongside setup.py):
    packages=find_packages(),
    # If your Python packages are in a subfolder, e.g., 'src':
    # packages=find_packages(where='src'),
    # package_dir={'': 'src'},
    
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8', # Example: Specify compatible Python versions
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License', # TODO: Choose your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', # TODO: Specify your minimum Python version
)