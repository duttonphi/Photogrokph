# PhotoGrokfff - Tool to Wrangle Your Digitized Photographs
# Designed by @DuttonΦ w/ coding assistant Grok (xAI March 2025)

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import shutil
import argparse
import re
import yaml

class ImageDuplicator:
    def __init__(self, root, input_folder):
        self.root = root
        self.input_folder = os.path.abspath(input_folder)
        self.current_index = 0
        self.max_thumbnail_size = 350
        self.thumbnail_container_height = 400
        self.copy_counts = {}
        self.split_counts = {}
        self.grid_mode = None
        self.desc_visible = False
        self.descriptions = self.load_descriptions()
        
        self.root.title("PhotoGrokfff")
        self.root.configure(bg="black")
        self.root.geometry("+100+100")
        
        self.style = ttk.Style()
        self.style.configure("Default.TLabel", font=("Arial", 10), foreground="white")
        self.style.configure("Highlighted.TLabel", font=("Arial", 20), foreground="#00FF00")
        self.style.configure("Black.TFrame", background="black")
        self.style.configure("Black.TCheckbutton", background="black", foreground="white")
        
        self.filename_frame = ttk.Frame(root, style="Black.TFrame")
        self.filename_frame.pack(pady=5)
        self.filename_label = ttk.Label(self.filename_frame, text="Loading...", font=("Arial", 12), foreground="#FFFFFF")
        self.filename_label.pack()

        self.progress_frame = ttk.Frame(root, style="Black.TFrame")
        self.progress_frame.pack()
        self.progress_label = ttk.Label(self.progress_frame, text="", style="Default.TLabel")
        self.progress_label.pack()

        self.copy_count_frame = ttk.Frame(root, style="Black.TFrame")
        self.copy_count_frame.pack()
        self.copy_count_label = ttk.Label(self.copy_count_frame, text="Copy count: 0", style="Default.TLabel")
        self.copy_count_label.pack()

        self.split_count_frame = ttk.Frame(root, style="Black.TFrame")
        self.split_count_frame.pack()
        self.split_count_label = ttk.Label(self.split_count_frame, text="Split count: 0", style="Default.TLabel")
        self.split_count_label.pack()

        self.total_files_frame = ttk.Frame(root, style="Black.TFrame")
        self.total_files_frame.pack()
        self.total_files_label = ttk.Label(self.total_files_frame, text="Total files: 0", style="Default.TLabel")
        self.total_files_label.pack()

        self.thumbnail_frame = ttk.Frame(root, style="Black.TFrame", height=self.thumbnail_container_height)
        self.thumbnail_frame.pack(fill=tk.X, pady=5)
        self.thumbnail_frame.pack_propagate(False)
        
        self.canvas = tk.Canvas(self.thumbnail_frame, bg="black", width=self.max_thumbnail_size, height=self.max_thumbnail_size)
        self.canvas.pack(expand=True)

        self.nav_frame = ttk.Frame(root, style="Black.TFrame")
        self.nav_frame.pack(pady=5)

        self.prev_split_btn = ttk.Button(self.nav_frame, text="Prev w/ Split", command=self.prev_with_split)
        self.prev_split_btn.pack(side=tk.LEFT, padx=5)

        self.prev_copy_btn = ttk.Button(self.nav_frame, text="Prev w/ Copy", command=self.prev_with_copy)
        self.prev_copy_btn.pack(side=tk.LEFT, padx=5)

        self.prev_btn = ttk.Button(self.nav_frame, text="Prev", command=self.prev_image)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(self.nav_frame, text="Next", command=self.next_image)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.next_copy_btn = ttk.Button(self.nav_frame, text="Next w/ Copy", command=self.next_with_copy)
        self.next_copy_btn.pack(side=tk.LEFT, padx=5)

        self.next_split_btn = ttk.Button(self.nav_frame, text="Next w/ Split", command=self.next_with_split)
        self.next_split_btn.pack(side=tk.LEFT, padx=5)

        self.goto_entry = ttk.Entry(self.nav_frame, width=5)
        self.goto_entry.pack(side=tk.LEFT, padx=5)
        self.goto_btn = ttk.Button(self.nav_frame, text="Goto", command=self.goto_image)
        self.goto_btn.pack(side=tk.LEFT, padx=5)

        self.dupe_frame = ttk.Frame(root, style="Black.TFrame")
        self.dupe_frame.pack(pady=5)

        for num in [2, 3, 4]:
            btn = ttk.Button(self.dupe_frame, text=str(num), 
                            command=lambda n=num: self.duplicate_image(n - 1))
            btn.pack(side=tk.LEFT, padx=5)

        self.custom_entry = ttk.Entry(self.dupe_frame, width=5)
        self.custom_entry.pack(side=tk.LEFT, padx=5)
        self.submit_btn = ttk.Button(self.dupe_frame, text="Submit", 
                                    command=self.submit_custom)
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        self.desc_btn = ttk.Button(self.dupe_frame, text="Desc", command=self.toggle_desc)
        self.desc_btn.pack(side=tk.LEFT, padx=5)

        self.dedup_btn = ttk.Button(self.dupe_frame, text="DeDup", command=self.deduplicate_image)
        self.dedup_btn.pack(side=tk.LEFT, padx=5)

        self.desplit_btn = ttk.Button(self.dupe_frame, text="DeSplit", command=self.desplit_image)
        self.desplit_btn.pack(side=tk.LEFT, padx=5)

        self.grid_split_frame = ttk.Frame(root, style="Black.TFrame")
        self.grid_split_frame.pack(pady=5)

        self.grid_top_frame = ttk.Frame(self.grid_split_frame, style="Black.TFrame")
        self.grid_top_frame.pack(side=tk.TOP)

        self.grid4_btn = ttk.Button(self.grid_top_frame, text="Grid4", command=lambda: self.toggle_grid("4"))
        self.grid4_btn.pack(side=tk.LEFT, padx=2)

        self.grid3_btn = ttk.Button(self.grid_top_frame, text="Grid3", command=lambda: self.toggle_grid("3"))
        self.grid3_btn.pack(side=tk.LEFT, padx=2)

        self.grid3down_btn = ttk.Button(self.grid_top_frame, text="Grid3Down", command=lambda: self.toggle_grid("3Down"))
        self.grid3down_btn.pack(side=tk.LEFT, padx=2)

        self.grid3across_btn = ttk.Button(self.grid_top_frame, text="Grid3Across", command=lambda: self.toggle_grid("3Across"))
        self.grid3across_btn.pack(side=tk.LEFT, padx=2)

        self.grid2down_btn = ttk.Button(self.grid_top_frame, text="Grid2Down", command=lambda: self.toggle_grid("2Down"))
        self.grid2down_btn.pack(side=tk.LEFT, padx=2)

        self.grid2across_btn = ttk.Button(self.grid_top_frame, text="Grid2Across", command=lambda: self.toggle_grid("2Across"))
        self.grid2across_btn.pack(side=tk.LEFT, padx=2)

        self.split_bottom_frame = ttk.Frame(self.grid_split_frame, style="Black.TFrame")
        self.split_bottom_frame.pack(side=tk.TOP)

        self.split4_btn = ttk.Button(self.split_bottom_frame, text="Split4", command=self.split4)
        self.split4_btn.pack(side=tk.LEFT, padx=2)

        self.split3_btn = ttk.Button(self.split_bottom_frame, text="Split3", command=self.split3)
        self.split3_btn.pack(side=tk.LEFT, padx=2)

        self.split3down_btn = ttk.Button(self.split_bottom_frame, text="Split3Down", command=self.split3down)
        self.split3down_btn.pack(side=tk.LEFT, padx=2)

        self.split3across_btn = ttk.Button(self.split_bottom_frame, text="Split3Across", command=self.split3across)
        self.split3across_btn.pack(side=tk.LEFT, padx=2)

        self.split2down_btn = ttk.Button(self.split_bottom_frame, text="Split2Down", command=self.split2down)
        self.split2down_btn.pack(side=tk.LEFT, padx=2)

        self.split2across_btn = ttk.Button(self.split_bottom_frame, text="Split2Across", command=self.split2across)
        self.split2across_btn.pack(side=tk.LEFT, padx=2)

        self.desc_frame = ttk.Frame(root, style="Black.TFrame")
        self.desc_text = tk.Text(self.desc_frame, height=2, width=50, bg="black", fg="white", font=("Arial", 10))
        self.desc_text.pack(pady=5)
        self.desc_text.bind("<KeyRelease>", self.update_description)

        self.auto_frame = ttk.Frame(root, style="Black.TFrame")
        self.auto_advance_var = tk.BooleanVar(value=True)
        self.auto_advance_check = ttk.Checkbutton(self.auto_frame, text="AutoAdvance", 
                                                 variable=self.auto_advance_var, style="Black.TCheckbutton")
        self.auto_advance_check.pack(side=tk.LEFT, padx=5)
        
        self.about_btn = ttk.Button(self.auto_frame, text="About", command=self.show_about)
        self.about_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_file_list()
        self.load_image()

    def load_descriptions(self):
        desc_file = os.path.join(self.input_folder, "descriptions.yaml")
        if os.path.exists(desc_file):
            with open(desc_file, "r") as f:
                return yaml.safe_load(f) or {}
        return {}

    def save_descriptions(self):
        desc_file = os.path.join(self.input_folder, "descriptions.yaml")
        with open(desc_file, "w") as f:
            yaml.safe_dump(self.descriptions, f, default_flow_style=False)

    def update_description(self, event=None):
        if self.desc_visible and self.image_files:
            current_file = self.image_files[self.current_index]
            desc = self.desc_text.get("1.0", tk.END).strip()
            if desc:
                self.descriptions[current_file] = desc
            elif current_file in self.descriptions:
                del self.descriptions[current_file]
            self.save_descriptions()

    def show_about(self):
        about_win = tk.Toplevel(self.root)
        about_win.title("About PhotoGrokfff")
        about_win.configure(bg="black")
        about_win.geometry("625x400")
        
        about_text = (
            "PhotoGrokfff\n\n"
            "A tool for wrangling manually digitized photographs.\n\n\n"
            "  So you used your phone to digitize hundreds of old family photo prints.\n"
            "  You got clever and laid out a 2x2 grid of physical photographs in order to effectively digitize 4, 3, or 2 at a time.\n"
            "  Oops! Now you need to split that 1 image into 4, 3, or 2 parts!\n\n"
            "  That's what this tool is for! You split the image after looking at a grid overlay preview.\n"
            "  If the grid isn't to your liking because photos were crooked when digitized, then just\n"
            "  use the 'duplicate' buttons labeled '4','3','2' which is the number of logical images in your core image.\n"
            "  After making duplicates you can manually crop them outside of this tool.\n\n"
            "Features:\n\n"
            "- Display 4,3,2 quadrant reference grids\n"
            "- Duplicate images with '2', '3', '4' for manual cropping (when grid does not align to core image).\n"
            "- Auto-split multi-photo snaps with 'Split' buttons (4, 3, etc.) into separate files. (Use Grid buttons to see grid)\n"
            "- Navigate originals or jump to next/prev duplicates/splits that have copy/split counts.\n"
            "- Write descriptions for each photo, saved in 'descriptions.yaml'. (see 'Desc' button)\n"
            "Built for tinkers and Makers to support quick 4scans-at-one-time photo digitizing workflow.\n\n"
            "~|~ Code Assistant: Grok3 (March 2025) ~|~ App Designed by @DuttonΦ ~|~"
        )
        
        label = tk.Label(about_win, text=about_text, bg="black", fg="white", font=("Arial", 12), justify=tk.LEFT)
        label.pack(pady=10, padx=10)
        
        close_btn = ttk.Button(about_win, text="Close", command=about_win.destroy)
        close_btn.pack(pady=5)

    def refresh_file_list(self):
        self.all_files = [f for f in os.listdir(self.input_folder) 
                          if not f.startswith('.') and f.lower().endswith(('.jpg', '.png', '.jpeg'))]
        self.image_files = [f for f in self.all_files if "copy" not in f.lower()]
        print(f"Found {len(self.all_files)} total image files in {self.input_folder}")
        print(f"Logical originals (no 'copy'): {len(self.image_files)}")
        if self.all_files:
            print(f"First few files: {self.all_files[:3]}")
        
        numeral_counts = set()
        for f in self.image_files:
            match = re.search(r' - (\d+)\.', f)
            if match:
                numeral_counts.add(int(match.group(1)))
        if numeral_counts:
            max_numeral = max(numeral_counts)
            print(f"Max numeral from filenames: {max_numeral}")
            if max_numeral != len(self.image_files):
                print(f"Warning: Numeral count ({max_numeral}) differs from logical count ({len(self.image_files)})")
        
        self.update_copy_counts()
        self.update_split_counts()

    def update_copy_counts(self):
        self.copy_counts.clear()
        for orig_file in self.image_files:
            base_name, _ = os.path.splitext(orig_file)
            count = sum(1 for f in self.all_files if f.startswith(f"{base_name}.copy") and 
                       f.lower().endswith(('.jpg', '.png', '.jpeg')))
            self.copy_counts[orig_file] = count

    def update_split_counts(self):
        self.split_counts.clear()
        for orig_file in self.image_files:
            base_name, _ = os.path.splitext(orig_file)
            count = sum(1 for f in self.all_files if f.startswith(f"{base_name}.SPLIT") and 
                       f.lower().endswith(('.jpg', '.png', '.jpeg')))
            self.split_counts[orig_file] = count

    def load_image(self):
        if not self.image_files:
            self.filename_label.config(text=f"No .jpg, .png, or .jpeg files found in {self.input_folder}", foreground="red")
            self.progress_label.config(text="")
            self.copy_count_label.config(text="Copy count: 0", style="Default.TLabel")
            self.split_count_label.config(text="Split count: 0", style="Default.TLabel")
            self.total_files_label.config(text="Total files: 0")
            if self.desc_visible:
                self.desc_frame.pack_forget()
                self.desc_visible = False
            self.auto_frame.pack_forget()
            return
        
        raw_filename = self.image_files[self.current_index]
        image_path = os.path.normpath(os.path.join(self.input_folder, raw_filename))
        print(f"Raw filename: {raw_filename}")
        print(f"Full path to load: {image_path}")
        print(f"Path exists: {os.path.isfile(image_path)}")
        
        try:
            self.image = Image.open(image_path)
            orig_width, orig_height = self.image.size
            aspect = orig_width / orig_height
            if aspect > 1:
                thumb_width = self.max_thumbnail_size
                thumb_height = int(self.max_thumbnail_size / aspect)
            else:
                thumb_height = self.max_thumbnail_size
                thumb_width = int(self.max_thumbnail_size * aspect)
            
            self.canvas.config(width=thumb_width, height=thumb_height)
            thumb = self.image.copy()
            thumb.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(thumb)
            
            self.canvas.delete("all")
            self.canvas.create_image(thumb_width//2, thumb_height//2, anchor="center", image=self.photo)
            
            if self.grid_mode:
                self.draw_grid(thumb_width, thumb_height)
            
            filename = raw_filename
            if "copy" in filename.lower():
                self.filename_label.config(text=filename, foreground="green")
            else:
                self.filename_label.config(text=filename, foreground="#FFFFFF")
            
            self.progress_label.config(text=f"Image {self.current_index + 1} of {len(self.image_files)}")
            self.total_files_label.config(text=f"Total files: {len(self.all_files)}")
            count = self.copy_counts.get(filename, 0)
            self.copy_count_label.config(text=f"Copy count: {count}")
            if count > 0:
                self.copy_count_label.configure(style="Highlighted.TLabel")
            else:
                self.copy_count_label.configure(style="Default.TLabel")
            
            split_count = self.split_counts.get(filename, 0)
            self.split_count_label.config(text=f"Split count: {split_count}")
            if split_count > 0:
                self.split_count_label.configure(style="Highlighted.TLabel")
            else:
                self.split_count_label.configure(style="Default.TLabel")
            
            self.desc_text.delete("1.0", tk.END)
            desc = self.descriptions.get(filename, "")
            if desc:
                self.desc_text.insert("1.0", desc)
            
            if self.desc_visible:
                self.desc_frame.pack(pady=5)
            else:
                self.desc_frame.pack_forget()
            
            self.auto_frame.pack(pady=5)
        except Exception as e:
            print(f"Failed to load {image_path}: {e}")
            self.filename_label.config(text=f"Error: {e}", foreground="red")
            self.progress_label.config(text="")
            self.copy_count_label.config(text="Copy count: 0", style="Default.TLabel")
            self.split_count_label.config(text="Split count: 0", style="Default.TLabel")
            self.total_files_label.config(text="Total files: 0")
            if self.desc_visible:
                self.desc_frame.pack_forget()
                self.desc_visible = False
            self.auto_frame.pack_forget()

    def draw_grid(self, width, height):
        line_width = 3
        line_color = "red"
        
        if self.grid_mode in ["4", "3"]:
            self.canvas.create_line(width//2, 0, width//2, height, fill=line_color, width=line_width)
            self.canvas.create_line(0, height//2, width, height//2, fill=line_color, width=line_width)
            if self.grid_mode == "3":
                self.canvas.create_rectangle(width//2, height//2, width, height, 
                                            fill="#FF5555", outline="")
        elif self.grid_mode == "3Down":
            self.canvas.create_line(0, height//3, width, height//3, fill=line_color, width=line_width)
            self.canvas.create_line(0, 2*height//3, width, 2*height//3, fill=line_color, width=line_width)
        elif self.grid_mode == "3Across":
            self.canvas.create_line(width//3, 0, width//3, height, fill=line_color, width=line_width)
            self.canvas.create_line(2*width//3, 0, 2*width//3, height, fill=line_color, width=line_width)
        elif self.grid_mode == "2Down":
            self.canvas.create_line(0, height//2, width, height//2, fill=line_color, width=line_width)
        elif self.grid_mode == "2Across":
            self.canvas.create_line(width//2, 0, width//2, height, fill=line_color, width=line_width)

    def toggle_grid(self, mode):
        if self.grid_mode == mode:
            self.grid_mode = None
        else:
            self.grid_mode = mode
        self.load_image()

    def toggle_desc(self):
        self.desc_visible = not self.desc_visible
        if not self.desc_visible:
            self.update_description()
        self.load_image()

    def prev_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_image()

    def prev_with_copy(self):
        current = self.current_index
        while current > 0:
            current -= 1
            filename = self.image_files[current]
            if self.copy_counts.get(filename, 0) > 0:
                self.current_index = current
                self.load_image()
                return
        print("No previous file with copies found.")

    def next_with_copy(self):
        current = self.current_index
        while current < len(self.image_files) - 1:
            current += 1
            filename = self.image_files[current]
            if self.copy_counts.get(filename, 0) > 0:
                self.current_index = current
                self.load_image()
                return
        print("No next file with copies found.")

    def prev_with_split(self):
        current = self.current_index
        while current > 0:
            current -= 1
            filename = self.image_files[current]
            if self.split_counts.get(filename, 0) > 0:
                self.current_index = current
                self.load_image()
                return
        print("No previous file with splits found.")

    def next_with_split(self):
        current = self.current_index
        while current < len(self.image_files) - 1:
            current += 1
            filename = self.image_files[current]
            if self.split_counts.get(filename, 0) > 0:
                self.current_index = current
                self.load_image()
                return
        print("No next file with splits found.")

    def goto_image(self):
        try:
            goto_index = int(self.goto_entry.get()) - 1
            if 0 <= goto_index < len(self.image_files):
                self.current_index = goto_index
                self.load_image()
            else:
                print(f"Invalid index. Enter a number between 1 and {len(self.image_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def duplicate_image(self, num_copies):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - already duplicated.")
            return
        
        input_path = os.path.join(self.input_folder, current_file)
        for i in range(num_copies):
            output_path = os.path.join(self.input_folder, f"{base_name}.copy{i+1}{ext}")
            shutil.copy(input_path, output_path)
            print(f"Created: {output_path}")
        
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def deduplicate_image(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's already a copy.")
            return
        
        all_files = os.listdir(self.input_folder)
        for f in all_files:
            if f.startswith(f"{base_name}.copy") and "copy" in f.lower() and f.lower().endswith(('.jpg', '.png', '.jpeg')):
                copy_path = os.path.join(self.input_folder, f)
                os.remove(copy_path)
                print(f"Deleted: {copy_path}")
        
        self.refresh_file_list()
        self.load_image()

    def desplit_image(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's already a copy.")
            return
        
        all_files = os.listdir(self.input_folder)
        for f in all_files:
            if f.startswith(f"{base_name}.SPLIT") and "SPLIT" in f and f.lower().endswith(('.jpg', '.png', '.jpeg')):
                split_path = os.path.join(self.input_folder, f)
                os.remove(split_path)
                print(f"Deleted: {split_path}")
        
        self.refresh_file_list()
        self.load_image()

    def split4(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        half_width = orig_width // 2
        half_height = orig_height // 2
        
        crop1 = self.image.crop((0, 0, half_width, half_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((half_width, 0, orig_width, half_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        crop3 = self.image.crop((0, half_height, half_width, orig_height))
        crop3.save(os.path.join(self.input_folder, f"{base_name}.SPLIT3{ext}"))
        crop4 = self.image.crop((half_width, half_height, orig_width, orig_height))
        crop4.save(os.path.join(self.input_folder, f"{base_name}.SPLIT4{ext}"))
        
        print(f"Split {current_file} into 4: {base_name}.SPLIT[1-4]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def split3(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        half_width = orig_width // 2
        half_height = orig_height // 2
        
        crop1 = self.image.crop((0, 0, half_width, half_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((half_width, 0, orig_width, half_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        crop3 = self.image.crop((0, half_height, half_width, orig_height))
        crop3.save(os.path.join(self.input_folder, f"{base_name}.SPLIT3{ext}"))
        
        print(f"Split {current_file} into 3: {base_name}.SPLIT[1-3]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def split3down(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        third_height = orig_height // 3
        
        crop1 = self.image.crop((0, 0, orig_width, third_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((0, third_height, orig_width, 2*third_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        crop3 = self.image.crop((0, 2*third_height, orig_width, orig_height))
        crop3.save(os.path.join(self.input_folder, f"{base_name}.SPLIT3{ext}"))
        
        print(f"Split {current_file} into 3 down: {base_name}.SPLIT[1-3]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def split3across(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        third_width = orig_width // 3
        
        crop1 = self.image.crop((0, 0, third_width, orig_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((third_width, 0, 2*third_width, orig_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        crop3 = self.image.crop((2*third_width, 0, orig_width, orig_height))
        crop3.save(os.path.join(self.input_folder, f"{base_name}.SPLIT3{ext}"))
        
        print(f"Split {current_file} into 3 across: {base_name}.SPLIT[1-3]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def split2down(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        half_height = orig_height // 2
        
        crop1 = self.image.crop((0, 0, orig_width, half_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((0, half_height, orig_width, orig_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        
        print(f"Split {current_file} into 2 down: {base_name}.SPLIT[1-2]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def split2across(self):
        current_file = self.image_files[self.current_index]
        base_name, ext = os.path.splitext(current_file)
        if "copy" in base_name.lower():
            print(f"Skipping {current_file} - it's a copy.")
            return
        
        orig_width, orig_height = self.image.size
        half_width = orig_width // 2
        
        crop1 = self.image.crop((0, 0, half_width, orig_height))
        crop1.save(os.path.join(self.input_folder, f"{base_name}.SPLIT1{ext}"))
        crop2 = self.image.crop((half_width, 0, orig_width, orig_height))
        crop2.save(os.path.join(self.input_folder, f"{base_name}.SPLIT2{ext}"))
        
        print(f"Split {current_file} into 2 across: {base_name}.SPLIT[1-2]{ext}")
        self.refresh_file_list()
        self.load_image()
        if self.auto_advance_var.get():
            self.root.after(1000, self.next_image)

    def submit_custom(self):
        try:
            num_copies = int(self.custom_entry.get())
            if 2 <= num_copies <= 10:
                self.duplicate_image(num_copies - 1)
            else:
                print("Please enter a number between 2 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    parser = argparse.ArgumentParser(description="PhotoGrokfff - Photo Management Tool")  # Updated desc
    parser.add_argument("input_folder", help="Directory containing images and duplicates/splits")
    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: {args.input_folder} is not a valid directory.")
        return

    root = tk.Tk()
    app = ImageDuplicator(root, args.input_folder)
    root.mainloop()

if __name__ == "__main__":
    main()