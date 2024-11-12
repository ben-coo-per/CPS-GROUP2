#ifndef APPSTATE_H
#define APPSTATE_H

// Define the app states
enum AppState {
    Idle = 0,
    Recording = 1,
    Playback = 2
};

// Declare the appState variable as extern so it can be accessed across files
extern AppState appState;
extern String lightPattern;

#endif
