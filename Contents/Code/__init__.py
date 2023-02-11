import re
import datetime
import json
import subprocess
from os.path import abspath
import platform

media_name_regex = r"(Only[F|f]ans[ ]?)\-? ([a-zA-Z0-9]+)( \-)? ([0-9]{4})[ ]?\-?([0-9]{2})[ ]?\-?([0-9]{2})[ ]?\-? ([0-9]+)[ ]?\-? (.+)"
result_id_regex = r"onlyfans::actor::(.+)::scene_id::([0-9]+)::post_year::([0-9]+)::post_month::([0-9]+)::post_day::([0-9]+)"

def Start():
  pass

def ValidatePrefs():
  pass

def FixTitle(title):
  fixed_title = title
  # Because camel casing is somehow applied as a transformation of the text, try to account for that in common initialisms
  fixed_title = re.sub("^Pov ", "POV ", fixed_title)
  fixed_title = re.sub(" Pov$", " POV", fixed_title)
  fixed_title = re.sub(" Pov ", " POV ", fixed_title)
  return fixed_title

def ExecFanGopher(args):
    platform_system = platform.system()
    fan_gopher_executable = ""
    if platform_system == "Windows":
      fan_gopher_executable = "winx64-1.0.2.exe"
    elif platform_system == "Darwin":
      fan_gopher_executable = "macx64-1.0.2"
    else:
      # Assume Linux for all other scenarios
      fan_gopher_executable = "linuxx64-1.0.2"

    # Working directory is presumed to be:
    # Plex Media Server\Plug-in Support\Data\com.plexapp.agents.fansforyou
    # However, we want to be executing from:
    # Plex Media Server\Plug-ins\FansForYou.Bundle\Contents\Code
    fan_gopher_path = abspath('../../../Plug-ins/FansForYou.Bundle/Contents/Code/fan-gopher-' + fan_gopher_executable)
    final_args = [fan_gopher_path]
    final_args.extend(args)
    app_output = "" + subprocess.check_output(final_args)
    for outputLine in app_output.split('\n'):
      if outputLine.startswith('{') and outputLine.endswith('}'):
        return outputLine
    return ""


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
    scene_title = FixTitle(regex_match.group(8))

    outputJson = ExecFanGopher(["-postID=" + scene_id, "-creatorName=" + artist, "-verify=true"])
    parsedResults = json.loads(outputJson)
    if "error" in parsedResults:
      if "true" == parsedResults["error"]:
        Log("Unable to verify post for creator " + artist + " can be found for ID " + scene_id + ": " + parsedResults["errorMessage"])
        return

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

    detailOutput = ExecFanGopher(["-postID=" + scene_id, "-creatorName=" + artist, "-get-details=true"])
    parsedDetails = json.loads(detailOutput)
    if "error" in parsedDetails:
      if "true" == parsedDetails["error"]:
        Log("Unable to get details for post for creator " + artist + " can be found for ID " + scene_id + ": " + parsedDetails["errorMessage"])
        return

    # Actors
    metadata.roles.clear()
    for actorDetail in parsedDetails["actorDetails"]:
      role = metadata.roles.new()
      role.name = actorDetail["actorName"]
      role.photo = actorDetail["profileImageUrl"]

    metadata.content_rating = "XXX"
    metadata.originally_available_at = datetime.datetime(int(year), int(month), int(day))
    metadata.year = metadata.originally_available_at.year
    metadata.summary = parsedDetails["videoDetails"]["videoDescription"]
    
    metadata.collections.clear()
    metadata.collections.add(artist)
    metadata.collections.add("OnlyFans")