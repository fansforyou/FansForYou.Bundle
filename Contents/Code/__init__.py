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
      results.Append(MetadataSearchResult(id="onlyfans::no_match", name="no match -> " + media.name, year=int(year), lang='en', score=100))
      return

    artist = regex_match.group(2)
    year = regex_match.group(3)
    scene_id = regex_match.group(6)
    scene_title = regex_match.group(7)

    results.Append(MetadataSearchResult(id="onlyfans::" + artist + "::" + scene_id, name=scene_title, year=int(year), lang='en', score=100))

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

    #artist_image_search = HTML.ElementFromURL("https://www.google.com/search?q=" + artist + "+onlyfans.com").('//div[contains(@class, "isv-r")]')
    # if len(artist_image_search) > 0:
    #   role.photo = artist_image_search[0].xpath('//img[contains(@class, "rg_i")]')[0].attrib["src"]

    metadata.content_rating = "XXX"
    
    metadata.collections.clear()
    metadata.collections.add(artist)
    metadata.collections.add("OnlyFans")
    #metadata.originally_available_at = Datetime.ParseDate(str(year) + "-" + str(month) + "-" + str(day)).date()
    #metadata.year = metadata.originally_available_at.year
    #metadata.summary = 'this is a test of the summary stuff'