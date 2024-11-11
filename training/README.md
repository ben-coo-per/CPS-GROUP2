# Wekinator

In our Wekinator setup, we're using eight neural networks. We chose this instead of a classifier because we wanted to capture the nuanced balance of themes within people's stories, as these narratives rarely align with a single theme but rather reflect varying degrees of multiple themes. Since Wekinator doesn’t natively support multi-class responses that provide "measured" values across themes, we chose to implement a continuous model for each theme, yielding values between 0 and 1.

Initially, we experimented with linear and polynomial regression, but the results were bad, with most models achieving an R² below 0.6. The neural network approach, however, performed better as we added hidden layers. This layering likely allowed the network to capture complex patterns in the word vectors that simpler models couldn’t, making it better at identifying each story’s alignment with different themes.

### Data

The [data](data/stories.csv) used for this project came from a range of sources:

- Primary recordings of people in our cohort (19)
- Reddit threadds of people talking about their favorite objects (47)
- Transcripts from the GQ videoseries "10 things I can't live without" (665)

The data is then transformed into vector representations from an NLP library (spacy) and sent to Wekinator.

---

# Training the models

This directory holds the code used to train and test the Wekinator model.

To train the model run:

1. Create a new Wekinator project with the following settings:
   - Port is set to `6448` (alternatively, you can tell the python script to target a different port in a future step)
   - INPUT: 300 inputs with the OSC message set to `/sentiment/input`
   - OUTPUT: 8 outputs, OSC Message is set to `/wek/outputs`
   - Set model type to "Continuous"
2. Adjust your window sizes so the Wekinator GUI is visible, then make sure the first_input_x, first_input_y coordinated are set to where the first model's input box is (I used the MacOS screenshot tool to find these coords)
3. Click "Start Recording"
4. Run `python -m training.main` and the python gui controller will automatically update the Wekinator weights & send data
5. Once all of the data is in Wekinator, click "Train"

#### Wekinator Models

Optionally, you can rename the wekinator models to match the mappings:

- Religion & Beliefs
- Loved Ones
- Travel & Cultures
- Achievements & Triumph
- Hobbies & Interests
- Aspirations
- Cues of Relief or Reassurance
- Practicality & Utility

## Testing Outputs

1. Make sure Wekinator is set to "Running"
2. (Optional - values will also be in Wekinator) Open two terminals and, in the first, run
   ```
   python -m training.listener
   ```
3. In the second terminal, run
   ```
   python -m training.tester --story <YOUR TEST STORY>
   ```
