# Paper Review Dataset

Curated dataset of academic papers and their reviews, sampled from 2024 and 2025. The workflow for creating the dataset is outlined below.

## Data Organization

- **Original Papers Folder**  
  Contains Excel sheets for each year:  
  - `2024.xlsx` (~7k+ papers)  
  - `2025.xlsx` (~7k+ papers)  

- **data.csv**  
  - Combined both 2024 and 2025 Excel sheets.  
  - Randomly sampled **200 papers** from the combined dataset.  

- **data_final.csv**  
  - Fetched all reviews for the 200 sampled papers using `fetch_reviews.py`.  
  - Randomly sampled **150 reviews** for final analysis.
  
## Dataset Summary

During the review fetching process, we obtained the following results:  

| Metric | Value |
|--------|-------|
| Papers processed | 200 |
| Papers with reviews | 196 |
| Total reviews collected from papers above | 761 |
| Final sampled reviews | 150 |

## Scripts

- **fetch_reviews.py**  
  - Script used to fetch reviews for each paper in the sampled dataset.  

## Notes

- Sampling was performed randomly .  

