# TO-DO's - Plan to follow

## **Analyse “metadata” fields:**

- [x]  Find all duplicate datasets that have “ISIC” word in the title in Kaggle
- [ ]  **Content size (**contentSize**) -** Compare dataset sizes to identify potential duplicates based on size of the dataset (datasets with identical or very similar sizes may be duplicates)

## **Selecting a representative sample**

Instead of downloading all duplicate datasets, I was thinking focusing on a **representative sample** that is sufficient for my analysis (still download a small sample of it.)

**Criteria for selection would be something like:**

- **Top N datasets by size, I believe that l**arger datasets are more likely to be complete duplicates.

**Example what I am planning to do :**

- [ ]  Choose the top 5-10 duplicate datasets based on contentSize_MB  and download a sample for them.

## **Documenting limitations and assumptions**

- [ ]  Acknowledging that due to resource constraints, the analysis is based on a subset of the data. The findings may not generalize to all duplicates on Kaggle.

## Methods planning to be done

Applying those methods to the sample images I have downloaded

**Image Size Comparison**

- [ ]  Number of images
- [ ]  Filename comparison on image names
- [ ]  Image dimensions
- [ ]  File size of images
- [ ]  Identify datasets that have been resized or compressed.

**Pixel-by-Pixel Comparison**

- [ ]  Determine if duplicates are exact copies or if modifications have been made.

**Hashing Techniques**

- [ ]  Generate hashes for the images in your sample.
- [ ]  Compare with original dataset**, i**dentify matches and near-matches.

## **Baseline Model Tests**

- [ ]  **Selecting two datasets:** Choosing the original dataset and one duplicate dataset from the sample.
- [ ]  **Training and evaluating models:** Using a machine learning model (a CNN for image classification maybe).
- [ ]  **Comparing outcomes:** Analyzing performance metrics to see if duplicates impact model results (accuracy, precision, recall, F1-score, and ROC curves.)

## Research (Overlead)

- [ ]  Researching why duplicates exist on Kaggle - possible reasons maybe include ease of access, personal modifications, or lack of awareness.
- [ ]  Discussing how data duplication might affect research quality.
- [ ]  Analyzing whether duplicates comply with the licensing terms of the original datasets.
- [ ]  Identifying potential legal issues arising from unauthorized duplication.
- [ ]  Carbon footprint of storing all those datasets in Kaggle