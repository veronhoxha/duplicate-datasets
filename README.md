# Duplication Detection in Medical Imaging Datasets: A Comparative Study of ISIC Data on Kaggle


## Introduction
This repository hosts all the necessary resources for the Research Project titled ``"Duplication Detection in Medical Imaging Datasets: A Comparative Study of ISIC Data on Kaggle"``.

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
  - [Code](#code)
  - [Data](#data)
    - [Metadata](#metadata)
    - [Subfolders](#subfolders)
  - [Additional Folders](#additional-folders)
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Project Structure

### Code
- `01_isic_datasets_metadata.ipynb`: Jupyter Notebook for retrieving ISIC metadata from Kaggle.
- `02_year_matching_on_name_initial_comparison.ipynb`: Jupyter Notebook for initial data processing steps.
- `03_comparison_methods.ipynb`: Jupyter Notebook for performing all image comparison methods.
- `libraries/utils.py`: Python file containing functions used in `01_isic_datasets_metadata.ipynb` and `02_year_matching_on_name_initial_comparison.ipynb`.
- `libraries/comparison_methods.py`: Python file containing functions used in `03_comparison_methods.ipynb`.

### Data
All data is located in the **"data"** folder, organized as follows:

#### Metadata:

- Contains retrieved and processed metadata for ISIC datasets.

#### Subfolders:

- `duplicate_data`: Contains duplicate datasets. Due to the large size of the datasets, only one image per dataset and set is included to be able to do a code execution.
- `original_data`: Contains original datasets. Similarly, only one image per dataset and set is included for the same reason.
- `hashes`: Results from the hash comparison.
- `pixel_by_pixel_comparison`: Results from the pixel-by-pixel comparison.
- `size_dimension_comparison`: Results from the size and dimension comparison.


### Additional Folders
- `"images"`: Directory containing images used in the report.

## Installation
Ensure you have Python 3.12.6 installed (other versions may work, but this is the version used for this project). Then, install the required packages by running:
- `pip install -r requirements.txt`

## Usage
To run the notebook and recreate results:
1. Execute the three Jupyter Notebooks in the following order:
    - `01_isic_datasets_metadata.ipynb`
	- `02_year_matching_on_name_initial_comparison.ipynb`
	- `03_comparison_methods.ipynb`

## Contributors
- **Veron Hoxha** - Researcher. For questions or collaborations, contact: veho@itu.dk / veron.hoxha@yahoo.com

## License
This project is licensed under the MIT License.
