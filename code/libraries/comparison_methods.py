############ COMPARISON METHODS ############

### IMPORTS ###
import os
from PIL import Image
import csv
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
from matplotlib_venn import venn2_unweighted
from pywaffle import Waffle
import re

# WARNINGS
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")


###################################################################################################


#### CHECKING IF ALL IMAGES IN ARE 8-BIT ####

def is_image_8_bit(image_path):
    ''' 
    Checks if an image is 8 bits per channel. 
    '''
    with Image.open(image_path) as img:
        mode_to_bitdepth = {
            '1': 1,
            'L': 8,
            'P': 8,
            'RGB': 24, 
            'RGBA': 32, 
            'CMYK': 32,
            'I': 32,
            'F': 32
        }
        return mode_to_bitdepth.get(img.mode) in [24, 32, 8]


def are_all_images_8_bit(folder_path):
    '''
    Checks if all images in specific subfolders within the given folder are 8 bits per channel.

    Parameters:
        - folder_path: Path to the folder containing subfolders "train", "test", and "val".

    Returns:
        - boolean: True if all images are 8 bits per channel, False otherwise.
    '''
    
    subfolders = ["train", "test", "val"]
    for subfolder in subfolders:
        dir_path = os.path.join(folder_path, subfolder)
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    if not is_image_8_bit(file_path):
                        return False
    return True


def compare_bit_depths(duplicate_folder, original_folder):
    ''' 
    Compares bit depth for two folders and prints if all images are 8-bit. 
    '''
    
    result_duplicate = are_all_images_8_bit(duplicate_folder)
    result_original = are_all_images_8_bit(original_folder)
    print(f"Comparing bit depth for folders: {duplicate_folder} vs {original_folder}")
    print(f"Duplicate folder all 8-bit: {result_duplicate}")
    print(f"Original folder all 8-bit: {result_original}")


#### IMAGE FILE NAME, SIZE AND DIMENSION COMPARISON #### 


def count_images_and_get_filenames(directory):
    '''
    Function to count the number of images in a directory and get the filenames of the images.
    
    Parameters:
        - directory: Path to the directory containing images.
        
    Returns:
        - len(image_filenames): Number of images in the directory.
        - image_filenames: Set of filenames of the images in the directory.
    '''
    
    image_extensions = {".jpg", ".jpeg", ".png"}
    image_filenames = set()
    
    for file_name in os.listdir(directory):
        if os.path.splitext(file_name)[1].lower() in image_extensions:
            image_filenames.add(file_name)
    return len(image_filenames), image_filenames


def count_images_in_subfolders(main_directory):
    '''
    Function to count the number of images in specific subfolders within a main directory.

    Parameters:
        - main_directory: Path to the main directory containing subfolders.

    Returns:
        A dictionary with counts of images in 'train', 'test', 'val' subfolders.
    '''
    
    subfolders = ['train', 'test', 'val'] 
    image_extensions = {".jpg", ".jpeg", ".png"} 
    counts = {}  
    
    for folder in subfolders:
        directory = os.path.join(main_directory, folder)
        if os.path.exists(directory):
            count = 0
            for file_name in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, file_name)) and os.path.splitext(file_name)[1].lower() in image_extensions:
                    count += 1
            counts[folder] = count
        else:
            counts[folder] = "N/A" 

    return counts


def compare_image_counts_and_filenames(folder_duplicate, folder_original):
    '''
    Function to compare the number of images and filenames in the duplicate and original folders.
    
    Parameters:
        -  folder_duplicate: Path to the folder containing duplicate images.
        -  folder_original: Path to the folder containing original images.
        
    Returns:
        - results: Dictionary containing the comparison results for the train, test and val subfolders.
    '''
    
    subfolders = ["train", "test", "val"]
    results = {}

    for subfolder in subfolders:
        dir_duplicate = os.path.join(folder_duplicate, subfolder)
        dir_original = os.path.join(folder_original, subfolder)

        if os.path.exists(dir_duplicate) and os.path.exists(dir_original):
            count_duplicate, filenames_duplicate = count_images_and_get_filenames(dir_duplicate)
            count_original, filenames_original = count_images_and_get_filenames(dir_original)
            difference = count_original - count_duplicate
            missing_in_duplicate = filenames_original - filenames_duplicate
            missing_in_original = filenames_duplicate - filenames_original
            common_files = filenames_duplicate & filenames_original

            results[subfolder] = {
                "Duplicate Folder": count_duplicate,
                "Original Folder": count_original,
                "Match": count_duplicate == count_original and len(missing_in_original) == 0 and len(missing_in_duplicate) == 0,
                "Common Files": list(common_files),
                "Missing images in Original Folder": list(missing_in_original),
                "Missing images in Duplicate Folder": list(missing_in_duplicate),
                "Difference in Count": difference
            }
            
        elif os.path.exists(dir_duplicate) and not os.path.exists(dir_original):
            count_duplicate, filenames_duplicate = count_images_and_get_filenames(dir_duplicate)
            missing_in_original = filenames_duplicate - filenames_original 
            results[subfolder] = {
                "Duplicate Folder": count_duplicate,
                "Original Folder": "Directory not found",
                "Match": False,
                "Common Files": [],
                "Missing images in Original Folder": list(missing_in_original),
                "Missing images in Duplicate Folder": [],
                "Difference in Count": count_duplicate
            }
        elif not os.path.exists(dir_duplicate) and os.path.exists(dir_original):
            count_original, filenames_original = count_images_and_get_filenames(dir_original)
            missing_in_duplicate = filenames_original - filenames_duplicate 
            results[subfolder] = {
                "Duplicate Folder": "Directory not found",
                "Original Folder": count_original,
                "Match": False,
                "Common Files": [],
                "Missing images in Original Folder": [],
                "Missing images in Duplicate Folder": list(missing_in_duplicate),
                "Difference in Count": count_original
            }
        else:
            results[subfolder] = {
                "Duplicate Folder": "Directory not found",
                "Original Folder": "Directory not found",
                "Match": "N/A",
                "Common Files": [],
                "Missing images in Original Folder": [],
                "Missing images in Duplicate Folder": [],
                "Difference in Count": "N/A"
            }

    return results


def get_image_dimensions(directory, filenames):
    '''
    Functions to get the dimensions of images in a directory.
    
    Parameters:
        - directory: Path to the directory containing the images.
        - filenames: List of filenames of the images.
        
    Returns:
        - dimensions: Dictionary containing the dimensions of the images.
    '''
    
    dimensions = {}
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        try:
            with Image.open(filepath) as img:
                dimensions[filename] = img.size # width x height
        except Exception as e:
            dimensions[filename] = None
    return dimensions


def get_file_sizes(directory, filenames):
    '''
    Functions to get the dimensions of images in a directory.
    
    Parameters:
        - directory: Path to the directory containing the images.
        - filenames: List of filenames of the images.
        
    Returns:
        - sizes: Dictionary containing the sizes of the images.
    '''
    
    sizes = {}
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        try:
            sizes[filename] = os.path.getsize(filepath) #returns the size in BYTES
        except Exception as e:
            sizes[filename] = None
    return sizes


def compare_image_dimensions_and_sizes(folder_duplicate, folder_original, result_description, result_description_update, results):
    '''
    Function to compare the dimensions and sizes of images in the duplicate and original folders.
    
    Parameters:
        - folder_duplicate: Path to the folder containing duplicate images.
        - folder_original: Path to the folder containing original images.
        - result_description: Description of the comparison results.
        - result_description_update: Updated description of the comparison results.
        - results: Dictionary containing the comparison results for the train, test and val subfolders.
        
    Returns:
        - results: Updated dictionary containing the comparison results for the train, test and val subfolders.
    '''
    
    for subfolder in results.keys():
        dir_duplicate = os.path.join(folder_duplicate, subfolder)
        dir_original = os.path.join(folder_original, subfolder)

        details = results[subfolder]
        common_files = details["Common Files"]

        if (os.path.exists(dir_duplicate) and os.path.exists(dir_original) and common_files) or (not os.path.exists(dir_duplicate) and os.path.exists(dir_original) and common_files) or (os.path.exists(dir_duplicate) and not os.path.exists(dir_original) and common_files):
           
            # getting dimensions
            dimensions_duplicate = get_image_dimensions(dir_duplicate, common_files)
            dimensions_original = get_image_dimensions(dir_original, common_files)
           
            # getting file sizes
            sizes_duplicate = get_file_sizes(dir_duplicate, common_files)
            sizes_original = get_file_sizes(dir_original, common_files)

            mismatched_dimensions = []
            mismatched_sizes = []
            for filename in common_files:
                dim_duplicate = dimensions_duplicate.get(filename)
                dim_original = dimensions_original.get(filename)
                size_duplicate = sizes_duplicate.get(filename)
                size_original = sizes_original.get(filename)

                # comparing dimensions
                if dim_duplicate != dim_original:
                    mismatched_dimensions.append({
                        "Filename": filename,
                        "Dimension Duplicate": dim_duplicate,
                        "Dimension Original": dim_original
                    })
                    
                # comparing file sizes
                if size_duplicate != size_original:
                    mismatched_sizes.append({
                        "Filename": filename,
                        "Size Duplicate": size_duplicate,
                        "Size Original": size_original
                    })

            details["Mismatched Dimensions"] = mismatched_dimensions
            details["Mismatched Sizes"] = mismatched_sizes

            subfolder_safe = subfolder.replace(" ", "_")
            result_desc_safe = result_description_update.replace(" ", "_")
            
            # dimensions
            csv_filename_dims = f"../data/size_dimension_comparison/mismatched_dimensions_{result_desc_safe}_{subfolder_safe}.csv"
            with open(csv_filename_dims, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Filename", "Dimension Duplicate", "Dimension Original"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in mismatched_dimensions:
                    writer.writerow(row)
            
            # sizes
            csv_filename_sizes = f"../data/size_dimension_comparison/mismatched_sizes_{result_desc_safe}_{subfolder_safe}.csv"
            with open(csv_filename_sizes, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Filename", "Size Duplicate", "Size Original"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in mismatched_sizes:
                    writer.writerow(row)

            # dimensions
            csv_filename_all_dims = f"../data/size_dimension_comparison/all_dimensions_{result_desc_safe}_{subfolder_safe}.csv"
            with open(csv_filename_all_dims, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Filename", "Dimension Duplicate", "Dimension Original"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for filename in common_files:
                    writer.writerow({
                        "Filename": filename,
                        "Dimension Duplicate": dimensions_duplicate.get(filename),
                        "Dimension Original": dimensions_original.get(filename)
                    })
                    
            # sizes
            csv_filename_all_sizes = f"../data/size_dimension_comparison/all_sizes_{result_desc_safe}_{subfolder_safe}.csv"
            with open(csv_filename_all_sizes, mode="w", newline="", encoding="utf-8") as csvfile:
                fieldnames = ["Filename", "Size Duplicate", "Size Original"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for filename in common_files:
                    writer.writerow({
                        "Filename": filename,
                        "Size Duplicate": sizes_duplicate.get(filename),
                        "Size Original": sizes_original.get(filename)
                    })

            details["Mismatched Dimensions Count"] = len(mismatched_dimensions)
            details["Mismatched Sizes Count"] = len(mismatched_sizes)

        else:
            # directories or common files missing
            details["Mismatched Dimensions"] = []
            details["Mismatched Sizes"] = []
            details["Mismatched Dimensions Count"] = "N/A"
            details["Mismatched Sizes Count"] = "N/A"

    return results




#### PIXEL BY PIXEL COMPARISON #### 


def pixel_compare(image_path_a, image_path_b):
    '''
    Function to compare two images pixel by pixel.
    
    Parameters:
        - image_path_a: Path to the first image used for comparison.
        - image_path_b: Path to the second image used for comparison.
    
    Returns:
        - True if the images are identical, False otherwise.
    '''
    
    try:
        with Image.open(image_path_a) as img_a, Image.open(image_path_b) as img_b:
            if img_a.size != img_b.size:
                return False
            # checking images are in the same mode
            if img_a.mode != img_b.mode:
                img_b = img_b.convert(img_a.mode)
            # comparing pixel data
            return list(img_a.getdata()) == list(img_b.getdata())
    except Exception as e:
        return False
    
    
def perform_pixel_comparison(folder_duplicate, folder_original, subfolder):
    '''
    Function to perform pixel by pixel comparison of images in the duplicate and original folders.
    
    - Parameters:
        - folder_duplicate: Path to the folder containing duplicate images.
        - folder_original: Path to the folder containing original images.
        - subfolder: Subfolder being compared (train, test, val).
        
    - Returns:
        - None
    '''
    
    dir_duplicate = os.path.join(folder_duplicate, subfolder)
    dir_original = os.path.join(folder_original, subfolder)
    
    if not os.path.exists(dir_duplicate) or not os.path.exists(dir_original):
        print(f"Either duplicate or original directory does not exist for subfolder {subfolder}.")
        return
    
    folder_duplicate_update = os.path.basename(folder_duplicate).replace("-", " ")
    folder_original_update = os.path.basename(folder_original)
    match = re.search(r'201[0-9]', folder_duplicate_update)
    substring = match.group()
    
    result_desc_safe = f"Data_{substring}_-_(Duplicate_Data_-_{os.path.basename(folder_duplicate)}_vs_Original_Data_-_{os.path.basename(folder_original)})"
    subfolder_safe = subfolder.replace(" ", "_")
    
    dimensions_csv = f"../data/size_dimension_comparison/all_dimensions_{result_desc_safe}_{subfolder_safe}.csv"
    mismatched_sizes_csv = f"../data/size_dimension_comparison/mismatched_sizes_{result_desc_safe}_{subfolder_safe}.csv"
    
    # checking if CSV files exist
    if not os.path.exists(dimensions_csv):
        print(f"Dimensions CSV file not found: {dimensions_csv}")
        return
    if not os.path.exists(mismatched_sizes_csv):
        print(f"Mismatched sizes CSV file not found: {mismatched_sizes_csv}")
        return

    dimensions_df = pd.read_csv(dimensions_csv)
    mismatched_sizes_df = pd.read_csv(mismatched_sizes_csv)
    
    # finding images with matching dimensions
    dimensions_df["Dimensions Match"] = dimensions_df["Dimension Duplicate"] == dimensions_df["Dimension Original"]
    matching_dimensions_df = dimensions_df[dimensions_df["Dimensions Match"]]
    
    # finding images with mismatched sizes and matching dimensions (we can only compare images pixel by pixel if they have same dimensions)
    # images_to_compare = pd.merge(matching_dimensions_df[["Filename"]], mismatched_sizes_df[["Filename"]], on="Filename")
    
    images_to_compare = matching_dimensions_df[["Filename"]]
    
    # print(f"\nPerforming pixel comparison for {result_desc_safe} - {subfolder}:")
    print(f"  {subfolder.capitalize()} -")
    print(f"    Number of images to compare: {len(images_to_compare)}")
    
    if images_to_compare.empty:
        print("No images to compare for this subfolder.")
        return
    
    result_desc_safe = f"Data_{substring}_-_(Duplicate_Data_-_{os.path.basename(folder_duplicate)}_vs_Original_Data_-_{os.path.basename(folder_original)})"
    subfolder_safe = subfolder.replace(" ", "_")
    csv_filename = f"../data/pixel_by_pixel_comparison/pixel_comparison_{result_desc_safe}_{subfolder_safe}.csv"

    if os.path.exists(csv_filename):
        pixel_comparison_df = pd.read_csv(csv_filename)
        total_images = len(pixel_comparison_df)
        identical_images = pixel_comparison_df['Identical'].sum()
        different_images = total_images - identical_images
        print(f"    Total images compared: {total_images}")
        print(f"    Identical images: {identical_images} - ({(identical_images / total_images * 100)})%")
        print(f"    Different images: {different_images} - ({(different_images / total_images * 100)})%")
    
    else:
        # pixel-by-pixel comparison
        pixel_comparison_results = []
        for index, row in images_to_compare.iterrows():
            filename = row["Filename"]
            image_path_duplicate = os.path.join(dir_duplicate, filename)
            image_path_original = os.path.join(dir_original, filename)
            
            if not os.path.exists(image_path_duplicate):
                print(f"Duplicate image not found: {image_path_duplicate}")
                continue
            if not os.path.exists(image_path_original):
                print(f"Original image not found: {image_path_original}")
                continue
            
            identical = pixel_compare(image_path_duplicate, image_path_original)
            
            pixel_comparison_results.append({
                "Filename": filename,
                "Identical": identical
            })
        
        pixel_comparison_df = pd.DataFrame(pixel_comparison_results)
        
        csv_filename = f"../data/pixel_by_pixel_comparison/pixel_comparison_{result_desc_safe}_{subfolder_safe}.csv"
        pixel_comparison_df.to_csv(csv_filename, index=False)
        
        total_images = len(pixel_comparison_df)
        identical_images = pixel_comparison_df["Identical"].sum()
        different_images = total_images - identical_images
        
        # print(f"  {subfolder.capitalize()} -")
        print(f"    Total images compared: {total_images}")
        print(f"    Identical images: {identical_images} - ({(identical_images / total_images * 100)})%")
        print(f"    Different images: {different_images} - ({(different_images / total_images * 100)})%")




#### HASHING COMPARISON ####


def compute_file_hashes(image_folder, dataset_name):
    '''
    Function to compute hashes for images in a folder.
    
    Parameters:
        - image_folder: Path to the folder containing images.
        - dataset_name: Name of the dataset.
        
    Returns:
        - hashes: List of dictionaries containing the hashes of the images.
    '''
    
    image_extensions = {".jpg", ".jpeg", ".png"}
    hashes = []
    for root, dirs, files in os.walk(image_folder):
        for file_name in files:
            if os.path.splitext(file_name)[1].lower() in image_extensions:
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                        file_hash = hashlib.md5(file_data).hexdigest()
                    subfolder = os.path.relpath(root, image_folder)
                    hashes.append({
                        "Dataset": dataset_name,
                        "Subfolder": subfolder,
                        "FilePath": file_path,
                        "FileName": file_name,
                        "FileHash": file_hash
                    })
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
    return hashes


def compare_hashes_for_pair(hashes_df, duplicate_dataset_name, original_dataset_name):
    '''
    Function to compare hashes for images in the duplicate and original datasets.
    
    Parameters:
        - hashes_df: DataFrame containing the hashes of images.
        - duplicate_dataset_name: Name of the duplicate dataset.
        - original_dataset_name: Name of the original dataset.
    
    Returns:
        - duplicate_pairs: List of dictionaries containing the hashes of duplicate and original.
    '''
    
    duplicate_df = hashes_df[hashes_df["Dataset"] == duplicate_dataset_name].copy()
    original_df = hashes_df[hashes_df["Dataset"] == original_dataset_name].copy()
    
    duplicate_df.reset_index(drop=True, inplace=True)
    original_df.reset_index(drop=True, inplace=True)
    
    duplicate_pairs = pd.merge(
        duplicate_df,
        original_df,
        on="FileHash",
        suffixes=("_Duplicate", "_Original")
    )
    
    duplicate_pairs = duplicate_pairs.to_dict("records")
    
    return duplicate_pairs




#### IMAGE FILENAME COMPARISON VENN DIAGRAM ####


def plot_waffle_for_all_pairs(all_comparison_results):
    '''
    Function to plot Waffle charts for all pairs of datasets.
    
    Parameters:
        - all_comparison_results: Dictionary containing the comparison results for all pairs of datasets.
        
    Returns:
        - None
    '''

    colors = {
        "Missing images in Duplicate Folder": "#a0b39c",
        "Common Files": "#f2cf8b", 
        "Missing images in Original Folder": "#61618a"
        
    }

    for pair_index, (comparison_results, folder_original, folder_duplicate) in all_comparison_results.items():
        folder_duplicate_update = os.path.basename(folder_duplicate).replace("-", " ")
        folder_original_update = os.path.basename(folder_original)
        match = re.search(r'201[0-9]', folder_duplicate_update)
        substring = match.group()
        
        for subfolder, details in comparison_results.items():
            data = {
                "Missing images in Duplicate Folder": len(details.get("Missing images in Duplicate Folder", [])),
                "Common Files": len(details.get("Common Files", [])),
                "Missing images in Original Folder": len(details.get("Missing images in Original Folder", [])),
               
            }
            
            total = sum(data.values())
            if total == 0:
                continue  
            
            rounded_data = {key: round(value / total * 100) for key, value in data.items()}

            while sum(rounded_data.values()) < 100:
                rounded_data[max(rounded_data, key=rounded_data.get)] += 1
            while sum(rounded_data.values()) > 100:
                rounded_data[max(rounded_data, key=rounded_data.get)] -= 1

            try:
                plt.figure()
                fig = plt.figure(
                    FigureClass=Waffle,
                    rows=10,
                    columns=10,
                    figsize=(8, 8),
                    values=rounded_data,
                    colors=[colors[key] for key in rounded_data.keys()],
                    title={
                        'label': f"Data {substring} - {subfolder.capitalize()} ({data['Missing images in Duplicate Folder']}, {data['Common Files']}, {data['Missing images in Original Folder']})",
                        'loc': 'left',
                        'fontdict': {
                            'fontsize': 25
                        }
                    },
                )
                fig.axes[0].get_legend().remove()
                plt.show() 
            except ZeroDivisionError:
                print("")