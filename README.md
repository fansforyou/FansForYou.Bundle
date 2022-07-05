# FansForYou Plex Agent

This is an _unofficial_ OnlyFans Plex Metadata agent for managing your OnlyFans content.

At this time, this is largely nothing more than something that parses metadata from the filename. It does _not_ contact the OnlyFans website to download information about the scene.

Your filename should look like the following template:

```
OnlyFans - <OnlyFans account ID> - <date of post> - <post ID> - <title>.mp4
```

As an example:

```
OnlyFans - Petittits - 2022-02-10 - 268440502 - Dirty Talk and POV.mp4
```

## Installation

Download the FansForYou.Bundle.zip of your preferred release and place the contents of that ZIP file within a `Plug-ins\FansForYou.bundle` directory (such that, for example, the `Contents` folder is directly beneath that folder) within your Plex Media Service user data (e.g., within `%LOCALAPPDATA%\Plex Media Server\` on Windows).

## Troubleshooting

If you need help troubleshooting issues with this agent, refer to here.

### Logs

The CLI utility used by this agent - `fan-gopher` - writes logs to the `fan-gopher.log` file located in `Plug-in Support\Data\com.plexapp.agents.fansforyou` within your Plex Media Server user data (e.g., within `%LOCALAPPDATA%\Plex Media Server\` on Windows).