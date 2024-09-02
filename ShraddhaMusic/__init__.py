from ShraddhaMusic.core.bot import Shraddha
from ShraddhaMusic.core.dir import dirr
from ShraddhaMusic.core.git import git
from ShraddhaMusic.core.userbot import Userbot
from ShraddhaMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Shraddha()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
Instagram = InstaAPI()
