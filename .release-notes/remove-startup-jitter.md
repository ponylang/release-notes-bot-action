## Remove random startup jitter

The bot no longer waits up to 60 seconds before starting. Rate-limit collisions are handled by the existing exponential backoff when they actually occur.
