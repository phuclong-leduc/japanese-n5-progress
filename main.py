# This program shows the current Japanese learning progress of Le Duc Phuc Long
# (and was made by him too! =))

import tkinter as tk
from tkinter import font
from datetime import date, timedelta

# --- Configuration ---
# Adjust these values to match your study plan
LESSONS_IN_COURSE = 50
DAYS_PER_LESSON = 3
START_DATE = date(2025, 9, 10)

# --- GUI Design & Colors ---
# Feel free to change these colors to your liking!
# You can find color names here: http://www.tcl.tk/man/tcl8.6/TkCmd/colors.htm
WINDOW_BG = "#2E3440"       # A dark, calm blue-gray
PRIMARY_TEXT = "#ECEFF4"    # Off-white for readability
SECONDARY_TEXT = "#D8DEE9"  # Lighter gray for secondary info
ACCENT_COLOR = "#88C0D0"    # A cool, light blue for highlights
PROGRESS_BAR_EMPTY = "#4C566A" # Dark gray for the empty part of the bar
PROGRESS_BAR_FILL = "#A3BE8C"  # A calm, pleasant green for the filled bar

# --- Calculation Logic ---
def calculate_progress():
    """Calculates all the necessary progress details."""
    today = date.today()
    days_passed = (today - START_DATE).days

    if days_passed < 0:
        return None

    current_lesson_number = (days_passed // DAYS_PER_LESSON) + 1
    day_in_current_lesson = (days_passed % DAYS_PER_LESSON) + 1
    
    total_days_for_course = LESSONS_IN_COURSE * DAYS_PER_LESSON
    estimated_end_date = START_DATE + timedelta(days=total_days_for_course - 1)

    completion_percentage = min(100.0, (days_passed / total_days_for_course) * 100.0)

    return {
        "today": today.strftime('%A, %B %d, %Y'),
        "current_lesson": current_lesson_number,
        "day_in_lesson": day_in_current_lesson,
        "completion_percentage": completion_percentage,
        "estimated_end": estimated_end_date.strftime('%B %d, %Y'),
        "course_completed": current_lesson_number > LESSONS_IN_COURSE
    }

# --- Main Application Window ---
class ProgressApp(tk.Tk):
    def __init__(self, progress_data):
        super().__init__()
        self.progress_data = progress_data
        
        # --- Window Setup ---
        self.title("Le Duc Phuc Long's Japanese Learning Journey")
        self.geometry("600x450")
        self.configure(bg=WINDOW_BG)
        self.resizable(False, False) # Prevents resizing the window

        # --- Font Setup ---
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.header_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.body_font = font.Font(family="Helvetica", size=12)
        self.small_font = font.Font(family="Helvetica", size=10)
        self.jp_font = font.Font(family="Yu Gothic UI", size=14, weight="bold") # Good for Japanese characters

        # --- Create and place widgets ---
        self.create_widgets()

    def create_widgets(self):
        # Create a main frame to hold all content
        main_frame = tk.Frame(self, bg=WINDOW_BG, padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)

        # --- Header ---
        title_label = tk.Label(main_frame, text="🇯🇵 Japanese Learning Journey 🇯🇵",
                               font=self.title_font, bg=WINDOW_BG, fg=PRIMARY_TEXT)
        title_label.pack(pady=(0, 5))

        subtitle_label = tk.Label(main_frame, text=f"Today: {self.progress_data['today']}",
                                  font=self.body_font, bg=WINDOW_BG, fg=SECONDARY_TEXT)
        subtitle_label.pack(pady=(0, 25))

        # --- Check if course is completed ---
        if self.progress_data['course_completed']:
            self.display_completion_message(main_frame)
        else:
            self.display_progress_details(main_frame)

        # --- Footer ---
        footer_label = tk.Label(main_frame, text="頑張ってください (Ganbatte kudasai!)",
                                font=self.jp_font, bg=WINDOW_BG, fg=ACCENT_COLOR)
        footer_label.pack(side="bottom", pady=(20, 0))

    def display_progress_details(self, parent_frame):
        # --- Current Lesson Info ---
        lesson_frame = tk.Frame(parent_frame, bg=WINDOW_BG)
        lesson_frame.pack(pady=10, fill="x")
        
        tk.Label(lesson_frame, text="Current Focus:", font=self.header_font,
                 bg=WINDOW_BG, fg=ACCENT_COLOR).pack()
        tk.Label(lesson_frame, text=f"Lesson {self.progress_data['current_lesson']}", font=self.title_font,
                 bg=WINDOW_BG, fg=PRIMARY_TEXT).pack()
        tk.Label(lesson_frame, text=f"Day {self.progress_data['day_in_lesson']} of {DAYS_PER_LESSON}",
                 font=self.body_font, bg=WINDOW_BG, fg=SECONDARY_TEXT).pack()
        
        # --- Separator ---
        separator = tk.Frame(parent_frame, bg=SECONDARY_TEXT, height=1, width=400)
        separator.pack(pady=20)
        
        # --- Course Overview ---
        overview_frame = tk.Frame(parent_frame, bg=WINDOW_BG)
        overview_frame.pack(pady=10, fill="x")

        tk.Label(overview_frame, text="Course Overview", font=self.header_font,
                 bg=WINDOW_BG, fg=ACCENT_COLOR).pack()
        
        # Progress Bar
        progress_text = f"{self.progress_data['completion_percentage']:.1f}% Complete"
        tk.Label(overview_frame, text=progress_text, font=self.body_font,
                 bg=WINDOW_BG, fg=PRIMARY_TEXT).pack(pady=(10,5))
        
        bar_canvas = tk.Canvas(overview_frame, width=300, height=22, bg=PROGRESS_BAR_EMPTY,
                               highlightthickness=0, relief='flat', borderwidth=0)
        bar_canvas.pack()
        
        fill_width = 300 * (self.progress_data['completion_percentage'] / 100)
        bar_canvas.create_rectangle(0, 0, fill_width, 22, fill=PROGRESS_BAR_FILL, outline="")
        
        # Estimated End Date
        tk.Label(overview_frame, text=f"Estimated Finish: {self.progress_data['estimated_end']}",
                 font=self.body_font, bg=WINDOW_BG, fg=SECONDARY_TEXT).pack(pady=5)

    def display_completion_message(self, parent_frame):
        completion_text = "🎉 Congratulations! 🎉"
        completion_subtext = "You have completed the course!"
        
        tk.Label(parent_frame, text=completion_text, font=self.title_font,
                 bg=WINDOW_BG, fg=PROGRESS_BAR_FILL).pack(pady=(20, 10))
        tk.Label(parent_frame, text=completion_subtext, font=self.header_font,
                 bg=WINDOW_BG, fg=PRIMARY_TEXT).pack()

# --- Main Execution ---
if __name__ == "__main__":
    progress_data = calculate_progress()
    if progress_data is None:
        # Handle future start date with a simple dialog
        root = tk.Tk()
        root.withdraw() # Hide the main window
        tk.messagebox.showinfo("Not Yet!", f"Your Japanese learning journey is scheduled to begin on {START_DATE.strftime('%B %d, %Y')}.")
    else:
        app = ProgressApp(progress_data)
        app.mainloop()