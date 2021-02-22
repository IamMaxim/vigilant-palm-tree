# Storage format

This document describes storage format for events from 3 sources: _engagement estimator_, _keyboard source_, _mouse_ source. Every event must have a timestamp so it possible to restore the timeline of user's **presence/absense** from the records sequence.

## Engagement estimator

### Engagement level change

Interaction states are described in details in [_interaction-states_ document](interaction-states.md). Here we will just assign integer codes to each of them. A record will be made only when the engagement level has changed.

| 0          | 1            | 2      | 3           | 4       |
| ---------- | ------------ | ------ | ----------- | ------- |
| engagement | conferencing | idling | distraction | absense |

```SQL
time: TEXT ("YYYY-MM-DD HH:MM:SS.SSS");
engagement_level: INTEGER (0-4);
```

## Keyboard source

### Key press

```SQL
time: TEXT ("YYYY-MM-DD HH:MM:SS.SSS");
key_code: TEXT;
```

## Mouse source

As of optimization techniques, for continious input channels like _mouse position_ or _mouse wheel scroll_, we will use hybrid of change-based and interval-based record *(since the wheel scroll is always relative, only interval-based optimisation is used)*. That is, an attempt to record a new entry will only be made every 100ms *(this interval can be easily adjusted later depending on the needs)*, and such attempt will only succeed if the current value differs from the last recorded one. This will allow us to save resources by recording only the non-redundant data as well as to have minimal impact on CPU because we record on the relevant time.

### Button click

| 0          | 1           | 2            |
| ---------- | ----------- | ------------ |
| left click | right click | middle click |

```SQL
time: TEXT ("YYYY-MM-DD HH:MM:SS.SSS");
key_code: INTEGER;
```

### Cursor position change

```SQL
time: TEXT ("YYYY-MM-DD HH:MM:SS.SSS");
cursor_position_x: INTEGER;
cursor_position_y: INTEGER;
```

### Wheel scroll

```SQL
time: TEXT ("YYYY-MM-DD HH:MM:SS.SSS");
scroll_delta: REAL;
```
