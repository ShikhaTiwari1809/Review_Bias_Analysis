"""
Fetch OpenReview reviews and expand data by reviewer using official OpenReview Python client.
"""

import csv
import time
import random
from pathlib import Path

try:
    import openreview.api
except ImportError:
    print("[ERROR] openreview-py not installed!")
    print("        Please run: pip install openreview-py")
    exit(1)

# Configuration
INPUT_FILE = "papers/data_trim.csv"
OUTPUT_FILE = "papers/data_final.csv"
DELAY_SECONDS = 2.0
SAMPLE_SIZE = 150


def fetch_reviews(client, paper_id):
    """
    Fetch all official reviews for a given paper from OpenReview.

    Args:
        client: OpenReview API client
        paper_id: The OpenReview paper/forum ID

    Returns:
        List of review objects, or empty list if error/no reviews
    """
    try:
        notes = client.get_all_notes(forum=paper_id)

        reviews = []
        for note in notes:
            invitations = note.invitations if hasattr(note, "invitations") else []
            for invitation in invitations:
                if "Official_Review" in invitation:
                    reviews.append(note)
                    break
        return reviews

    except Exception as e:
        print(f"  [X] Error for {paper_id}: {str(e)[:80]}")
        return []


def extract_reviewer_id(review):
    """
    Extract reviewer ID from review signatures.

    Args:
        review: Review object from OpenReview API

    Returns:
        Reviewer ID string, or None if not found
    """
    try:
        signatures = review.signatures if hasattr(review, "signatures") else []
        if signatures and len(signatures) > 0:
            return signatures[0]
        return None
    except Exception:
        return None


def main():
    print("=" * 60)
    print("OpenReview Review Fetcher")
    print("=" * 60)

    # Initialize OpenReview client
    print("\n[*] Connecting to OpenReview API...")
    try:
        client = openreview.api.OpenReviewClient(baseurl="https://api2.openreview.net")
        print("[OK] Connected successfully")
    except Exception as e:
        print(f"[ERROR] Failed to connect to OpenReview API: {e}")
        return

    print(f"\n[*] Reading input file: {INPUT_FILE}")
    papers = []

    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                papers.append(
                    {"paper_id": row["paper_id"], "forum_url": row["forum_url"]}
                )
    except FileNotFoundError:
        print(f"[ERROR] Input file '{INPUT_FILE}' not found!")
        return
    except Exception as e:
        print(f"[ERROR] Error reading input file: {e}")
        return

    print(f"[OK] Loaded {len(papers)} papers")

    # Fetch reviews for each paper
    print(f"\n[*] Fetching reviews from OpenReview API...")
    print(f"    (Rate limit: {DELAY_SECONDS}s delay between requests)")
    print(
        f"    This will take approximately {int(len(papers) * DELAY_SECONDS / 60)} minutes...\n"
    )

    expanded_rows = []
    papers_with_reviews = 0
    total_reviews = 0
    errors = 0

    for idx, paper in enumerate(papers, 1):
        paper_id = paper["paper_id"]
        forum_url = paper["forum_url"]

        print(f"[{idx}/{len(papers)}] Fetching: {paper_id}", end=" ", flush=True)

        reviews = fetch_reviews(client, paper_id)

        if reviews:
            review_count = 0
            for review in reviews:
                reviewer_id = extract_reviewer_id(review)
                if reviewer_id:
                    expanded_rows.append(
                        {
                            "paper_id": paper_id,
                            "forum_url": forum_url,
                            "reviewer_id": reviewer_id,
                        }
                    )
                    review_count += 1

            if review_count > 0:
                print(f"[OK] {review_count} reviews")
                papers_with_reviews += 1
                total_reviews += review_count
            else:
                print("[OK] 0 reviews (no valid reviewer IDs)")
        else:
            if len(reviews) == 0:
                print("[OK] 0 reviews")
            else:
                errors += 1

        # Rate limiting delay between requests
        if idx < len(papers):
            time.sleep(DELAY_SECONDS)

    print(f"\n[*] Summary:")
    print(f"    Papers processed: {len(papers)}")
    print(f"    Papers with reviews: {papers_with_reviews}")
    print(f"    Total reviews collected: {total_reviews}")
    print(f"    Errors encountered: {errors}")

    if not expanded_rows:
        print("\n[ERROR] No reviews were collected. Cannot create output file.")
        print("        Possible reasons:")
        print("        - Papers don't have official reviews yet")
        print("        - Rate limiting is preventing access")
        print("        - Wrong invitation pattern for these papers")
        return

    # Sample 150 rows
    sample_count = min(SAMPLE_SIZE, len(expanded_rows))
    if len(expanded_rows) > SAMPLE_SIZE:
        print(
            f"\n[*] Randomly sampling {sample_count} rows from {len(expanded_rows)} total..."
        )
        sampled_rows = random.sample(expanded_rows, sample_count)
    else:
        print(
            f"\n[WARN] Only {len(expanded_rows)} rows available (less than {SAMPLE_SIZE})"
        )
        sampled_rows = expanded_rows

    print(f"\n[*] Writing output file: {OUTPUT_FILE}")

    try:
        Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["paper_id", "forum_url", "reviewer_id"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sampled_rows)

        print(f"[OK] Successfully wrote {len(sampled_rows)} rows to {OUTPUT_FILE}")

    except Exception as e:
        print(f"[ERROR] Error writing output file: {e}")
        return

    print("\n" + "=" * 60)
    print("[SUCCESS] Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
