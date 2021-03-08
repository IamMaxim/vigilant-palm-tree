# Glossary

The keys terms used in the project.

## Conceptual terms

| Term                  | Description                                                                                                         |
| --------------------- | ------------------------------------------------------------------------------------------------------------------- |
| **Gaze code**         | Representation of user's gaze, encoded as 3 states (workspace, elsewhere, absent)                                   |
| **Voice code**        | Representation of user's voice, encoded as 2 states (present, absent).                                              |
| **Interaction state** | Estimation of user's activity at any given time based on their gaze and speech inputs.                              |
| **Engagement level**  | Scale of user's involment into their working process. Consists of 5 levels mapping to the interaction states.       |
| **User presence**     | State of active engagement. Corresponds to the engagement levels 0-1.                                               |
| **User absence**      | State of lack of engagement. Corresponds to the engagement levels 2-4.                                              |
| **Tracking sequence** | Present/absent timeline used for representing user's activities over a period of time.                              |
| **Storage format**    | Data fields and their types used for storing recoding sequence. There are 2 such formats - for SQL and File stores. |

## Technical terms

### Base classes

| Term               | Description                                                              |
| ------------------ | ------------------------------------------------------------------------ |
| **Source node**    | Base class for data sources, e.g. `DeviceVideoSource`, `KeyboardSource`  |
| **Processor node** | Base class for data processors, e.g. `SpeechDetector`, `MouseCompressor` |
| **Sink node**      | Base class for data sinks, e.g. `SQLiteStore`, `GraphView`               |

### Source nodes

| Term                  | Description                                                              |
| --------------------- | ------------------------------------------------------------------------ |
| **DeviceVideoSource** | Provides a video stream coming from a physical device (e.g. webcamera)   |
| **MP4VideoSource**    | Provides a video stream coming from an MP4 video file.                   |
| **DeviceAudioSource** | Provides an audio stream coming from a physical device (e.g. microphone) |
| **WAVAudioSource**    | Provides an audio stream coming from a WAV audio file.                   |
| **KeyboardSource**    | Provides a stream of keystrokes coming to the system.                    |
| **MouseSource**       | Provides a stream of mouse events (move, click) coming to the system.    |

### Processor nodes

| Term                    | Description                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| **GazeDetector**        | Converts a video stream to a stream of gaze codes.                                               |
| **SpeechDetector**      | Detects speech in an audio stream and outputs a signal stream for that.                          |
| **EngagementEstimator** | Converts the gaze code and the speech presence signal into a prediction of the engagement level. |
| **MouseCompressor**     | Compresses a stream of mouse events to reduce redundancy.                                        |

### Sink nodes

| Term             | Description                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------- |
| **VideoDisplay** | Displays a video stream in a window.                                                     |
| **SQLiteStore**  | Persistently store the engagement level and keyboard/mouse events in an SQLite database. |
| **FileStore**    | Persistently store the audio and keyboard/mouse events in the filesystem.                |
| **GraphView**    | Displays an ongoing graph of presence of the user.                                       |
