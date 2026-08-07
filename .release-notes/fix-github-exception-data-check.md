## Fix crash on unexpected GitHub error response format

When GitHub returned an error in an unexpected format, the bot could crash with a TypeError instead of retrying or reporting the original error.
