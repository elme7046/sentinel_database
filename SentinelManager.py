# Import the required libraries
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk
import os
import shutil

#TODO

class FaceWithData:
	def __init__(self, face, name, data):
		self.face = face
		self.name = name
		self.data = data

	def get_face(self):
		return self.face
	
	def set_face(self, face):
		self.face = face
	
	def get_name(self):
		return self.name
	
	def set_name(self, name):
		self.name = name

	def get_data(self):
		return self.data
	
	def set_data(self, data):
		self.data = data

	def __str__(self):
		return self.face + "|" + self.name + "|" + self.data

class GUI():
	def __init__(self, root):
		self.root = root

		self.faces_known = []
		self.faces_unknown = []
		self.faces_whitelist = []
		self.faces_blacklist = []
		self.all_faces = []

		self.image_list = []
		self.list_type = ""

		self.get_images()

		self.image_index = 0

		self.root.geometry("1280x600")
		
		self.screen_panel = tk.Frame(self.root, width=1080, height=600)
		self.screen_panel.pack(side="left")
		self.screen_panel.pack_propagate(False)
		
		self.functions_panel = tk.Frame(self.root, width=200, height=600, background="red")
		self.functions_panel.pack(side="left")
		self.functions_panel.pack_propagate(False)

		#Screen Panel Assets
		self.top_panel = tk.Frame(self.screen_panel, width=1080, height=540, background="#B0B0B0")
		self.top_panel.pack(side="top")
		self.top_panel.pack_propagate(False)

		self.prev_button = tk.Button(self.top_panel, text="Prev", width=7, height=2,
							   command=self.prev_image)
		self.prev_button.pack(side="left")

		self.canvas = Canvas(self.top_panel, width=960, height=540)
		self.canvas.pack(side="left")
		
		self.next_button = tk.Button(self.top_panel, text="Next", width=7, height=2,
							   command=self.next_image)
		self.next_button.pack(side="left")
		
		self.bottom_panel = tk.Frame(self.screen_panel, width=1080, height=60, background="#FF0000")
		self.bottom_panel.pack(side="top")
		self.bottom_panel.pack_propagate(False)

		# self.left_button_frame = tk.Frame(self.bottom_panel, width=540, height=200, background="red")
		# self.left_button_frame.pack_propagate(False)
		# self.left_button_frame.pack(side="left")
		# self.right_button_frame = tk.Frame(self.bottom_panel, width=540, height=200, background="blue")
		# self.right_button_frame.pack_propagate(False)
		# self.right_button_frame.pack(side="right")

		self.button_whitelist = tk.Button(self.bottom_panel, text="Whitelist", width=35, height=5,
								command=lambda:self.select_list(self.faces_whitelist, "w", "Whitelist"))
		self.button_whitelist.pack(side="left", padx=(5,5), pady=(5,5))
		
		self.button_known = tk.Button(self.bottom_panel, text="Known", width=35, height=5, 
								command=lambda:self.select_list(self.faces_known, "k", "Known"))
		self.button_known.pack(side="left", padx=(5,5), pady=(5,5))
		self.button_unknown = tk.Button(self.bottom_panel, text="Unknown", width=35, height=5,
								command=lambda:self.select_list(self.faces_unknown, "u", "Unknown"))
		self.button_unknown.pack(side="left", padx=(5,5), pady=(5,5))

		# self.button_blacklist = tk.Button(self.right_button_frame, text="Blacklist", width=35, height=5,
		# 						command=self.select_blacklist_list)
		# self.button_blacklist.pack(side="right", padx=(5,5), pady=(5,5))


		#Functions Panel assets
		self.list_label = tk.Label(self.functions_panel, width=20, height=2, text="No List", font=("Arial 24"))
		self.list_label.pack(side="top", pady=(10,10))

		self.current_face_name = tk.Label(self.functions_panel, width=20, height=2, text="", font=("Arial 24"))
		self.current_face_name.pack(side="top")

		self.face_name = tk.Entry(self.functions_panel, width=20, font=("Arial 24"))
		self.face_name.pack(side="top")

		self.rename_button = tk.Button(self.functions_panel, width=20, height=3, text="Rename",
								command=lambda : self.rename_image(self.face_name.get()))
		self.rename_button.pack(side="top", pady=(5,5))

		self.move_whitelist_button = tk.Button(self.functions_panel, width=20, height=3, text="Move to Whitelist",
								command=lambda : self.move_to_list(self.faces_whitelist, "w"))
		self.move_whitelist_button.pack(side="top", pady=(5,5))
		self.remove_whitelist_button = tk.Button(self.functions_panel, width=20, height=3, text="Remove from Whitelist",
								command=lambda : self.move_to_list(self.faces_known, "k"))
		self.remove_whitelist_button.pack(side="top", pady=(5,5))
	
	def get_images(self, reset=False):
		if(reset):
			self.faces_known = []
			self.faces_unknown = []
			self.faces_whitelist = []
			self.faces_blacklist = []
		for root, dirs, files in os.walk(".", topdown=False):
			for name in files:
				if '.png' in name:
					full_name = os.path.join(root, name)
					tokens = name.split('.')
					if len(tokens) == 3:
						face_name = tokens[0]
						list_type = tokens[1]
						if list_type == "k":
							self.faces_known.append(FaceWithData(full_name, face_name, list_type))
						elif list_type == "u":
							self.faces_unknown.append(FaceWithData(full_name, face_name, list_type))
						elif list_type == "b":
							self.faces_blacklist.append(FaceWithData(full_name, face_name, list_type))
						elif list_type == "w":
							self.faces_whitelist.append(FaceWithData(full_name, face_name, list_type))
						else:
							continue
						self.all_faces.append(FaceWithData(full_name, face_name, list_type))
					
	
	def next_image(self):
		if(len(self.image_list) == 0):
			self.update_canvas()
			return
		self.image_index += 1
		if(self.image_index > len(self.image_list)-1):
			self.image_index = 0
		self.update_canvas(self.image_list[self.image_index])

	def prev_image(self):
		if(len(self.image_list) == 0):
			self.update_canvas()
			return
		self.image_index -= 1
		if(self.image_index < 0):
			self.image_index = len(self.image_list)-1
		self.update_canvas(self.image_list[self.image_index])

	def select_list(self, list_type, list_letter, list_text):
		self.image_list = list_type
		self.list_type = list_letter
		self.image_index = 0
		self.list_label["text"] = list_text
		if(self.select_default_image() != 1):
			self.update_canvas(self.image_list[self.image_index])

	def return_list(self):
		if(self.list_type == "k"):
			return self.faces_known
		elif(self.list_type == "u"):
			return self.faces_unknown
		elif(self.list_type == "w"):
			return self.faces_whitelist
		else:
			return self.image_list

	def move_to_list(self, to_list, list_letter):
		
		if(len(self.image_list) > 0):
			image = self.image_list.pop(self.image_index)
			curr_name = image.get_face()
			new_name = curr_name.split('.')
			new_name[-2] = list_letter
			
			#gone = self.image_list.pop(self.image_index)
			#self.return_list().remove(self.image_index)
			os.rename(curr_name, '.'.join(new_name))
			image.set_face('.'.join(new_name))
			to_list.append(image)
		else:
			messagebox.showwarning("Invalid image!", "Please select an image")
			return
		
		if(len(self.image_list) > 0):
			if(self.image_index == 0):
				image_index = len(self.image_list) - 1
				self.update_canvas(self.image_list[image_index])
			else:
				self.update_canvas(self.image_list[self.image_index-1])
		else:
			self.update_canvas()

	def rename_image(self, name):
		#self.update_canvas()
		if(len(self.image_list) > 0):
			if(name.strip() != "" and name.isalnum()):
				curr_name = self.image_list[self.image_index].get_face()
				if self.list_type == "u":
					new_name = self.image_list[self.image_index].get_face().split('/')[-1]
					new_path = "/".join(self.image_list[self.image_index].get_face().split('/')[:-1]) + self.face_name.get() + ".k.png"
					self.image_list[self.image_index].set_face(new_path)
					self.image_list[self.image_index].set_name(name)
				else:
					new_name = self.image_list[self.image_index].get_face().split('/')[-1]
					new_path = "/".join(self.image_list[self.image_index].get_face().split('/')[:-1]) + self.face_name.get() + "." + self.list_type + ".png"
					self.image_list[self.image_index].set_face(new_path)
					self.image_list[self.image_index].set_name(name)

				shutil.copyfile(curr_name, new_path)
				os.remove(curr_name)

				if(self.list_type=="u"):
					self.move_to_list(self.faces_known, "k")

				if(len(self.image_list) > 0):
					#self.image_list[self.image_index].set_name(name)
					self.current_face_name["text"] = self.image_list[self.image_index].get_name()
				else:
					self.current_face_name["text"] = "Default no image"
				self.face_name.delete(0, END)
				

			else:
				messagebox.showwarning("Invalid name!", "The name you have chosen is invalid. Please remove any non-alphanumeric characters")
		self.update_canvas(self.image_list[self.image_index])

	def delete_image(self):
		if(len(self.image_list) > 0):
			ask = messagebox.askquestion("!!!", "Do you really want to delete this image")
		else:
			messagebox.showerror("Empty List!", "There are no images under this list.")

		if(ask == 'yes'):
			curr_name = self.image_list[self.image_index].get_face()
			new_name = curr_name.split('.')
			new_name[-2] = 'b'
			
			gone = self.image_list.pop(self.image_index)
			#self.return_list().remove(self.image_index)
			os.rename(curr_name, '.'.join(new_name))
		else:
			pass


	def select_default_image(self):
		if(len(self.image_list) == 0):
			self.update_canvas()
			return 1
		else:
			return 0

	def update_canvas(self, image=None):
		self.canvas.delete("all")
		if(type(image) == FaceWithData):
			face = image.get_face()
			img = Image.open(face)
			self.img = ImageTk.PhotoImage(img.resize((960,540)))
			self.current_face_name["text"] = image.get_name()
		else:
			pic = Image.open("./default.png")
			self.img = ImageTk.PhotoImage(pic.resize((960,540)))
			self.current_face_name["text"] = "No Image Selected"

		self.canvas.create_image(0, 0, image=self.img, anchor="nw")
		self.root.update()

if __name__ == "__main__":
	win = tk.Tk()
	gui = GUI(win)
	win.mainloop()