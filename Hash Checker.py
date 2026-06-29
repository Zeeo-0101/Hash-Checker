import os
import hashlib as hash
import threading
import tkinter as tk
from tkinter import filedialog, ttk
import customtkinter as ctk
import time
from tkinter import filedialog, ttk, messagebox
import csv
import sys

class HashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Checker v1.0")
        self.root.geometry("780x600")
        self.root.minsize(720, 520)
        
        # 预设值
        self.themes = ["System", "Dark", "Light"]
        self.colors = ["blue", "dark-blue", "green"]
        self.hash_algorithms = ["md5", "sha1", "sha256", "sha512"]

        #读取配置
        self._read_config()
        self._setup_ui()

    def _read_config(self):
        self.ini_path=os.path.join(os.path.dirname(os.path.abspath(sys.executable)),"config.ini")
        self.config={"theme":"Dark","color":"dark-blue"}
        ini_dict={}
        if os.path.exists(self.ini_path) and os.path.isfile(self.ini_path):
            with open(self.ini_path, 'r') as f:
                ini_list=f.readlines()

            for rule in ini_list:
                rule=rule.strip().split(":")
                if len(rule)==2:
                    ini_dict[rule[0]]=rule[1]

            if "theme" in ini_dict and ini_dict["theme"] in self.themes:
                    ctk.set_appearance_mode(ini_dict["theme"])
                    self.config["theme"]=ini_dict["theme"]
            if "color" in ini_dict and ini_dict["color"] in self.colors:
                    ctk.set_default_color_theme(ini_dict["color"])
                    self.config["color"]=ini_dict["color"]
        else:
            with open(self.ini_path, 'w') as f:
                f.write("theme:dark\ncolor:dark-blue")
            ctk.set_appearance_mode("System")
            ctk.set_default_color_theme("dark-blue")

    def _setup_ui(self):
        top_ctn = ctk.CTkFrame(self.root, fg_color="transparent")
        top_ctn.pack(fill="x")
        
        self.theme_menu = ctk.CTkOptionMenu(top_ctn, values=self.themes,command=self.change_config,width=80)
        self.theme_menu.set(self.config["theme"])
        self.theme_menu.place(relx=0.87,rely=0.2)

        self.color_menu = ctk.CTkOptionMenu(top_ctn, values=self.colors,command=self.change_config,width=80)
        self.color_menu.set(self.config["color"])
        self.color_menu.place(relx=0.72,rely=0.2)
        

        self.title_label = ctk.CTkLabel(top_ctn, text="哈希校对器", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(15, 0))

        self.tabview = ctk.CTkTabview(self.root, width=720, height=480)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        self.tab_text = self.tabview.add("[ 文本比对 ]")
        self.tab_file = self.tabview.add("[ 文件比对 ]")
        self.tab_folder = self.tabview.add("[ 文件夹比对 ]")

        self._build_text_tab()
        self._build_file_tab()
        self._build_folder_tab()

        self.status_var = tk.StringVar(value="状态: 就绪")
        self.status_label = ctk.CTkLabel(self.root, textvariable=self.status_var, text_color="gray", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=25, pady=(0, 10))

    # ================= 业务核心：三大哈希计算函数 ================= #
    
    def on_compare_text(self):
        text_a = self.text_a_input.get("1.0", "end-1c")
        text_b = self.text_b_input.get("1.0", "end-1c")
        
        hash_a=hash.sha256(text_a.encode()).hexdigest()
        hash_b=hash.sha256(text_b.encode()).hexdigest()
        #文本直接比对
        is_match = True if text_a == text_b else False

        log = f"[文本对比完成]\n结果: \n文本 A:{hash_a}\n文本 B:{hash_b}\n\n{'两段文本完全一致' if is_match else '内容不一致！'}"
        self.write_log(self.text_result, log)

    def calc_file_hash(self, filepath, algorithm):
        try:
            with open(filepath, 'rb') as f:
                res = hash.file_digest(f, algorithm)
            return res.hexdigest()
        except Exception as e:
            return f"ERROR: {str(e)}"

    def scan_folder_hashes(self, base_folder, algorithm, name):###返回 {相对路径: 哈希值} 的字典
        folder_dict = {}
        total_file_sum=0
        for _,_,files_num in os.walk(base_folder):
            total_file_sum+=len(files_num)
        calc_num=0
        for root_dir, _, files in os.walk(base_folder):
            for filename in files:
                full_path = os.path.join(root_dir, filename)
                # 相对路径
                rel_path = os.path.relpath(full_path, base_folder)
                file_hash = self.calc_file_hash(full_path, algorithm)
                if not file_hash.startswith("ERROR"):
                    folder_dict[rel_path] = file_hash
                calc_num+=1
                self.root.after(0,lambda: self.btn_run_folder.configure(text=f"{name}: {calc_num/total_file_sum*100:.2f}%已扫描"))
        self.root.after(0,lambda: self.btn_run_folder.configure(text=f"跨目录差分扫描"))
        return folder_dict

    # ================= UI 与异步线程触发 ================= #
    
    def _build_text_tab(self):
        frame = self.tab_text
        frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="文本 A:").grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        self.text_a_input = ctk.CTkTextbox(frame, height=70)
        self.text_a_input.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(frame, text="文本 B:").grid(row=1, column=0, sticky="nw", padx=10, pady=10)
        self.text_b_input = ctk.CTkTextbox(frame, height=70)
        self.text_b_input.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        ctrl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        ctrl_frame.grid(row=2, column=0, columnspan=2, pady=5)

        ctk.CTkButton(ctrl_frame, text="开始比对", command=self.on_compare_text).pack(side="left", padx=20)

        ctk.CTkLabel(frame, text="结果:").grid(row=3, column=0, sticky="nw", padx=10, pady=10)
        self.text_result = ctk.CTkTextbox(frame, height=120, state="disabled", fg_color=("gray90", "gray16"))
        self.text_result.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        frame.rowconfigure(3, weight=1)

    def _build_file_tab(self):
        frame = self.tab_file
        frame.columnconfigure(1, weight=1)

        self.file1_path = tk.StringVar()
        self.file2_path = tk.StringVar()

        ctk.CTkLabel(frame, text="文件 A:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkEntry(frame, textvariable=self.file1_path, placeholder_text="选择文件 A...").grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60, command=lambda: self._browse(self.file1_path, True)).grid(row=0, column=2, padx=10)

        ctk.CTkLabel(frame, text="文件 B \n/Hash:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkEntry(frame, textvariable=self.file2_path, placeholder_text="选择文件 B 或粘贴待检验的哈希值...").grid(row=1, column=1, sticky="ew", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60, command=lambda: self._browse(self.file2_path, True)).grid(row=1, column=2, padx=10)

        ctrl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        ctrl_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ctk.CTkLabel(ctrl_frame, text="算法:").pack(side="left", padx=5)
        self.file_algo_menu = ctk.CTkOptionMenu(ctrl_frame, values=self.hash_algorithms, width=100)
        self.file_algo_menu.set("sha256")
        self.file_algo_menu.pack(side="left", padx=10)

        ctk.CTkButton(ctrl_frame, text="开始比对", command=lambda: self.start_thread(self._thread_compare_file)).pack(side="left", padx=20)

        ctk.CTkLabel(frame, text="结果:").grid(row=3, column=0, sticky="nw", padx=10, pady=10)
        self.file_result = ctk.CTkTextbox(frame, height=140, state="disabled", fg_color=("gray90", "gray16"))
        self.file_result.grid(row=3, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)
        frame.rowconfigure(3, weight=1)

    def _build_folder_tab(self):
        frame = self.tab_folder
        frame.columnconfigure(1, weight=1)

        self.folder1_path = tk.StringVar()
        self.folder2_path = tk.StringVar()

        ctk.CTkLabel(frame, text="目录 A:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkEntry(frame, textvariable=self.folder1_path, placeholder_text="主核算文件夹 A...").grid(row=0, column=1, sticky="ew", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60, command=lambda: self._browse(self.folder1_path, False)).grid(row=0, column=2, padx=10)

        ctk.CTkLabel(frame, text="目录 B:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        ctk.CTkEntry(frame, textvariable=self.folder2_path, placeholder_text="待核算文件夹 B...").grid(row=1, column=1, sticky="ew", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60, command=lambda: self._browse(self.folder2_path, False)).grid(row=1, column=2, padx=10)

        ctrl_frame = ctk.CTkFrame(frame, fg_color="transparent")
        ctrl_frame.grid(row=2, column=0, columnspan=3, pady=5)
        
        ctk.CTkLabel(ctrl_frame, text="算法:").pack(side="left", padx=5)
        self.folder_algo_menu = ctk.CTkOptionMenu(ctrl_frame, values=self.hash_algorithms, width=100)
        self.folder_algo_menu.set("sha256")
        self.folder_algo_menu.pack(side="left", padx=10)

        self.btn_run_folder = ctk.CTkButton(ctrl_frame, text="跨目录差分扫描", command=lambda: self.start_thread(self._thread_compare_folder))
        self.btn_run_folder.pack(side="left", padx=20)

        ctk.CTkLabel(frame, text="结果:").grid(row=3, column=0, sticky="nw", padx=10, pady=10)
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("黑体", 12, "bold"))
        style.configure("Treeview", rowheight=25)

        columns = ("file", "status", "hash_a", "hash_b")
        self.tree_result = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree_result.heading("file", text="文件路径")
        self.tree_result.heading("status", text="匹配状态")
        self.tree_result.heading("hash_a", text="目录 A 哈希")
        self.tree_result.heading("hash_b", text="目录 B 哈希")
        
        self.tree_result.column("file", width=200)
        self.tree_result.column("status", width=80, anchor="center")
        self.tree_result.column("hash_a", width=120)
        self.tree_result.column("hash_b", width=120)

        self.tree_result.grid(row=0, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_result.yview)
        self.tree_result.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

    # ================= 控制与线程 ================= #
    def change_config(self,_):
        theme=self.theme_menu.get()
        color=self.color_menu.get()
        ctk.set_appearance_mode(theme)
        with open(self.ini_path, 'w') as f:
                f.write(f"theme:{theme}\ncolor:{color}")


    def _browse(self, var, is_file=True):
        path = filedialog.askopenfilename() if is_file else filedialog.askdirectory()
        if path: var.set(path)

    def write_log(self, text_widget, content):
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", content)
        text_widget.configure(state="disabled")

    def write_log_add(self, text_widget, content):
        text_widget.configure(state="normal")
        text_widget.insert("end", content)
        text_widget.configure(state="disabled")

    def start_thread(self, target_func):
        t = threading.Thread(target=target_func, daemon=True)
        t.start()

    def export_to_csv(self):
        if not hasattr(self, 'raw_report_data') or not self.raw_report_data:
            messagebox.showwarning("提示", "当前没有可导出的比对数据。")
            return
        
        while True:    
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV 表格文件", "*.csv"), ("所有文件", "*.*")],
                title="保存比对报告",
                initialfile=f"哈希比对报告_{int(time.time())}.csv"
            )
            if file_path:
                break
            else:
                if messagebox.askyesno("退出","退出将不再保存报告，确定吗？"):
                    break
        
        if file_path:
            try:
                with open(file_path, mode='w', encoding='utf-8-sig', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["相对路径", "匹配状态", "目录 A 哈希", "目录 B 哈希"])
                    writer.writerows(self.raw_report_data)
                
                messagebox.showinfo("导出成功", f"完整报告已成功保存至：\n{file_path}")
            except Exception as e:
                messagebox.showerror("导出失败", f"文件保存过程中发生错误：\n{str(e)}")



    # ================= 触发的线程回调 ================= #

    def _thread_compare_file(self):
        f1 = self.file1_path.get()
        f2 = self.file2_path.get()
        algo = self.file_algo_menu.get()
        
        if not f1 or not os.path.exists(f1):
            self.write_log(self.file_result, "错误: 请选择有效的源文件。")
            return
            
        self.status_var.set("状态: 正在计算文件哈希值...")
        hash_a = self.calc_file_hash(f1, algo)
        
        # 判断 B 是文件还是粘贴过来的哈希
        if os.path.exists(f2) and os.path.isfile(f2):
            hash_b = self.calc_file_hash(f2, algo)
            is_match = (hash_a == hash_b)
            log = f"[文件双向比对完成]\n算法: {algo}\n文件 A: {f1}\n文件 B: {f2}\n\nHash A: {hash_a}\nHash B: {hash_b}\n\n结果: {'文件完全一致' if is_match else '文件内容已被篡改/不一致！'}"
        else:
            is_match = (hash_a.lower() == f2.strip().lower())
            log = f"[文件单向指纹校验]\n算法: {algo}\n文件 A: {f1}\n\n计算 Hash: {hash_a}\n期望 Hash: {f2 if f2 else '未提供'}\n\n结果: {'指纹核对正确' if is_match else '指纹不匹配！'}"
            
        self.write_log(self.file_result, log)
        self.status_var.set("状态: 就绪")

    def _thread_compare_folder(self):
        time_start=time.time()
        self.root.after(0, lambda: self.btn_run_folder.configure(state="disabled"))

        dir_a = self.folder1_path.get()
        dir_b = self.folder2_path.get()
        algo = self.folder_algo_menu.get()
        
        one_folder_mode=False
        if dir_a and os.path.isdir(dir_a) and dir_b=="":
            self.status_var.set("状态: 正在扫描文件夹 A...")
            dict_a = self.scan_folder_hashes(dir_a, algo, "目录 A")
            dict_b={}
            one_folder_mode=True
        elif dir_a and os.path.isdir(dir_a) and dir_b and os.path.isdir(dir_b):
            self.status_var.set("状态: 正在扫描文件夹 A...")
            dict_a = self.scan_folder_hashes(dir_a, algo, "目录 A")
            self.status_var.set("状态: 正在扫描文件夹 B...")
            dict_b = self.scan_folder_hashes(dir_b, algo, "目录 B")
        else:
            self.status_var.set("状态: 错误 - 无效的目录")
            self.root.after(0, lambda: self.tree_result.insert("", "end", values=("无效的目录! 请至少保证目录 A的地址合法性!","","","")))
            self.root.after(0, lambda: self.btn_run_folder.configure(state="normal"))
            return
        

        self.root.after(0, lambda: self.status_var.set("状态: 正在生成比对报告..."))
        self.root.after(0, lambda: [self.tree_result.delete(item) for item in self.tree_result.get_children()])
        
        all_files = set(dict_a.keys()).union(set(dict_b.keys()))
        len_all_files = len(all_files)
        is_all_match = True
        
        # 文件分类：分为“一致”和“有差异”两个列表
        diff_items = []
        match_items = []
        #原数据缓存
        self.raw_report_data = []


        for rel_path in sorted(all_files):
            hash_a = dict_a.get(rel_path)
            hash_b = dict_b.get(rel_path)

            if hash_a and hash_b:
                if hash_a == hash_b:
                    status = "一致"
                else:
                    status = "不一致！"
                    is_all_match = False
            elif hash_a and not hash_b:
                status = "目录 B 缺失"
                hash_b = "None"
                is_all_match = False
            elif not hash_a and hash_b:
                status = "目录 A 缺失"
                hash_a = "None"
                is_all_match = False

            #添加进原数据缓存中
            if one_folder_mode:
                status = ""
                hash_b = ""
            self.raw_report_data.append([rel_path, status, hash_a, hash_b])

            disp_a = "None" if hash_a == "None" else f"{hash_a[:6]}...{hash_a[-6:]}"
            disp_b = "None" if hash_b == "None" else f"{hash_b[:6]}...{hash_b[-6:]}"
            disp_b = disp_b if one_folder_mode==False else ""

            row_data = (rel_path, status, disp_a, disp_b)
            if status == "一致":
                match_items.append(row_data)
            else:
                diff_items.append(row_data)

        # 渲染逻辑：优先渲染有差异的文件。如果超过 1000 条差异，截断。
        items_to_display = diff_items if not is_all_match else match_items
        display_limit = 1000
        
        def update_ui():
            for row in items_to_display[:display_limit]:
                self.tree_result.insert("", "end", values=row)
            
            self.status_var.set("状态: 完成")
            tip_text = f"共{len_all_files}个文件" + ("，为保证流畅，已省略部分" if len(items_to_display) > display_limit else "")
            status_text = "全部一致!" if is_all_match else f"发现 {len(diff_items)} 处差异！"
            status_text = status_text if one_folder_mode==False else ""
            self.tree_result.insert("", "end", values=(tip_text, status_text, "仅显示前、后6位哈希", "完整浏览可点击导出"))
            self.btn_run_folder.configure(state="normal")
            #结束弹窗
            used_time=time.time()-time_start
            if one_folder_mode:
                summary_msg = f"文件夹比对完成! 耗时{used_time:.2f}s\n\n当前为单文件夹模式！\n\n是否立刻导出包含完整报告？"
            else:
                summary_msg = f"文件夹比对完成! 耗时{used_time:.2f}s\n\n结果：{'所有文件完全一致!' if is_all_match else f'! 发现 {len(diff_items)} 处差异文件！'}\n\n是否立刻导出包含完整报告？"
            
            if messagebox.askyesno("比对完成", summary_msg):
                self.export_to_csv() 

            
        # 将 UI 渲染任务交回主线程
        self.root.after(0, update_ui)




if __name__ == "__main__":
    root = ctk.CTk()
    app = HashApp(root)
    root.mainloop()



