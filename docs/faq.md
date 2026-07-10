# FAQ

## Why APScheduler 3.x and not 4?

APScheduler 4 has been in pre-release for years. The 3.x line is stable and covers interval + cron completely. The pin is `>= 3.10, < 4`; the module will migrate deliberately when 4 ships stable.

## How do I stop jobs in tests?

Either shut the container down (jobs stop with it) or set `scheduling.enabled: false` in the test config.

## What happens if a job overlaps its next tick?

APScheduler's default policy applies: a still-running job skips the next fire with a warning. Keep scheduled work shorter than its interval or delegate the heavy part to pico-celery.

## Why did my async job block the event loop?

It does not: async methods run through `asyncio.run` inside the scheduler's own worker thread, not on your application's loop. For loop-integrated work, schedule a sync method that enqueues onto your loop instead.
