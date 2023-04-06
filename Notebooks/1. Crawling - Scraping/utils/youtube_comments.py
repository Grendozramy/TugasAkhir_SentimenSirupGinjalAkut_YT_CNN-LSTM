import csv
from datetime import datetime as dt

# Initialize an empty list to store comments
comments = []

# Get today's date in the format 'dd-mm-yyyy'
today = dt.today().strftime('%d-%m-%Y')

# Function to process comments and optionally save them to a CSV file
def process_comments(response_items, csv_output=False):
    for res in response_items:
        comment = {}
        comment['snippet'] = res['snippet']['topLevelComment']['snippet']
        comment['snippet']['parentId'] = None
        comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
        comments.append(comment['snippet'])

    # Save comments to a CSV file if csv_output is True
    if csv_output:
        make_csv(comments)

    print(f'Finished processing {len(comments)} comments.')
    return comments

# Function to save comments to a CSV file
def make_csv(comments, channelID=None):
    header = comments[0].keys()

    # Set the filename based on the channelID and today's date
    if channelID:
        filename = f'comments_{channelID}_{today}.csv'
    else:
        filename = f'comments_{today}.csv'

    # Write the comments to the CSV file
    with open(filename, 'w', encoding='utf8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=header, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(comments)
