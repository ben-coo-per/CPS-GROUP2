# Wekinator Training

This directory holds the code used to train and test the Wekinator model.
To train the model run

1. Create a new Wekinator project with the following settings:
   - Port is set to `6448` (alternatively, you can tell the python script to target a different port in a future step)
   - INPUT: 300 inputs with the OSC message set to `/sentiment/input`
   - OUTPUT: 1 output OSC Message is set to `/wek/outputs`
   - Set model type to classifier
2. Click "Start Recording" & set the output model to "1"
3. Run `python training.py` and you will be guided through each class.
4. When a class finishes sending, you will be prompted to set the next class in Wekinator and continue.
5. Once all of the data is in Wekinator, click "Train"

### Wekinator class mapping

To change the number of classes or change the data, you can update the `stories.py` file in the data dir.
Joy = 1
Trust (or Acceptance) = 2
Fear = 3
Surprise = 4
Sadness = 5
Disgust = 6
Anger = 7
Anticipation = 8

# To test outputs

1. Make sure Wekinator is set to "Running"
2. Open two terminals and, in the first, run
   ```
   python listener.py
   ```
3. In the second terminal, run
   ```
   python tester.py --story <YOUR TEST STORY>
   ```
