# grey-point-bot

Reddit bot to keep track of "Grey Points" given out by [CGPGrey](https://www.youtube.com/cgpgrey). You can find a history and ranking chart of Grey Point recipients at [this google sheet](https://docs.google.com/spreadsheets/d/18_Y1TrcEZHHYesYX8lVO9BdbbEPWWMPaLZ1DONwOQjI/edit?usp=sharing).

# What triggers the bot?
A point is awarded by CGPGrey ([/u/MindOfMetalAndWheels](https://old.reddit.com/user/MindOfMetalAndWheels)) anytime he replies to a post or comment with the keywords `+1 grey point`, `+1 internet point` or `+1 ⚙️` anywhere in his reply. The plural versions of those keywords will also trigger the bot (etc. `+1 grey points`). 

For example, this comment will trigger the bot:  
``` 
+1 internet points to you!
```  
This comment would not:
```
+1 points of internet!
```

# How does this bot work?
The bot is written in Python and is hosted is hosted on a Heroku server.

## Dependencies
- [pygsheets](https://github.com/nithinmurali/pygsheets)
- [praw](https://github.com/praw-dev/praw)
- [emoji](https://github.com/carpedm20/emoji)
- [pandas](https://github.com/pandas-dev/pandas)
