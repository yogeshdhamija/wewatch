# We Watch

## Dependencies
- pipenv

## Makefile
- `init`
- `redis`
- `run`
- `clean`


## Dev Notes

Implementation idea for how to securely invite others to watch videos:

- Uploading new video creates random invite key, stored in db along with video.
- Owner can watch video anytime by going to `/watch/<id>` and it will only let them watch if they own the video (already implemented).
- Others (including owner, if they prefer) can watch by going to `/wewatch/<invite-key>`.
- Note: Must give owner option to re-create invite key, rendering old one invalid.

Pros:
- Anyone can join by clicking `/wewatch/<inite-key>` link.
- Can't find other people's videos unless have invite key.
- Distinction maintained between owner and watcher-- watcher can't delete video from owner's library.
- Owner has ability to make video private by choosing not to generate invite key.

Cons:
- Can't distinguish between watchers-- watchers cannot have viewing-only-rights, etc.
