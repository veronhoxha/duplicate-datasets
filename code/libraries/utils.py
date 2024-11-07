############ UTILS ############

### IMPORTS ###
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import mlcroissant as mlc
import plotly.express as px
import os
import re
import numpy as np

# WARNINGS
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")




###################################################################################################




def parse_size(size_str):
    '''
    Size string parser that converts a human readable size string to bytes.
    Supported units are B, KB, MB, GB, TB.
    
    Parameters:
        - size_str: Human-readable size string.
        
    Returns:
        - size_in_bytes: Size in bytes.
        - unit: Size unit.
    '''
    
    size_str = size_str.strip()
    size_regex = r'([\d\.]+)\s*([KMGT]?B)'
    match = re.match(size_regex, size_str, re.IGNORECASE)
    if not match:
        return None, None
    size_value, unit = match.groups()
    size_value = float(size_value)
    unit = unit.upper()
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
    }
    size_in_bytes = size_value * units.get(unit, 1)
    
    return size_in_bytes, unit


def flatten_metadata(metadata, parent_key='', sep='.'):
    '''
    Function to flatten a nested dictionary with lists to a flat dictionary.
    
    Parameters:
        - metadata: Nested dictionary with lists.
        - parent_key: Parent key for the current level.
        - sep: Separator between keys.
    
    Returns:
        - dict: Flattened dictionary.
    '''
    
    items = []
    for k, v in metadata.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_metadata(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            if all(isinstance(i, dict) for i in v):
                for idx, item in enumerate(v):
                    items.extend(flatten_metadata(item, f"{new_key}_{idx}", sep=sep).items())
            else:
                items.append((new_key, '; '.join(map(str, v))))
        else:
            items.append((new_key, v))
    return dict(items)


def convert_dataset_to_croissant(dataset):
    '''
    Function to convert a Kaggle dataset to a Croissant metadata dictionary.
    
    Parameters:
        - dataset: Kaggle dataset object.
    
    Returns:
        - croissant_metadata: Croissant metadata dictionary.
    
    '''
    
    if dataset.tags:
        keywords = [tag.name for tag in dataset.tags]
    else:
        keywords = []
    
    # parsing the dataset.size
    size_in_bytes = None
    if dataset.size:
        try:
            size_in_bytes = float(dataset.size)
        except ValueError:
            size_in_bytes, size_unit = parse_size(dataset.size)
        except TypeError:
            size_in_bytes = None
    else:
        size_in_bytes = None
    
    # converting the size to MB
    if size_in_bytes:
        content_size_mb = size_in_bytes / (1024 * 1024)
        content_size_str = f"{content_size_mb}"
    else:
        content_size_str = "Unknown"
    
    owner_username = dataset.ref.split('/')[0]
    
    croissant_metadata = {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            # there is a lot of other metadata here but i dont need them for now at least
        },
        "@type": "Dataset",
        "name": dataset.title,
        "alternateName": dataset.subtitle if dataset.subtitle else '',
        "description": dataset.description if dataset.description else '',
        "url": f"https://www.kaggle.com/{dataset.ref}",
        "identifier": dataset.id,
        "creator": {
            "@type": "Person",
            "name": dataset.creatorName if dataset.creatorName else owner_username,
            "url": f"https://www.kaggle.com/{owner_username}"
        },
        "license": {
            "@type": "CreativeWork",
            "name": dataset.licenseName
        },
        "keywords": keywords,
        "dateModified": dataset.lastUpdated.isoformat() if dataset.lastUpdated else None,
        "isAccessibleForFree": True,
        "distribution": [
            {
                "@type": "DataDownload",
                "contentUrl": f"https://www.kaggle.com/datasets/{dataset.ref}/download",
                "contentSize": content_size_str,
                "encodingFormat": "application/zip"
            }
        ],
        "isPrivate": dataset.isPrivate,
        "downloadCount": dataset.downloadCount,
        "viewCount": dataset.viewCount,
        "voteCount": dataset.voteCount,
        "usabilityRating": dataset.usabilityRating,
        "conformsTo": "http://mlcommons.org/croissant/1.0"
    }
    return croissant_metadata




#########################################################################




def extract_year(name):
    '''
    Function to extract the year from the dataset name.
    
    Parameters:
        - name: Dataset name.
    
    Returns:
        - year: Year extracted from the dataset name.
    '''
    
    match = re.search(r'\b(20\d{2})\b', name)
    return int(match.group(0)) if match else None


def find_potential_duplicates(original_df, kaggle_df):
    '''
    Function to find potential duplicates between the original dataset and the Kaggle dataset matched by year on the dataset name.
    
    Parameters:
        - original_df: Original dataset DataFrame.
        - kaggle_df: Duplicate Kaggle dataset DataFrame.
        
    Returns:
        - duplicates: DataFrame with potential duplicates.
    '''
    
    duplicates = []

    for index, kaggle_row in kaggle_df.iterrows():
        kaggle_content_size = kaggle_row['contentSize']
        kaggle_name = kaggle_row['name']
        kaggle_url = kaggle_row['url']
        kaggle_year = kaggle_row['Year']

        for _, original_row in original_df.iterrows():
            original_size = original_row['contentSize']
            original_name = original_row['name']
            orginal_url = original_row['url']
            original_year = original_row['Year']

            # percentage difference in contentSize
            percentage_difference = round(abs(kaggle_content_size - original_size) / original_size * 100, 2)

            # checking if the years match
            if kaggle_year == original_year:
                duplicates.append({
                    'Kaggle Dataset Name': kaggle_name,
                    "Kaggle Dataset URL": kaggle_url,
                    'Kaggle Size (MB)': kaggle_content_size,
                    'Original Dataset Name': original_name,
                    'Orginal Dataset URL': orginal_url,
                    'Original Size (MB)': original_size,
                    'Size Difference (%)': percentage_difference,
                })

    return pd.DataFrame(duplicates)


def size_difference_category(percentage):
    '''
    Function to categorize the "Size Difference (%)" percentage.
    
    Parameters: 
        - percentage: Size difference percentage.
        
    Returns: 
        - category: Categorized size difference.
    '''
    
    if percentage <= 30:
        return '1-30%'
    elif percentage <= 60:
        return '30-60%'
    else:
        return '60-100%'