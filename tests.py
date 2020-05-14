import emoji
from main import contains_point_trigger


def test_contains_point_trigger():
    test_comments = [f'+1 Grey points to you. {emoji.emojize(":gear:")}',
                     f'+1 {emoji.emojize(":gear:")}',
                     '+1 grey point',
                     '+1 GrEyPoInT',
                     '+1greypoint',
                     'the opposite of -1 is +1',
                     '+1 to you',
                     '+2 grey points',
                     '+1 othertext grey point'
                     ]
    results = [contains_point_trigger(comment) for comment in test_comments]

    assert results == [True, True, True, True, True, False, False, False, False]
    print('Passed contains_point_trigger')


if __name__ == '__main__':
    test_contains_point_trigger()
