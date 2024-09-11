import os
import shutil
import logging
import argparse
import time
import hashlib

# Generates an MD5 hash that acts as a unique identifier for the file.
def file_identifier(file_path):
    file_id = hashlib.md5()
    with open(file_path, "rb") as file:
        # Read the file in chunks of 4096 bytes to avoid memory overload
        for file_data in iter(lambda: file.read(4096), b""):
            file_id.update(file_data)
    return file_id.hexdigest()

# Synchronizes the source folder with the replica folder. The replica folder will be an exact copy of the source folder.
def sync_folders(source_folder, replica_folder):
    
    # Copies files from source to replica
    def copy_files_from_source_to_replica():
        
        # Walks through the source folder and copies all files that are missing or outdated in the replica.
        for root, dirs, files in os.walk(source_folder):
            relative_path = os.path.relpath(root, source_folder)
            replica_dir = os.path.join(replica_folder, relative_path)

            # Create directory in the replica if it doesn't exist
            if not os.path.exists(replica_dir):
                os.makedirs(replica_dir)
                logging.info(f"Directory created: {replica_dir}")
                logging.info(f"Replicating directory: {replica_dir}")

            # Copy files from source to replica
            for file_name in files:
                source_file = os.path.join(root, file_name)
                replica_file = os.path.join(replica_dir, file_name)

                # If the file doesn't exist in the replica or is different (based on the hash), copy it
                if not os.path.exists(replica_file) or file_identifier(source_file) != file_identifier(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"File copied: {source_file} to {replica_file}")
                    logging.info(f"Replicating file: {source_file} to {replica_file}")
    
    # Remove files from the replica that no longer exist in the source
    def remove_files_not_in_source():
        for root, dirs, files in os.walk(replica_folder):
            # Create the relative path between replica and source
            relative_path = os.path.relpath(root, replica_folder)
            source_dir = os.path.join(source_folder, relative_path)

            # Remove files that no longer exist in the source
            for file_name in files:
                replica_file = os.path.join(root, file_name)
                source_file = os.path.join(source_dir, file_name)

                # If the file no longer exists in the source, remove it from the replica
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.info(f"File removed: {replica_file}")
                    logging.info(f"Removing file: {replica_file} from replica (does not exist in source)")
            
                # Remove directories that no longer exist in the source (if empty)
            for dir_name in dirs:
                replica_dir = os.path.join(root, dir_name)
                source_dir_path = os.path.join(source_dir, dir_name)
    
                # If the directory no longer exists in the source, and is empty, remove it
                if not os.path.exists(source_dir_path):
                    try:
                        os.rmdir(replica_dir)
                        logging.info(f"Directory removed: {replica_dir}")
                    except OSError:
                        logging.warning(f"Could not remove directory (not empty): {replica_dir}")
    
    # Call the synchronization and removal functions
    logging.info(f"Starting synchronization from source: {source_folder} to replica: {replica_folder}")
    copy_files_from_source_to_replica()
    remove_files_not_in_source()
    logging.info(f"Synchronization completed between {source_folder} and {replica_folder}")

# Main function of the program
def main():
    # Define and read the command line arguments
    parser = argparse.ArgumentParser(description="Folder synchronization tool.")
    parser.add_argument('source', help='Path to the source folder')
    parser.add_argument('replica', help='Path to the replica folder')
    parser.add_argument('log_file', help='Path to the log file')
    parser.add_argument('interval', type=int, help='Synchronization interval (in seconds)')
    args = parser.parse_args()

    # Check to ensure synchronization is unidirectional (source -> replica)
    if os.path.samefile(args.source, args.replica):
        print("The source folder and replica folder cannot be the same.")
        return

    # If the replica folder is being used as the source, stop the execution
    if 'replica' in os.path.basename(args.source).lower():
        print("Error: Synchronization from 'replica' to 'source' is not allowed. The process must be from 'source' to 'replica'.")
        return

    # Configure the logger without the 'filename' argument
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(message)s',
        handlers=[logging.FileHandler(args.log_file), logging.StreamHandler()]  # Logs to file and console
    )

    # Loop to synchronize at each interval
    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
