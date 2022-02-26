import re
import datetime

media_name_regex = r"(Only[F|f]ans[ ]?)\-? (.+)?\-? ([0-9]{4})[ ]?\-?([0-9]{2})[ ]?\-?([0-9]{2})[ ]?\-? ([0-9]+)[ ]?\-? (.+)"
result_id_regex = r"(onlyfans::)(.+)::([0-9]+)"

def Start():
  pass

def ValidatePrefs():
  pass


class FansForYouAgent(Agent.Movies):
  name = 'FansForYou'
  languages = [Locale.Language.English]
  accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.lambda', 'com.plexapp.agents.xbmcnfo']
  primary_provider = True

  def search(self, results, media, lang):
    regex_match = re.search(media_name_regex, media.name)
    if not regex_match:
      return

    artist = regex_match.group(2)
    year = regex_match.group(3)
    scene_id = regex_match.group(6)
    scene_title = regex_match.group(7)

    searchResult = MetadataSearchResult(id="onlyfans::" + artist + "::" + scene_id, name=scene_title, year=int(year), lang='en', score=100)
    results.Append(searchResult)

  def update(self, metadata, media, lang):
    regex_match = re.search(result_id_regex, metadata.id)
    if not regex_match:
      metadata.title = "no match -> " + metadata.id
      return

    artist = regex_match.group(2)
    scene_id = regex_match.group(3)

    # Actors
    metadata.roles.clear()
    role = metadata.roles.new()
    role.name = artist
    role.photo = "https://ei.phncdn.com/videos/202006/12/323077461/original/(m=q4G2NUVbeaAaGwObaaaa)(mh=RU_hAfm4aELT9_eo)0.jpg"

    metadata.content_rating = "XXX"
    metadata.title = scene_title
    #metadata.originally_available_at = Datetime.ParseDate(str(year) + "-" + str(month) + "-" + str(day)).date()
    #metadata.year = metadata.originally_available_at.year
    #metadata.summary = 'this is a test of the summary stuff'

    # Collections
    metadata.collections.clear()
    metadata.collections.add(artist)
    metadata.collections.add("OnlyFans")