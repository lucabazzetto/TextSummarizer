# Import required GUI components
from tkinter import filedialog, messagebox # File dialogs and message boxes

class FileHandler:
    """Handles file operations for loading/saving text content"""
    @staticmethod
    def load_text(parent):
        """
        Open and read text file content
        Args:
            parent: Parent window for dialog positioning
        Returns:
            str: File content or None if cancelled/error
        """
        # Configure file selection dialog
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt")], # Limit to .txt files
            title="Select Text File" # Dialog title
        )
        if file_path: # Proceed if user selected file
            try:
                # Open file with UTF-8 encoding
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read() # Return file contents
            except Exception as e:  # Handle any file errors
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}") # Show detailed error
        return None # Return empty if cancelled or error

    @staticmethod
    def save_summary(parent, content):
        """
        Save summary text to file
        Args:
            parent: Parent window for dialog positioning
            content: Text content to save
        """
        # Configure save file dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", # Auto-add .txt extension
            filetypes=[("Text Files", "*.txt")],  # Force text files
            title="Save Summary" # Dialog title
        )
        if file_path: # Proceed if user provided path
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content) # Save text content
                messagebox.showinfo("Success", "Summary saved successfully!") # User feedback
            except Exception as e: # Handle write errors
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}") # Detailed error