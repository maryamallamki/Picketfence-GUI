#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pylinac import PicketFence
from pylinac.settings import get_dicom_cmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidgetItem, QHBoxLayout,QLayoutItem, QMessageBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QLabel, QFrame, QPushButton, QFileDialog, QAction, QMenuBar, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon, QImage
from PyQt5.QtCore import Qt
from pylinac import PicketFence
import matplotlib.pyplot as plt  # Import matplotlib for plotting
from matplotlib.colors import LinearSegmentedColormap
from pylinac.settings import get_dicom_cmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from py_linq import Enumerable
from pylinac import PicketFence
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSizePolicy  # Import QSizePolicy


class PicketFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        
        self.canvas_pf = None
        self.canvas_hist = None
        self.canvas_leaf = None

        self.setWindowTitle("Picket Fence Analysis")
        self.setGeometry(100, 100, 1000, 800)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        load_action = QAction("Load file", self)
        load_action.triggered.connect(self.load_image)
        file_menu.addAction(load_action)
        save_action = QAction("Save Results", self)
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)
        
        

        self.layout = QVBoxLayout()
        
        # Create a vertical layout for top, table, and bottom frames
        vertical_layout = QVBoxLayout()
        
        load_file_layout = QHBoxLayout()
        self.browse_button = QPushButton("Load File", self)
        self.browse_button.clicked.connect(self.load_image)
        load_file_layout.addWidget(self.browse_button)
        self.file_link_edit = QLineEdit(self)
        self.file_link_edit.setPlaceholderText("Selected File Link")
        load_file_layout.addWidget(self.file_link_edit)
        
        #vertical_layout.addLayout(load_file_layout)
        self.layout.addLayout(load_file_layout)
        
        
        self.top_frame = QFrame(self)
        self.top_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.top_frame.setLineWidth(2)
        self.top_frame.setFixedHeight(130)
        self.top_frame.setFixedWidth(400)
        top_layout = QVBoxLayout(self.top_frame)
        
        tolerance_layout = QHBoxLayout()
        tolerance_label = QLabel("Tolerance")
        self.tolerance_edit = QLineEdit(self)
        self.tolerance_edit.setPlaceholderText("Enter value")
        self.tolerance_edit.setText("0.15")
        tolerance_layout.addWidget(tolerance_label)
        tolerance_layout.addWidget(self.tolerance_edit)

        action_tolerance_layout = QHBoxLayout()
        action_tolerance_label = QLabel("Action Tolerance")
        self.action_tolerance_edit = QLineEdit(self)
        self.action_tolerance_edit.setPlaceholderText("Enter value")
        self.action_tolerance_edit.setText("0.03")
        action_tolerance_layout.addWidget(action_tolerance_label)
        action_tolerance_layout.addWidget(self.action_tolerance_edit)

        picket_layout = QHBoxLayout()
        picket_label = QLabel("Picket")
        self.picket_edit = QLineEdit(self)
        self.picket_edit.setPlaceholderText("Enter value")
        picket_layout.addWidget(picket_label)
        picket_layout.addWidget(self.picket_edit)

        leaf_layout = QHBoxLayout()
        leaf_label = QLabel("Leaf")
        self.leaf_edit = QLineEdit(self)
        self.leaf_edit.setPlaceholderText("Enter value")
        leaf_layout.addWidget(leaf_label)
        leaf_layout.addWidget(self.leaf_edit)
        
        top_layout.addLayout(tolerance_layout)
        top_layout.addLayout(action_tolerance_layout)
        top_layout.addLayout(picket_layout)
        top_layout.addLayout(leaf_layout)
        
        # Table frame
        self.table_frame = QFrame(self)
        self.table_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.table_frame.setLineWidth(2)
        self.table_frame.setFixedHeight(550)
        self.table_frame.setFixedWidth(400)
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Picket Fence Results", "Values"])
        table_layout = QVBoxLayout(self.table_frame)
        table_layout.addWidget(self.table_widget)
        
        # Bottom frame
        self.bottom_frame = QFrame(self)
        self.bottom_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.bottom_frame.setLineWidth(2)
        self.bottom_frame.setFixedHeight(60)
        self.bottom_frame.setFixedWidth(400)
        bottom_layout = QHBoxLayout(self.bottom_frame)
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_all_data)
        bottom_layout.addWidget(self.clear_button)
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_files)
        bottom_layout.addWidget(self.submit_button)
        
        # Add top, table, and bottom frames to the vertical layout
        vertical_layout.addWidget(self.top_frame)
        vertical_layout.addWidget(self.table_frame)
        vertical_layout.addWidget(self.bottom_frame)
        
        # Create a horizontal layout for the table frame and the image display frame
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(vertical_layout)

    
        # Create the main image display frame
        self.image_display_frame = QFrame(self)
        self.image_display_layout = QVBoxLayout(self.image_display_frame)
        self.image_display_frame.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.image_display_frame.setLineWidth(2)
        self.image_display_frame.setFixedHeight(772)
        self.image_display_frame.setFixedWidth(900)

        self.image_display_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Add the image display frame to the horizontal layout
        horizontal_layout.addWidget(self.image_display_frame)
        
        # Set the main layout for the main widget
        self.layout.addLayout(horizontal_layout)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    # Initialize other attributes and connections
        self.selected_files = []
        self.pdf_pages = None



    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", "Images (*.png *.dcm);;All Files (*)", options=options
        )

        if files:
            self.selected_files = files  # Store the selected files
            try:
               self.selected_files = files  # Store the selected files
               self.file_link_edit.setText(", ".join(self.selected_files))  # Display the selected file paths
               self.update_display()
               
            except Exception as e:
                # QMessageBox.critical(self, "Error", f"An error occurred while loading the file: {str(e)}")  
                 QMessageBox.critical(self, "error", str(e))

    def update_display(self):
        if self.selected_files:
            tolerance_text = self.tolerance_edit.text().strip()
            action_tolerance_text = self.action_tolerance_edit.text().strip()

        if not tolerance_text or not action_tolerance_text:
           # QMessageBox.warning(self, "Incomplete Information", "Please enter both tolerance and action tolerance.")
            return

        try:
            tolerance = float(tolerance_text)
            action_tolerance = float(action_tolerance_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Tolerance and action tolerance must be valid numbers.")
            return

            
            pf = PicketFence(self.selected_files[0])
            pf.analyze(tolerance, action_tolerance)
            pf = PicketFence(self.selected_files[0])
            pf.analyze(float(self.tolerance_edit.text()), float(self.action_tolerance_edit.text()))
            self.table_widget.setRowCount(0)
            for key, value in pf.results_data(as_dict=True).items():
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(key))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(value)))

            fig, ax = plt.subplots(figsize=(7, 7))
            ax.imshow(pf.image.array, cmap=get_dicom_cmap())
            for mlc_meas in pf.mlc_meas:
                mlc_meas.plot2axes(ax.axes, width=1.5)
            self.canvas_widget.figure = fig
            self.canvas_widget.draw()

    def clear_all_data(self):
        self.selected_files = []  # Clear the selected_files list
        self.file_link_edit.clear()  # Clear the file link edit field
        self.tolerance_edit.clear()
        self.action_tolerance_edit.clear()
        self.picket_edit.clear()
        self.leaf_edit.clear()
        self.clear_table()
        self.clear_canvas()
        self.selected_file = None
        

        
      # Clear and delete the canvas objects
        if self.canvas_pf:
           self.canvas_pf.deleteLater()
           self.canvas_pf = None
        if self.canvas_hist:
           self.canvas_hist.deleteLater()
           self.canvas_hist = None
        if self.canvas_leaf:
           self.canvas_leaf.deleteLater()
           self.canvas_leaf = None

        # Clear the images displayed in layouts
        self.clear_images()

    def clear_table(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)

    def clear_canvas(self):
        self.canvas_pf.figure.clear()
        self.canvas_pf.draw()
        self.canvas_hist.figure.clear()
        self.canvas_hist.draw()
        self.canvas_leaf.figure.clear()
        self.canvas_leaf.draw()
        
        
    def clear_images(self):
        while self.image_display_layout.count() > 0:
            widget_item = self.image_display_layout.takeAt(0)
            if isinstance(widget_item, QWidgetItem):
                widget = widget_item.widget()
                if widget:
                    widget.deleteLater()  # Delete the widget
            elif isinstance(widget_item, QLayoutItem):
                sub_layout = widget_item.layout()
                if sub_layout:
                    self.clear_sub_layout(sub_layout)

        # Clear the histogram display layout
        while self.histogram_display_layout.count() > 0:
            widget_item = self.histogram_display_layout.takeAt(0)
            if isinstance(widget_item, QWidgetItem):
                widget = widget_item.widget()
                if widget:
                    widget.deleteLater()  # Delete the widget
            elif isinstance(widget_item, QLayoutItem):
                sub_layout = widget_item.layout()
                if sub_layout:
                    self.clear_sub_layout(sub_layout)
    def clear_sub_layout(self, layout):
        while layout.count() > 0:
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_sub_layout(item.layout())    
        

    def submit_files(self):
        tolerance_text = self.tolerance_edit.text().strip()
        action_tolerance_text = self.action_tolerance_edit.text().strip()
        leaf_text = self.leaf_edit.text().strip()
        picket_text = self.picket_edit.text().strip()

        print(f"tolerance_text: '{tolerance_text}'")
        print(f"action_tolerance_text: '{action_tolerance_text}'")
        print(f"leaf_text: '{leaf_text}'")
        print(f"picket_text: '{picket_text}'")

        if not tolerance_text or not action_tolerance_text or not leaf_text or not picket_text:
            QMessageBox.warning(self, "Incomplete Information", "Please enter all required information.")
            return

        try:
            leaf = int(leaf_text)
            picket = int(picket_text)

        # Convert tolerance and action_tolerance to floats
            tolerance = float(tolerance_text)
            action_tolerance = float(action_tolerance_text)

            print(f"Tolerance: {tolerance}")
            print(f"Action Tolerance: {action_tolerance}")
            print(f"Leaf Profile: {leaf}")
            print(f"Picket: {picket}")

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Leaf, Picket, Tolerance, and Action Tolerance must be valid numbers.")
            return
        pf = PicketFence(self.selected_files[0])  # Use the first selected file

        if tolerance is not None and action_tolerance is not None:
            try:
                pf.analyze(tolerance, action_tolerance)
            except Exception as error:
                QMessageBox.warning(self, "Invalid Input", str(error))
        else:
            QMessageBox.warning(self, "Invalid Input", "Tolerance and Action Tolerance must be valid numbers.")
            return
            
            

 
       # Display the results in the table
        PF_dictionary = pf.results_data(as_dict=True)
        print(PF_dictionary)

        for key, value in PF_dictionary.items():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(key))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(value)))
            
        # Determine if the leafs have passed or failed
        has_failed = any(str != 'False' for str in PF_dictionary.values())
        print(PF_dictionary["passed"])
        if(PF_dictionary["passed"]):
            QMessageBox.information(self, "Picket Fence Analysis", "The leafs  test has passed .")
        else:
            QMessageBox.critical(self, "Picket Fence Analysis", "The leafs test has failed .")
     
        
        print("Submitting Files:", self.selected_files)   
        
       
        print(pf.results())
        
      
        
        
        #analysed image dispaly
        figure_size = (8, 8)
        fig, ax = plt.subplots(figsize=figure_size)
        ax.imshow(pf.image.array, cmap=get_dicom_cmap())
        leaf_error_subplot = True  # Replace with your condition for showing the subplot
        if leaf_error_subplot:
            pf._add_leaf_error_subplot(ax)
        guard_rails = True  # Replace with your condition for adding guard rails
        if guard_rails:
            for picket in pf.pickets:
                picket.add_guards_to_axes(ax.axes)

            # Add MLC peaks to the axes
        mlc_peaks = True  # Replace with your condition for adding MLC peaks
        if mlc_peaks:
            for mlc_meas in pf.mlc_meas:
                mlc_meas.plot2axes(ax.axes, width=1.5)

        # Create a canvas for the figure
        canvas_pf = FigureCanvas(fig)
        canvas_pf.draw()
        self.canvas_pf = canvas_pf  # Assign the canvas to the attribute
        self.image_display_layout.addWidget(canvas_pf)

        
        
        # histogram
        errors = Enumerable(pf.mlc_meas).select_many(lambda m: m.error).to_list()
        fig_hist, ax_hist = plt.subplots(figsize=figure_size)
        ax_hist.hist(errors, 10)#pf.plot_histogram()
        # put this in a function
        canvas_hist = FigureCanvas(fig_hist)
        canvas_hist.draw()
        self.canvas_hist = canvas_hist  # Assign the canvas to the attribute
        self.image_display_layout.addWidget(canvas_hist)
        
        
        # Call the plot_leaf_profile method using the pf object
        figure_size = (8, 8)
        picket = 2
        leaf = 20
        mlc_meas = Enumerable(pf.mlc_meas).single(
            lambda m: leaf in m.full_leaf_nums and m.picket_num == picket
        )
        print(mlc_meas)
        import numpy as np
        pix_vals = np.median(mlc_meas._image_window, axis=0)
        offset_pixels = max(mlc_meas._approximate_idx - mlc_meas._spacing / 2, 0)
        x_values = np.array(range(len(pix_vals))) + offset_pixels

        fig_leaf, ax_leaf = plt.subplots(figsize=figure_size)
        
        ax_leaf.plot(x_values, pix_vals)
        ax_leaf.set_title(f"MLC profile Leaf: {leaf}, Picket: {picket}")
        for picket_pos in mlc_meas.picket_positions:
            ax_leaf.axvline(
                x=picket_pos * mlc_meas._image.dpmm,
                label="Fitted picket location",
                color="black",
            )
        for pos, bg_color in zip(mlc_meas.get_peak_positions(), mlc_meas.bg_color):
            ax_leaf.axvline(pos, color=bg_color, label="Measured MLC position")
            
            for lg, rg, m in zip(
                    pf.pickets[picket].left_guard_separated,
                    pf.pickets[picket].right_guard_separated,
                    mlc_meas.marker_lines):
                
              g_val = lg(m.point1.y)
              rg_val = rg(m.point1.y)
              ax_leaf.axvline(g_val, color="green", label="Guard rail")
              ax_leaf.axvline(rg_val, color="green", label="Guard rail")
            
            
        ax_leaf.legend()
        canvas_leaf = FigureCanvas(fig_leaf)
        canvas_leaf.draw()
        self.canvas_leaf = canvas_leaf  # Assign the canvas to the attribute
        self.image_display_layout.addWidget(canvas_leaf)
       
        profile_and_histogram_layout = QHBoxLayout()

    # Add the leaf profile canvas to the layout
        profile_and_histogram_layout.addWidget(canvas_leaf)
        profile_and_histogram_layout.addSpacing(10)
        profile_and_histogram_layout.addWidget(canvas_hist)
        self.image_display_layout.addLayout(profile_and_histogram_layout)
        self.browse_button.setEnabled(True)
        
        
        
        
           

    def save_results(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
           self, "Save Results", "", "PDF Files (*.pdf);;PNG Files (*.png)", options=options
       )
        if file_name:
           # Save the PDF report using the PicketFence object
           if file_name.endswith(".pdf"):
               self.save_as_pdf(file_name)
           elif file_name.endswith(".png"):
               self.save_as_png(file_name)

    def save_as_pdf(self, file_name):
       if self.pdf_pages is None:
           self.pdf_pages = PdfPages(file_name)
           pf = PicketFence(self.selected_files[0])  # Create a PicketFence instance
           pf.analyze(float(self.tolerance_edit.text()), float(self.action_tolerance_edit.text()))
           pf.publish_pdf(file_name)  # Save the PDF report using PDFSaver

    def save_as_png(self, file_name):
       # Save the PNG image using the PicketFence object
       pf = PicketFence(self.selected_files[0])
       pf.analyze(float(self.tolerance_edit.text()), float(self.action_tolerance_edit.text()))
       pf.save_analyzed_image(file_name)
        
        
        
    
    
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PicketFenceApp()
    window.show()
    sys.exit(app.exec_())
