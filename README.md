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
- `"01_isic_datasets_metadata.ipynb"`: Jupyter Notebook for retrieving ISIC metadata from Kaggle.
- `"02_year_matching_on_name_initial_comparison.ipynb"`: Jupyter Notebook for initial data processing steps.
- `"03_comparison_methods.ipynb"`: Jupyter Notebook for performing all image comparison methods.
- `"libraries/utils.py"`: Python file containing functions used in `"01_isic_datasets_metadata.ipynb"` and `"02_year_matching_on_name_initial_comparison.ipynb"`.
- `"libraries/comparison_methods.py"`: Python file containing functions used in `"03_comparison_methods.ipynb"`.

### Data
All data is located in the **"data"** folder, organized as follows:

#### Metadata:

- Contains retrieved and processed metadata for ISIC datasets.

#### Subfolders:

- `"duplicate_data"`: Contains duplicate datasets. Due to the large size of the datasets, only one image per dataset and set is included to be able to do a code execution. Note that if running the code with one image for dataset the results for the pixel-by-pixel comparison are derived from the original complete datasets, not just the single images shown here in the repo. The code is designed to read previously saved results from one full execution, as running a pixel-by-pixel comparison on the complete datasets is very time-consuming.
- `"original_data"`: Contains original datasets. Similarly, only one image per dataset and set is included for the same reason.
- `"hashes"`: Results from the hash comparison.
- `"pixel_by_pixel_comparison"`: Results from the pixel-by-pixel comparison.
- `"size_dimension_comparison"`: Results from the size and dimension comparison.


### Additional Folders
- `"images"`: Directory containing images used in the report.
- `"report"`: Directory containing the report of the study in PDF format.

## Installation
Prerequisites: Ensure Python 3.12.6 is installed on your machine. Other versions might work, but this project was developed with 3.12.6.

**1. Create and Activate a Virtual Environment**

Create a Virtual Environment in the root directory of this project by running the following commands:
  - For macOS/Linux:
      - ``python3 -m venv .venv``
      - ``source .venv/bin/activate``
  - For Windows:
      - ``python -m venv .venv``
      - ``.venv\Scripts\activate``

**2. Install Required Packages**

When the virtual environment is activated, install all necessary packages by running:
  - `pip install -r requirements.txt`

## Usage
To run the notebook and recreate results:
1. Execute the three Jupyter Notebooks in the following order:
    - `"01_isic_datasets_metadata.ipynb"`
    - `"02_year_matching_on_name_initial_comparison.ipynb"`
    - `"03_comparison_methods.ipynb"`

## Contributors
- **Veron Hoxha** - Researcher. For questions or collaborations, contact: veho@itu.dk / veron.hoxha@yahoo.com

## License
This project is licensed under the MIT License.
