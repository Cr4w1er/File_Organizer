import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件整理工具")
        self.root.geometry("500x300")
        
        # 变量
        self.folder_path = tk.StringVar()
        
        # 创建UI元素
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="文件整理工具", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # 路径选择部分
        path_frame = tk.Frame(self.root)
        path_frame.pack(pady=10, padx=20, fill=tk.X)
        
        path_label = tk.Label(path_frame, text="选择文件夹:")
        path_label.pack(side=tk.LEFT)
        
        path_entry = tk.Entry(path_frame, textvariable=self.folder_path, width=40)
        path_entry.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(path_frame, text="浏览", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress.pack(pady=20)
        
        # 操作按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        organize_btn = tk.Button(btn_frame, text="整理文件", command=self.organize_files)
        organize_btn.pack(side=tk.LEFT, padx=10)
        
        exit_btn = tk.Button(btn_frame, text="退出", command=self.root.quit)
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
    
    def organize_files(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showerror("错误", "请先选择文件夹!")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("错误", "文件夹不存在!")
            return
        
        try:
            # 获取所有文件
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            if not files:
                messagebox.showinfo("提示", "文件夹中没有文件!")
                return
            
            # 按文件名分组
            file_groups = {}
            for file in files:
                name, ext = os.path.splitext(file)
                if name not in file_groups:
                    file_groups[name] = []
                file_groups[name].append(file)
            
            total_files = len(files)
            processed = 0
            self.progress['maximum'] = total_files
            
            # 为每个文件组创建文件夹并移动文件
            for name, files in file_groups.items():
                dest_folder = os.path.join(folder_path, name)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                for file in files:
                    src = os.path.join(folder_path, file)
                    dest = os.path.join(dest_folder, file)
                    shutil.move(src, dest)
                    processed += 1
                    self.progress['value'] = processed
                    self.status_label.config(text=f"正在处理: {file}")
                    self.root.update_idletasks()
            
            self.status_label.config(text="文件整理完成!", fg="green")
            messagebox.showinfo("完成", f"共处理了 {processed} 个文件!")
            self.progress['value'] = 0
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误:\n{str(e)}")
            self.status_label.config(text="整理过程中出错!", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
