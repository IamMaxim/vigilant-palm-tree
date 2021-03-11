# Storage format

This document describes storage format for events from 3 sources: _engagement estimator_, _keyboard source_, _mouse source_, _audio source_. Every event must have a timestamp so it possible to restore the timeline of user's **presence/absense** from the records sequence.

## Engagement estimator

Interaction states are described in details in [_interaction-states_ document](interaction-states.md). Here we will just assign integer codes to each of them. A record will be made only when the engagement level has changed.

| 1          | 2            | 3      | 4           | 5       |
| ---------- | ------------ | ------ | ----------- | ------- |
| engagement | conferencing | idling | distraction | absense |

SQLite

```SQL
code: integer NOT NULL;
timestamp: integer NOT NULL;
```

## Keyboard source

SQLite

```sql
type text NOT NULL;
scancode: text NOT NULL;
modifiers: text NOT NULL;
timestamp: integer NOT NULL;
```

FileStore

```text
f'{event_type} {name} {scan_code} {time}\n'
```

## Mouse source

As of optimization techniques, for continious input channels like _mouse position_ or _mouse wheel scroll_, we will use hybrid of change-based and interval-based record _(since the wheel scroll is always relative, only interval-based optimisation is used)_. That is, an attempt to record a new entry will only be made every 100ms _(this interval can be easily adjusted later depending on the needs)_, and such attempt will only succeed if the current value differs from the last recorded one. This will allow us to save resources by recording only the non-redundant data as well as to have minimal impact on CPU because we record on the relevant time.

SQLite

```sql
type text NOT NULL;
x integer;
y integer;
wheel_delta integer;
button text;
timestamp integer NOT NULL;
```

FileStore

```text
# button
f'button {button} {type} {time}\n'

# wheel
f'wheel {delta} {time}\n'

# move
f'move {x} {y} {time}\n'
```

## Audio source

FileStore

```text
frame
```

_The audio frame is an **np.ndarray**._
