# Interaction state machine

During their work, a user can perform different actions, such as moving the mouse, leaving the seat, or typing on the keyboard. Due to the fact that those actions are immediate, it is possible to instantly transition from any state to any other.

Each of the following states is defined in terms of those 3 parameters:

- **Gaze**: workspace(💻), elsewhere (🌲), none (❌);
- **Voice**: any (❔), present (✔), none (❌);
- **Input**: any(❔), mouse & keyboard (✔), none (❌).

## States

### Engagement

| Gaze | Voice | Input |
| ---- | ----- | ----- |
| 💻   | ❔    | ✔     |

In this state the user is actively engaged in their work through visual focus on the workspace (that is, the monitor or the table in front of them) and active input from the mouse and/or keyboard.

### Idling

| Gaze | Voice | Input |
| ---- | ----- | ----- |
| 💻   | ❔    | ❌    |

In this state the user is passively engaged in the work, i.e. he is thinking about the problem or sketching on a paper. Due to the lack of the input, no traceable progress can be recognized.

### Conferencing

| Gaze | Voice | Input |
| ---- | ----- | ----- |
| 💻   | ✔     | ❌    |

In this state the user is communicating with their voice through an app (i.e. Zoom) on their device.

### Distraction

| Gaze | Voice | Input |
| ---- | ----- | ----- |
| 🌲   | ❔    | ❔    |

In this state the user is being distracted from their work by looking outside of the workspace. For example, they are talking to a person nearby.

### Absense

| Gaze | Voice | Input |
| ---- | ----- | ----- |
| ❌   | ❔    | ❔    |

In this state the user has left their workplace. No work is being done.
