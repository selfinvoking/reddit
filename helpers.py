import datetime

# Get all post approvals/removals from the mod log
# Note: limited by the 3 month cap on the mod log
# Todo: Might be possible to use the pushshift api work around this limit
def get_actioned_submissions(reddit):
    actioned_ids = {}
    actioned_posts = []

    for action_type in ['approvelink' 'removedlink']:
        for action in reddit.subreddit('learnjapanese').mod.log(action=action_type, limit=99999):
            if action.target_fullname != None:
                actioned_ids[action.target_fullname] = action.created_utc

    for post in reddit.info(fullnames=actioned_ids.keys()):
        post.mod_action_utc = actioned_ids[post.name]
        actioned_posts.append(post)
    
    return actioned_posts

# Group a given list of submissions by the utc hour they were posted
def group_reddit_submission_by_utc_hour(submissions):
    submissions_by_hour = {}

    for submission in submissions:
        hour = datetime.datetime.fromtimestamp(submission.created_utc).hour

        if hour not in submissions_by_hour: 
            submissions_by_hour[hour] = []

        submissions_by_hour[hour].append(submission)

    return submissions_by_hour