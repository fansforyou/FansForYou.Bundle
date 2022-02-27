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

## Actor Portrait URLs

Since this agent does not communicate with OnlyFans itself, this metadata agent exposes a way to provide a JSON object that keys OnlyFans account IDs to a portrait URL you have provided for that actor.

Using the example above, if you want a specific portrait URL to be used for the Petittits actor portrait, you can specify that in the actor portrait URLs like so:

```
{"Petittits":"https://i.ytimg.com/vi/iik25wqIuFo/maxresdefault.jpg"}
```

This _is_ case-sensitive, so make sure your OnlyFans account IDs are consistent!