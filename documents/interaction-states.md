# Interaction state machine

During their work, a user can perform different actions, such as moving the mouse, leaving the seat, or typing on the keyboard. Due to the fact that those actions are immediate, it is possible to instantly transition from any state to any other.

Each of the following states is defined in terms of those 2 parameters:

- **Gaze**: looking at the workspace(💻), looking elsewhere (🌲), not present (❌);
- **Voice**: any (❔), present (✔), none (❌);

## States

### Engagement

| Gaze | Voice |
| ---- | ----- |
| 💻   | ❌    |

In this state the user is actively engaged in their work through visual focus on the workspace (that is, the monitor in front of them).

### Conferencing

| Gaze | Voice |
| ---- | ----- |
| 💻   | ✔     |

In this state the user is communicating with their voice through an app (i.e. Zoom) on their device. It can also account for some collaborative work (i.e. pair programming).

### Idling

| Gaze | Voice |
| ---- | ----- |
| 🌲   | ❌    |

In this state the user is no longer actively focusing on their workspace, while still physically being on their seat and not communicating verbally.

### Distraction

| Gaze | Voice |
| ---- | ----- |
| 🌲   | ✔     |

In this state the user is being distracted from their work by looking outside of the workspace. For example, they are talking to a person nearby.

### Absense

| Gaze | Voice |
| ---- | ----- |
| ❌   | ❔    |

In this state the user has left their workplace. No work is being done.
