# r/LearnJapanese

# Obtain the average time between a post submission and being approved/removed.
# Group the averages by UTC hour (posted date)

import os
import csv
import helpers
import statistics
from dotenv import load_dotenv
import praw # https://praw.readthedocs.io/

# Load .env
load_dotenv()

# Cap the actioned time to a set number of hours, 
# this allows for the removal of statistical outliers.
# If a post has gone 12+ hours without being actioned it is
# likely a unique scenario and not indicative of normal behavior
cap_hours = 12

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent="script",
    username=os.getenv('USERNAME'),
    password=os.getenv('PASSWORD'),
)

# Grab our submissions
print('Getting submissions (may take a minute)....')
submissions = helpers.get_actioned_submissions(reddit)

# Group submissions by UTC hour created
print('Grouping submissions...')
submissions_by_hour = helpers.group_reddit_submission_by_utc_hour(submissions)

# Work out average approval time for each group
print('Calculating averages....')
action_times_by_hour = {}
for hour in submissions_by_hour:
    for submission in submissions_by_hour[hour]:
        if submission.approved:
            approval_time = (submission.mod_action_utc - submission.created_utc) / 60 #Record time in minutes for better precision

            if approval_time < (60 * cap_hours):
                if hour not in action_times_by_hour:
                    action_times_by_hour[hour] = []
                action_times_by_hour[hour].append(approval_time)

# Write the results to output.csv, also print them for convenience
with open('output.csv', mode='w') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    csv_writer.writerow(['UTC', 'PST', 'EST', 'JST'])

    for hour in range(24):
        pst_hour = (hour + 16) % 24
        est_hour = (hour + 19) % 24
        jst_hour = (hour + 9) % 24
        print('Avg time for hour UTC ', hour, ' = ', int(statistics.mean(action_times_by_hour[hour])))
        csv_writer.writerow([hour, pst_hour, est_hour, jst_hour, int(statistics.mean(action_times_by_hour[hour]))])