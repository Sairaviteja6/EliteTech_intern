import hashlib
import os

def calculate_hashes(file_path):
    """Calculate multiple hash algorithms for a file."""
    if not os.path.isfile(file_path):  # Check if file exists
        print("Error: File not found!")
        return None

    file_size = os.path.getsize(file_path)  # Get file size
    chunk_size = 4096  # Default chunk size set to 4 KB
    
    print(f"File Size: {file_size / (1024 * 1024):.2f} MB | Chunk Size: {chunk_size / 1024} KB")

    # Initialize hash objects
    hash_algorithms = {
        "MD5": hashlib.md5(),
        "SHA-1": hashlib.sha1(),
        "SHA-256": hashlib.sha256(),
        "SHA-512": hashlib.sha512()
    }

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            for algo in hash_algorithms.values():
                algo.update(chunk)

    # Generate hash values
    return {name: algo.hexdigest() for name, algo in hash_algorithms.items()}

def compare_hashes(before_hashes, after_hashes):
    """Compare hash values before and after update."""
    print("\nComparing Hashes...")
    for algo in before_hashes:
        if before_hashes[algo] == after_hashes[algo]:
            print(f"{algo}: Hash MATCHES")
        else:
            print(f"{algo}: Hash CHANGED")

def modify_file(file_path):
    """Allow the user to modify the file by adding text."""
    user_text = input("Enter text to append to the file: ")
    with open(file_path, "a") as file:
        file.write("\n" + user_text)
    print("File modified successfully!")

# Get file path from user
file_path = input("Enter the file path: ").strip()

# Calculate hash before update
print("Calculating hashes before update...")
before_hashes = calculate_hashes(file_path)
if not before_hashes:
    exit()

print("\nInitial File Hashes:")
for algo, hash_val in before_hashes.items():
    print(f"{algo}: {hash_val}")

# Ask user if they want to modify the file
modify_choice = input("\nDo you want to modify the file? (yes/no): ").strip().lower()
if modify_choice == "yes":
    modify_file(file_path)
    print("Calculating hashes after update...")
    after_hashes = calculate_hashes(file_path)
    if not after_hashes:
        exit()
    
    print("\nUpdated File Hashes:")
    for algo, hash_val in after_hashes.items():
        print(f"{algo}: {hash_val}")
    
    # Compare hashes
    compare_hashes(before_hashes, after_hashes)
else:
    print("No modifications were made. Exiting...")
