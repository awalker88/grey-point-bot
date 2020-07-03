import praw
import emoji
import pygsheets as pyg
import pandas as pd
from time import time
from datetime import datetime
from time import sleep

# todo: revoke grey point if user edits comment to accept award
# todo: https://www.reddit.com/r/CGPGrey/comments/dz43wa/the_sneaky_plan_to_subvert_the_electoral_college/f87g08w/?context=8&depth=9


def main():
    pass
    reddit = praw.Reddit(
        username=os.environ["reddit_username"],
        password=os.environ["reddit_password"],
        client_id=os.environ["reddit_client_id"],
        client_secret=os.environ["reddit_client_secret"],
        user_agent='grey-points-bot v1'
    )

    # while True:
    stream_start_time = time()
    print('starting stream', stream_start_time)
    client = pyg.authorize(
        # service_account_env_var='sheet_client_secret_json' todo: for local
    )

    workbook = client.open('Grey Points')
    print('workbook:::', workbook)
    points_list_ws: pyg.Worksheet = workbook.worksheet_by_title('Points List')
    for comment in reddit.redditor('MindOfMetalAndWheels').stream.comments():
        print(comment.body)
        if should_add(points_list_ws, comment):
            print(f'would reply to {comment.body}')
            add_comment_to_sheet(comment, points_list_ws)
            reply(comment)

        sleep(.25)


def should_add(worksheet: pyg.Worksheet, comment: praw.reddit.models.Comment):
    """
    Whether or not a comment passes the criteria for adding to the Google Sheet and replying
    :param worksheet: worksheet containing grey points
    :param comment: comment by Grey
    :return: Whether comment passes
    """
    # not in sheet
    worksheet_df = worksheet.get_as_df()
    if comment.id in worksheet_df['Comment ID'].to_list():
        return False

    # grey deleted his comment or it was removed
    if comment.removal_reason is not None:
        return False

    # parent is deleted
    if comment.parent().author is None:
        return False

    # doesn't contain point_trigger
    if not contains_point_trigger(comment.body):
        return False

    return True


def contains_point_trigger(text: str):
    valid_triggers = ['+1 grey points', '+1 grey point', '+1 :gear:', '+1 internet point', '+1 internet points']

    # clean comment text
    text = emoji.demojize(text)
    text = text.lower().replace(' ', '')

    for trigger in valid_triggers:
        if trigger.lower().replace(' ', '') in text:
            return True

    return False


def add_comment_to_sheet(comment: praw.reddit.models.Comment, worksheet: pyg.Worksheet):
    worksheet_df = worksheet.get_as_df()
    formatted_utc = datetime.utcfromtimestamp(comment.created_utc)
    new_entry = {
        'Point ID': worksheet_df['Point ID'].max() + 1,
        'Username': rf'/u/{comment.parent().author}',
        'Comment Link': rf'old.reddit.com/comments/{comment.link_id[3:]}/_/{comment.id}/?context=3',
        'Subreddit': rf"/r/{comment.subreddit}",
        'Date': formatted_utc.strftime('%Y-%m-%d  %H:%M:%S'),
        'Comment ID': comment.id
                 }

    worksheet_df = pd.concat([worksheet_df, pd.DataFrame(new_entry, index=[1])])
    worksheet.set_dataframe(worksheet_df, start='A1')


def reply(comment: praw.reddit.models.Comment):
    recipient = comment.parent()
    if recipient.author == 'MindOfMetalAndWheels':
        # Probably shouldn't let Grey give points to himself...
        personal_reply = f"Hmmmm... something about the ability to give points to yourself doesn't seem quite right 🤔 u/{recipient.author}  "
    elif recipient.author == 'grey-point-bot':
        personal_reply = f"Probably best if I stay out of the rankings :)  "

    else:
        personal_reply = f"Congrats u/{recipient.author}, you just earned a Grey Point!  "

    footer = f"&nbsp;" \
             f"\n\nYou can view all recipients of Grey Points [here](https://docs.google.com/spreadsheets/d/18_Y1TrcEZHHYesYX8lVO9BdbbEPWWMPaLZ1DONwOQjI/edit?usp=sharing)  " \
             f".\n___\n" \
             f"^(beep boop i'm a bot | [GitHub](https://github.com/awalker88/grey-point-bot) | [report issues here](https://www.reddit.com/message/compose/?to=awalker88&amp;subject=Grey Points Issue&amp;message=Enter the issue here) | [Click here for more info](https://github.com/awalker88/grey-point-bot/edit/master/README.md))"

    text = personal_reply + footer
    comment.reply(text)


if __name__ == '__main__':
    print('starting loop')
    main()


