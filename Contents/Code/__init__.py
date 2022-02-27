import re
import datetime
import json

media_name_regex = r"(Only[F|f]ans[ ]?)\-? (.+)( \-)? ([0-9]{4})[ ]?\-?([0-9]{2})[ ]?\-?([0-9]{2})[ ]?\-? ([0-9]+)[ ]?\-? (.+)"
result_id_regex = r"onlyfans::actor::(.+)::scene_id::([0-9]+)::post_year::([0-9]+)::post_month::([0-9]+)::post_day::([0-9]+)"

actor_portrait_urls = json.loads(Prefs["actor_portrait_urls"])
default_actor_portrait_url = Prefs["default_actor_portrait_url"]

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
      Log("Media name did not match the media name regex: " + media.name)
      return

    artist = regex_match.group(2)
    year = regex_match.group(4)
    month = regex_match.group(5)
    day = regex_match.group(6)
    scene_id = regex_match.group(7)
    scene_title = regex_match.group(8)

    results.Append(MetadataSearchResult(id="onlyfans::actor::" + artist + "::scene_id::" + scene_id + "::post_year::" + year + "::post_month::" + month + "::post_day::" + day, name=scene_title, year=int(year), lang='en', score=100))

  def update(self, metadata, media, lang):
    regex_match = re.search(result_id_regex, metadata.id)
    if not regex_match:
      Log("Metadata ID did not match the result ID regex: " + metadata.id)
      return

    artist = regex_match.group(1)
    scene_id = regex_match.group(2)
    year = int(regex_match.group(3))
    month = int(regex_match.group(4))
    day = int(regex_match.group(5))

    # Actors
    metadata.roles.clear()
    role = metadata.roles.new()
    role.name = artist
    if artist in actor_portrait_urls.keys():
      role.photo = actor_portrait_urls[artist]
    else:
      role.photo = default_actor_portrait_url

    metadata.content_rating = "XXX"
    metadata.originally_available_at = datetime.datetime(int(year), int(month), int(day))
    metadata.year = metadata.originally_available_at.year
    
    metadata.collections.clear()
    metadata.collections.add(artist)
    metadata.collections.add("OnlyFans")