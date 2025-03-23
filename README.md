# Expert System for Medical Diagnosis

This project is a simple expert system implemented in Python. It uses **Pygame** for the user interface and **Graphviz** for visualizing the knowledge base. The expert system is designed for medical diagnosis with a focus on respiratory and cardiac domains, though it can be extended to other domains with minimal modifications.

---

## Features

- **Interactive UI:**  
  A graphical interface built using Pygame to input facts (symptoms) and visualize the inference process.
  
- **Forward Chaining Inference Engine:**  
  Uses a forward chaining approach to apply rules and deduce conclusions based on the entered facts.
  
- **Knowledge Base Visualization:**  
  Generates a visual representation of the knowledge base using Graphviz. Nodes represent facts (in blue) and rules (in gray), with edges connecting conditions to conclusions.

- **Domain Selection:**  
  Supports respiratory, cardiac, or a combination of both domains for inference, with pre-defined rules for each domain.

---

## Project Structure

- **main.py:**  
  The only source file for this project. It contains:
  - Helper functions for drawing text.
  - Core expert system classes: `KnowledgeBase`, `Rule`, `InferenceEngine`, and `Visualizer`.
  - An advanced user interface class (`UserInterface`) built with Pygame.
  - Application initialization and execution logic.

---

## Requirements

- **Python 3.6+**
- **Pygame:** For creating the graphical user interface.
- **Graphviz:** For generating the knowledge base visualization.
  - Ensure you have both the Python package (`graphviz`) and the Graphviz software installed on your system.

### Installing Dependencies

You can install the necessary Python packages using pip:

```bash
pip install pygame graphviz
```

For Graphviz installation, refer to the [Graphviz download page](https://graphviz.org/download/) for instructions specific to your operating system.

---

## Usage

1. **Run the Application:**

   Execute the main file to start the expert system interface:
   
   ```bash
   python main.py
   ```

2. **Interacting with the Expert System:**

   - **Enter Facts:**  
     Type a symptom (fact) into the input box and press **Enter** or click the **Add Fact** button.
   
   - **Submit for Inference:**  
     Click the **Submit** button to process the entered facts using the forward chaining inference engine. The inferred facts will be displayed in the Inference Output panel.
   
   - **Reset:**  
     Use the **Reset** button to clear all entered facts, inferred results, and event logs.
   
   - **Visualize Knowledge Base:**  
     Click the **Visualize** button to generate and display a graphical representation of the current knowledge base. This will open the visualization in your default image viewer and display a scaled version in the UI.

3. **Domain Selection:**

   - Choose between **Respiratory**, **Cardiac**, or **Both** domains using the radio buttons. The selected domain will determine which set of rules is applied during inference.

---

## Notes

- The system demonstrates a simple expert system mechanism and serves as a starting point for more advanced implementations.
- You can extend the knowledge base by adding more facts and rules or adapting the UI to include more functionalities.
- The project is intended for educational purposes and may be adapted for other diagnostic domains with further development.