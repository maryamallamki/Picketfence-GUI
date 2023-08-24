

```markdown
# Picket Fence Analysis Application

This is a PyQt5-based application for performing Picket Fence analysis on medical images. Picket Fence analysis is a technique used in radiation therapy to evaluate the accuracy of multi-leaf collimators (MLCs) in linear accelerators.

## Getting Started

To use this application, make sure you have Python 3 and the required dependencies installed. You can install the dependencies using the following command:

```bash
pip install pylinac matplotlib PyQt5 py-linq
```

## How to Run

Run the application by executing the following command:

```bash
python picketfenceGUI.py
```

Replace `picketfenceGUI.py` with the name of the Python script that contains the provided code.

## Usage

1. Launch the application.
2. Use the "Load File" button to select the DICOM or PNG image to be analyzed.
3. Enter the tolerance and action tolerance values in the respective input fields.
4. Enter the picket and leaf numbers to analyze (optional).
5. Click the "Submit" button to perform the Picket Fence analysis.
6. The results will be displayed in a table and visualized through graphs.

## Saving Results

You can save the analysis results as a PDF report or a PNG image:

- To save as a PDF report, click the "Save Results" button and choose a file name with the `.pdf` extension.
- To save the analyzed image as a PNG, also click the "Save Results" button and choose a file name with the `.png` extension.

