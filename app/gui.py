# Import required modules
import tkinter as tk # Base GUI module
from tkinter import ttk  # Themed widgets for modern look
from .summarizer import TextSummarizer  # Core summarization logic
from .utils import FileHandler # File operations handler

class TextSummarizerApp:
    def __init__(self):
        """Initialize main application components"""
        self.root = tk.Tk()  # Create root window
        self.summarizer = TextSummarizer() # Initialize NLP processor
        self.file_handler = FileHandler() # Initialize file manager
        self._create_styles() # Setup visual styles
        self._configure_root() # Configure window properties    
        self._setup_frames()# Build UI components

    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

    def _configure_root(self):
        """Configure main window properties"""
        self.root.title("Text Summarizer Pro") # Window title
        self.root.geometry("1000x700") # Initial size
        self.root.minsize(800, 600) # Minimum size constraints
        self.root.configure(bg=self.colors['background']) # Background color

    def _create_styles(self):
        """Define color scheme and widget styles"""
        self.colors = {
            'primary': '#2A3F5F', # Dark blue for primary elements
            'secondary': '#4F88C6', # Medium blue for secondary elements
            'background': '#F5F7FA', # Off-white background
            'text': '#2D3748' # Dark gray for text
        }
        # Configure ttk button style
        self.style = ttk.Style()
        self.style.configure('TButton', 
                             font=('Helvetica', 12), # Button text style
                             padding=8)  # Internal spacing
        # Define button states
        self.style.map('TButton',
            foreground=[('active', 'black'), ('!active', 'black')], # Text color
            background=[ # Background colors
                ('active', self.colors['secondary']), # Hover state
                ('!active', self.colors['primary']) # Normal state
            ]
        )

    def _setup_frames(self):
        """Create main container and sub-components"""
        self.main_frame = ttk.Frame(self.root) # Primary container
        self._create_input_section() # Text input area
        self._create_controls() # Control buttons and slider
        self._create_output_section() # Summary display area
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20) # Layout

    def _create_input_section(self):
        """Build text input section"""
        input_frame = ttk.LabelFrame(self.main_frame, text="Input Text", padding=15)
        # Text input widget with scrollbar
        self.input_text = tk.Text(input_frame, 
                                  wrap=tk.WORD, # Word wrapping
                                  height=15, # Visible lines
                                  font=('Helvetica', 12)) # Text formatting
        scrollbar = ttk.Scrollbar(input_frame, command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=scrollbar.set) # Link scrollbar
        # Layout components
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        input_frame.pack(fill=tk.BOTH, expand=True)

    def _create_controls(self):
        """Create control panel with interactive elements"""
        control_frame = ttk.Frame(self.main_frame)
        self.percentage = tk.DoubleVar(value=0.5) # Default 50% summary ratio
       
        # File load button
        ttk.Button(control_frame, 
                   text="Load File", 
                   command=self._load_file
                   ).pack(side=tk.LEFT, padx=5)
        
        # Summary length slider
        ttk.Scale(control_frame, 
                  variable=self.percentage, 
                  from_=0.1, to=0.9, 
                  command=self._update_percentage_label
                  ).pack(side=tk.LEFT, padx=15)
        
        # Percentage display label
        self.percentage_label = ttk.Label(control_frame, text="50%")
        self.percentage_label.pack(side=tk.LEFT, padx=5)
        
        # Summary generation button
        ttk.Button(control_frame, 
                   text="Generate Summary", 
                   command=self._generate_summary
                   ).pack(side=tk.LEFT, padx=10)
        
        control_frame.pack(fill=tk.X, pady=15)

    def _create_output_section(self):
        """Build summary output section"""
        output_frame = ttk.LabelFrame(self.main_frame, text="Summary", padding=15)
        # Summary display widget
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=10, font=('Helvetica', 12))
        scrollbar = ttk.Scrollbar(output_frame, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Layout components
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Action buttons container
        button_frame = ttk.Frame(self.main_frame)
        ttk.Button(button_frame, text="Save Summary", command=self._save_summary).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self._clear_all).pack(side=tk.RIGHT, padx=5)
        button_frame.pack(fill=tk.X, pady=10)

    def _update_percentage_label(self, *args):
        """Update percentage display when slider moves"""
        self.percentage_label.config(text=f"{int(self.percentage.get()*100)}%")

    def _load_file(self):
        """Handle file loading operation"""
        content = self.file_handler.load_text(self.root)
        if content:
            self.input_text.delete(1.0, tk.END) # Clear current text
            self.input_text.insert(tk.END, content) # Insert new content

    def _generate_summary(self):
        """Trigger summary generation"""
        text = self.input_text.get(1.0, tk.END).strip()
        if text:
            # Generate and display summary
            summary = self.summarizer.summarize(text, self.percentage.get())
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, summary)

    def _save_summary(self):
        """Handle summary saving"""
        summary = self.output_text.get(1.0, tk.END).strip()
        if summary:
            self.file_handler.save_summary(self.root, summary)

    def _clear_all(self):
        """Reset all inputs and outputs"""
        self.input_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.percentage.set(0.5)
        self.percentage_label.config(text="50%")