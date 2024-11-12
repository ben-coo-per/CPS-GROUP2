
![image](https://github.com/user-attachments/assets/c13a14fa-3d20-4a08-b5a8-2ff5180cef94)

This flowchart outlines the data flow from when a participant presses the record button to when they receive a printed commemorative ticket.

1. **Initiation and Recording**: The process begins when the participant presses a button, which triggers the system to update the `AppState` to "RECORDING." This state change activates audio recording, allowing the participant to share their story related to the object they’ve placed on the podium. When the participant releases the button, the recording stops, and the `AppState` shifts to "LOADING." The recorded audio file is then saved to a temporary location for further processing.

2. **Transcription and Vectorization**: Once the audio is saved, it is sent to a transcription API (e.g., OpenAI Whisper) to convert the spoken story into text. This transcription is subsequently processed with Natural Language Processing (NLP) using SpaCy to transform the text into vectorized data. This vectorization makes it possible to analyze the story’s thematic content numerically, enabling it to be processed by machine learning models.

3. **Theme Detection with Wekinator**: The vectorized transcription is fed into a series of Wekinator neural network models. Each model represents a different theme, and the continuous output values (normalized between 0 and 1) indicate the degree to which the story aligns with each theme. This approach provides a nuanced understanding of the story, capturing multiple themes as opposed to a single classification.

4. **Serial Communication and Output Updates**: The normalized theme outputs are packaged for serial communication with the Arduino, which manages the lighting and motor effects in response to the detected themes. The system enters the "PLAYBACK" state, where the lights and motors are updated to reflect a unique color pattern or motion that visually embodies the themes present in the participant’s story.

5. **Ticket Generation and Idle State**: After the visual feedback is provided, the system generates a personalized ticket with information about the object and themes detected in the story. The ticket is printed, providing a keepsake for the participant. The system then resets, updating the `AppState` and `Arduino AppState` to "IDLE," ready for the next participant to initiate a new story session by pressing the button again.
