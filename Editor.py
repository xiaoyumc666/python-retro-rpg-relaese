import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import base64
import zlib
import hashlib
import os
import datetime

class SaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("存档编辑器")
        self.root.geometry("900x600")
        self.root.configure(bg='#2b2b2b')
        
        # 颜色主题
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#ffffff',
            'button_bg': '#3c3f41',
            'button_fg': '#ffffff',
            'highlight': '#4a6c8f',
            'warning': '#ff6b68',
            'success': '#6b8e23',
            'info': '#4682b4',
            'gold': '#ffd700'
        }
        
        # 字体
        self.header_font = ('Arial', 18, 'bold')
        self.normal_font = ('Arial', 12)
        self.small_font = ('Arial', 10)
        
        # 存档数据
        self.save_data = None
        self.current_file = None
        
        # 创建主界面
        self.create_main_interface()
    
    def create_main_interface(self):
        """创建主界面"""
        # 标题
        title_label = tk.Label(
            self.root,
            text="存档编辑器",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=20)
        
        # 按钮框架
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # 选择存档按钮
        select_btn = tk.Button(
            button_frame,
            text="选择存档文件",
            command=self.select_save_file,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=20,
            height=2
        )
        select_btn.pack(side='left', padx=10)
        
        # 保存修改按钮
        save_btn = tk.Button(
            button_frame,
            text="保存修改",
            command=self.save_changes,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=20,
            height=2
        )
        save_btn.pack(side='left', padx=10)
        
        # 保存为新文件按钮
        save_as_btn = tk.Button(
            button_frame,
            text="保存为新文件",
            command=self.save_as_new,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=20,
            height=2
        )
        save_as_btn.pack(side='left', padx=10)
        
        # 数据编辑区域
        self.edit_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.edit_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 创建笔记本（标签页）
        self.notebook = ttk.Notebook(self.edit_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # 玩家数据标签页
        self.player_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.player_tab, text="玩家数据")
        
        # 游戏状态标签页
        self.game_tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(self.game_tab, text="游戏状态")
        
        # 初始提示
        self.initial_label = tk.Label(
            self.edit_frame,
            text="请选择一个存档文件来编辑",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.initial_label.pack(expand=True)
    
    def select_save_file(self):
        """选择存档文件"""
        file_path = filedialog.askopenfilename(
            title="选择存档文件",
            filetypes=[("存档文件", "*"), ("所有文件", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "saves")
        )
        
        if file_path:
            self.current_file = file_path
            self.load_save_file(file_path)
    
    def load_save_file(self, file_path):
        """加载并解密存档文件"""
        try:
            with open(file_path, 'r') as f:
                encrypted_data = f.read().strip()
            
            # 解密数据
            save_data = self._decrypt_save_data(encrypted_data)
            if save_data:
                self.save_data = save_data
                self.display_save_data()
                messagebox.showinfo("成功", "存档文件加载成功！")
            else:
                messagebox.showerror("错误", "解密存档失败！")
        except Exception as e:
            messagebox.showerror("错误", f"加载存档失败: {str(e)}")
    
    def display_save_data(self):
        """显示存档数据"""
        # 移除初始提示
        if hasattr(self, 'initial_label') and self.initial_label.winfo_exists():
            self.initial_label.destroy()
        
        # 清空标签页内容
        for widget in self.player_tab.winfo_children():
            widget.destroy()
        for widget in self.game_tab.winfo_children():
            widget.destroy()
        
        # 显示玩家数据
        self.display_player_data()
        
        # 显示游戏状态
        self.display_game_data()
    
    def display_player_data(self):
        """显示玩家数据"""
        if not self.save_data or 'player' not in self.save_data:
            return
        
        player_data = self.save_data['player']
        
        # 创建滚动区域
        canvas = tk.Canvas(self.player_tab, bg=self.colors['bg'])
        scrollbar = tk.Scrollbar(self.player_tab, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定滚轮
        def on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        canvas.bind("<Button-4>", on_mouse_wheel)
        canvas.bind("<Button-5>", on_mouse_wheel)
        
        # 显示玩家数据
        row = 0
        for key, value in player_data.items():
            if key == 'inventory':
                # 特殊处理背包数据
                frame = tk.LabelFrame(
                    scrollable_frame,
                    text="背包",
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg=self.colors['bg']
                )
                frame.grid(row=row, column=0, columnspan=3, padx=10, pady=5, sticky='ew')
                
                # 新增物品按钮
                add_item_btn = tk.Button(
                    frame,
                    text="新增物品",
                    command=self.add_new_item,
                    font=self.small_font,
                    bg=self.colors['button_bg'],
                    fg=self.colors['button_fg'],
                    width=10
                )
                add_item_btn.grid(row=0, column=0, padx=10, pady=5, sticky='w')
                
                # 显示背包物品
                if isinstance(value, dict):
                    item_row = 1
                    for item_name, quantity in value.items():
                        tk.Label(
                            frame,
                            text=item_name,
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg=self.colors['bg'],
                            width=20,
                            anchor='w'
                        ).grid(row=item_row, column=0, padx=10, pady=2, sticky='w')
                        
                        entry = tk.Entry(
                            frame,
                            font=self.small_font,
                            bg='#1e1e1e',
                            fg=self.colors['fg'],
                            width=10
                        )
                        entry.insert(0, str(quantity))
                        entry.grid(row=item_row, column=1, padx=10, pady=2, sticky='w')
                        entry.bind('<FocusOut>', lambda e, item=item_name: self.update_inventory_item(e, item))
                        
                        # 删除物品按钮
                        delete_btn = tk.Button(
                            frame,
                            text="删除",
                            command=lambda item=item_name: self.delete_inventory_item(item, frame),
                            font=self.small_font,
                            bg=self.colors['warning'],
                            fg=self.colors['button_fg'],
                            width=6
                        )
                        delete_btn.grid(row=item_row, column=2, padx=10, pady=2, sticky='w')
                        
                        item_row += 1
                
            elif isinstance(value, dict):
                # 处理嵌套字典
                frame = tk.LabelFrame(
                    scrollable_frame,
                    text=key,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg=self.colors['bg']
                )
                frame.grid(row=row, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
                
                nested_row = 0
                for nested_key, nested_value in value.items():
                    tk.Label(
                        frame,
                        text=nested_key,
                        font=self.small_font,
                        fg=self.colors['fg'],
                        bg=self.colors['bg'],
                        width=20,
                        anchor='w'
                    ).grid(row=nested_row, column=0, padx=10, pady=2, sticky='w')
                    
                    entry = tk.Entry(
                        frame,
                        font=self.small_font,
                        bg='#1e1e1e',
                        fg=self.colors['fg'],
                        width=30
                    )
                    entry.insert(0, str(nested_value))
                    entry.grid(row=nested_row, column=1, padx=10, pady=2, sticky='w')
                    entry.bind('<FocusOut>', lambda e, k=key, nk=nested_key: self.update_value(e, k, nk))
                    
                    nested_row += 1
            else:
                # 处理普通值
                tk.Label(
                    scrollable_frame,
                    text=key,
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg=self.colors['bg'],
                    width=20,
                    anchor='w'
                ).grid(row=row, column=0, padx=10, pady=2, sticky='w')
                
                entry = tk.Entry(
                    scrollable_frame,
                    font=self.small_font,
                    bg='#1e1e1e',
                    fg=self.colors['fg'],
                    width=30
                )
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, padx=10, pady=2, sticky='w')
                entry.bind('<FocusOut>', lambda e, k=key: self.update_value(e, k))
            
            row += 1
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def display_game_data(self):
        """显示游戏状态数据"""
        if not self.save_data or 'game_state' not in self.save_data:
            return
        
        game_data = self.save_data['game_state']
        
        # 创建滚动区域
        canvas = tk.Canvas(self.game_tab, bg=self.colors['bg'])
        scrollbar = tk.Scrollbar(self.game_tab, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 绑定滚轮
        def on_mouse_wheel(event):
            if event.delta:
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        canvas.bind("<MouseWheel>", on_mouse_wheel)
        canvas.bind("<Button-4>", on_mouse_wheel)
        canvas.bind("<Button-5>", on_mouse_wheel)
        
        # 显示游戏状态数据
        row = 0
        for key, value in game_data.items():
            if key == 'pets':
                # 特殊处理宠物数据
                frame = tk.LabelFrame(
                    scrollable_frame,
                    text="宠物",
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg=self.colors['bg']
                )
                frame.grid(row=row, column=0, columnspan=3, padx=10, pady=5, sticky='ew')
                
                # 新增宠物按钮
                add_pet_btn = tk.Button(
                    frame,
                    text="新增宠物",
                    command=self.add_new_pet,
                    font=self.small_font,
                    bg=self.colors['button_bg'],
                    fg=self.colors['button_fg'],
                    width=10
                )
                add_pet_btn.grid(row=0, column=0, padx=10, pady=5, sticky='w')
                
                # 显示宠物列表
                if isinstance(value, list):
                    pet_row = 1
                    for i, pet in enumerate(value):
                        pet_frame = tk.Frame(frame, bg=self.colors['bg'])
                        pet_frame.grid(row=pet_row, column=0, columnspan=3, padx=10, pady=2, sticky='ew')
                        
                        # 宠物名称
                        tk.Label(
                            pet_frame,
                            text=f"宠物 {i+1}: {pet.get('name', '未知')}",
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg=self.colors['bg'],
                            width=20,
                            anchor='w'
                        ).grid(row=0, column=0, padx=10, pady=2, sticky='w')
                        
                        # 宠物等级
                        tk.Label(
                            pet_frame,
                            text="等级:",
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg=self.colors['bg'],
                            width=10,
                            anchor='w'
                        ).grid(row=1, column=0, padx=10, pady=2, sticky='w')
                        
                        level_entry = tk.Entry(
                            pet_frame,
                            font=self.small_font,
                            bg='#1e1e1e',
                            fg=self.colors['fg'],
                            width=10
                        )
                        level_entry.insert(0, str(pet.get('level', 1)))
                        level_entry.grid(row=1, column=1, padx=10, pady=2, sticky='w')
                        level_entry.bind('<FocusOut>', lambda e, idx=i, key='level': self.update_pet_value(e, idx, key))
                        
                        # 宠物类型
                        tk.Label(
                            pet_frame,
                            text="类型:",
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg=self.colors['bg'],
                            width=10,
                            anchor='w'
                        ).grid(row=2, column=0, padx=10, pady=2, sticky='w')
                        
                        type_entry = tk.Entry(
                            pet_frame,
                            font=self.small_font,
                            bg='#1e1e1e',
                            fg=self.colors['fg'],
                            width=10
                        )
                        type_entry.insert(0, str(pet.get('type', '普通')))
                        type_entry.grid(row=2, column=1, padx=10, pady=2, sticky='w')
                        type_entry.bind('<FocusOut>', lambda e, idx=i, key='type': self.update_pet_value(e, idx, key))
                        
                        # 宠物忠诚度
                        tk.Label(
                            pet_frame,
                            text="忠诚度:",
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg=self.colors['bg'],
                            width=10,
                            anchor='w'
                        ).grid(row=3, column=0, padx=10, pady=2, sticky='w')
                        
                        loyalty_entry = tk.Entry(
                            pet_frame,
                            font=self.small_font,
                            bg='#1e1e1e',
                            fg=self.colors['fg'],
                            width=10
                        )
                        loyalty_entry.insert(0, str(pet.get('loyalty', 50)))
                        loyalty_entry.grid(row=3, column=1, padx=10, pady=2, sticky='w')
                        loyalty_entry.bind('<FocusOut>', lambda e, idx=i, key='loyalty': self.update_pet_value(e, idx, key))
                        
                        # 删除宠物按钮
                        delete_btn = tk.Button(
                            pet_frame,
                            text="删除",
                            command=lambda idx=i: self.delete_pet(idx),
                            font=self.small_font,
                            bg=self.colors['warning'],
                            fg=self.colors['button_fg'],
                            width=6
                        )
                        delete_btn.grid(row=0, column=2, padx=10, pady=2, sticky='w')
                        
                        pet_row += 1
            else:
                tk.Label(
                    scrollable_frame,
                    text=key,
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg=self.colors['bg'],
                    width=20,
                    anchor='w'
                ).grid(row=row, column=0, padx=10, pady=2, sticky='w')
                
                if isinstance(value, list):
                    # 处理列表
                    text = tk.Text(
                        scrollable_frame,
                        font=self.small_font,
                        bg='#1e1e1e',
                        fg=self.colors['fg'],
                        width=30,
                        height=3
                    )
                    text.insert('1.0', str(value))
                    text.grid(row=row, column=1, padx=10, pady=2, sticky='w')
                    text.bind('<FocusOut>', lambda e, k=key: self.update_list_value(e, k))
                else:
                    # 处理普通值
                    entry = tk.Entry(
                        scrollable_frame,
                        font=self.small_font,
                        bg='#1e1e1e',
                        fg=self.colors['fg'],
                        width=30
                    )
                    entry.insert(0, str(value))
                    entry.grid(row=row, column=1, padx=10, pady=2, sticky='w')
                    entry.bind('<FocusOut>', lambda e, k=key: self.update_value(e, k, None, True))
            
            row += 1
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def update_value(self, event, key, nested_key=None, is_game_state=False):
        """更新值"""
        if not self.save_data:
            return
        
        value = event.widget.get()
        
        try:
            # 尝试转换为适当的类型
            if value.isdigit():
                value = int(value)
            elif '.' in value and all(c.isdigit() or c == '.' for c in value):
                value = float(value)
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
        except:
            pass
        
        if is_game_state:
            self.save_data['game_state'][key] = value
        elif nested_key:
            self.save_data['player'][key][nested_key] = value
        else:
            self.save_data['player'][key] = value
    
    def update_list_value(self, event, key):
        """更新列表值"""
        if not self.save_data:
            return
        
        value = event.widget.get('1.0', 'end-1c')
        
        try:
            # 尝试解析为列表
            value = eval(value)
            if isinstance(value, list):
                self.save_data['game_state'][key] = value
        except:
            pass
    
    def update_inventory_item(self, event, item_name):
        """更新背包物品数量"""
        if not self.save_data or 'player' not in self.save_data or 'inventory' not in self.save_data['player']:
            return
        
        value = event.widget.get()
        
        try:
            quantity = int(value)
            if quantity > 0:
                self.save_data['player']['inventory'][item_name] = quantity
            else:
                # 如果数量为0或负数，删除物品
                del self.save_data['player']['inventory'][item_name]
                # 刷新显示
                self.display_save_data()
        except:
            pass
    
    def delete_inventory_item(self, item_name, frame):
        """删除背包物品"""
        if not self.save_data or 'player' not in self.save_data or 'inventory' not in self.save_data['player']:
            return
        
        if item_name in self.save_data['player']['inventory']:
            del self.save_data['player']['inventory'][item_name]
            # 刷新显示
            self.display_save_data()
    
    def update_pet_value(self, event, pet_index, key):
        """更新宠物属性值"""
        if not self.save_data or 'game_state' not in self.save_data or 'pets' not in self.save_data['game_state']:
            return
        
        value = event.widget.get()
        
        try:
            # 尝试转换为适当的类型
            if value.isdigit():
                value = int(value)
            elif '.' in value and all(c.isdigit() or c == '.' for c in value):
                value = float(value)
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
        except:
            pass
        
        # 确保宠物列表存在且索引有效
        if 0 <= pet_index < len(self.save_data['game_state']['pets']):
            self.save_data['game_state']['pets'][pet_index][key] = value
    
    def delete_pet(self, pet_index):
        """删除宠物"""
        if not self.save_data or 'game_state' not in self.save_data or 'pets' not in self.save_data['game_state']:
            return
        
        # 确保索引有效
        if 0 <= pet_index < len(self.save_data['game_state']['pets']):
            del self.save_data['game_state']['pets'][pet_index]
            # 刷新显示
            self.display_save_data()
    
    def add_new_pet(self):
        """新增宠物"""
        if not self.save_data or 'game_state' not in self.save_data:
            return
        
        # 创建新增宠物对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("新增宠物")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 宠物名称
        name_label = tk.Label(
            dialog,
            text="宠物名称:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        name_label.pack(anchor='w', padx=20, pady=10)
        
        name_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=30
        )
        name_entry.pack(anchor='w', padx=20, pady=5)
        
        # 宠物等级
        level_label = tk.Label(
            dialog,
            text="等级:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        level_label.pack(anchor='w', padx=20, pady=10)
        
        level_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=10
        )
        level_entry.insert(0, "1")
        level_entry.pack(anchor='w', padx=20, pady=5)
        
        # 宠物类型
        type_label = tk.Label(
            dialog,
            text="类型:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        type_label.pack(anchor='w', padx=20, pady=10)
        
        type_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=10
        )
        type_entry.insert(0, "普通")
        type_entry.pack(anchor='w', padx=20, pady=5)
        
        # 宠物忠诚度
        loyalty_label = tk.Label(
            dialog,
            text="忠诚度:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        loyalty_label.pack(anchor='w', padx=20, pady=10)
        
        loyalty_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=10
        )
        loyalty_entry.insert(0, "50")
        loyalty_entry.pack(anchor='w', padx=20, pady=5)
        
        # 按钮
        def add_pet():
            pet_name = name_entry.get().strip()
            level_str = level_entry.get().strip()
            pet_type = type_entry.get().strip()
            loyalty_str = loyalty_entry.get().strip()
            
            if not pet_name:
                messagebox.showinfo("提示", "请输入宠物名称")
                return
            
            try:
                level = int(level_str)
                if level <= 0:
                    messagebox.showinfo("提示", "等级必须大于0")
                    return
                
                loyalty = int(loyalty_str)
                if loyalty < 0 or loyalty > 100:
                    messagebox.showinfo("提示", "忠诚度必须在0-100之间")
                    return
                
                # 确保宠物列表存在
                if 'pets' not in self.save_data['game_state']:
                    self.save_data['game_state']['pets'] = []
                
                # 创建新宠物
                new_pet = {
                    'name': pet_name,
                    'level': level,
                    'type': pet_type,
                    'loyalty': loyalty,
                    'skills': []  # 默认空技能列表
                }
                
                # 添加宠物
                self.save_data['game_state']['pets'].append(new_pet)
                
                # 刷新显示
                self.display_save_data()
                
                dialog.destroy()
                messagebox.showinfo("成功", "宠物已添加")
            except ValueError:
                messagebox.showinfo("提示", "请输入有效的数值")
        
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="添加",
            command=add_pet,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        add_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=10)
    
    def add_new_item(self):
        """新增物品"""
        if not self.save_data or 'player' not in self.save_data:
            return
        
        # 创建新增物品对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("新增物品")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 物品名称
        name_label = tk.Label(
            dialog,
            text="物品名称:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        name_label.pack(anchor='w', padx=20, pady=10)
        
        name_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=30
        )
        name_entry.pack(anchor='w', padx=20, pady=5)
        
        # 物品数量
        quantity_label = tk.Label(
            dialog,
            text="数量:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        quantity_label.pack(anchor='w', padx=20, pady=10)
        
        quantity_entry = tk.Entry(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            width=10
        )
        quantity_entry.insert(0, "1")
        quantity_entry.pack(anchor='w', padx=20, pady=5)
        
        # 按钮
        def add_item():
            item_name = name_entry.get().strip()
            quantity_str = quantity_entry.get().strip()
            
            if not item_name:
                messagebox.showinfo("提示", "请输入物品名称")
                return
            
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    messagebox.showinfo("提示", "数量必须大于0")
                    return
                
                # 确保背包字典存在
                if 'inventory' not in self.save_data['player']:
                    self.save_data['player']['inventory'] = {}
                
                # 添加物品
                self.save_data['player']['inventory'][item_name] = quantity
                
                # 刷新显示
                self.display_save_data()
                
                dialog.destroy()
                messagebox.showinfo("成功", "物品已添加到背包")
            except ValueError:
                messagebox.showinfo("提示", "请输入有效的数量")
        
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        add_btn = tk.Button(
            button_frame,
            text="添加",
            command=add_item,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        add_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=10)
    
    def save_changes(self):
        """保存修改"""
        if not self.save_data or not self.current_file:
            messagebox.showinfo("提示", "请先选择一个存档文件")
            return
        
        try:
            # 加密数据
            encrypted_data = self._encrypt_save_data(self.save_data)
            
            # 写入文件
            with open(self.current_file, 'w') as f:
                f.write(encrypted_data)
            
            messagebox.showinfo("成功", "修改已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def save_as_new(self):
        """保存为新文件"""
        if not self.save_data:
            messagebox.showinfo("提示", "请先选择一个存档文件")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存为新文件",
            filetypes=[("存档文件", "*"), ("所有文件", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "saves"),
            initialfile=f"save_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if file_path:
            try:
                # 加密数据
                encrypted_data = self._encrypt_save_data(self.save_data)
                
                # 写入文件
                with open(file_path, 'w') as f:
                    f.write(encrypted_data)
                
                messagebox.showinfo("成功", "文件已保存为新存档！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def _encrypt_save_data(self, data):
        """加密存档数据"""
        # 1. 将数据转换为JSON字符串
        json_data = json.dumps(data, ensure_ascii=False)
        
        # 2. 压缩数据
        compressed_data = zlib.compress(json_data.encode('utf-8'))
        
        # 3. 计算校验和
        checksum = hashlib.sha256(compressed_data).hexdigest()
        
        # 4. 将校验和和数据合并
        combined_data = checksum.encode('utf-8') + b'\n' + compressed_data
        
        # 5. 使用base64编码
        encrypted_data = base64.b64encode(combined_data)
        
        return encrypted_data.decode('utf-8')
    
    def _decrypt_save_data(self, encrypted_data):
        """解密存档数据"""
        try:
            # 1. base64解码
            combined_data = base64.b64decode(encrypted_data)
            
            # 2. 分离校验和和数据
            lines = combined_data.split(b'\n', 1)
            if len(lines) != 2:
                return None
            
            stored_checksum = lines[0].decode('utf-8')
            compressed_data = lines[1]
            
            # 3. 验证校验和
            calculated_checksum = hashlib.sha256(compressed_data).hexdigest()
            if stored_checksum != calculated_checksum:
                print("存档文件已被篡改！")
                return None
            
            # 4. 解压数据
            json_data = zlib.decompress(compressed_data).decode('utf-8')
            
            # 5. 解析JSON
            data = json.loads(json_data)
            
            return data
        except Exception as e:
            print(f"解密存档失败: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    editor = SaveEditor(root)
    root.mainloop()
