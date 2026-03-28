import os

# Create required directories
dirs = ['templates', 'reports']
base_path = os.path.dirname(__file__)

for dir_name in dirs:
    dir_path = os.path.join(base_path, dir_name)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created directory: {dir_path}")

print("\nDirectories created successfully!")
