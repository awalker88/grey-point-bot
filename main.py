import praw
import emoji
import pygsheets as pyg
import pandas as pd
from time import time
import os

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
    print('environ test::::', reddit)

    # while True:
    # print('starting stream')
    # stream_start_time = time()
    # cmmts = []
    # client = pyg.authorize()
    # workbook = client.open('heroku test')
    # worksheet: pyg.Worksheet = workbook.worksheet_by_title('Sheet1')
    # for comment in reddit.redditor('awalker88').stream.comments():
    #     cmmts.append([comment.id, comment.body])
    #     # if comment.created_utc > stream_start_time and contains_point_trigger(comment.body):
    #     #     print('replying')
    #     #     # update_sheets()
    #     #     reply(comment)
    #
    #     cmmt_df = pd.DataFrame(cmmts, columns=['Comment IDs', 'Text'])
    #     worksheet.set_dataframe(cmmt_df, start='A1')


def contains_point_trigger(text: str):
    valid_triggers = ['+1 grey points', '+1 grey point', '+1 :gear:', '+1 internet point', '+1 internet points']

    # clean comment text
    text = emoji.demojize(text)
    text = text.lower().replace(' ', '')

    for trigger in valid_triggers:
        if trigger.lower().replace(' ', '') in text:
            return True

    return False


def add_comment_to_sheet(comment: praw.reddit.models.Comment):
    client = pyg.authorize()
    workbook = client.open('Grey Points')
    points_list = pd.DataFrame(workbook.worksheet_by_title('Points List').get_as_df())
    next_id = points_list['Comment ID'].max() + 1
    username = f'/u/{comment.parent().author()}'
    comment_link = 'www.reddit.com/comments/' + comment.link_id.url.str[3:] + '/_/' + comment.id


def reply(comment: praw.reddit.models.Comment):
    recipient = comment.parent()
    text = f"Congrats u/{recipient.author}, you just earned a Grey Point!  " \
           f"&nbsp;" \
           f"\n\nYou can view all recepients of Grey Points [here](https://docs.google.com/spreadsheets/d/18_Y1TrcEZHHYesYX8lVO9BdbbEPWWMPaLZ1DONwOQjI/edit#gid=546994114)  " \
           f".\n___\n" \
           f"^(beep boop i'm a bot | [GitHub](https://github.com/awalker88/grey-point-bot) | report issues [here](https://www.reddit.com/message/compose/?to=awalker88&amp;subject=Grey Points Issue&amp;message=Enter the issue here) | Grey click here if you want more info )"

    comment.reply(text)


if __name__ == '__main__':
    print('starting loop')
    main()


