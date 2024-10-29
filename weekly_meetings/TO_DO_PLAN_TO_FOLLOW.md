# TO-DO's - Plan to follow

## **Analyse metadata fields:**

- [x]  Find all duplicate datasets that have “ISIC” word in the title in Kaggle.
- [x]  Content size (**contentSize**) - Compare dataset sizes to identify potential duplicates based on size of the dataset with a condition that the title has the same year (datasets with identical or very similar sizes and same year on the title may be really close duplicates).

## **Selecting a representative sample**

Instead of downloading all duplicate datasets, I was thinking focusing on a **representative sample** that is sufficient for my analysis (depending how many datasets I am going to compare if there will be 4-5 of them with each being 15-30gb, my laptop can handle it and that might be a solution, if no, if avaliable only a comparison in training or test data might be a solution as well).

**Criteria for selection would be something like:**

Results that I will get from comparison done in contentSize and name matching of original datasets and duplicate ones. I believe that two datasets so the original one and the duplicate one containing the almost the same contentSize and year in the name is a good indication to be investigate more if they are close duplicates.

- [x]  Choose the duplicate datasets based on results you get from contentSize and name comparison and either download the full dataset or maybe if avaliable just the training/test data (don't want to run in storage problem).

## Methods planning to be done

Applying those methods to the images I have downloaded:

**Image Size Comparison**

- [x]  Number of images comparison.
- [x]  Filename comparison on image names.
- [x]  Image dimensions comparison.
- [x]  File size of images comparison.

**Pixel-by-Pixel Comparison**

- [x]  Determine if duplicates are exact copies or if modifications have been made (identify datasets that have been resized or compressed).

**Hashing Techniques**

- [x]  Generate hashes for the images.
- [x]  Compare with original dataset, identify matches and near-matches.

## **Baseline Model Tests**

- [ ]  **Selecting two datasets:** Choosing the original dataset and one duplicate dataset from the sample.
- [ ]  **Training and evaluating models:** Using a machine learning model (a CNN for image classification maybe).
- [ ]  **Comparing outcomes:** Analysing results with performance metrics (accuracy, precision, recall, F1-score, and ROC curves.)

## Research (Overleaf) - Potential tasks

- [ ]  Researching why duplicates exist on Kaggle - possible reasons maybe include ease of access, personal modifications, or lack of awareness.
- [ ]  Discussing how data duplication might affect research quality.
- [ ]  Analysing whether duplicates comply with the licensing terms of the original datasets.
- [ ]  Identifying potential legal issues arising from unauthorised duplication.
- [ ]  Carbon footprint of storing all those datasets in Kaggle.

### **Documenting limitations and assumptions**

- [ ]  Acknowledging the limitations and if any assumptions.

