# Aphantasia and the Stroop Effect

**An independently programmed Python/PsychoPy experiment for an honors research project**

## Research background

*Aphantasia* is the absence or marked reduction of voluntary visual mental imagery. Someone with aphantasia may know what an object looks like without being able to picture it in their mind. This raises a question about cognition: does the ability to form mental images influence how we process visual information, even in tasks that do not explicitly ask us to imagine anything?

I explored this question using the **Stroop task**, a classic experiment in selective attention. Participants identify the ink color of a stimulus while ignoring its meaning. For example, the word “red” printed in blue ink creates a conflict between reading the word and naming the color. Comparing responses across conditions can help distinguish interference from facilitation in color identification.

**Research question:** How might differences in visual mental imagery be associated with reaction time and accuracy in the Stroop task, particularly with facilitation and interference?

## Designing and programming the experiment

For my honors research project, **I taught myself Python and used PsychoPy to program the behavioral experiment myself**. Instead of relying on a ready-made task, I implemented the stimulus presentation, trial randomization, keyboard responses, response timing, accuracy scoring, and data export.

The program (`s_stroop.py`) includes:

- **Three conditions:** congruent (color word and ink color match), incongruent (they conflict), and neutral (`XXXX` in colored ink).
- **60 trials per participant:** 20 trials in each condition, with randomized order and a constraint against three successive trials sharing the same condition or ink color.
- **Four response keys:** `1` = red, `2` = black, `3` = blue, `4` = green. Instructions and color words are presented in Chinese.
- **Timed responses:** up to 2 seconds to respond, followed by a 0.5-second interval between trials.
- **Trial-level data recording:** participant ID, age, condition, stimulus, ink color, key pressed, accuracy, and reaction time, exported to an individual CSV file.

## Data collection at Shanghai Jiao Tong University

**I conducted behavioral data collection in a psychology laboratory at Shanghai Jiao Tong University**, using the experiment I had programmed. The study included **33 participants: 3 with aphantasia and 30 controls**. This gave me experience administering an experiment and collecting reaction-time and accuracy data directly from participants, rather than working only with an existing dataset.

After collection, I analyzed the results using Stroop, interference, and facilitation indices. Given the small number of participants with aphantasia, I used Crawford–Howell single-case comparisons to examine their responses relative to the control group. The exploratory analysis suggested an unusual, reduced or reversed facilitation pattern in the aphantasia cases, a finding that requires caution because of the small sample.

## Repository contents

- **`s_stroop.py`** — the PsychoPy experiment used to present stimuli and record behavioral responses.

The uploaded script implements data collection; the statistical analyses were carried out separately. Participant-level data are not included in this public repository.

## Running the experiment

1. Install Python and [PsychoPy](https://www.psychopy.org/).
2. Open `s_stroop.py` in a Python environment with PsychoPy available and run the script.
3. Enter a participant ID and age, then follow the on-screen instructions.
4. The script saves trial responses to a file named `data_<participant_id>.csv` in the working directory.

The script uses the `Microsoft YaHei` font for Chinese text and may require a compatible font to be installed or configured on other systems.
