#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
复古文字冒险 RPG 游戏 - Tkinter 图形化版本
基于 Python tkinter 模块实现的功能丰富的文字冒险游戏
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import time
import os
import random
import datetime
import threading
from PIL import Image, ImageTk
import json

class GameGUI:
    """游戏主GUI类，管理所有图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("复古文字冒险 RPG - 图形化版本")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # 设置图标（如果有的话）
        # self.root.iconbitmap("icon.ico")
        
        # 游戏实例
        self.game = Game(self)
        
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
        
        # 设置根窗口
        self.root.configure(bg=self.colors['bg'])
        
        # 加载自定义字体
        self.title_font = ('Helvetica', 24, 'bold')
        self.header_font = ('Helvetica', 16, 'bold')
        self.normal_font = ('Helvetica', 12)
        self.small_font = ('Helvetica', 10)
        
        # 创建主框架
        self.create_main_frame()
        
        # 显示主菜单
        self.show_main_menu()
    
    def create_main_frame(self):
        """创建主框架"""
        # 顶部标题
        self.title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            self.title_frame,
            text="复古文字冒险 RPG",
            font=self.title_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack()
        
        # 主内容区域
        self.content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 左侧游戏信息区域
        self.info_frame = tk.Frame(self.content_frame, bg=self.colors['bg'], width=250)
        self.info_frame.pack(side='left', fill='y', padx=(0, 10))
        self.info_frame.pack_propagate(False)
        
        # 右侧主显示区域
        self.display_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        self.display_frame.pack(side='right', fill='both', expand=True)
        
        # 创建显示区域组件
        self.create_info_panel()
        self.create_display_panel()
        
        # 底部状态栏
        self.status_frame = tk.Frame(self.root, bg=self.colors['bg'], height=30)
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="就绪",
            font=self.small_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.status_label.pack(side='left')
    
    def create_info_panel(self):
        """创建信息面板"""
        # 玩家信息
        self.player_info_frame = tk.LabelFrame(
            self.info_frame,
            text="玩家信息",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        self.player_info_frame.pack(fill='x', pady=5)
        
        self.player_name_label = tk.Label(
            self.player_info_frame,
            text="名称: -",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        self.player_name_label.pack(fill='x', padx=5, pady=2)
        
        self.player_level_label = tk.Label(
            self.player_info_frame,
            text="等级: -",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        self.player_level_label.pack(fill='x', padx=5, pady=2)
        
        # 生命值进度条
        self.hp_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.hp_frame.pack(fill='x', padx=5, pady=2)
        
        self.hp_label = tk.Label(
            self.hp_frame,
            text="HP:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            width=3
        )
        self.hp_label.pack(side='left')
        
        self.hp_progress = ttk.Progressbar(
            self.hp_frame,
            length=150,
            mode='determinate',
            style='red.Horizontal.TProgressbar'
        )
        self.hp_progress.pack(side='left', padx=5)
        
        self.hp_value_label = tk.Label(
            self.hp_frame,
            text="0/0",
            font=self.small_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.hp_value_label.pack(side='left')
        
        # 经验值进度条
        self.exp_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.exp_frame.pack(fill='x', padx=5, pady=2)
        
        self.exp_label = tk.Label(
            self.exp_frame,
            text="EXP:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            width=3
        )
        self.exp_label.pack(side='left')
        
        self.exp_progress = ttk.Progressbar(
            self.exp_frame,
            length=150,
            mode='determinate',
            style='blue.Horizontal.TProgressbar'
        )
        self.exp_progress.pack(side='left', padx=5)
        
        self.exp_value_label = tk.Label(
            self.exp_frame,
            text="0/100",
            font=self.small_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.exp_value_label.pack(side='left')
        
        # 属性信息
        self.attrs_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.attrs_frame.pack(fill='x', padx=5, pady=2)
        
        self.attack_label = tk.Label(
            self.attrs_frame,
            text="⚔️ 攻击: 0",
            font=self.small_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.attack_label.pack(side='left', padx=5)
        
        self.defense_label = tk.Label(
            self.attrs_frame,
            text="🛡️ 防御: 0",
            font=self.small_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.defense_label.pack(side='left', padx=5)
        
        self.gold_label = tk.Label(
            self.attrs_frame,
            text="💰 金币: 0",
            font=self.small_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        self.gold_label.pack(side='left', padx=5)
        
        # 游戏状态
        self.game_info_frame = tk.LabelFrame(
            self.info_frame,
            text="游戏状态",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        self.game_info_frame.pack(fill='x', pady=5)
        
        self.day_label = tk.Label(
            self.game_info_frame,
            text="📅 第 1 天",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        self.day_label.pack(fill='x', padx=5, pady=2)
        
        self.time_label = tk.Label(
            self.game_info_frame,
            text="⏰ 08:00",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        self.time_label.pack(fill='x', padx=5, pady=2)
        
        self.scene_label = tk.Label(
            self.game_info_frame,
            text="📍 当前位置: -",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w',
            wraplength=230
        )
        self.scene_label.pack(fill='x', padx=5, pady=2)
        
        # 成就计数
        self.achievement_count_label = tk.Label(
            self.game_info_frame,
            text="🏆 成就: 0/0",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        self.achievement_count_label.pack(fill='x', padx=5, pady=2)
    
    def create_display_panel(self):
        """创建显示面板"""
        # 消息显示区域
        self.message_frame = tk.LabelFrame(
            self.display_frame,
            text="游戏消息",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        self.message_frame.pack(fill='both', expand=True, pady=5)
        
        self.message_text = scrolledtext.ScrolledText(
            self.message_frame,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=15
        )
        self.message_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 配置文本标签
        self.message_text.tag_config('info', foreground='#87ceeb')
        self.message_text.tag_config('success', foreground='#98fb98')
        self.message_text.tag_config('warning', foreground='#ffa07a')
        self.message_text.tag_config('error', foreground='#ff6b68')
        self.message_text.tag_config('gold', foreground='#ffd700')
        
        # 场景描述区域
        self.scene_frame = tk.LabelFrame(
            self.display_frame,
            text="场景描述",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        self.scene_frame.pack(fill='x', pady=5)
        
        self.scene_description = tk.Text(
            self.scene_frame,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=4
        )
        self.scene_description.pack(fill='x', padx=5, pady=5)
        
        # 操作按钮区域
        self.action_frame = tk.LabelFrame(
            self.display_frame,
            text="操作面板",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        self.action_frame.pack(fill='x', pady=5)
        
        # 创建按钮网格
        self.button_frame = tk.Frame(self.action_frame, bg=self.colors['bg'])
        self.button_frame.pack(fill='x', padx=5, pady=5)
        
        # 按钮字典
        self.buttons = {}
    
    def create_action_buttons(self, buttons_config):
        """创建操作按钮"""
        # 清除现有按钮
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # 创建新按钮
        row = 0
        col = 0
        max_cols = 4
        
        for button_config in buttons_config:
            btn = tk.Button(
                self.button_frame,
                text=button_config['text'],
                command=button_config['command'],
                font=self.normal_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                relief='raised',
                width=15,
                height=1
            )
            btn.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            
            self.button_frame.grid_columnconfigure(col, weight=1)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def show_main_menu(self):
        """显示主菜单"""
        self.clear_display()
        
        # 创建主菜单按钮
        buttons_config = [
            {'text': '🎮 新游戏', 'command': self.new_game},
            {'text': '📂 加载游戏', 'command': self.load_game},
            {'text': '⚙️ 游戏设置', 'command': self.show_settings},
            {'text': '🏆 成就系统', 'command': self.show_achievements},
            {'text': '❌ 退出游戏', 'command': self.root.quit}
        ]
        
        self.create_action_buttons(buttons_config)
        
        # 显示欢迎信息
        welcome_text = """
              复古文字冒险 RPG           
             Copyright by xiaoyu

欢迎来到复古文字冒险 RPG 的图形化版本！
使用下方的按钮开始你的冒险之旅。
"""
        self.add_message(welcome_text, 'gold')
        
        # 更新状态
        self.status_label.config(text="主菜单")
    
    def new_game(self):
        """开始新游戏"""
        # 选择难度
        self.select_difficulty()
    
    def select_difficulty(self):
        """选择游戏难度"""
        # 创建难度选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择难度")
        dialog.geometry("500x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择游戏难度",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 难度说明
        difficulty_text = tk.Text(
            dialog,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=8,
            width=50
        )
        difficulty_text.pack(padx=10, pady=5)
        difficulty_text.insert('1.0', """
1. 简单 - 适合新手玩家，敌人较弱，资源丰富
2. 普通 - 平衡的游戏体验
3. 困难 - 挑战性较高，敌人更强
4. 极难 - 非常具有挑战性，需要精心策略
5. 究极 - 极限挑战，只有最资深的玩家才能生存
        """)
        difficulty_text.config(state='disabled')
        
        # 难度选择按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        difficulties = [
            ('简单', 'easy'),
            ('普通', 'normal'),
            ('困难', 'hard'),
            ('极难', 'extreme'),
            ('究极', 'ultimate')
        ]
        
        for text, value in difficulties:
            btn = tk.Button(
                button_frame,
                text=text,
                command=lambda v=value: self.set_difficulty_and_create_character(v, dialog),
                font=self.normal_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                width=8
            )
            btn.pack(side='left', padx=5)
    
    def set_difficulty_and_create_character(self, difficulty, dialog):
        """设置难度并创建角色"""
        self.game.config['difficulty'] = difficulty
        dialog.destroy()
        self.create_character()
    
    def create_character(self):
        """创建角色"""
        # 输入角色名
        name = simpledialog.askstring("创建角色", "请输入你的名字:", parent=self.root)
        if not name:
            name = "冒险者"
        
        # 选择魔法属系
        self.select_magic_affinity(name)
    
    def select_magic_affinity(self, player_name):
        """选择魔法属系"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择魔法属系")
        dialog.geometry("500x550")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择你的魔法属系",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 魔法属系说明
        magic_frame = tk.Frame(dialog, bg=self.colors['bg'])
        magic_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        magic_options = [
            ('🔥 火属性', 'fire', '造成高额单体伤害，燃烧效果'),
            ('💧 水属性', 'water', '降低敌人攻击力，冰冻效果'),
            ('🌪️ 风属性', 'wind', '增加自身闪避，旋风攻击'),
            ('⛰️ 土属性', 'earth', '增加自身防御力，石化效果'),
            ('☀️ 光属性', 'light', '对黑暗系敌人有加成，净化效果'),
            ('🌑 暗属性', 'dark', '高风险高回报，诅咒效果')
        ]
        
        for text, value, desc in magic_options:
            btn = tk.Button(
                magic_frame,
                text=text,
                command=lambda v=value, n=player_name: self.start_new_game(n, v, dialog),
                font=self.normal_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                width=20,
                height=2
            )
            btn.pack(fill='x', pady=2)
            
            desc_label = tk.Label(
                magic_frame,
                text=desc,
                font=self.small_font,
                fg=self.colors['fg'],
                bg=self.colors['bg']
            )
            desc_label.pack(pady=(0, 5))
    
    def start_new_game(self, player_name, magic_affinity, dialog):
        """开始新游戏"""
        dialog.destroy()
        
        # 创建玩家
        diff_settings = self.game.difficulty_settings[self.game.config['difficulty']]
        
        base_hp = int(random.randint(30, 50) * diff_settings['player_hp_multiplier'])
        base_attack = int(random.randint(5, 12) * diff_settings['player_attack_multiplier'])
        base_defense = int(random.randint(2, 8) * diff_settings['player_defense_multiplier'])
        
        self.game.player = Player(player_name, base_hp, base_attack, base_defense)
        self.game.player.magic_affinity = magic_affinity
        self.game.player.magic_power = 5
        
        # 初始化物品
        self.game.player.add_item("新手剑", 1)
        self.game.player.add_item("新手药水", 2)
        
        # 设置初始场景
        self.game.current_scene = "forest"
        
        # 解锁初始成就
        self.game.unlock_achievement("初次冒险")
        
        # 开始游戏
        self.game.game_state = "playing"
        self.game.add_message(f"欢迎来到这个世界，{player_name}！你的冒险之旅即将开始...")
        
        # 更新显示
        self.update_game_info()
        self.show_game_interface()
    
    def load_game(self):
        """加载游戏"""
        saves = self.game.get_save_files()
        
        if not saves:
            messagebox.showinfo("提示", "没有找到存档文件。")
            return
        
        # 创建存档选择对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("选择存档")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择要加载的存档",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 存档列表
        listbox = tk.Listbox(
            dialog,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=10
        )
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        for save in saves:
            listbox.insert(tk.END, f"{save['name']} - {save['date']}")
        
        def on_load():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                if self.game.load_save_game(saves[index]['file']):
                    messagebox.showinfo("成功", "游戏加载成功！")
                    dialog.destroy()
                    self.game.game_state = "playing"
                    self.update_game_info()
                    self.show_game_interface()
                else:
                    messagebox.showerror("错误", "游戏加载失败！")
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        load_btn = tk.Button(
            button_frame,
            text="加载",
            command=on_load,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        load_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def show_settings(self):
        """显示游戏设置"""
        dialog = tk.Toplevel(self.root)
        dialog.title("游戏设置")
        dialog.geometry("400x350")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="游戏设置",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 设置选项
        settings_frame = tk.Frame(dialog, bg=self.colors['bg'])
        settings_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 自动保存
        auto_save_var = tk.BooleanVar(value=self.game.config['auto_save'])
        auto_save_check = tk.Checkbutton(
            settings_frame,
            text="自动保存",
            variable=auto_save_var,
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            selectcolor=self.colors['bg'],
            activebackground=self.colors['bg']
        )
        auto_save_check.pack(anchor='w', pady=5)
        
        # 战斗动画
        battle_anim_var = tk.BooleanVar(value=self.game.config['battle_animations'])
        battle_anim_check = tk.Checkbutton(
            settings_frame,
            text="战斗动画",
            variable=battle_anim_var,
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            selectcolor=self.colors['bg'],
            activebackground=self.colors['bg']
        )
        battle_anim_check.pack(anchor='w', pady=5)
        
        # 文字速度
        speed_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        speed_frame.pack(anchor='w', pady=5)
        
        speed_label = tk.Label(
            speed_frame,
            text="文字速度:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        speed_label.pack(side='left')
        
        speed_var = tk.StringVar()
        if self.game.config['text_speed'] < 0.05:
            speed_var.set("快")
        elif self.game.config['text_speed'] < 0.1:
            speed_var.set("中")
        else:
            speed_var.set("慢")
        
        speed_combo = ttk.Combobox(
            speed_frame,
            textvariable=speed_var,
            values=["快", "中", "慢"],
            state="readonly",
            width=10
        )
        speed_combo.pack(side='left', padx=5)
        
        # 难度选择
        difficulty_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        difficulty_frame.pack(anchor='w', pady=5)
        
        difficulty_label = tk.Label(
            difficulty_frame,
            text="游戏难度:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        difficulty_label.pack(side='left')
        
        difficulty_map = {
            "easy": "简单",
            "normal": "普通",
            "hard": "困难",
            "extreme": "极难",
            "ultimate": "究极"
        }
        
        difficulty_var = tk.StringVar(value=difficulty_map[self.game.config['difficulty']])
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=difficulty_var,
            values=["简单", "普通", "困难", "极难", "究极"],
            state="readonly",
            width=10
        )
        difficulty_combo.pack(side='left', padx=5)
        
        def save_settings():
            # 保存自动保存设置
            self.game.config['auto_save'] = auto_save_var.get()
            
            # 保存战斗动画设置
            self.game.config['battle_animations'] = battle_anim_var.get()
            
            # 保存文字速度
            speed_map = {"快": 0.02, "中": 0.05, "慢": 0.1}
            self.game.config['text_speed'] = speed_map[speed_var.get()]
            
            # 保存难度
            reverse_difficulty_map = {
                "简单": "easy",
                "普通": "normal",
                "困难": "hard",
                "极难": "extreme",
                "究极": "ultimate"
            }
            self.game.config['difficulty'] = reverse_difficulty_map[difficulty_var.get()]
            
            messagebox.showinfo("成功", "设置已保存！")
            dialog.destroy()
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        save_btn = tk.Button(
            button_frame,
            text="保存",
            command=save_settings,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        save_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def show_achievements(self):
        """显示成就系统"""
        dialog = tk.Toplevel(self.root)
        dialog.title("成就系统")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"成就系统 ({len(self.game.achievements)}/{len(self.game.achievements_list)})",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 成就列表
        frame = tk.Frame(dialog, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        canvas = tk.Canvas(frame, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 显示成就
        for achievement, description in self.game.achievements_list.items():
            frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            frame.pack(fill='x', padx=5, pady=2)
            
            status = "✓" if achievement in self.game.achievements else "✗"
            status_color = self.colors['success'] if achievement in self.game.achievements else self.colors['warning']
            
            status_label = tk.Label(
                frame,
                text=status,
                font=self.normal_font,
                fg=status_color,
                bg='#1e1e1e',
                width=2
            )
            status_label.pack(side='left')
            
            achievement_label = tk.Label(
                frame,
                text=f"{achievement}: {description}",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e',
                anchor='w'
            )
            achievement_label.pack(side='left', fill='x', expand=True)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def show_game_interface(self):
        """显示游戏界面"""
        # 创建游戏操作按钮
        buttons_config = [
            {'text': '🔍 探索', 'command': self.explore_area},
            {'text': '💤 休息', 'command': self.rest},
            {'text': '🎒 背包', 'command': self.show_inventory},
            {'text': '📊 角色', 'command': self.show_character_status},
            {'text': '📜 任务', 'command': self.show_quests},
            {'text': '🗺️ 地图', 'command': self.show_map},
            {'text': '💬 NPC', 'command': self.interact_with_npc},
            {'text': '💾 保存', 'command': self.show_save_menu},
            {'text': '⏸️ 菜单', 'command': self.pause_game}
        ]
        
        # 添加场景特定操作
        scene = self.game.scenes[self.game.current_scene]
        if scene['name'] == "宁静小镇":
            buttons_config.append({'text': '🏪 商店', 'command': self.visit_shop})
            buttons_config.append({'text': '🏨 旅馆', 'command': self.visit_inn})
        
        if 'unique_actions' in scene and scene['unique_actions']:
            for action in scene['unique_actions']:
                buttons_config.append({
                    'text': action,
                    'command': lambda a=action: self.perform_unique_action(a)
                })
        
        self.create_action_buttons(buttons_config)
        
        # 更新场景显示
        self.update_scene_display()
    
    def update_game_info(self):
        """更新游戏信息显示"""
        if self.game.player:
            # 玩家信息
            self.player_name_label.config(text=f"名称: {self.game.player.name}")
            self.player_level_label.config(text=f"等级: {self.game.player.level}")
            
            # 生命值
            hp_percent = (self.game.player.hp / self.game.player.max_hp) * 100
            self.hp_progress['value'] = hp_percent
            self.hp_value_label.config(text=f"{self.game.player.hp}/{self.game.player.max_hp}")
            
            # 经验值
            exp_needed = self.game.player.exp_to_next_level()
            exp_percent = (self.game.player.exp / exp_needed) * 100
            self.exp_progress['value'] = exp_percent
            self.exp_value_label.config(text=f"{self.game.player.exp}/{exp_needed}")
            
            # 属性
            self.attack_label.config(text=f"⚔️ 攻击: {self.game.player.attack}")
            self.defense_label.config(text=f"🛡️ 防御: {self.game.player.defense}")
            self.gold_label.config(text=f"💰 金币: {self.game.player.gold}")
            
            # 游戏状态
            self.day_label.config(text=f"📅 第 {self.game.day_count} 天")
            self.time_label.config(text=f"⏰ {self.game.game_time.strftime('%H:%M')}")
            self.achievement_count_label.config(
                text=f"🏆 成就: {len(self.game.achievements)}/{len(self.game.achievements_list)}"
            )
    
    def update_scene_display(self):
        """更新场景显示"""
        scene = self.game.scenes[self.game.current_scene]
        self.scene_label.config(text=f"📍 当前位置: {scene['name']}")
        
        # 清空场景描述
        self.scene_description.delete('1.0', tk.END)
        self.scene_description.insert('1.0', scene['description'])
        
        # 检查场景时间限制
        if scene['time_restriction']:
            current_hour = self.game.game_time.hour
            open_hour, close_hour = scene['time_restriction']
            
            if not (open_hour <= current_hour < close_hour):
                self.scene_description.insert(
                    tk.END,
                    f"\n⚠️ 这个地方现在不开放 (开放时间: {open_hour:02d}:00-{close_hour:02d}:00)"
                )
    
    def add_message(self, message, tag=None):
        """添加消息到显示区域"""
        self.message_text.insert(tk.END, message + "\n", tag)
        self.message_text.see(tk.END)
        self.root.update()
    
    def clear_display(self):
        """清空显示区域"""
        self.message_text.delete('1.0', tk.END)
        self.scene_description.delete('1.0', tk.END)
    
    def explore_area(self):
        """探索当前区域"""
        self.game.explore_area()
        self.update_game_info()
        self.update_scene_display()
    
    def rest(self):
        """休息恢复生命值"""
        self.game.rest()
        self.update_game_info()
        self.add_message(f"你休息了一会儿，恢复了生命值。", 'info')
    
    def show_inventory(self):
        """显示背包"""
        dialog = tk.Toplevel(self.root)
        dialog.title("背包")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"背包 - 金币: {self.game.player.gold}",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 物品列表
        if not self.game.player.inventory:
            empty_label = tk.Label(
                dialog,
                text="你的背包是空的。",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg']
            )
            empty_label.pack(pady=20)
        else:
            frame = tk.Frame(dialog, bg=self.colors['bg'])
            frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            canvas = tk.Canvas(frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 显示物品
            for item_name, quantity in self.game.player.inventory.items():
                item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
                item_frame.pack(fill='x', padx=5, pady=2)
                
                if item_name in self.game.items:
                    item_info = self.game.items[item_name]
                    description = item_info['description']
                    item_type = item_info['type']
                    
                    type_icons = {
                        'consumable': '🧪',
                        'weapon': '⚔️',
                        'armor': '🛡️',
                        'accessory': '💍',
                        'material': '📦',
                        'treasure': '💎',
                        'key': '🔑'
                    }
                    icon = type_icons.get(item_type, '📦')
                else:
                    description = "未知物品"
                    icon = '❓'
                
                item_label = tk.Label(
                    item_frame,
                    text=f"{icon} {item_name} x{quantity}",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                item_label.pack(side='left')
                
                desc_label = tk.Label(
                    item_frame,
                    text=f"- {description}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                desc_label.pack(side='left', padx=5)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # 操作按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        use_btn = tk.Button(
            button_frame,
            text="使用物品",
            command=lambda: self.use_item_dialog(dialog),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        use_btn.pack(side='left', padx=5)
        
        close_btn = tk.Button(
            button_frame,
            text="关闭",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(side='left', padx=5)
    
    def use_item_dialog(self, parent):
        """使用物品对话框"""
        parent.destroy()
        
        # 获取可用的消耗品
        usable_items = []
        for item_name, quantity in self.game.player.inventory.items():
            if item_name in self.game.items:
                item_info = self.game.items[item_name]
                if item_info['type'] == 'consumable':
                    usable_items.append((item_name, quantity, item_info['description']))
        
        if not usable_items:
            messagebox.showinfo("提示", "没有可用的物品。")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("使用物品")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择要使用的物品",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 物品列表
        frame = tk.Frame(dialog, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        listbox = tk.Listbox(
            frame,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=10
        )
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        
        listbox.config(yscrollcommand=scrollbar.set)
        
        for item_name, quantity, description in usable_items:
            listbox.insert(tk.END, f"{item_name} x{quantity} - {description}")
        
        def on_use():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                item_name = usable_items[index][0]
                
                # 使用物品
                if self.game.player.use_item(item_name):
                    if item_name in self.game.items:
                        item_info = self.game.items[item_name]
                        if item_info['effect'] == 'heal':
                            heal_amount = item_info['value']
                            self.game.player.hp = min(
                                self.game.player.max_hp,
                                self.game.player.hp + heal_amount
                            )
                            self.add_message(f"你使用了 {item_name}，恢复了 {heal_amount} 点生命值。", 'success')
                        elif item_info['effect'] == 'exp':
                            exp_gained = item_info['value']
                            self.game.player.gain_exp(exp_gained)
                            self.add_message(f"你使用了 {item_name}，获得了 {exp_gained} 点经验值。", 'info')
                    
                    self.update_game_info()
                    messagebox.showinfo("成功", f"使用了 {item_name}！")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "使用物品失败！")
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        use_btn = tk.Button(
            button_frame,
            text="使用",
            command=on_use,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        use_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def show_character_status(self):
        """显示角色状态"""
        dialog = tk.Toplevel(self.root)
        dialog.title("角色状态")
        dialog.geometry("400x700")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"{self.game.player.name} 的状态",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 基础属性
        info_frame = tk.Frame(dialog, bg=self.colors['bg'])
        info_frame.pack(fill='x', padx=20, pady=5)
        
        info_items = [
            f"等级: {self.game.player.level}",
            f"经验值: {self.game.player.exp}/{self.game.player.exp_to_next_level()}",
            f"生命值: {self.game.player.hp}/{self.game.player.max_hp}",
            f"攻击力: {self.game.player.attack}",
            f"防御力: {self.game.player.defense}",
            f"金币: {self.game.player.gold}"
        ]
        
        for item in info_items:
            label = tk.Label(
                info_frame,
                text=item,
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg'],
                anchor='w'
            )
            label.pack(fill='x', pady=2)
        
        # 魔法信息
        if self.game.player.magic_affinity:
            magic_config = self.game.player.magic_config[self.game.player.magic_affinity]
            
            magic_frame = tk.LabelFrame(
                dialog,
                text="魔法信息",
                font=self.header_font,
                fg=self.colors['fg'],
                bg=self.colors['bg'],
                relief='ridge'
            )
            magic_frame.pack(fill='x', padx=20, pady=10)
            
            magic_items = [
                f"魔法属系: {magic_config['name']}",
                f"魔法等级: {self.game.player.magic_level}",
                f"魔法强度: {self.game.player.magic_power}",
                f"魔法效果: {magic_config['effect']}"
            ]
            
            for item in magic_items:
                label = tk.Label(
                    magic_frame,
                    text=item,
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg=self.colors['bg'],
                    anchor='w'
                )
                label.pack(fill='x', padx=5, pady=2)
        
        # 装备信息
        equip_frame = tk.LabelFrame(
            dialog,
            text="装备",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        equip_frame.pack(fill='x', padx=20, pady=10)
        
        equip_items = [
            f"武器: {self.game.player.equipped['weapon'] or '无'}",
            f"盔甲: {self.game.player.equipped['armor'] or '无'}",
            f"饰品: {self.game.player.equipped['accessory'] or '无'}"
        ]
        
        for item in equip_items:
            label = tk.Label(
                equip_frame,
                text=item,
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg'],
                anchor='w'
            )
            label.pack(fill='x', padx=5, pady=2)
        
        # 成就信息
        achievement_frame = tk.LabelFrame(
            dialog,
            text="成就进度",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        achievement_frame.pack(fill='x', padx=20, pady=10)
        
        achievement_label = tk.Label(
            achievement_frame,
            text=f"已解锁: {len(self.game.achievements)}/{len(self.game.achievements_list)}",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            anchor='w'
        )
        achievement_label.pack(padx=5, pady=5)
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def show_quests(self):
        """显示任务列表"""
        dialog = tk.Toplevel(self.root)
        dialog.title("任务列表")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="任务列表",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 进行中的任务
        active_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(active_frame, text="进行中")
        
        active_quests = []
        for quest_name, quest_data in self.game.quests.items():
            if quest_data['status'] == 'active':
                active_quests.append((quest_name, quest_data))
        
        if active_quests:
            canvas = tk.Canvas(active_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(active_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for quest_name, quest_data in active_quests:
                quest_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=quest_name,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge'
                )
                quest_frame.pack(fill='x', padx=5, pady=5)
                
                desc_label = tk.Label(
                    quest_frame,
                    text=f"描述: {quest_data['description']}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=400
                )
                desc_label.pack(fill='x', padx=5, pady=2)
                
                # 显示任务进度
                if 'target' in quest_data:
                    progress_frame = tk.Frame(quest_frame, bg='#1e1e1e')
                    progress_frame.pack(fill='x', padx=5, pady=2)
                    
                    for target, required in quest_data['target'].items():
                        if target in self.game.player.inventory:
                            current = self.game.player.inventory[target]
                        else:
                            current = 0
                        
                        progress_label = tk.Label(
                            progress_frame,
                            text=f"  {target}: {current}/{required}",
                            font=self.small_font,
                            fg=self.colors['fg'],
                            bg='#1e1e1e'
                        )
                        progress_label.pack(anchor='w')
                
                # 奖励信息
                reward_text = self.game.format_reward(quest_data['reward'])
                reward_label = tk.Label(
                    quest_frame,
                    text=f"奖励: {reward_text}",
                    font=self.small_font,
                    fg=self.colors['success'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                reward_label.pack(fill='x', padx=5, pady=2)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        else:
            empty_label = tk.Label(
                active_frame,
                text="没有进行中的任务。",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        
        # 可接取的任务
        available_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(available_frame, text="可接取")
        
        available_quests = []
        for quest_name, quest_data in self.game.quests.items():
            if quest_data['status'] == 'available':
                available_quests.append((quest_name, quest_data))
        
        if available_quests:
            canvas = tk.Canvas(available_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(available_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for quest_name, quest_data in available_quests:
                quest_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=quest_name,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge'
                )
                quest_frame.pack(fill='x', padx=5, pady=5)
                
                desc_label = tk.Label(
                    quest_frame,
                    text=f"描述: {quest_data['description']}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=400
                )
                desc_label.pack(fill='x', padx=5, pady=2)
                
                reward_text = self.game.format_reward(quest_data['reward'])
                reward_label = tk.Label(
                    quest_frame,
                    text=f"奖励: {reward_text}",
                    font=self.small_font,
                    fg=self.colors['success'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                reward_label.pack(fill='x', padx=5, pady=2)
                
                def accept(q_name=quest_name, q_data=quest_data):
                    q_data['status'] = 'active'
                    self.add_message(f"任务 '{q_name}' 已接取！", 'success')
                    dialog.destroy()
                
                accept_btn = tk.Button(
                    quest_frame,
                    text="接取任务",
                    command=accept,
                    font=self.small_font,
                    bg=self.colors['button_bg'],
                    fg=self.colors['button_fg']
                )
                accept_btn.pack(pady=5)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        else:
            empty_label = tk.Label(
                available_frame,
                text="没有可接取的任务。",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def show_map(self):
        """显示地图"""
        # 创建地图对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("世界地图")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="世界地图",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 当前位置信息
        current_scene = self.game.scenes[self.game.current_scene]
        info_label = tk.Label(
            dialog,
            text=f"当前位置: {current_scene['name']}",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        info_label.pack(pady=5)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 按维度分组场景
        dimensions = {
            'mainland': {'name': '🌍 主大陆', 'scenes': []},
            'underground': {'name': '🪨 地下世界', 'scenes': []},
            'sky': {'name': '☁️ 天空领域', 'scenes': []}
        }
        
        for scene_key, scene_data in self.game.scenes.items():
            dimension = scene_data.get('dimension', 'mainland')
            if dimension in dimensions:
                dimensions[dimension]['scenes'].append((scene_key, scene_data))
        
        # 通用滚轮函数
        def on_mouse_wheel(event, canvas):
            if event.delta:
                # Windows / Mac
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                # Linux
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        for dim_key, dim_info in dimensions.items():
            dim_frame = tk.Frame(notebook, bg='#1e1e1e')
            notebook.add(dim_frame, text=dim_info['name'])
            
            # 按等级要求排序
            dim_info['scenes'].sort(key=lambda x: x[1]['required_level'])
            
            canvas = tk.Canvas(dim_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(dim_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # ========== 绑定滚轮 ==========
            # Windows & Mac
            canvas.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            # Linux
            canvas.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            # 让鼠标在子控件上也能滚动
            def bind_wheel_recursive(widget):
                widget.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
                widget.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
                widget.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
                for child in widget.winfo_children():
                    bind_wheel_recursive(child)
            # ========== 绑定结束 ==========
            
            for scene_key, scene_data in dim_info['scenes']:
                if scene_key == self.game.current_scene:
                    continue
                
                scene_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=scene_data['name'],
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge'
                )
                scene_frame.pack(fill='x', padx=5, pady=5)
                
                desc_label = tk.Label(
                    scene_frame,
                    text=scene_data['description'][:100] + "...",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=400
                )
                desc_label.pack(fill='x', padx=5, pady=2)
                
                # 解锁条件
                if not hasattr(self.game, 'unlocked_scenes'):
                    self.game.unlocked_scenes = {'forest', 'town'}
                
                is_unlocked = scene_key in self.game.unlocked_scenes
                unlock_cost = self.game.calculate_unlock_cost(scene_data)
                
                if is_unlocked:
                    status_text = "✅ 已解锁"
                    status_color = self.colors['success']
                else:
                    status_text = f"🔒 需解锁: {unlock_cost['gold']}金币"
                    status_color = self.colors['warning']
                
                status_label = tk.Label(
                    scene_frame,
                    text=status_text,
                    font=self.small_font,
                    fg=status_color,
                    bg='#1e1e1e'
                )
                status_label.pack(anchor='w', padx=5, pady=2)
                
                # 移动按钮
                def move(s_key=scene_key, s_data=scene_data):
                    self.game.handle_scene_selection(s_key, s_data)
                    dialog.destroy()
                    self.update_game_info()
                    self.update_scene_display()
                    self.show_game_interface()
                
                move_btn = tk.Button(
                    scene_frame,
                    text="前往",
                    command=move,
                    font=self.small_font,
                    bg=self.colors['button_bg'],
                    fg=self.colors['button_fg']
                )
                move_btn.pack(pady=5)
            
            # 递归绑定所有子控件滚轮
            bind_wheel_recursive(scrollable_frame)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)


    
    def interact_with_npc(self):
        """与NPC交互"""
        current_scene_key = self.game.current_scene
        scene = self.game.scenes[current_scene_key]
        
        if not scene['npcs']:
            messagebox.showinfo("提示", "这个地方没有NPC。")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("NPC列表")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择要交谈的NPC",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # NPC列表
        frame = tk.Frame(dialog, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        listbox = tk.Listbox(
            frame,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=10
        )
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        
        listbox.config(yscrollcommand=scrollbar.set)
        
        for npc_name in scene['npcs']:
            listbox.insert(tk.END, npc_name)
        
        def on_talk():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                npc_name = scene['npcs'][index]
                dialog.destroy()
                self.talk_to_npc(npc_name)
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        talk_btn = tk.Button(
            button_frame,
            text="交谈",
            command=on_talk,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        talk_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def talk_to_npc(self, npc_name):
        """与特定NPC交谈"""
        if npc_name not in self.game.npcs:
            messagebox.showinfo("提示", f"{npc_name} 暂无对话数据。")
            return
        
        npc_data = self.game.npcs[npc_name]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"与 {npc_name} 交谈")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"与 {npc_name} 交谈",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 对话内容
        dialogue_text = tk.Text(
            dialog,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=6
        )
        dialogue_text.pack(fill='x', padx=10, pady=5)
        dialogue_text.insert('1.0', f"{npc_name}: \"{npc_data['dialogue']}\"")
        dialogue_text.config(state='disabled')
        
        # 可用选项
        options_frame = tk.LabelFrame(
            dialog,
            text="可用选项",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        options_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 检查是否有任务
        available_quests = []
        for quest_name, quest_data in self.game.quests.items():
            if quest_data['status'] == 'available' and quest_name in npc_data.get('quests', []):
                available_quests.append(quest_name)
        
        completable_quests = []
        for quest_name, quest_data in self.game.quests.items():
            if quest_data['status'] == 'active' and quest_name in npc_data.get('quests', []):
                if self.game.is_quest_completable(quest_data):
                    completable_quests.append(quest_name)
        
        # 创建按钮
        button_frame = tk.Frame(options_frame, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        # 交谈
        talk_btn = tk.Button(
            button_frame,
            text="继续交谈",
            command=lambda: self.add_message(f"{npc_name}: \"{npc_data['dialogue']}\"", 'info'),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15
        )
        talk_btn.pack(pady=5)
        
        # 交易
        if 'trades' in npc_data and npc_data['trades']:
            trade_btn = tk.Button(
                button_frame,
                text="交易",
                command=lambda: self.trade_with_npc(npc_name, dialog),
                font=self.normal_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                width=15
            )
            trade_btn.pack(pady=5)
        
        # 可接取任务
        for quest_name in available_quests:
            quest_data = self.game.quests[quest_name]
            
            quest_frame = tk.Frame(button_frame, bg=self.colors['bg'])
            quest_frame.pack(fill='x', pady=5)
            
            quest_label = tk.Label(
                quest_frame,
                text=f"任务: {quest_name}",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg']
            )
            quest_label.pack()
            
            def accept(q_name=quest_name):
                self.game.quests[q_name]['status'] = 'active'
                self.add_message(f"任务 '{q_name}' 已接取！", 'success')
                dialog.destroy()
            
            accept_btn = tk.Button(
                quest_frame,
                text="接取任务",
                command=accept,
                font=self.small_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg']
            )
            accept_btn.pack()
        
        # 可完成任务
        for quest_name in completable_quests:
            quest_data = self.game.quests[quest_name]
            
            complete_frame = tk.Frame(button_frame, bg=self.colors['bg'])
            complete_frame.pack(fill='x', pady=5)
            
            complete_label = tk.Label(
                complete_frame,
                text=f"任务: {quest_name} (可完成)",
                font=self.normal_font,
                fg=self.colors['success'],
                bg=self.colors['bg']
            )
            complete_label.pack()
            
            def complete(q_name=quest_name, q_data=quest_data):
                # 给予奖励
                if 'exp' in q_data['reward']:
                    exp_gained = q_data['reward']['exp']
                    self.game.player.gain_exp(exp_gained)
                    self.add_message(f"获得 {exp_gained} 经验值", 'success')
                
                if 'gold' in q_data['reward']:
                    gold_gained = q_data['reward']['gold']
                    self.game.player.gold += gold_gained
                    self.add_message(f"获得 {gold_gained} 金币", 'success')
                
                if 'items' in q_data['reward']:
                    for item in q_data['reward']['items']:
                        self.game.player.add_item(item, 1)
                        self.add_message(f"获得物品: {item}", 'success')
                
                q_data['status'] = 'completed'
                self.update_game_info()
                self.add_message(f"任务 '{q_name}' 完成！", 'success')
                dialog.destroy()
            
            complete_btn = tk.Button(
                complete_frame,
                text="提交任务",
                command=complete,
                font=self.small_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg']
            )
            complete_btn.pack()
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="离开",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def trade_with_npc(self, npc_name, parent_dialog):
        """与NPC交易"""
        npc_data = self.game.npcs[npc_name]
        
        if 'trades' not in npc_data or not npc_data['trades']:
            messagebox.showinfo("提示", f"{npc_name} 没有可交易的物品。")
            return
        
        parent_dialog.destroy()
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{npc_name} 的商店")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"{npc_name} 的商店 - 你的金币: {self.game.player.gold}",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 购买页面
        buy_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(buy_frame, text="购买")
        
        canvas = tk.Canvas(buy_frame, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(buy_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        trade_items = list(npc_data['trades'].items())
        
        for item_name, price in trade_items:
            item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            item_frame.pack(fill='x', padx=5, pady=2)
            
            if item_name in self.game.items:
                description = self.game.items[item_name]['description']
            else:
                description = "神秘物品"
            
            item_label = tk.Label(
                item_frame,
                text=f"{item_name} - {price} 金币",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            item_label.pack(side='left', padx=5)
            
            desc_label = tk.Label(
                item_frame,
                text=description,
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            desc_label.pack(side='left', padx=5)
            
            def buy(item=item_name, cost=price):
                if self.game.player.gold >= cost:
                    self.game.player.gold -= cost
                    self.game.player.add_item(item, 1)
                    self.update_game_info()
                    messagebox.showinfo("成功", f"购买了 {item}！")
                    
                    # 更新标题显示
                    title_label.config(text=f"{npc_name} 的商店 - 你的金币: {self.game.player.gold}")
                else:
                    messagebox.showerror("错误", "金币不足！")
            
            buy_btn = tk.Button(
                item_frame,
                text="购买",
                command=buy,
                font=self.small_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg']
            )
            buy_btn.pack(side='right', padx=5)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 出售页面
        sell_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(sell_frame, text="出售")
        
        if self.game.player.inventory:
            canvas = tk.Canvas(sell_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(sell_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            sellable_items = []
            for item_name, quantity in self.game.player.inventory.items():
                if item_name in self.game.items:
                    item_info = self.game.items[item_name]
                    if item_info['type'] in ['material', 'treasure', 'consumable']:
                        sellable_items.append((item_name, quantity, item_info['value']))
            
            for item_name, quantity, value in sellable_items:
                item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
                item_frame.pack(fill='x', padx=5, pady=2)
                
                item_label = tk.Label(
                    item_frame,
                    text=f"{item_name} x{quantity} - {value} 金币/个",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e'
                )
                item_label.pack(side='left', padx=5)
                
                # 出售数量输入
                quantity_var = tk.StringVar(value="1")
                quantity_spinbox = tk.Spinbox(
                    item_frame,
                    from_=1,
                    to=quantity,
                    textvariable=quantity_var,
                    width=5
                )
                quantity_spinbox.pack(side='left', padx=5)
                
                def sell(item=item_name, max_q=quantity, cost=value):
                    try:
                        qty = int(quantity_var.get())
                        qty = min(max_q, max(1, qty))
                        total = cost * qty
                        self.game.player.remove_item(item, qty)
                        self.game.player.gold += total
                        self.update_game_info()
                        messagebox.showinfo("成功", f"出售了 {qty} 个 {item}，获得 {total} 金币！")
                        
                        # 更新标题显示
                        title_label.config(text=f"{npc_name} 的商店 - 你的金币: {self.game.player.gold}")
                        dialog.destroy()
                        self.trade_with_npc(npc_name, dialog)
                    except ValueError:
                        messagebox.showerror("错误", "请输入有效的数量！")
                
                sell_btn = tk.Button(
                    item_frame,
                    text="出售",
                    command=sell,
                    font=self.small_font,
                    bg=self.colors['button_bg'],
                    fg=self.colors['button_fg']
                )
                sell_btn.pack(side='right', padx=5)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        else:
            empty_label = tk.Label(
                sell_frame,
                text="没有可出售的物品。",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="离开",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def visit_shop(self):
        """访问商店"""
        dialog = tk.Toplevel(self.root)
        dialog.title("商店")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text=f"商店 - 你的金币: {self.game.player.gold}",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 商品列表
        shop_items = [
            ("治疗药水", 50, "恢复50点生命值"),
            ("力量药水", 80, "临时增加10点攻击力"),
            ("防御药水", 80, "临时增加10点防御力"),
            ("面包", 15, "恢复15点生命值"),
            ("草药", 20, "恢复20点生命值")
        ]
        
        frame = tk.Frame(dialog, bg='#1e1e1e')
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        canvas = tk.Canvas(frame, bg='#1e1e1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for item_name, price, description in shop_items:
            item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
            item_frame.pack(fill='x', padx=5, pady=2)
            
            item_label = tk.Label(
                item_frame,
                text=f"{item_name} - {price} 金币",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            item_label.pack(side='left', padx=5)
            
            desc_label = tk.Label(
                item_frame,
                text=description,
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            desc_label.pack(side='left', padx=5)
            
            def buy(item=item_name, cost=price):
                if self.game.player.gold >= cost:
                    self.game.player.gold -= cost
                    self.game.player.add_item(item, 1)
                    self.update_game_info()
                    messagebox.showinfo("成功", f"购买了 {item}！")
                    title_label.config(text=f"商店 - 你的金币: {self.game.player.gold}")
                else:
                    messagebox.showerror("错误", "金币不足！")
            
            buy_btn = tk.Button(
                item_frame,
                text="购买",
                command=buy,
                font=self.small_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg']
            )
            buy_btn.pack(side='right', padx=5)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="离开",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def visit_inn(self):
        """访问旅馆"""
        dialog = tk.Toplevel(self.root)
        dialog.title("旅馆")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="旅馆",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 信息
        info_label = tk.Label(
            dialog,
            text="住宿费用: 50 金币 (恢复全部生命值，推进游戏时间)",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        info_label.pack(pady=5)
        
        gold_label = tk.Label(
            dialog,
            text=f"你的金币: {self.game.player.gold}",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        gold_label.pack(pady=5)
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        def stay():
            if self.game.player.gold >= 50:
                self.game.player.gold -= 50
                self.game.player.hp = self.game.player.max_hp
                self.game.game_time += datetime.timedelta(hours=8)
                self.game.day_count += 1
                self.update_game_info()
                messagebox.showinfo("成功", "你好好休息了一晚，恢复了全部生命值。")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "金币不足！")
        
        stay_btn = tk.Button(
            button_frame,
            text="住宿",
            command=stay,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        stay_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="离开",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def perform_unique_action(self, action):
        """执行场景独特操作"""
        self.game.perform_unique_action(action)
        self.update_game_info()
        self.update_scene_display()
    
    def show_save_menu(self):
        """显示保存菜单"""
        dialog = tk.Toplevel(self.root)
        dialog.title("保存游戏")
        dialog.geometry("300x320")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="保存游戏",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(expand=True)
        
        quick_save_btn = tk.Button(
            button_frame,
            text="快速保存",
            command=lambda: self.quick_save(dialog),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        quick_save_btn.pack(pady=5)
        
        slot_save_btn = tk.Button(
            button_frame,
            text="保存到存档位",
            command=lambda: self.save_to_slot(dialog),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        slot_save_btn.pack(pady=5)
        
        delete_btn = tk.Button(
            button_frame,
            text="删除存档",
            command=lambda: self.show_delete_save_menu(dialog),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        delete_btn.pack(pady=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        cancel_btn.pack(pady=5)
    
    def quick_save(self, parent):
        """快速保存"""
        if self.game.save_game():
            messagebox.showinfo("成功", "游戏已保存！")
            parent.destroy()
        else:
            messagebox.showerror("错误", "保存失败！")
    
    def save_to_slot(self, parent):
        """保存到存档位"""
        parent.destroy()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("选择存档位")
        dialog.geometry("300x200")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择存档位",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(expand=True)
        
        for i in range(1, 4):
            btn = tk.Button(
                button_frame,
                text=f"存档位 {i}",
                command=lambda slot=i: self.save_to_slot_number(slot, dialog),
                font=self.normal_font,
                bg=self.colors['button_bg'],
                fg=self.colors['button_fg'],
                width=12,
                height=1
            )
            btn.pack(pady=2)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=12,
            height=1
        )
        cancel_btn.pack(pady=5)
    
    def save_to_slot_number(self, slot, parent):
        """保存到指定存档位"""
        if self.game.save_game(slot):
            messagebox.showinfo("成功", f"游戏已保存到存档位 {slot}！")
            parent.destroy()
        else:
            messagebox.showerror("错误", "保存失败！")
    
    def show_delete_save_menu(self, parent):
        """显示删除存档菜单"""
        parent.destroy()
        
        saves = self.game.get_save_files()
        
        if not saves:
            messagebox.showinfo("提示", "没有找到存档文件。")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("删除存档")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择要删除的存档",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 存档列表
        frame = tk.Frame(dialog, bg=self.colors['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        listbox = tk.Listbox(
            frame,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=10
        )
        listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=listbox.yview)
        scrollbar.pack(side='right', fill='y')
        
        listbox.config(yscrollcommand=scrollbar.set)
        
        for save in saves:
            listbox.insert(tk.END, f"{save['name']} - {save['date']}")
        
        def on_delete():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                save_file = saves[index]['file']
                save_name = saves[index]['name']
                
                if messagebox.askyesno("确认", f"确定要删除存档 '{save_name}' 吗？"):
                    try:
                        os.remove(os.path.join(self.game.saves_dir, save_file))
                        messagebox.showinfo("成功", "存档已删除！")
                        dialog.destroy()
                    except Exception as e:
                        messagebox.showerror("错误", f"删除存档失败: {e}")
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        delete_btn = tk.Button(
            button_frame,
            text="删除",
            command=on_delete,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        delete_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def pause_game(self):
        """暂停游戏"""
        dialog = tk.Toplevel(self.root)
        dialog.title("暂停菜单")
        dialog.geometry("300x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="暂停菜单",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 按钮
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(expand=True)
        
        resume_btn = tk.Button(
            button_frame,
            text="继续游戏",
            command=dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        resume_btn.pack(pady=5)
        
        save_btn = tk.Button(
            button_frame,
            text="保存游戏",
            command=lambda: [dialog.destroy(), self.show_save_menu()],
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        save_btn.pack(pady=5)
        
        settings_btn = tk.Button(
            button_frame,
            text="游戏设置",
            command=lambda: [dialog.destroy(), self.show_settings()],
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        settings_btn.pack(pady=5)
        
        menu_btn = tk.Button(
            button_frame,
            text="返回主菜单",
            command=lambda: [dialog.destroy(), setattr(self.game, 'game_state', "menu"), self.show_main_menu()],
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=15,
            height=2
        )
        menu_btn.pack(pady=5)


class Game:
    """游戏主类，管理所有游戏功能 - 适配GUI版本"""
    
    def __init__(self, gui):
        """初始化游戏"""
        self.gui = gui
        self.player = None
        self.current_map = None
        self.game_time = datetime.datetime.now().replace(hour=8, minute=0, second=0)
        self.game_running = False
        self.game_state = "menu"
        self.saves_dir = os.path.join(os.path.expanduser("~"), "retro_rpg_saves")
        self.current_scene = None
        self.battle = None
        self.achievements = set()
        self.day_count = 1
        self.messages = []
        self.enemies_defeated = 0
        self.quests_completed = 0
        self.trades_completed = 0
        self.unlocked_scenes = {'forest', 'town'}
        
        # 游戏配置
        self.config = {
            "auto_save": True,
            "text_speed": 0.05,
            "battle_animations": True,
            "difficulty": "normal"
        }
        
        # 难度系数配置
        self.difficulty_settings = {
            'easy': {
                'player_hp_multiplier': 1.5,
                'player_attack_multiplier': 1.3,
                'player_defense_multiplier': 1.4,
                'monster_hp_multiplier': 0.7,
                'monster_attack_multiplier': 0.8,
                'monster_defense_multiplier': 0.7,
                'exp_multiplier': 1.2,
                'gold_multiplier': 1.3,
                'item_drop_chance': 0.8,
                'location_level_reduction': 2
            },
            'normal': {
                'player_hp_multiplier': 1.0,
                'player_attack_multiplier': 1.0,
                'player_defense_multiplier': 1.0,
                'monster_hp_multiplier': 1.0,
                'monster_attack_multiplier': 1.0,
                'monster_defense_multiplier': 1.0,
                'exp_multiplier': 1.0,
                'gold_multiplier': 1.0,
                'item_drop_chance': 0.6,
                'location_level_reduction': 0
            },
            'hard': {
                'player_hp_multiplier': 0.8,
                'player_attack_multiplier': 0.9,
                'player_defense_multiplier': 0.8,
                'monster_hp_multiplier': 1.5,
                'monster_attack_multiplier': 1.3,
                'monster_defense_multiplier': 1.4,
                'exp_multiplier': 1.3,
                'gold_multiplier': 1.2,
                'item_drop_chance': 0.5,
                'location_level_reduction': -1
            },
            'extreme': {
                'player_hp_multiplier': 0.6,
                'player_attack_multiplier': 0.8,
                'player_defense_multiplier': 0.7,
                'monster_hp_multiplier': 2.0,
                'monster_attack_multiplier': 1.6,
                'monster_defense_multiplier': 1.8,
                'exp_multiplier': 1.5,
                'gold_multiplier': 1.4,
                'item_drop_chance': 0.4,
                'location_level_reduction': -2
            },
            'ultimate': {
                'player_hp_multiplier': 0.5,
                'player_attack_multiplier': 0.7,
                'player_defense_multiplier': 0.6,
                'monster_hp_multiplier': 3.0,
                'monster_attack_multiplier': 2.0,
                'monster_defense_multiplier': 2.5,
                'exp_multiplier': 2.0,
                'gold_multiplier': 1.5,
                'item_drop_chance': 0.3,
                'location_level_reduction': -3
            }
        }
        
        # 初始化游戏数据
        self.initialize_game_data()
    
    def initialize_game_data(self):
        """初始化游戏数据 - 保持与原游戏相同"""
        # 场景数据
        self.scenes = {
            "forest": {
                "name": "神秘森林",
                "description": "茂密的森林，阳光透过树叶洒下斑驳的光影。",
                "enemies": ["野狼", "森林精灵", "巨熊"],
                "items": ["草药", "木材", "蘑菇"],
                "npcs": ["猎人", "德鲁伊"],
                "events": ["迷路", "发现宝藏", "遇到旅行者"],
                "required_level": 1,
                "required_gold": 10,
                "required_exp": 10,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": False
            },
            "town": {
                "name": "宁静小镇",
                "description": "温馨的小镇，有各种商店和友善的居民。",
                "enemies": [],
                "items": ["面包", "药水", "装备"],
                "npcs": ["铁匠", "商人", "医生", "旅馆老板"],
                "events": ["集市", "节日庆典", "城镇公告"],
                "required_level": 1,
                "required_gold": 20,
                "required_exp": 50,
                "time_restriction": (6, 22),
                "dimension": "mainland",
                "is_boss": False
            },
            "wilderness": {
                "name": "荒野",
                "description": "广阔的荒野，风很大，视野开阔。",
                "enemies": ["野马", "沙漠蝎子", "游牧强盗"],
                "items": ["仙人掌", "沙漠玫瑰", "古老的箭头"],
                "npcs": ["游牧民", "商人"],
                "events": ["沙尘暴", "发现绿洲", "遇到商队"],
                "required_level": 2,
                "required_gold": 50,
                "required_exp": 100,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": False
            },
            "castle": {
                "name": "古老城堡",
                "description": "庄严的城堡，散发着历史的气息和神秘的氛围。",
                "enemies": ["守卫", "幽灵", "恶魔"],
                "items": ["皇家宝物", "魔法书", "剑"],
                "npcs": ["国王", "骑士", "魔法师"],
                "events": ["宫廷宴会", "比武大会", "神秘仪式"],
                "required_level": 3,
                "required_gold": 100,
                "required_exp": 200,
                "time_restriction": (8, 20),
                "dimension": "mainland",
                "is_boss": False
            },
            "tower": {
                "name": "魔法高塔",
                "description": "高耸入云的魔法塔，散发着神秘的魔法能量。",
                "enemies": ["魔法构装体", "元素精灵", "暗影法师"],
                "items": ["魔法水晶", "法术书", "魔法杖"],
                "npcs": ["大法师", "学徒", "魔法商人"],
                "events": ["魔法风暴", "时空裂缝", "元素失控"],
                "required_level": 4,
                "required_gold": 200,
                "required_exp": 350,
                "time_restriction": (9, 18),
                "dimension": "mainland",
                "is_boss": False
            },
            "grand_market": {
                "name": "大集市",
                "description": "热闹非凡的大型集市，来自各地的商人和冒险者在这里交易各种珍稀物品。",
                "enemies": [],
                "items": ["稀有药水", "魔法卷轴", "神秘水晶"],
                "npcs": ["集市管理员", "商人联盟会长", "珍品收藏家"],
                "events": ["拍卖会", "商人聚会", "特价促销"],
                "required_level": 5,
                "required_gold": 300,
                "required_exp": 500,
                "time_restriction": (8, 20),
                "dimension": "mainland",
                "is_boss": False,
                "unique_actions": ["随机商品购买", "珍品拍卖", "黑市交易"]
            },
            "volcano": {
                "name": "火山地带",
                "description": "炽热的火山区域，熔岩流淌，热浪滚滚。",
                "enemies": ["熔岩怪", "火元素", "火山龙"],
                "items": ["火焰水晶", "火山灰", "龙鳞"],
                "npcs": ["火山学者", "龙骑士", "火焰祭司"],
                "events": ["火山喷发", "发现熔岩洞", "龙的试炼"],
                "required_level": 6,
                "required_gold": 500,
                "required_exp": 800,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": False,
                "unique_actions": ["采集熔岩样本", "寻找龙蛋", "与火焰精灵交流"]
            },
            "ice_kingdom": {
                "name": "冰雪王国",
                "description": "被永恒冰雪覆盖的王国，城堡由冰雕成，闪烁着蓝色的光芒。",
                "enemies": ["冰元素", "雪怪", "冰霜巨人"],
                "items": ["冰晶", "雪莲花", "冰冻核心"],
                "npcs": ["冰雪女王", "冰雕师", "冬季法师"],
                "events": ["冰雪节", "冰雕比赛", "极光观赏"],
                "required_level": 7,
                "required_gold": 800,
                "required_exp": 1200,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": False,
                "unique_actions": ["参加冰雕比赛", "寻找雪精灵", "攀登冰峰"]
            },
            "ruins": {
                "name": "古代遗迹",
                "description": "古老文明的遗迹，充满了谜题和陷阱。",
                "enemies": ["石像鬼", "古代守卫", "亡灵法师"],
                "items": ["古代文物", "神秘符文", "失落的技术"],
                "npcs": ["考古学家", "寻宝者", "遗迹守护者"],
                "events": ["机关陷阱", "宝藏发现", "古代灵魂"],
                "required_level": 8,
                "required_gold": 1200,
                "required_exp": 1800,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": False
            },
            "dragon_lair": {
                "name": "龙穴",
                "description": "强大的火龙栖息之地，洞穴深处散发着炽热的光芒。",
                "enemies": ["熔岩守卫", "火焰巨兽", "远古火龙"],
                "items": ["龙鳞", "龙心", "火焰宝石"],
                "npcs": ["龙骑士", "驯龙师"],
                "events": ["龙的觉醒", "火焰风暴", "最终试炼"],
                "required_level": 10,
                "required_gold": 2000,
                "required_exp": 3000,
                "time_restriction": None,
                "dimension": "mainland",
                "is_boss": True,
                "boss_name": "远古火龙",
                "unique_actions": ["龙的试炼", "获取龙之力", "成为龙骑士"]
            },
            
            # ========== 地下世界维度 (Underground) ==========
            "cave": {
                "name": "黑暗洞穴",
                "description": "潮湿阴冷的洞穴，偶尔传来滴水声和奇怪的叫声。",
                "enemies": ["蝙蝠", "洞穴蜘蛛", "石魔"],
                "items": ["矿石", "水晶", "古代金币"],
                "npcs": ["矿工", "考古学家"],
                "events": ["洞穴坍塌", "发现矿脉", "遇到迷路的冒险者"],
                "required_level": 4,
                "required_gold": 250,
                "required_exp": 400,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": False
            },
            "dungeon": {
                "name": "地下监狱",
                "description": "阴森的地下监狱，充满了痛苦和绝望的气息。",
                "enemies": ["骷髅兵", "僵尸", "食尸鬼"],
                "items": ["锁链", "钥匙", "囚犯的日记"],
                "npcs": ["囚犯", "典狱长"],
                "events": ["越狱", "发现秘密通道", "遇到被诅咒的灵魂"],
                "required_level": 6,
                "required_gold": 500,
                "required_exp": 500,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": False
            },
            "dwarven_mine": {
                "name": "矮人矿坑",
                "description": "矮人挖掘的巨大矿坑，充满了各种珍贵的矿石和宝石。",
                "enemies": ["矿洞蜘蛛", "岩石傀儡", "矮人守卫"],
                "items": ["秘银矿石", "矮人啤酒", "宝石"],
                "npcs": ["矮人矿工", "铁匠", "矿洞主管"],
                "events": ["矿洞坍塌", "发现宝藏", "矮人宴会"],
                "required_level": 8,
                "required_gold": 800,
                "required_exp": 600,
                "time_restriction": (6, 20),
                "dimension": "underground",
                "is_boss": False,
                "unique_actions": ["挖矿", "锻造武器", "参加矮人宴会"]
            },
            "poison_marsh": {
                "name": "毒沼",
                "description": "充满有毒气体和致命生物的危险沼泽。",
                "enemies": ["毒蛙", "沼泽蛇", "毒气怪"],
                "items": ["毒蘑菇", "解毒草药", "沼泽水晶"],
                "npcs": ["制毒师", "草药师"],
                "events": ["毒气喷发", "沼泽下陷", "发现古代遗迹"],
                "required_level": 10,
                "required_gold": 1200,
                "required_exp": 700,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": False
            },
            "crystal_cavern": {
                "name": "水晶洞穴",
                "description": "到处都是发光水晶的美丽洞穴，蕴含强大的魔法能量。",
                "enemies": ["水晶守卫", "魔法构装体", "水晶龙"],
                "items": ["魔法水晶", "水晶碎片", "能量核心"],
                "npcs": ["水晶矿工", "魔法师"],
                "events": ["水晶共鸣", "能量爆发", "空间裂缝"],
                "required_level": 12,
                "required_gold": 1800,
                "required_exp": 800,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": False
            },
            "underworld": {
                "name": "冥界",
                "description": "连接生死的神秘领域，充满了亡灵和各种奇异生物。",
                "enemies": ["亡灵战士", "冥界守卫", "灵魂收割者"],
                "items": ["灵魂石", "冥界之火", "死亡契约"],
                "npcs": ["冥界使者", "灵魂向导", "冥王"],
                "events": ["灵魂审判", "冥界暴动", "生死抉择"],
                "required_level": 14,
                "required_gold": 2500,
                "required_exp": 900,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": False
            },
            "shadow_realm": {
                "name": "暗影界",
                "description": "充满黑暗能量的平行世界，是暗影生物的家园。",
                "enemies": ["暗影刺客", "黑暗骑士", "暗影巨兽"],
                "items": ["暗影水晶", "黑暗精华", "隐身药水"],
                "npcs": ["暗影法师", "黑暗商人"],
                "events": ["暗影风暴", "空间扭曲", "黑暗仪式"],
                "required_level": 16,
                "required_gold": 3000,
                "required_exp": 1000,
                "time_restriction": (6, 18),
                "dimension": "underground",
                "is_boss": False
            },
            "ancient_library": {
                "name": "古代图书馆",
                "description": "收藏着远古知识的地下图书馆，书籍会自己移动。",
                "enemies": ["知识守卫", "书虫怪", "智慧幽灵"],
                "items": ["魔法书", "智慧卷轴", "知识结晶"],
                "npcs": ["图书管理员", "学者", "古代贤者"],
                "events": ["知识风暴", "书籍暴动", "时空穿越"],
                "required_level": 18,
                "required_gold": 3500,
                "required_exp": 1100,
                "time_restriction": (8, 22),
                "dimension": "underground",
                "is_boss": False,
                "unique_actions": ["学习禁术", "解读古代文字", "与书籍交流"]
            },
            "mechanical_city": {
                "name": "机械都市",
                "description": "矮人建造的地下机械都市，充满了各种自动化装置。",
                "enemies": ["机械守卫", "蒸汽机器人", "疯狂科学家"],
                "items": ["机械零件", "蒸汽核心", "魔法电池"],
                "npcs": ["工程师", "发明家", "机械师"],
                "events": ["机械暴动", "能源危机", "科技展览"],
                "required_level": 20,
                "required_gold": 4000,
                "required_exp": 1200,
                "time_restriction": (6, 23),
                "dimension": "underground",
                "is_boss": False,
                "unique_actions": ["发明创造", "改造机械", "参加科技展"]
            },
            "demon_pit": {
                "name": "恶魔深渊",
                "description": "通往地狱的入口，强大的恶魔领主在此统治。",
                "enemies": ["恶魔卫士", "地狱犬", "深渊领主"],
                "items": ["恶魔之角", "地狱火石", "黑暗灵魂石"],
                "npcs": ["恶魔祭司", "被诅咒的灵魂"],
                "events": ["恶魔召唤", "灵魂献祭", "最终对决"],
                "required_level": 22,
                "required_gold": 5000,
                "required_exp": 1300,
                "time_restriction": None,
                "dimension": "underground",
                "is_boss": True,
                "boss_name": "深渊领主",
                "unique_actions": ["恶魔契约", "灵魂救赎", "地狱探险"]
            },
            
            # ========== 天空领域维度 (Sky) ==========
            "cloud_village": {
                "name": "云中村庄",
                "description": "建在云层上的宁静村庄，村民们会飞行。",
                "enemies": ["风元素", "飞行野兽", "云精灵"],
                "items": ["云朵精华", "飞行药水", "风之水晶"],
                "npcs": ["村长", "飞行导师", "云之祭司"],
                "events": ["云朵丰收", "飞行比赛", "天空庆典"],
                "required_level": 22,
                "required_gold": 7500,
                "required_exp": 1400,
                "time_restriction": (6, 20),
                "dimension": "sky",
                "is_boss": False,
                "unique_actions": ["学习飞行", "云朵采集", "参加飞行比赛"]
            },
            "floating_island": {
                "name": "浮空岛",
                "description": "漂浮在空中的神秘岛屿，充满了稀有资源。",
                "enemies": ["岛守卫", "飞行怪物", "元素生物"],
                "items": ["浮空石", "天空草", "飞行羽毛"],
                "npcs": ["岛民", "采集者", "研究者"],
                "events": ["岛屿移动", "资源喷发", "神秘光门"],
                "required_level": 23,
                "required_gold": 8000,
                "required_exp": 1500,
                "time_restriction": None,
                "dimension": "sky",
                "is_boss": False
            },
            "sky_city": {
                "name": "天空之城",
                "description": "宏伟的空中都市，建筑金碧辉煌，充满魔法能量。",
                "enemies": ["天空守卫", "天使战士", "魔法构装体"],
                "items": ["天空宝石", "天使羽毛", "飞行扫帚"],
                "npcs": ["城主", "天空法师", "飞行商人"],
                "events": ["空中阅兵", "魔法表演", "商业峰会"],
                "required_level": 24,
                "required_gold": 8500,
                "required_exp": 1600,
                "time_restriction": (6, 22),
                "dimension": "sky",
                "is_boss": False
            },
            "sky_pirates_ship": {
                "name": "天空海盗船",
                "description": "飞行的海盗船，在天空中掠夺过往的飞行船只。",
                "enemies": ["海盗船长", "飞行海盗", "火炮手"],
                "items": ["海盗宝藏", "飞行罗盘", "天空地图"],
                "npcs": ["海盗厨师", "被俘虏的商人"],
                "events": ["海盗袭击", "宝藏发现", "船长对决"],
                "required_level": 25,
                "required_gold": 9000,
                "required_exp": 1700,
                "time_restriction": None,
                "dimension": "sky",
                "is_boss": False
            },
            "celestial_garden": {
                "name": "天空花园",
                "description": "美丽的空中花园，种植着各种珍稀的魔法植物。",
                "enemies": ["花精灵", "植物守卫", "花园管家"],
                "items": ["天空花", "治愈草药", "魔法种子"],
                "npcs": ["园丁", "植物学家", "花仙子"],
                "events": ["花开时节", "花粉风暴", "精灵聚会"],
                "required_level": 26,
                "required_gold": 9500,
                "required_exp": 1800,
                "time_restriction": (8, 18),
                "dimension": "sky",
                "is_boss": False,
                "unique_actions": ["采集花粉", "种植魔法植物", "与花精灵交流"]
            },
            "time_shrine": {
                "name": "时光神殿",
                "description": "掌控时间的神秘神殿，可以看到过去和未来。",
                "enemies": ["时间守卫", "时空怪物", "历史幽灵"],
                "items": ["时光沙漏", "预言水晶", "时间碎片"],
                "npcs": ["时间祭司", "历史学家", "时空旅行者"],
                "events": ["时间风暴", "历史重现", "未来预言"],
                "required_level": 27,
                "required_gold": 10000,
                "required_exp": 1900,
                "time_restriction": (6, 12),
                "dimension": "sky",
                "is_boss": False,
                "unique_actions": ["时间旅行", "改变历史", "预见未来"]
            },
            "fairy_kingdom": {
                "name": "精灵王国",
                "description": "精灵们的空中王国，充满了自然魔法和美丽的建筑。",
                "enemies": ["精灵战士", "自然守卫", "森林巨兽"],
                "items": ["精灵之尘", "自然水晶", "生命药水"],
                "npcs": ["精灵王", "森林祭司", "精灵公主"],
                "events": ["精灵庆典", "自然仪式", "王国会议"],
                "required_level": 28,
                "required_gold": 11000,
                "required_exp": 2000,
                "time_restriction": (6, 20),
                "dimension": "sky",
                "is_boss": False
            },
            "star_gazing_plateau": {
                "name": "观星台",
                "description": "位于高山之巅的巨大观星台，可以清晰地看到宇宙中的星辰。",
                "enemies": ["星灵", "天文守卫", "时空裂缝"],
                "items": ["星尘", "流星碎片", "天文望远镜"],
                "npcs": ["天文学家", "占星师", "星际旅行者"],
                "events": ["流星雨", "星象变化", "遇见星神"],
                "required_level": 29,
                "required_gold": 12000,
                "required_exp": 2200,
                "time_restriction": (6, 18),
                "dimension": "sky",
                "is_boss": False,
                "unique_actions": ["观测星空", "占卜命运", "穿越时空"]
            },
            "sky_palace": {
                "name": "天空宫殿",
                "description": "漂浮在最高云层之上的华丽宫殿，由黄金和宝石建造。",
                "enemies": ["天使守卫", "雷元素", "风暴领主"],
                "items": ["天使羽毛", "天空宝石", "神圣光环"],
                "npcs": ["天空之王", "天使长", "云端使者"],
                "events": ["神圣仪式", "天使舞蹈", "遇见神灵"],
                "required_level": 30,
                "required_gold": 13000,
                "required_exp": 2500,
                "time_restriction": (6, 18),
                "dimension": "sky",
                "is_boss": False
            },
            "celestial_throne": {
                "name": "天界王座",
                "description": "最终的试炼之地，创世神的居所，只有最强大的勇者才能到达。",
                "enemies": ["神之守卫", "元素君主", "创世神"],
                "items": ["神之祝福", "世界之心", "永恒水晶"],
                "npcs": ["创世神", "命运女神", "时间守护者"],
                "events": ["最终审判", "世界重塑", "新的开始"],
                "required_level": 35,
                "required_gold": 15000,
                "required_exp": 5000,
                "time_restriction": None,
                "dimension": "sky",
                "is_boss": True,
                "boss_name": "创世神",
                "unique_actions": ["最终试炼", "成神之路", "世界拯救"],
                "is_final_boss": True
            }
        }
        
        # 敌人数据
        self.enemies = {
            "野狼": {"hp": 30, "attack": 8, "defense": 3, "exp": 20, "gold": 15, "drops": ["狼牙", "狼皮"]},
            "森林精灵": {"hp": 25, "attack": 10, "defense": 2, "exp": 25, "gold": 20, "drops": ["精灵之尘", "魔法草药"]},
            "巨熊": {"hp": 60, "attack": 15, "defense": 8, "exp": 50, "gold": 40, "drops": ["熊皮", "熊胆"]},
            "野马": {"hp": 40, "attack": 10, "defense": 5, "exp": 30, "gold": 25, "drops": ["马鬃", "马皮"]},
            "沙漠蝎子": {"hp": 25, "attack": 12, "defense": 3, "exp": 25, "gold": 15, "drops": ["蝎尾针", "蝎毒"]},
            "游牧强盗": {"hp": 45, "attack": 14, "defense": 6, "exp": 35, "gold": 30, "drops": ["强盗头巾", "弯刀"]},
            "守卫": {"hp": 50, "attack": 15, "defense": 10, "exp": 40, "gold": 35, "drops": ["守卫盔甲", "守卫剑"]},
            "幽灵": {"hp": 35, "attack": 18, "defense": 5, "exp": 45, "gold": 30, "drops": ["幽灵精华", "灵魂石"]},
            "恶魔": {"hp": 100, "attack": 25, "defense": 15, "exp": 100, "gold": 80, "drops": ["恶魔之角", "地狱火石"]},
            "魔法构装体": {"hp": 70, "attack": 20, "defense": 12, "exp": 65, "gold": 45, "drops": ["魔法核心", "金属零件"]},
            "元素精灵": {"hp": 40, "attack": 25, "defense": 8, "exp": 70, "gold": 50, "drops": ["元素精华", "魔法水晶碎片"]},
            "暗影法师": {"hp": 60, "attack": 30, "defense": 10, "exp": 85, "gold": 60, "drops": ["暗影长袍", "黑暗法术书"]},
            "熔岩怪": {"hp": 115, "attack": 30, "defense": 20, "exp": 130, "gold": 110, "drops": ["熔岩核心", "耐热鳞片"]},
            "火元素": {"hp": 95, "attack": 35, "defense": 15, "exp": 125, "gold": 95, "drops": ["火焰精华", "灼热碎片"]},
            "火山龙": {"hp": 200, "attack": 40, "defense": 30, "exp": 200, "gold": 200, "drops": ["龙鳞", "龙心", "龙焰宝石"]},
            "冰元素": {"hp": 80, "attack": 25, "defense": 20, "exp": 110, "gold": 75, "drops": ["冰之精华", "冰晶碎片"]},
            "雪怪": {"hp": 120, "attack": 28, "defense": 22, "exp": 150, "gold": 100, "drops": ["雪怪毛皮", "冰冻核心", "巨型牙齿"]},
            "冰霜巨人": {"hp": 180, "attack": 35, "defense": 28, "exp": 180, "gold": 150, "drops": ["巨人战斧", "冰霜水晶", "巨人心脏"]},
            "石像鬼": {"hp": 90, "attack": 18, "defense": 20, "exp": 75, "gold": 55, "drops": ["石像鬼之眼", "坚硬石片"]},
            "古代守卫": {"hp": 85, "attack": 22, "defense": 18, "exp": 80, "gold": 60, "drops": ["古代盔甲碎片", "守卫徽章"]},
            "亡灵法师": {"hp": 75, "attack": 28, "defense": 15, "exp": 90, "gold": 70, "drops": ["亡灵法术书", "骨杖"]},
            "熔岩守卫": {"hp": 150, "attack": 32, "defense": 25, "exp": 160, "gold": 120, "drops": ["熔岩护盾", "火焰剑"]},
            "火焰巨兽": {"hp": 180, "attack": 38, "defense": 22, "exp": 190, "gold": 150, "drops": ["火焰核心", "巨兽牙齿"]},
            "远古火龙": {"hp": 500, "attack": 60, "defense": 40, "exp": 1000, "gold": 1000, "drops": ["远古龙鳞", "龙之心", "火焰宝珠", "龙之祝福"], "is_boss": True, "boss_theme": "主大陆最终Boss", "special_abilities": ["火焰吐息", "龙鳞屏障", "烈焰风暴"]},
            "蝙蝠": {"hp": 15, "attack": 5, "defense": 1, "exp": 10, "gold": 5, "drops": ["蝙蝠翼", "夜视药水"]},
            "洞穴蜘蛛": {"hp": 20, "attack": 7, "defense": 2, "exp": 15, "gold": 10, "drops": ["蜘蛛丝", "毒牙"]},
            "石魔": {"hp": 80, "attack": 12, "defense": 15, "exp": 60, "gold": 50, "drops": ["魔晶石", "石头心脏"]},
            "骷髅兵": {"hp": 35, "attack": 12, "defense": 8, "exp": 30, "gold": 20, "drops": ["骷髅头", "骨粉"]},
            "僵尸": {"hp": 55, "attack": 10, "defense": 12, "exp": 40, "gold": 25, "drops": ["僵尸牙齿", "腐肉"]},
            "食尸鬼": {"hp": 45, "attack": 18, "defense": 6, "exp": 45, "gold": 30, "drops": ["食尸鬼爪", "黑暗精华"]},
            "矿洞蜘蛛": {"hp": 30, "attack": 14, "defense": 5, "exp": 35, "gold": 25, "drops": ["强化蜘蛛丝", "矿洞毒液"]},
            "岩石傀儡": {"hp": 120, "attack": 18, "defense": 25, "exp": 85, "gold": 60, "drops": ["岩石核心", "傀儡零件"]},
            "矮人守卫": {"hp": 70, "attack": 20, "defense": 15, "exp": 65, "gold": 50, "drops": ["矮人战斧", "守卫盔甲"]},
            "毒蛙": {"hp": 25, "attack": 15, "defense": 3, "exp": 30, "gold": 20, "drops": ["毒蛙毒液", "蛙腿"]},
            "沼泽蛇": {"hp": 40, "attack": 18, "defense": 6, "exp": 45, "gold": 35, "drops": ["蛇毒", "蛇皮"]},
            "毒气怪": {"hp": 60, "attack": 22, "defense": 8, "exp": 60, "gold": 45, "drops": ["毒气核心", "防毒面具"]},
            "水晶守卫": {"hp": 95, "attack": 25, "defense": 20, "exp": 90, "gold": 70, "drops": ["水晶剑", "守卫护盾"]},
            "水晶龙": {"hp": 250, "attack": 35, "defense": 30, "exp": 250, "gold": 200, "drops": ["水晶龙鳞", "龙晶"]},
            "亡灵战士": {"hp": 85, "attack": 22, "defense": 12, "exp": 75, "gold": 55, "drops": ["亡灵剑", "战士盔甲"]},
            "冥界守卫": {"hp": 110, "attack": 25, "defense": 18, "exp": 95, "gold": 70, "drops": ["冥界之剑", "守卫徽章"]},
            "灵魂收割者": {"hp": 90, "attack": 30, "defense": 10, "exp": 100, "gold": 80, "drops": ["收割者镰刀", "灵魂石"]},
            "暗影刺客": {"hp": 65, "attack": 35, "defense": 8, "exp": 95, "gold": 75, "drops": ["暗影匕首", "刺客斗篷"]},
            "黑暗骑士": {"hp": 130, "attack": 28, "defense": 22, "exp": 120, "gold": 90, "drops": ["黑暗之剑", "骑士盔甲"]},
            "暗影巨兽": {"hp": 200, "attack": 32, "defense": 25, "exp": 180, "gold": 150, "drops": ["巨兽利爪", "暗影核心"]},
            "知识守卫": {"hp": 80, "attack": 20, "defense": 15, "exp": 70, "gold": 50, "drops": ["智慧之书", "守卫之剑"]},
            "书虫怪": {"hp": 45, "attack": 18, "defense": 6, "exp": 45, "gold": 30, "drops": ["书虫毒液", "知识结晶"]},
            "智慧幽灵": {"hp": 70, "attack": 25, "defense": 10, "exp": 85, "gold": 60, "drops": ["智慧精华", "幽灵之书"]},
            "机械守卫": {"hp": 125, "attack": 22, "defense": 28, "exp": 90, "gold": 75, "drops": ["机械零件", "守卫核心"]},
            "蒸汽机器人": {"hp": 100, "attack": 28, "defense": 20, "exp": 85, "gold": 65, "drops": ["蒸汽核心", "机器人零件"]},
            "疯狂科学家": {"hp": 60, "attack": 35, "defense": 10, "exp": 100, "gold": 80, "drops": ["科学笔记", "实验器材"]},
            "恶魔卫士": {"hp": 180, "attack": 35, "defense": 30, "exp": 200, "gold": 150, "drops": ["恶魔之剑", "卫士盔甲"]},
            "地狱犬": {"hp": 150, "attack": 38, "defense": 25, "exp": 180, "gold": 130, "drops": ["地狱犬牙", "恶魔之血"]},
            "深渊领主": {"hp": 800, "attack": 80, "defense": 50, "exp": 2000, "gold": 2000, "drops": ["深渊之剑", "领主王冠", "黑暗之心", "恶魔契约"], "is_boss": True, "boss_theme": "地下世界最终Boss", "special_abilities": ["黑暗波动", "灵魂收割", "深渊传送", "恶魔召唤"]},
            "风元素": {"hp": 90, "attack": 32, "defense": 15, "exp": 140, "gold": 90, "drops": ["风之精华", "空气水晶", "轻盈羽毛"]},
            "飞行野兽": {"hp": 85, "attack": 28, "defense": 18, "exp": 120, "gold": 80, "drops": ["野兽羽毛", "飞行肉"]},
            "云精灵": {"hp": 75, "attack": 30, "defense": 15, "exp": 115, "gold": 85, "drops": ["云之精华", "精灵羽毛"]},
            "岛守卫": {"hp": 100, "attack": 25, "defense": 22, "exp": 105, "gold": 75, "drops": ["守卫之剑", "岛屿水晶"]},
            "飞行怪物": {"hp": 95, "attack": 30, "defense": 18, "exp": 115, "gold": 80, "drops": ["飞行翼", "怪物牙齿"]},
            "天空守卫": {"hp": 120, "attack": 32, "defense": 25, "exp": 135, "gold": 100, "drops": ["天空之剑", "守卫盔甲"]},
            "天使战士": {"hp": 130, "attack": 35, "defense": 28, "exp": 150, "gold": 120, "drops": ["天使之剑", "神圣盔甲"]},
            "海盗船长": {"hp": 110, "attack": 38, "defense": 20, "exp": 140, "gold": 110, "drops": ["船长帽", "海盗剑"]},
            "飞行海盗": {"hp": 85, "attack": 32, "defense": 15, "exp": 110, "gold": 85, "drops": ["海盗匕首", "飞行装备"]},
            "火炮手": {"hp": 90, "attack": 40, "defense": 18, "exp": 125, "gold": 95, "drops": ["火炮零件", "火药"]},
            "花精灵": {"hp": 60, "attack": 25, "defense": 12, "exp": 85, "gold": 65, "drops": ["花之精华", "精灵粉末"]},
            "植物守卫": {"hp": 115, "attack": 28, "defense": 25, "exp": 120, "gold": 90, "drops": ["植物藤蔓", "守卫之盾"]},
            "花园管家": {"hp": 95, "attack": 32, "defense": 20, "exp": 115, "gold": 85, "drops": ["管家钥匙", "园艺工具"]},
            "时间守卫": {"hp": 140, "attack": 38, "defense": 30, "exp": 160, "gold": 130, "drops": ["时间之剑", "守卫沙漏"]},
            "时空怪物": {"hp": 160, "attack": 42, "defense": 25, "exp": 180, "gold": 150, "drops": ["时空碎片", "怪物核心"]},
            "历史幽灵": {"hp": 110, "attack": 35, "defense": 20, "exp": 135, "gold": 105, "drops": ["历史记录", "幽灵精华"]},
            "精灵战士": {"hp": 125, "attack": 35, "defense": 28, "exp": 145, "gold": 115, "drops": ["精灵之剑", "战士盔甲"]},
            "自然守卫": {"hp": 145, "attack": 32, "defense": 32, "exp": 155, "gold": 125, "drops": ["自然之盾", "守卫徽章"]},
            "森林巨兽": {"hp": 220, "attack": 40, "defense": 30, "exp": 220, "gold": 180, "drops": ["巨兽利爪", "森林核心"]},
            "星灵": {"hp": 130, "attack": 45, "defense": 25, "exp": 170, "gold": 140, "drops": ["星之精华", "灵魂石"]},
            "天文守卫": {"hp": 150, "attack": 38, "defense": 32, "exp": 165, "gold": 135, "drops": ["天文之剑", "守卫盔甲"]},
            "天使守卫": {"hp": 160, "attack": 42, "defense": 35, "exp": 180, "gold": 150, "drops": ["天使之剑", "神圣护盾"]},
            "雷元素": {"hp": 120, "attack": 48, "defense": 20, "exp": 175, "gold": 145, "drops": ["雷之精华", "闪电水晶"]},
            "风暴领主": {"hp": 280, "attack": 50, "defense": 35, "exp": 280, "gold": 220, "drops": ["风暴之剑", "领主王冠"]},
            "神之守卫": {"hp": 300, "attack": 60, "defense": 50, "exp": 500, "gold": 400, "drops": ["神圣之剑", "神之护盾", "守卫徽章"], "is_boss": True, "boss_theme": "创世神的守护者"},
            "元素君主": {"hp": 400, "attack": 70, "defense": 45, "exp": 800, "gold": 600, "drops": ["元素之剑", "君主王冠", "元素核心"], "is_boss": True, "boss_theme": "元素的掌控者"},
            "创世神": {"hp": 1500, "attack": 120, "defense": 80, "exp": 5000, "gold": 5000, "drops": ["创世神剑", "神之祝福", "世界之心", "永恒水晶", "成神之证"], "is_boss": True, "is_final_boss": True, "boss_theme": "最终创世神", "special_abilities": ["创世之光", "万物复苏", "时空扭曲", "神之审判", "世界重塑"], "difficulty_multiplier": 1.5}
        }
        
        # NPC数据
        self.npcs = {
            "猎人": {"dialogue": "小心森林深处，那里有危险的生物。", "quests": ["猎狼任务", "收集熊皮"], "trades": {"狼牙": 10, "狼皮": 25}},
            "德鲁伊": {"dialogue": "大自然的力量是无穷的，年轻的冒险者。", "quests": ["收集魔法草药", "寻找精灵之尘"], "trades": {"草药": 5, "魔法草药": 30}},
            "矿工": {"dialogue": "这个洞穴深处藏着珍贵的矿石，但也充满了危险。", "quests": ["收集矿石", "探索洞穴深处"], "trades": {"矿石": 8, "水晶": 20}},
            "考古学家": {"dialogue": "这些古老的遗迹隐藏着许多秘密等待我们发现。", "quests": ["寻找古代金币", "探索古代遗迹"], "trades": {"古代金币": 50, "考古发现": 100}},
            "铁匠": {"dialogue": "我可以为你打造最好的装备，但需要合适的材料。", "quests": ["收集铁矿", "寻找稀有金属"], "trades": {"剑": 100, "盔甲": 150, "铁矿": 15}},
            "商人": {"dialogue": "看看我的商品吧，有很多好东西！", "quests": ["送货任务", "寻找稀有物品"], "trades": {"药水": 30, "面包": 10, "装备": 80}},
            "医生": {"dialogue": "保持健康是冒险的基础。", "quests": ["收集草药", "寻找治疗药水配方"], "trades": {"治疗药水": 40, "草药": 5}},
            "旅馆老板": {"dialogue": "欢迎来到我们的旅馆，好好休息吧。", "quests": ["寻找失踪的客人", "收集食材"], "trades": {"住宿": 20, "食物": 15}},
            "国王": {"dialogue": "欢迎来到我的王国，勇敢的冒险者。", "quests": ["消灭恶魔", "拯救公主"], "trades": {"皇家宝物": 200, "爵位": 500}},
            "骑士": {"dialogue": "荣誉和勇气是骑士的准则。", "quests": ["参加比武大会", "保卫王国"], "trades": {"骑士剑": 150, "骑士盔甲": 200}},
            "魔法师": {"dialogue": "魔法的力量需要智慧和耐心来掌握。", "quests": ["寻找魔法书", "收集魔法材料"], "trades": {"魔法书": 100, "魔法药水": 60}},
            "囚犯": {"dialogue": "请帮帮我，我是被冤枉的！", "quests": ["调查冤案", "寻找证据"], "trades": {"情报": 30, "秘密信息": 50}},
            "典狱长": {"dialogue": "这里的囚犯都是危险分子，不要靠近他们。", "quests": ["押送囚犯", "调查越狱"], "trades": {"锁链": 25, "监狱钥匙": 100}},
            "游牧民": {"dialogue": "在这片荒野上，只有强者才能生存。", "quests": ["寻找水源", "抵御强盗"], "trades": {"皮革": 20, "游牧饰品": 40}},
            "大法师": {"dialogue": "魔法是宇宙的语言，只有真正理解它的人才能掌握其力量。", "quests": ["掌握元素魔法", "对抗暗影法师"], "trades": {"魔法水晶": 100, "法术书": 150, "魔法杖": 200}},
            "学徒": {"dialogue": "我正在努力学习魔法，希望有一天能成为像大法师那样强大的存在。", "quests": ["收集魔法材料", "练习基础法术"], "trades": {"魔法水晶碎片": 30, "元素精华": 50}},
            "魔法商人": {"dialogue": "我这里有来自各个位面的魔法物品，你感兴趣吗？", "quests": ["寻找稀有魔法物品", "收集位面碎片"], "trades": {"魔法杖": 180, "法术书": 120, "魔法水晶": 90}},
            "寻宝者": {"dialogue": "宝藏就在那里，等待着勇敢的人去发现！", "quests": ["寻找古代宝藏", "破解遗迹谜题"], "trades": {"古代文物": 80, "神秘符文": 120, "失落的技术": 150}},
            "遗迹守护者": {"dialogue": "我守护着这个古老的遗迹，防止不速之客的入侵。", "quests": ["证明你的价值", "帮助修复遗迹"], "trades": {"古代守卫徽章": 100, "遗迹地图": 150}},
            "船长": {"dialogue": "海洋是无情的，但也是慷慨的，只要你知道如何与它相处。", "quests": ["寻找失落的宝藏船", "对抗海怪"], "trades": {"珍珠": 50, "海图": 100, "航海装备": 150}},
            "渔夫": {"dialogue": "钓鱼需要耐心，就像生活一样。", "quests": ["捕获稀有鱼类", "寻找传说中的鱼"], "trades": {"海草": 15, "鱼": 25, "稀有鱼": 80}},
            "海洋商人": {"dialogue": "我从各个港口带来了珍奇的商品。", "quests": ["寻找深海珍珠", "收集海洋生物样本"], "trades": {"珍珠": 60, "沉船宝藏": 200, "海洋生物样本": 100}},
            "火山学者": {"dialogue": "火山的力量令人敬畏，它既能毁灭也能创造。", "quests": ["研究火山活动", "收集熔岩样本"], "trades": {"火焰水晶": 120, "火山灰": 30, "熔岩样本": 150}},
            "龙骑士": {"dialogue": "与龙的契约是神圣的，我们共同守护这片土地。", "quests": ["寻找龙蛋", "帮助受伤的龙"], "trades": {"龙鳞": 200, "龙骑士装备": 300, "龙焰宝石": 250}},
            "火焰祭司": {"dialogue": "火焰净化一切，也创造一切。", "quests": ["收集火焰精华", "参加火焰仪式"], "trades": {"火焰水晶": 100, "火焰精华": 150, "祭司的祝福": 200}},
            "冰原猎人": {"dialogue": "在这片冰原上，只有最强大的猎人才能够生存。", "quests": ["猎杀冰狼", "寻找失落的村庄"], "trades": {"冰狼牙": 80, "冰狼皮": 120, "冰霜箭": 150}},
            "雪人": {"dialogue": "呼噜呼噜，人类，你给我带吃的来了吗？", "quests": ["收集食物", "寻找温暖的衣物"], "trades": {"冰冻浆果": 40, "雪人友好护符": 200, "冰霜抗性药水": 150}},
            "冰魔法师": {"dialogue": "冰霜的力量是最纯粹的魔法，学会控制它，你将无敌。", "quests": ["收集冰霜水晶", "掌握冰系魔法"], "trades": {"冰霜水晶": 150, "冰系法术书": 250, "冰冻魔杖": 300}},
            "天空法师": {"dialogue": "在天空中，魔法的流动更加清晰，力量也更加强大。", "quests": ["学习飞行魔法", "收集天空水晶"], "trades": {"飞行法术书": 300, "天空水晶": 200, "飞行药水": 180}},
            "机械师": {"dialogue": "机械的力量可以改变世界，只要你知道如何正确地使用它。", "quests": ["修复机械装置", "收集零件"], "trades": {"机械零件": 80, "能量核心": 150, "机械宠物": 300}},
            "飞行骑士": {"dialogue": "在天空中战斗需要特殊的技巧和勇气，你准备好了吗？", "quests": ["空中战斗训练", "击败飞行怪物"], "trades": {"飞行盔甲": 250, "天空剑": 200, "飞行坐骑": 500}},
            "沼泽女巫": {"dialogue": "沼泽的秘密不是所有人都能理解的，你似乎有些特殊。", "quests": ["收集毒蘑菇", "制作解毒药水"], "trades": {"毒蘑菇": 60, "解毒药水": 120, "沼泽护符": 180}},
            "制毒师": {"dialogue": "毒药和解毒剂只有一线之隔，关键在于使用的人。", "quests": ["收集毒腺", "制作强力毒药"], "trades": {"毒腺": 80, "强力毒药": 150, "抗毒药水": 120}},
            "水晶矿工": {"dialogue": "这些水晶蕴含着巨大的能量，小心不要被它们的光芒迷惑。", "quests": ["收集能量水晶", "探索深层矿脉"], "trades": {"能量水晶": 120, "发光宝石": 80, "水晶工具": 150}},
            "宝石商": {"dialogue": "宝石不仅是财富的象征，它们还蕴含着强大的力量。", "quests": ["收集稀有宝石", "鉴定神秘宝石"], "trades": {"宝石项链": 200, "宝石戒指": 150, "宝石法杖": 300}},
            "光魔法师": {"dialogue": "光明魔法是最纯粹的魔法形式，它能够驱逐一切黑暗。", "quests": ["收集光明精华", "净化被诅咒的区域"], "trades": {"光明法术书": 250, "治疗水晶": 180, "光明法杖": 350}},
            "森林精灵": {"dialogue": "森林是我们的家园，我们保护它不受任何伤害。", "quests": ["保护森林", "与树灵沟通"], "trades": {"精灵之尘": 100, "生命之花": 150, "森林护符": 200}},
            "精灵女王": {"dialogue": "欢迎来到精灵的领地，人类。你身上有着不同寻常的气息。", "quests": ["寻找失落的精灵 artifact", "帮助精灵族"], "trades": {"精灵王冠": 500, "女王的祝福": 300, "精灵武器": 400}},
            "美人鱼": {"dialogue": "人类，你能在水下呼吸真是个奇迹，也许我们可以成为朋友。", "quests": ["收集珍珠", "探索沉船"], "trades": {"珍珠项链": 250, "水下呼吸药水": 200, "海洋护符": 300}},
            "海洋法师": {"dialogue": "海洋的力量深不可测，学会倾听它的声音，你将获得无穷的力量。", "quests": ["收集海洋之心", "平息海洋风暴"], "trades": {"海洋法术书": 300, "海洋水晶": 200, "潮汐法杖": 350}},
            "水下居民": {"dialogue": "我们已经在水下生活了数百年，适应了这个环境。", "quests": ["收集水下植物", "帮助建设水下城市"], "trades": {"水下建筑材料": 150, "水下灯": 100, "防水装备": 200}},
            "工程师": {"dialogue": "科技的力量是无限的，只要有足够的创造力和资源。", "quests": ["设计新机器", "收集稀有材料"], "trades": {"机械零件": 100, "能量核心": 180, "机械助手": 400}},
            "科学家": {"dialogue": "知识是最强大的力量，通过研究，我们可以理解这个世界的奥秘。", "quests": ["收集研究样本", "进行科学实验"], "trades": {"科学仪器": 200, "研究笔记": 150, "实验材料": 100}},
            "守墓人": {"dialogue": "这个小镇被诅咒了，只有找到解除诅咒的方法，我们才能获得安宁。", "quests": ["收集灵魂碎片", "解除诅咒"], "trades": {"镇魂石": 180, "驱魔药水": 150, "守墓人的钥匙": 200}},
            "幽灵居民": {"dialogue": "我们被困在这里已经很久了，帮助我们找到解脱的方法。", "quests": ["传递信息给生者", "寻找遗物"], "trades": {"幽灵精华": 120, "灵魂石": 180, "幽灵护符": 250}},
            "驱魔师": {"dialogue": "我专门处理超自然现象，这个小镇的情况很严重。", "quests": ["驱逐强大的幽灵", "净化被诅咒的物品"], "trades": {"驱魔符": 200, "圣水": 150, "驱魔剑": 300}},
            "龙族学者": {"dialogue": "龙族是这个世界上最古老、最强大的生物，研究它们是我的毕生追求。", "quests": ["收集龙鳞", "研究龙的行为"], "trades": {"龙族研究笔记": 300, "龙语词典": 250, "龙鳞护甲": 400}},
            "驯龙师": {"dialogue": "驯服龙需要耐心和勇气，但一旦成功，你将获得最强大的伙伴。", "quests": ["驯服幼龙", "与龙建立信任"], "trades": {"驯龙棒": 200, "龙食": 150, "龙鞍": 500}}
        }
        
        # 道具数据
        self.items = {
            "草药": {"type": "consumable", "effect": "heal", "value": 20, "description": "恢复20点生命值", "durability": 1},
            "木材": {"type": "material", "effect": None, "value": 5, "description": "用于制作或交易", "durability": 0},
            "蘑菇": {"type": "consumable", "effect": "heal", "value": 10, "description": "恢复10点生命值", "durability": 1},
            "矿石": {"type": "material", "effect": None, "value": 8, "description": "用于制作装备", "durability": 0},
            "水晶": {"type": "material", "effect": None, "value": 20, "description": "稀有材料", "durability": 0},
            "古代金币": {"type": "treasure", "effect": None, "value": 50, "description": "价值连城的古代金币", "durability": 0},
            "面包": {"type": "consumable", "effect": "heal", "value": 15, "description": "恢复15点生命值", "durability": 1},
            "药水": {"type": "consumable", "effect": "heal", "value": 50, "description": "恢复50点生命值", "durability": 1},
            "装备": {"type": "equipment", "effect": "attack", "value": 10, "description": "增加10点攻击力", "durability": 100},
            "仙人掌": {"type": "material", "effect": None, "value": 5, "description": "沙漠植物", "durability": 0},
            "沙漠玫瑰": {"type": "treasure", "effect": None, "value": 30, "description": "美丽的沙漠植物", "durability": 0},
            "古老的箭头": {"type": "material", "effect": None, "value": 10, "description": "古代遗物", "durability": 0},
            "皇家宝物": {"type": "treasure", "effect": None, "value": 200, "description": "珍贵的皇家宝物", "durability": 0},
            "魔法书": {"type": "consumable", "effect": "exp", "value": 100, "description": "增加100点经验值", "durability": 1},
            "剑": {"type": "weapon", "effect": "attack", "value": 25, "description": "增加25点攻击力", "durability": 50},
            "锁链": {"type": "material", "effect": None, "value": 25, "description": "坚固的锁链", "durability": 0},
            "钥匙": {"type": "key", "effect": None, "value": 100, "description": "神秘的钥匙", "durability": 1},
            "囚犯的日记": {"type": "treasure", "effect": None, "value": 50, "description": "囚犯的秘密日记", "durability": 0},
            "魔法水晶": {"type": "material", "effect": None, "value": 100, "description": "蕴含强大魔法能量的水晶", "durability": 0},
            "法术书": {"type": "consumable", "effect": "exp", "value": 200, "description": "增加200点经验值并学会新法术", "durability": 1},
            "魔法杖": {"type": "weapon", "effect": "attack", "value": 35, "description": "增加35点攻击力，附带魔法伤害", "durability": 80},
            "魔法水晶碎片": {"type": "material", "effect": None, "value": 30, "description": "魔法水晶的碎片，仍有微弱能量", "durability": 0},
            "元素精华": {"type": "material", "effect": None, "value": 50, "description": "元素力量的结晶", "durability": 0},
            "暗影长袍": {"type": "armor", "effect": "defense", "value": 25, "description": "增加25点防御力，附带暗影能量", "durability": 100},
            "黑暗法术书": {"type": "consumable", "effect": "exp", "value": 150, "description": "增加150点经验值，学会黑暗法术", "durability": 1},
            "古代文物": {"type": "treasure", "effect": None, "value": 80, "description": "来自远古文明的神秘物品", "durability": 0},
            "神秘符文": {"type": "material", "effect": None, "value": 120, "description": "刻有古老文字的神秘符文", "durability": 0},
            "失落的技术": {"type": "treasure", "effect": None, "value": 150, "description": "来自高度文明的失落技术", "durability": 0},
            "珍珠": {"type": "treasure", "effect": None, "value": 50, "description": "从深海采集的美丽珍珠", "durability": 0},
            "海草": {"type": "material", "effect": None, "value": 15, "description": "可食用的海草，也可用于制药", "durability": 0},
            "沉船宝藏": {"type": "treasure", "effect": None, "value": 200, "description": "从沉船上发现的珍贵宝藏", "durability": 0},
            "火焰水晶": {"type": "material", "effect": None, "value": 120, "description": "蕴含火焰力量的水晶", "durability": 0},
            "火山灰": {"type": "material", "effect": None, "value": 30, "description": "火山喷发后的灰烬，富含矿物质", "durability": 0},
            "龙鳞": {"type": "material", "effect": None, "value": 200, "description": "龙身上脱落的鳞片，极其珍贵", "durability": 0},
            "龙心": {"type": "treasure", "effect": None, "value": 500, "description": "龙的心脏，蕴含强大的生命力", "durability": 0},
            "龙焰宝石": {"type": "treasure", "effect": None, "value": 300, "description": "蕴含龙焰力量的宝石", "durability": 0},
            "龙骑士装备": {"type": "armor", "effect": "defense", "value": 50, "description": "龙骑士专用的强大盔甲", "durability": 200},
            "祭司的祝福": {"type": "accessory", "effect": "special", "value": 200, "description": "火焰祭司的祝福，增强所有属性", "durability": 0},
            "冰晶": {"type": "material", "effect": None, "value": 80, "description": "蕴含冰霜力量的晶体", "durability": 0},
            "雪莲花": {"type": "material", "effect": None, "value": 60, "description": "生长在极寒之地的珍贵草药", "durability": 0},
            "冰冻核心": {"type": "material", "effect": None, "value": 120, "description": "蕴含强大冰霜能量的核心", "durability": 0},
            "飞行羽毛": {"type": "material", "effect": None, "value": 100, "description": "能够让人飞行的神秘羽毛", "durability": 0},
            "天空水晶": {"type": "material", "effect": None, "value": 150, "description": "来自天空之城的神秘水晶", "durability": 0},
            "毒蘑菇": {"type": "material", "effect": None, "value": 40, "description": "含有剧毒的蘑菇，可用于制药", "durability": 0},
            "沼泽根茎": {"type": "material", "effect": None, "value": 35, "description": "沼泽中生长的特殊植物根茎", "durability": 0},
            "能量水晶": {"type": "material", "effect": None, "value": 120, "description": "蕴含巨大能量的水晶", "durability": 0},
            "发光宝石": {"type": "treasure", "effect": None, "value": 80, "description": "能够自行发光的美丽宝石", "durability": 0},
            "魔法碎片": {"type": "material", "effect": None, "value": 50, "description": "古代魔法物品的碎片", "durability": 0},
            "魔法浆果": {"type": "consumable", "effect": "heal", "value": 30, "description": "精灵森林中的神奇浆果，恢复30点生命值", "durability": 1},
            "生命之花": {"type": "material", "effect": None, "value": 150, "description": "蕴含强大生命力的花朵", "durability": 0},
            "海蓝宝石": {"type": "treasure", "effect": None, "value": 120, "description": "来自深海的美丽宝石", "durability": 0},
            "水下植物": {"type": "material", "effect": None, "value": 45, "description": "只能在深海中生长的特殊植物", "durability": 0},
            "齿轮": {"type": "material", "effect": None, "value": 30, "description": "机械都市中常见的零件", "durability": 0},
            "蒸汽核心": {"type": "material", "effect": None, "value": 100, "description": "蒸汽动力机械的核心部件", "durability": 0},
            "能量晶体": {"type": "material", "effect": None, "value": 150, "description": "高科技机械的能量来源", "durability": 0},
            "灵魂碎片": {"type": "material", "effect": None, "value": 120, "description": "幽灵的灵魂碎片，蕴含神秘力量", "durability": 0},
            "诅咒物品": {"type": "treasure", "effect": None, "value": 200, "description": "被强大诅咒附着的危险物品", "durability": 0},
            "神秘钥匙": {"type": "key", "effect": None, "value": 150, "description": "能够打开神秘门户的钥匙", "durability": 1},
            "龙蛋碎片": {"type": "material", "effect": None, "value": 300, "description": "龙蛋的碎片，蕴含强大的生命能量", "durability": 0},
            "宝藏": {"type": "treasure", "effect": None, "value": 500, "description": "传说中的宝藏，价值连城", "durability": 0},
            "冰狼牙": {"type": "material", "effect": None, "value": 60, "description": "冰狼的锋利牙齿", "durability": 0},
            "冰狼皮": {"type": "material", "effect": None, "value": 90, "description": "冰狼的毛皮，保暖效果极佳", "durability": 0},
            "冰霜精华": {"type": "material", "effect": None, "value": 120, "description": "冰霜元素的精华，蕴含强大的冰霜力量", "durability": 0},
            "雪怪毛皮": {"type": "material", "effect": None, "value": 100, "description": "雪怪的毛皮，极其保暖", "durability": 0},
            "巨人战斧": {"type": "weapon", "effect": "attack", "value": 45, "description": "冰霜巨人使用的巨大战斧，增加45点攻击力", "durability": 150},
            "冰霜水晶": {"type": "material", "effect": None, "value": 150, "description": "蕴含强大冰霜力量的水晶", "durability": 0},
            "巨人心脏": {"type": "treasure", "effect": None, "value": 250, "description": "冰霜巨人的心脏，蕴含巨大的生命力", "durability": 0},
            "风之精华": {"type": "material", "effect": None, "value": 100, "description": "风元素的精华，蕴含强大的风之力量", "durability": 0},
            "空气水晶": {"type": "material", "effect": None, "value": 80, "description": "蕴含空气元素力量的水晶", "durability": 0},
            "轻盈羽毛": {"type": "material", "effect": None, "value": 60, "description": "能够让人变得轻盈的神秘羽毛", "durability": 0},
            "飞行盔甲": {"type": "armor", "effect": "defense", "value": 35, "description": "专为飞行战斗设计的盔甲，增加35点防御力", "durability": 180},
            "飞行核心": {"type": "material", "effect": None, "value": 180, "description": "飞行装置的核心部件", "durability": 0},
            "雷鸟羽毛": {"type": "material", "effect": None, "value": 120, "description": "雷鸟的羽毛，蕴含雷电力量", "durability": 0},
            "雷电核心": {"type": "material", "effect": None, "value": 200, "description": "蕴含强大雷电力量的核心", "durability": 0},
            "飞行精华": {"type": "material", "effect": None, "value": 150, "description": "飞行生物的精华，能够让人飞行", "durability": 0},
            "毒蛙腿": {"type": "material", "effect": None, "value": 30, "description": "毒蛙的腿，含有剧毒", "durability": 0},
            "毒腺": {"type": "material", "effect": None, "value": 70, "description": "毒蛙的毒腺，可用于制作毒药", "durability": 0},
            "蜥蜴鳞片": {"type": "material", "effect": None, "value": 50, "description": "沼泽巨蜥的鳞片，坚硬耐用", "durability": 0},
            "蜥蜴蛋": {"type": "material", "effect": None, "value": 80, "description": "沼泽巨蜥的蛋，可食用或孵化", "durability": 0},
            "巫师长袍": {"type": "armor", "effect": "defense", "value": 30, "description": "亡灵巫师的长袍，增加30点防御力，附带魔法防护", "durability": 120},
            "灵魂石": {"type": "material", "effect": None, "value": 150, "description": "能够储存灵魂的神秘石头", "durability": 0},
            "水晶丝": {"type": "material", "effect": None, "value": 40, "description": "水晶蜘蛛的丝，坚韧且美丽", "durability": 0},
            "发光毒牙": {"type": "material", "effect": None, "value": 60, "description": "水晶蜘蛛的毒牙，能够发光", "durability": 0},
            "水晶碎片": {"type": "material", "effect": None, "value": 35, "description": "水晶洞穴中的水晶碎片", "durability": 0},
            "宝石碎片": {"type": "material", "effect": None, "value": 70, "description": "宝石魔像身上的宝石碎片", "durability": 0},
            "坚硬石片": {"type": "material", "effect": None, "value": 45, "description": "宝石魔像身上的石片，坚硬如铁", "durability": 0},
            "光明精华": {"type": "material", "effect": None, "value": 120, "description": "光明精灵的精华，蕴含强大的光明力量", "durability": 0},
            "治疗水晶": {"type": "consumable", "effect": "heal", "value": 80, "description": "能够快速恢复生命值的神奇水晶", "durability": 1},
            "精灵武器": {"type": "weapon", "effect": "attack", "value": 35, "description": "精灵守卫使用的武器，增加35点攻击力，附带自然魔法", "durability": 100},
            "自然精华": {"type": "material", "effect": None, "value": 100, "description": "蕴含自然力量的精华", "durability": 0},
            "树妖树枝": {"type": "material", "effect": None, "value": 60, "description": "树妖的树枝，蕴含生命力量", "durability": 0},
            "魔法木材": {"type": "material", "effect": None, "value": 80, "description": "蕴含魔法力量的特殊木材", "durability": 0},
            "鲨鱼牙齿": {"type": "material", "effect": None, "value": 40, "description": "鲨鱼的锋利牙齿", "durability": 0},
            "鲨鱼皮": {"type": "material", "effect": None, "value": 70, "description": "鲨鱼的皮，坚韧耐用", "durability": 0},
            "鱼油": {"type": "material", "effect": None, "value": 30, "description": "从鲨鱼体内提取的油，可用于多种用途", "durability": 0},
            "水之精华": {"type": "material", "effect": None, "value": 100, "description": "水元素的精华，蕴含强大的水之力量", "durability": 0},
            "海洋之心": {"type": "treasure", "effect": None, "value": 250, "description": "海洋的核心，蕴含强大的海洋力量", "durability": 0},
            "守卫三叉戟": {"type": "weapon", "effect": "attack", "value": 40, "description": "深海守卫使用的三叉戟，增加40点攻击力，附带水元素伤害", "durability": 120},
            "深海盔甲": {"type": "armor", "effect": "defense", "value": 35, "description": "深海守卫的盔甲，增加35点防御力，能够在水下呼吸", "durability": 150},
            "海洋水晶": {"type": "material", "effect": None, "value": 120, "description": "蕴含海洋力量的水晶", "durability": 0},
            "机械零件": {"type": "material", "effect": None, "value": 35, "description": "机械都市中的各种零件", "durability": 0},
            "守卫芯片": {"type": "material", "effect": None, "value": 100, "description": "机械守卫的控制芯片", "durability": 0},
            "润滑油": {"type": "material", "effect": None, "value": 25, "description": "用于维护机械的润滑油", "durability": 0},
            "构装体核心": {"type": "material", "effect": None, "value": 150, "description": "构装体的核心部件", "durability": 0},
            "金属碎片": {"type": "material", "effect": None, "value": 30, "description": "各种金属的碎片", "durability": 0},
            "控制芯片": {"type": "material", "effect": None, "value": 120, "description": "用于控制机械的高级芯片", "durability": 0},
            "诅咒水晶": {"type": "material", "effect": None, "value": 150, "description": "被诅咒的水晶，蕴含黑暗力量", "durability": 0},
            "僵尸牙齿": {"type": "material", "effect": None, "value": 30, "description": "僵尸的牙齿，含有病毒", "durability": 0},
            "腐肉": {"type": "material", "effect": None, "value": 15, "description": "僵尸的腐肉，可用于制作毒药或饲料", "durability": 0},
            "病毒样本": {"type": "material", "effect": None, "value": 80, "description": "从僵尸身上提取的病毒样本，可用于研究或制作疫苗", "durability": 0},
            "亡灵法术书": {"type": "consumable", "effect": "exp", "value": 250, "description": "记载亡灵魔法的法术书，增加250点经验值", "durability": 1},
            "骨杖": {"type": "weapon", "effect": "attack", "value": 38, "description": "亡灵法师使用的骨杖，增加38点攻击力，附带亡灵魔法", "durability": 80},
            "黑暗水晶": {"type": "material", "effect": None, "value": 150, "description": "蕴含黑暗力量的水晶", "durability": 0},
            "幼龙鳞": {"type": "material", "effect": None, "value": 200, "description": "幼龙的鳞片，蕴含龙的力量", "durability": 0},
            "龙血": {"type": "material", "effect": None, "value": 250, "description": "龙的血液，蕴含强大的生命力量", "durability": 0},
            "小龙牙": {"type": "material", "effect": None, "value": 150, "description": "幼龙的牙齿，锋利无比", "durability": 0},
            "守卫龙鳞": {"type": "material", "effect": None, "value": 250, "description": "龙守卫的鳞片，比普通龙鳞更加坚硬", "durability": 0},
            "龙守卫武器": {"type": "weapon", "effect": "attack", "value": 48, "description": "龙守卫使用的武器，增加48点攻击力，附带龙焰伤害", "durability": 180},
            "守卫徽章": {"type": "treasure", "effect": None, "value": 300, "description": "龙守卫的徽章，象征着荣誉和力量", "durability": 0},
            "远古龙鳞": {"type": "material", "effect": None, "value": 350, "description": "远古巨龙的鳞片，蕴含强大的龙之力", "durability": 0},
            "龙之宝石": {"type": "treasure", "effect": None, "value": 600, "description": "蕴含强大龙之力的宝石", "durability": 0},
            "远古龙骨": {"type": "material", "effect": None, "value": 400, "description": "远古巨龙的骨头，蕴含强大的龙之力", "durability": 0},
            "冰霜箭": {"type": "weapon", "effect": "attack", "value": 25, "description": "冰原猎人使用的特殊箭矢，增加25点攻击力，附带冰霜伤害", "durability": 50},
            "冰冻浆果": {"type": "consumable", "effect": "heal", "value": 25, "description": "极寒之地生长的特殊浆果，恢复25点生命值", "durability": 1},
            "雪人友好护符": {"type": "accessory", "effect": "special", "value": 200, "description": "雪人赠送的护符，能够与雪人友好相处", "durability": 0},
            "冰霜抗性药水": {"type": "consumable", "effect": "special", "value": 150, "description": "能够抵抗冰霜伤害的药水", "durability": 1},
            "冰系法术书": {"type": "consumable", "effect": "exp", "value": 250, "description": "记载冰系魔法的法术书，增加250点经验值", "durability": 1},
            "冰冻魔杖": {"type": "weapon", "effect": "attack", "value": 35, "description": "冰魔法师使用的魔杖，增加35点攻击力，附带冰系魔法", "durability": 100},
            "飞行法术书": {"type": "consumable", "effect": "exp", "value": 300, "description": "记载飞行魔法的法术书，增加300点经验值", "durability": 1},
            "飞行药水": {"type": "consumable", "effect": "special", "value": 180, "description": "能够让人飞行一段时间的药水", "durability": 1},
            "机械宠物": {"type": "accessory", "effect": "special", "value": 300, "description": "机械师制作的机械宠物，能够提供帮助", "durability": 0},
            "天空剑": {"type": "weapon", "effect": "attack", "value": 40, "description": "飞行骑士使用的剑，增加40点攻击力，附带风元素伤害", "durability": 120},
            "飞行坐骑": {"type": "accessory", "effect": "special", "value": 500, "description": "能够飞行的坐骑，大幅提高移动速度", "durability": 0},
            "解毒药水": {"type": "consumable", "effect": "special", "value": 120, "description": "能够解除各种毒素的药水", "durability": 1},
            "沼泽护符": {"type": "accessory", "effect": "special", "value": 180, "description": "沼泽女巫制作的护符，能够在沼泽中自由行动", "durability": 0},
            "强力毒药": {"type": "consumable", "effect": "special", "value": 150, "description": "能够对敌人造成强大毒性伤害的毒药", "durability": 1},
            "抗毒药水": {"type": "consumable", "effect": "special", "value": 120, "description": "能够抵抗毒素的药水", "durability": 1},
            "水晶工具": {"type": "material", "effect": None, "value": 150, "description": "用水晶制作的特殊工具，非常锋利", "durability": 0},
            "宝石项链": {"type": "accessory", "effect": "special", "value": 200, "description": "宝石商制作的精美项链，能够提升魅力", "durability": 0},
            "宝石戒指": {"type": "accessory", "effect": "special", "value": 150, "description": "宝石商制作的精美戒指，能够提升魔力", "durability": 0},
            "宝石法杖": {"type": "weapon", "effect": "attack", "value": 45, "description": "镶嵌了各种宝石的强大法杖，增加45点攻击力，附带多种元素魔法", "durability": 150},
            "光明法术书": {"type": "consumable", "effect": "exp", "value": 250, "description": "记载光明魔法的法术书，增加250点经验值", "durability": 1},
            "光明法杖": {"type": "weapon", "effect": "attack", "value": 40, "description": "光魔法师使用的法杖，增加40点攻击力，附带光明魔法", "durability": 120},
            "森林护符": {"type": "accessory", "effect": "special", "value": 200, "description": "森林精灵赠送的护符，能够与森林生物友好相处", "durability": 0},
            "精灵王冠": {"type": "accessory", "effect": "special", "value": 500, "description": "精灵女王的王冠，象征着精灵族的最高权力", "durability": 0},
            "女王的祝福": {"type": "accessory", "effect": "special", "value": 300, "description": "精灵女王的祝福，能够大幅提升各项属性", "durability": 0},
            "珍珠项链": {"type": "accessory", "effect": "special", "value": 250, "description": "用水下珍珠制作的项链，能够提升魅力", "durability": 0},
            "水下呼吸药水": {"type": "consumable", "effect": "special", "value": 200, "description": "能够让人在水下呼吸的药水", "durability": 1},
            "海洋护符": {"type": "accessory", "effect": "special", "value": 300, "description": "海洋法师制作的护符，能够在水下自由行动", "durability": 0},
            "海洋法术书": {"type": "consumable", "effect": "exp", "value": 300, "description": "记载海洋魔法的法术书，增加300点经验值", "durability": 1},
            "潮汐法杖": {"type": "weapon", "effect": "attack", "value": 45, "description": "海洋法师使用的法杖，增加45点攻击力，附带海洋魔法", "durability": 150},
            "水下建筑材料": {"type": "material", "effect": None, "value": 150, "description": "用于建设水下建筑的特殊材料", "durability": 0},
            "水下灯": {"type": "material", "effect": None, "value": 100, "description": "能够在水下发光的特殊灯具", "durability": 0},
            "防水装备": {"type": "armor", "effect": "defense", "value": 25, "description": "能够在水下使用的特殊装备，增加25点防御力", "durability": 100},
            "机械助手": {"type": "accessory", "effect": "special", "value": 400, "description": "工程师制作的高级机械助手，能够提供强大的帮助", "durability": 0},
            "科学仪器": {"type": "material", "effect": None, "value": 200, "description": "科学家使用的各种精密仪器", "durability": 0},
            "研究笔记": {"type": "material", "effect": None, "value": 150, "description": "科学家的研究笔记，记载了各种重要发现", "durability": 0},
            "实验材料": {"type": "material", "effect": None, "value": 100, "description": "进行科学实验所需的各种材料", "durability": 0},
            "镇魂石": {"type": "material", "effect": None, "value": 180, "description": "能够镇压灵魂的神秘石头", "durability": 0},
            "驱魔药水": {"type": "consumable", "effect": "special", "value": 150, "description": "能够驱逐邪恶灵魂的药水", "durability": 1},
            "守墓人的钥匙": {"type": "key", "effect": None, "value": 200, "description": "守墓人保管的特殊钥匙，能够打开神秘门户", "durability": 1},
            "幽灵护符": {"type": "accessory", "effect": "special", "value": 250, "description": "能够与幽灵沟通的神秘护符", "durability": 0},
            "驱魔符": {"type": "consumable", "effect": "special", "value": 200, "description": "能够驱逐邪恶灵魂的符咒", "durability": 1},
            "圣水": {"type": "consumable", "effect": "special", "value": 150, "description": "经过祝福的圣水，能够净化邪恶", "durability": 1},
            "驱魔剑": {"type": "weapon", "effect": "attack", "value": 45, "description": "驱魔师使用的特殊剑，增加45点攻击力，对邪恶生物有额外伤害", "durability": 150},
            "龙族研究笔记": {"type": "material", "effect": None, "value": 300, "description": "龙族学者的研究笔记，记载了龙族的各种信息", "durability": 0},
            "龙语词典": {"type": "material", "effect": None, "value": 250, "description": "记载龙语的词典，能够与龙沟通", "durability": 0},
            "龙鳞护甲": {"type": "armor", "effect": "defense", "value": 50, "description": "用龙鳞制作的强大护甲，增加50点防御力", "durability": 200},
            "驯龙棒": {"type": "material", "effect": None, "value": 200, "description": "驯龙师使用的特殊棒子，能够安抚龙的情绪", "durability": 0},
            "龙食": {"type": "material", "effect": None, "value": 150, "description": "专门喂养龙的特殊食物", "durability": 0},
            "龙鞍": {"type": "accessory", "effect": "special", "value": 500, "description": "专门为龙设计的鞍，能够骑乘龙", "durability": 0}
        }
        
        # 任务数据
        self.quests = {
            "猎狼任务": {"description": "杀死5只野狼", "target": {"野狼": 5}, "reward": {"exp": 100, "gold": 50, "items": ["猎人的弓"]}, "status": "available", "type": "main"},
            "收集熊皮": {"description": "收集3张熊皮", "target": {"熊皮": 3}, "reward": {"exp": 80, "gold": 40, "items": ["熊皮大衣"]}, "status": "available", "type": "side"},
            "收集魔法草药": {"description": "收集10个魔法草药", "target": {"魔法草药": 10}, "reward": {"exp": 120, "gold": 60, "items": ["治疗药水配方"]}, "status": "available", "type": "main"},
            "寻找精灵之尘": {"description": "收集5个精灵之尘", "target": {"精灵之尘": 5}, "reward": {"exp": 90, "gold": 45, "items": ["魔法护符"]}, "status": "available", "type": "side"},
            "收集矿石": {"description": "收集20个矿石", "target": {"矿石": 20}, "reward": {"exp": 150, "gold": 75, "items": ["矿工镐"]}, "status": "available", "type": "main"},
            "探索洞穴深处": {"description": "到达洞穴最深处", "target": {"action": "explore_cave_deep"}, "reward": {"exp": 200, "gold": 100, "items": ["洞穴地图"]}, "status": "available", "type": "side"},
            "送货任务": {"description": "将货物送到隔壁村庄", "target": {"action": "deliver_goods"}, "reward": {"exp": 100, "gold": 80, "items": ["商人的推荐信"]}, "status": "available", "type": "side"},
            "寻找稀有物品": {"description": "寻找3个稀有物品", "target": {"稀有物品": 3}, "reward": {"exp": 250, "gold": 150, "items": ["稀有收藏家"]}, "status": "available", "type": "side"},
            "消灭恶魔": {"description": "杀死城堡中的恶魔", "target": {"恶魔": 1}, "reward": {"exp": 500, "gold": 300, "items": ["恶魔克星", "皇家勋章"]}, "status": "available", "type": "main"},
            "拯救公主": {"description": "从城堡地牢中救出公主", "target": {"action": "save_princess"}, "reward": {"exp": 800, "gold": 500, "items": ["公主的祝福", "王国英雄称号"]}, "status": "available", "type": "main"},
            "掌握元素魔法": {"description": "收集所有元素精华", "target": {"元素精华": 5}, "reward": {"exp": 300, "gold": 200, "items": ["元素法师称号", "元素法杖"]}, "status": "available", "type": "main"},
            "对抗暗影法师": {"description": "击败魔法高塔中的暗影法师", "target": {"暗影法师": 3}, "reward": {"exp": 400, "gold": 250, "items": ["光明护符", "大法师的认可"]}, "status": "available", "type": "main"},
            "寻找古代宝藏": {"description": "在古代遗迹中找到失落的宝藏", "target": {"action": "find_ancient_treasure"}, "reward": {"exp": 500, "gold": 300, "items": ["古代宝藏图", "探险家称号"]}, "status": "available", "type": "main"},
            "破解遗迹谜题": {"description": "解开古代遗迹中的三个谜题", "target": {"action": "solve_ruin_puzzles"}, "reward": {"exp": 350, "gold": 180, "items": ["古代智慧", "解谜大师"]}, "status": "available", "type": "side"},
            "寻找失落的宝藏船": {"description": "在神秘海域找到传说中的宝藏船", "target": {"action": "find_treasure_ship"}, "reward": {"exp": 600, "gold": 400, "items": ["海盗王的宝藏", "航海家称号"]}, "status": "available", "type": "main"},
            "对抗海怪": {"description": "击败威胁船只的大海怪", "target": {"海怪": 2}, "reward": {"exp": 450, "gold": 280, "items": ["海怪猎人称号", "海洋之心"]}, "status": "available", "type": "main"},
            "研究火山活动": {"description": "收集火山地带的熔岩样本", "target": {"熔岩样本": 5}, "reward": {"exp": 320, "gold": 190, "items": ["火山研究笔记", "地质学家称号"]}, "status": "available", "type": "side"},
            "寻找龙蛋": {"description": "在火山地带找到并保护龙蛋", "target": {"action": "find_dragon_egg"}, "reward": {"exp": 700, "gold": 500, "items": ["龙骑士伙伴", "龙语者称号"]}, "status": "available", "type": "main"},
            "帮助受伤的龙": {"description": "治疗一只受伤的龙", "target": {"action": "heal_dragon"}, "reward": {"exp": 650, "gold": 450, "items": ["龙的祝福", "龙骑士装备"]}, "status": "available", "type": "main"},
            "收集火焰精华": {"description": "收集火山地带的火焰精华", "target": {"火焰精华": 8}, "reward": {"exp": 380, "gold": 220, "items": ["火焰祭司长袍", "火焰操控者称号"]}, "status": "available", "type": "side"},
            "猎杀冰狼": {"description": "在极寒之地猎杀10只冰狼", "target": {"冰狼": 10}, "reward": {"exp": 400, "gold": 250, "items": ["冰狼皮大衣", "冰原猎手称号"]}, "status": "available", "type": "main"},
            "寻找失落的村庄": {"description": "在极寒之地寻找失落的村庄", "target": {"action": "find_lost_village"}, "reward": {"exp": 350, "gold": 200, "items": ["村庄地图", "探险家称号"]}, "status": "available", "type": "side"},
            "收集冰霜水晶": {"description": "收集15个冰霜水晶", "target": {"冰霜水晶": 15}, "reward": {"exp": 450, "gold": 300, "items": ["冰霜魔杖", "冰系法师称号"]}, "status": "available", "type": "main"},
            "掌握冰系魔法": {"description": "学会三种冰系魔法", "target": {"action": "master_ice_magic"}, "reward": {"exp": 500, "gold": 350, "items": ["冰系法术书", "冰霜大师称号"]}, "status": "available", "type": "main"},
            "学习飞行魔法": {"description": "在天空之城学习飞行魔法", "target": {"action": "learn_flying_magic"}, "reward": {"exp": 480, "gold": 320, "items": ["飞行法术书", "飞行法师称号"]}, "status": "available", "type": "main"},
            "收集天空水晶": {"description": "收集20个天空水晶", "target": {"天空水晶": 20}, "reward": {"exp": 420, "gold": 280, "items": ["天空法杖", "天空使者称号"]}, "status": "available", "type": "side"},
            "修复机械装置": {"description": "帮助机械师修复10个机械装置", "target": {"action": "repair_mechanical_devices"}, "reward": {"exp": 400, "gold": 250, "items": ["机械零件工具箱", "机械师助手称号"]}, "status": "available", "type": "side"},
            "收集零件": {"description": "收集30个机械零件", "target": {"机械零件": 30}, "reward": {"exp": 380, "gold": 220, "items": ["机械宠物", "收藏家称号"]}, "status": "available", "type": "side"},
            "空中战斗训练": {"description": "完成飞行骑士的空中战斗训练", "target": {"action": "complete_air_combat_training"}, "reward": {"exp": 520, "gold": 350, "items": ["飞行盔甲", "空战大师称号"]}, "status": "available", "type": "main"},
            "击败飞行怪物": {"description": "击败15只飞行怪物", "target": {"雷鸟": 15}, "reward": {"exp": 450, "gold": 300, "items": ["天空剑", "飞行猎手称号"]}, "status": "available", "type": "side"},
            "收集毒蘑菇": {"description": "在迷雾沼泽收集25个毒蘑菇", "target": {"毒蘑菇": 25}, "reward": {"exp": 380, "gold": 220, "items": ["解毒药水配方", "制毒师助手称号"]}, "status": "available", "type": "side"},
            "制作解毒药水": {"description": "制作10瓶解毒药水", "target": {"action": "craft_antidote_potions"}, "reward": {"exp": 420, "gold": 280, "items": ["高级解毒药水", "药剂师称号"]}, "status": "available", "type": "main"},
            "收集毒腺": {"description": "收集15个毒腺", "target": {"毒腺": 15}, "reward": {"exp": 400, "gold": 250, "items": ["强力毒药配方", "制毒大师称号"]}, "status": "available", "type": "side"},
            "制作强力毒药": {"description": "制作5瓶强力毒药", "target": {"action": "craft_powerful_poisons"}, "reward": {"exp": 450, "gold": 300, "items": ["毒匕首", "毒药师称号"]}, "status": "available", "type": "main"},
            "收集能量水晶": {"description": "在水晶洞穴收集18个能量水晶", "target": {"能量水晶": 18}, "reward": {"exp": 420, "gold": 280, "items": ["水晶工具", "矿工大师称号"]}, "status": "available", "type": "side"},
            "探索深层矿脉": {"description": "探索水晶洞穴的深层矿脉", "target": {"action": "explore_deep_mines"}, "reward": {"exp": 480, "gold": 320, "items": ["稀有水晶", "探险家称号"]}, "status": "available", "type": "main"},
            "收集稀有宝石": {"description": "收集10个稀有宝石", "target": {"发光宝石": 10}, "reward": {"exp": 450, "gold": 300, "items": ["宝石项链", "珠宝商称号"]}, "status": "available", "type": "side"},
            "鉴定神秘宝石": {"description": "帮助宝石商鉴定5个神秘宝石", "target": {"action": "identify_mystery_gems"}, "reward": {"exp": 400, "gold": 250, "items": ["宝石鉴定工具", "鉴定大师称号"]}, "status": "available", "type": "side"},
            "收集光明精华": {"description": "收集12个光明精华", "target": {"光明精华": 12}, "reward": {"exp": 480, "gold": 320, "items": ["光明法杖", "光明使者称号"]}, "status": "available", "type": "main"},
            "净化被诅咒的区域": {"description": "净化3个被诅咒的区域", "target": {"action": "purify_cursed_areas"}, "reward": {"exp": 550, "gold": 380, "items": ["光明护符", "净化大师称号"]}, "status": "available", "type": "main"},
            "保护森林": {"description": "在精灵森林击败20个敌人", "target": {"森林狼": 20}, "reward": {"exp": 420, "gold": 280, "items": ["森林护符", "森林守卫称号"]}, "status": "available", "type": "side"},
            "与树灵沟通": {"description": "学会与树灵沟通", "target": {"action": "communicate_with_tree_spirits"}, "reward": {"exp": 480, "gold": 320, "items": ["生命之花", "德鲁伊称号"]}, "status": "available", "type": "main"},
            "寻找失落的精灵artifact": {"description": "寻找失落的精灵神器", "target": {"action": "find_lost_elf_artifact"}, "reward": {"exp": 600, "gold": 400, "items": ["精灵王冠", "精灵之友称号"]}, "status": "available", "type": "main"},
            "帮助精灵族": {"description": "完成5个精灵族的任务", "target": {"action": "help_elf_clan"}, "reward": {"exp": 550, "gold": 380, "items": ["精灵武器", "精灵盟友称号"]}, "status": "available", "type": "main"},
            "收集珍珠": {"description": "在水下城市收集25个珍珠", "target": {"珍珠": 25}, "reward": {"exp": 420, "gold": 280, "items": ["珍珠项链", "珠宝收集家称号"]}, "status": "available", "type": "side"},
            "探索沉船": {"description": "探索3艘沉船", "target": {"action": "explore_sunken_ships"}, "reward": {"exp": 500, "gold": 350, "items": ["沉船宝藏", "航海家称号"]}, "status": "available", "type": "main"},
            "收集海洋之心": {"description": "收集5个海洋之心", "target": {"海洋之心": 5}, "reward": {"exp": 550, "gold": 380, "items": ["海洋法杖", "海洋法师称号"]}, "status": "available", "type": "main"},
            "平息海洋风暴": {"description": "平息3场海洋风暴", "target": {"action": "calm_ocean_storms"}, "reward": {"exp": 600, "gold": 400, "items": ["海洋护符", "海洋守护者称号"]}, "status": "available", "type": "main"},
            "收集水下植物": {"description": "收集30个水下植物", "target": {"水下植物": 30}, "reward": {"exp": 400, "gold": 250, "items": ["水下灯", "海洋生物学家称号"]}, "status": "available", "type": "side"},
            "帮助建设水下城市": {"description": "帮助水下居民建设城市", "target": {"action": "help_build_underwater_city"}, "reward": {"exp": 520, "gold": 350, "items": ["防水装备", "建筑师称号"]}, "status": "available", "type": "side"},
            "设计新机器": {"description": "设计3台新机器", "target": {"action": "design_new_machines"}, "reward": {"exp": 580, "gold": 400, "items": ["机械助手", "发明家称号"]}, "status": "available", "type": "main"},
            "收集稀有材料": {"description": "收集20个稀有材料", "target": {"能量晶体": 20}, "reward": {"exp": 450, "gold": 300, "items": ["高级机械零件", "材料收集家称号"]}, "status": "available", "type": "side"},
            "收集研究样本": {"description": "收集25个研究样本", "target": {"病毒样本": 25}, "reward": {"exp": 420, "gold": 280, "items": ["科学仪器", "研究员称号"]}, "status": "available", "type": "side"},
            "进行科学实验": {"description": "进行10次科学实验", "target": {"action": "conduct_scientific_experiments"}, "reward": {"exp": 500, "gold": 350, "items": ["实验笔记", "科学家称号"]}, "status": "available", "type": "main"},
            "收集灵魂碎片": {"description": "在幽灵小镇收集15个灵魂碎片", "target": {"灵魂碎片": 15}, "reward": {"exp": 450, "gold": 300, "items": ["镇魂石", "灵魂收集者称号"]}, "status": "available", "type": "side"},
            "解除诅咒": {"description": "解除幽灵小镇的诅咒", "target": {"action": "lift_ghost_town_curse"}, "reward": {"exp": 650, "gold": 450, "items": ["驱魔剑", "驱魔大师称号"]}, "status": "available", "type": "main"},
            "传递信息给生者": {"description": "帮助5个幽灵传递信息给生者", "target": {"action": "deliver_messages_to_living"}, "reward": {"exp": 480, "gold": 320, "items": ["幽灵护符", "灵魂使者称号"]}, "status": "available", "type": "side"},
            "寻找遗物": {"description": "为幽灵寻找10个遗物", "target": {"action": "find_relics_for_ghosts"}, "reward": {"exp": 520, "gold": 350, "items": ["古董收藏家", "遗物收集者称号"]}, "status": "available", "type": "side"},
            "驱逐强大的幽灵": {"description": "驱逐5个强大的幽灵", "target": {"action": "exorcise_powerful_ghosts"}, "reward": {"exp": 600, "gold": 400, "items": ["驱魔符", "驱魔人称号"]}, "status": "available", "type": "main"},
            "净化被诅咒的物品": {"description": "净化15个被诅咒的物品", "target": {"诅咒物品": 15}, "reward": {"exp": 550, "gold": 380, "items": ["圣水", "净化大师称号"]}, "status": "available", "type": "side"},
            "收集龙鳞": {"description": "收集30个龙鳞", "target": {"龙鳞": 30}, "reward": {"exp": 580, "gold": 400, "items": ["龙鳞护甲", "龙族研究者称号"]}, "status": "available", "type": "side"},
            "研究龙的行为": {"description": "研究5种龙的行为", "target": {"action": "study_dragon_behavior"}, "reward": {"exp": 620, "gold": 420, "items": ["龙语词典", "龙族学者称号"]}, "status": "available", "type": "main"},
            "驯服幼龙": {"description": "驯服一只幼龙", "target": {"action": "tame_baby_dragon"}, "reward": {"exp": 700, "gold": 500, "items": ["龙鞍", "驯龙师称号"]}, "status": "available", "type": "main"},
            "与龙建立信任": {"description": "与龙建立信任关系", "target": {"action": "build_trust_with_dragon"}, "reward": {"exp": 650, "gold": 450, "items": ["龙骑士装备", "龙骑士称号"]}, "status": "available", "type": "main"}
        }
        
        # 成就数据
        self.achievements_list = {
            "初次冒险": "开始你的第一次冒险",
            "森林探索者": "探索完整个森林",
            "洞穴探险者": "深入洞穴探险",
            "城镇朋友": "与所有城镇NPC交谈",
            "荒野求生": "在荒野中生存3天",
            "城堡勇者": "进入古老城堡",
            "地牢英雄": "探索地下监狱",
            "战斗大师": "击败100个敌人",
            "收集家": "收集50个不同的物品",
            "任务达人": "完成20个任务",
            "富甲一方": "拥有1000金币",
            "等级达人": "达到20级",
            "铁匠大师": "打造10件装备",
            "药剂师": "使用50个消耗品",
            "冒险家": "探索所有场景",
            "救世主": "完成主线任务",
            "收藏家": "收集所有稀有物品",
            "战斗精英": "击败所有类型的敌人",
            "商人": "完成50次交易",
            "生存专家": "在游戏中生存30天",
            "冰洞探索者": "探索冰冻洞穴",
            "魔法森林使者": "探索魔法森林",
            "天空之城访客": "访问天空之城",
            "深海探索者": "探索水下城市",
            "幽灵镇勇者": "探索幽灵小镇",
            "浮空岛探险家": "探索浮空岛",
            "矮人矿坑挖掘者": "探索矮人矿坑",
            "知识追寻者": "探索古老图书馆",
            "沙漠绿洲发现者": "发现沙漠绿洲",
            "龙穴勇者": "探索龙穴",
            "机械都市访客": "访问机械都市",
            "毒沼幸存者": "穿越毒沼",
            "天空园丁": "探索天空花园",
            "暗影界行者": "进入暗影界",
            "水晶洞穴探索者": "探索水晶洞穴",
            "天空海盗": "登上天空海盗船",
            "时光旅行者": "访问时光神殿",
            "精灵王国使者": "访问精灵王国",
            "冥界访客": "进入冥界",
            "云中村民": "访问云中之村",
            "空中园丁": "探索空中花园",
            "暗影商人": "探索暗影市场",
            "水晶矿工": "探索水晶矿场",
            "天空村民": "访问天空村落",
            "水下居民": "访问水下村庄",
            "恶魔访客": "探索恶魔领域",
            "天使之城访客": "访问天使之城",
            "时光探索者": "探索时光废墟",
            "龙之岛探险家": "探索龙族岛屿",
            "大集市商人": "访问大集市",
            "魔法学徒": "访问魔法学院",
            "幽灵船乘客": "登上幽灵船",
            "空中酒客": "访问空中酒馆",
            "冰宫访客": "访问冰之宫殿",
            "火焰祭司": "访问火焰神殿",
            "风之谷探索者": "探索风之谷",
            "大地使者": "访问大地王国",
            "天空学者": "访问天空图书馆",
            "造梦师": "探索梦境领域",
            "虚空行者": "探索虚空空间",
            "天体观测者": "访问天体观测站",
            "最终胜利者": "击败暗影君主，拯救世界"
        }
    
    def add_message(self, message, tag=None):
        """添加游戏消息"""
        self.messages.append(message)
        if self.gui:
            self.gui.add_message(message, tag)
    
    def update_game_time(self):
        """更新游戏时间"""
        hours_passed = random.randint(1, 3)
        self.game_time += datetime.timedelta(hours=hours_passed)
        
        if self.game_time.hour < 8:
            self.day_count += 1
            self.add_message(f"🌅 新的一天开始了！现在是第 {self.day_count} 天。", 'info')
    
    def explore_area(self):
        """探索当前区域"""
        scene = self.scenes[self.current_scene]
        
        self.add_message(f"\n你开始探索{scene['name']}...", 'info')
        
        event_type = random.choice(['enemy', 'item', 'event', 'nothing'])
        
        if event_type == 'enemy' and scene['enemies']:
            enemy_name = random.choice(scene['enemies'])
            self.start_battle(enemy_name)
        elif event_type == 'item' and scene['items']:
            item_name = random.choice(scene['items'])
            quantity = random.randint(1, 3)
            self.player.add_item(item_name, quantity)
            self.add_message(f"你发现了 {quantity} 个 {item_name}！", 'success')
        elif event_type == 'event' and scene['events']:
            event = random.choice(scene['events'])
            self.trigger_event(event)
        else:
            self.add_message("你没有发现任何特别的东西。", 'info')
        
        exp_gained = random.randint(1, 5)
        self.player.gain_exp(exp_gained)
        self.add_message(f"探索获得 {exp_gained} 点经验值", 'info')
        
        self.update_game_time()
        self.gui.update_game_info()
    
    def start_battle(self, enemy_name):
        """开始战斗 - 简化版战斗系统"""
        enemy_data = self.enemies[enemy_name]
        
        difficulty = self.config['difficulty']
        diff_settings = self.difficulty_settings[difficulty]
        
        level_scaling = (self.player.level - 1) * 0.1
        attack_scaling = self.player.attack * 0.2
        defense_scaling = self.player.defense * 0.15
        
        enemy_hp = int(enemy_data['hp'] * (1 + level_scaling) * diff_settings['monster_hp_multiplier'])
        enemy_attack = int(enemy_data['attack'] * (1 + level_scaling + defense_scaling) * diff_settings['monster_attack_multiplier'])
        enemy_defense = int(enemy_data['defense'] * (1 + level_scaling + attack_scaling) * diff_settings['monster_defense_multiplier'])
        
        enemy_hp = min(max(enemy_hp, enemy_data['hp']), enemy_data['hp'] * 5)
        enemy_attack = min(max(enemy_attack, enemy_data['attack']), enemy_data['attack'] * 3)
        enemy_defense = min(max(enemy_defense, enemy_data['defense']), enemy_data['defense'] * 3)
        
        self.add_message(f"⚔️ 你遇到了 {enemy_name}！", 'warning')
        
        battle_round = 1
        original_hp = enemy_hp
        
        while enemy_hp > 0 and self.player.hp > 0:
            self.add_message(f"--- 回合 {battle_round} ---", 'info')
            self.add_message(f"{enemy_name} HP: {enemy_hp}/{original_hp}", 'warning')
            self.add_message(f"{self.player.name} HP: {self.player.hp}/{self.player.max_hp}", 'info')
            
            # 简单战斗逻辑 - 玩家攻击
            base_damage = max(1, self.player.attack - enemy_defense)
            damage_variation = random.randint(-2, 3)
            damage = max(1, base_damage + damage_variation)
            enemy_hp -= damage
            
            self.add_message(f"你对 {enemy_name} 造成了 {damage} 点伤害！", 'success')
            
            if enemy_hp <= 0:
                self.add_message(f"{enemy_name} 被击败了！", 'success')
                break
            
            # 敌人攻击
            base_damage = max(1, enemy_attack - self.player.defense)
            damage_variation = random.randint(-2, 3)
            damage = max(1, base_damage + damage_variation)
            self.player.hp = max(0, self.player.hp - damage)
            
            self.add_message(f"{enemy_name} 对你造成了 {damage} 点伤害！", 'error')
            
            if self.player.hp <= 0:
                self.add_message("你被击败了！", 'error')
                break
            
            battle_round += 1
            self.gui.update_game_info()
            time.sleep(1)
        
        # 战斗结果
        if self.player.hp > 0:
            exp_gained = int(enemy_data['exp'] * diff_settings['exp_multiplier'])
            gold_gained = int(enemy_data['gold'] * diff_settings['gold_multiplier'])
            
            self.player.gain_exp(exp_gained)
            self.player.gold += gold_gained
            
            self.add_message(f"战斗胜利！获得 {exp_gained} 经验值和 {gold_gained} 金币", 'success')
            
            if 'drops' in enemy_data and enemy_data['drops']:
                for drop_item in enemy_data['drops']:
                    if random.random() < diff_settings['item_drop_chance']:
                        self.player.add_item(drop_item, 1)
                        self.add_message(f"{enemy_name} 掉落了 {drop_item}！", 'success')
            
            self.update_quest_progress(enemy_name, 1)
            
            if enemy_name == "恶魔":
                self.unlock_achievement("城堡勇者")
            
            self.enemies_defeated += 1
            if self.enemies_defeated >= 100:
                self.unlock_achievement("战斗大师")
        else:
            self.player.hp = 1
            self.player.gold = max(0, self.player.gold - 50)
            self.add_message("你被击败了！损失了一些金币，勉强活了下来。", 'error')
        
        self.gui.update_game_info()
    
    def rest(self):
        """休息恢复生命值"""
        heal_amount = min(self.player.max_hp - self.player.hp, 20)
        self.player.hp += heal_amount
        self.add_message(f"\n你休息了一会儿，恢复了 {heal_amount} 点生命值。", 'info')
        self.update_game_time()
        self.gui.update_game_info()
    
    def trigger_event(self, event_name):
        """触发随机事件"""
        self.add_message(f"🎲 随机事件: {event_name}", 'info')
        
        if event_name == "迷路":
            self.add_message("你在森林中迷路了，花费了额外的时间才找到正确的路。", 'warning')
            self.update_game_time()
        elif event_name == "发现宝藏":
            treasure = random.choice(["古代金币", "水晶", "皇家宝物"])
            self.player.add_item(treasure, 1)
            self.add_message(f"你发现了一个隐藏的宝藏！获得了 {treasure}！", 'success')
        elif event_name == "遇到旅行者":
            gold_gained = random.randint(10, 50)
            self.player.gold += gold_gained
            self.add_message(f"获得 {gold_gained} 金币！", 'success')
        elif event_name == "洞穴坍塌":
            damage = random.randint(5, 20)
            self.player.hp = max(1, self.player.hp - damage)
            self.add_message(f"受到 {damage} 点伤害！", 'error')
        elif event_name == "发现矿脉":
            ore_count = random.randint(3, 8)
            self.player.add_item("矿石", ore_count)
            self.add_message(f"获得 {ore_count} 个矿石！", 'success')
        elif event_name == "节日庆典":
            self.player.hp = min(self.player.max_hp, self.player.hp + 30)
            self.add_message("恢复了30点生命值！", 'success')
        elif event_name == "沙尘暴":
            self.update_game_time()
            self.add_message("你花了额外的时间才穿越过去。", 'info')
        elif event_name == "发现绿洲":
            self.player.hp = min(self.player.max_hp, self.player.hp + 50)
            self.add_message("恢复了50点生命值！", 'success')
        elif event_name == "宫廷宴会":
            exp_gained = random.randint(50, 100)
            self.player.gain_exp(exp_gained)
            self.add_message(f"获得 {exp_gained} 经验值！", 'info')
        
        self.gui.update_game_info()
    
    def perform_unique_action(self, action):
        """执行场景独特操作"""
        self.add_message(f"\n你选择了: {action}", 'info')
        
        # 根据不同的操作执行不同的逻辑
        if action == "采集熔岩样本":
            if random.random() < 0.7:
                self.player.add_item("熔岩样本", 1)
                self.add_message("你成功采集了熔岩样本！", 'success')
                self.player.gain_exp(20)
            else:
                damage = random.randint(10, 30)
                self.player.hp = max(1, self.player.hp - damage)
                self.add_message(f"采集失败！你被熔岩烫伤了，受到 {damage} 点伤害。", 'error')
        
        elif action == "寻找龙蛋":
            if random.random() < 0.3:
                self.player.add_item("龙蛋", 1)
                self.add_message("你发现了一个龙蛋！这是极其珍贵的宝物！", 'success')
                self.unlock_achievement("龙蛋收集者")
            else:
                self.add_message("你仔细搜索了周围，但没有找到龙蛋。", 'info')
        
        elif action == "与火焰精灵交流":
            if random.random() < 0.6:
                self.player.add_item("火焰精华", 1)
                self.add_message("火焰精灵对你表示友好，赠予你火焰精华。", 'success')
                self.player.gain_exp(30)
            else:
                self.add_message("火焰精灵对你保持警惕，不愿与你交流。", 'info')
        
        elif action == "参加冰雕比赛":
            if random.random() < 0.5:
                self.player.add_item("冰雕大赛奖杯", 1)
                self.player.gold += 100
                self.add_message("恭喜你获得冰雕比赛冠军！获得奖杯和100金币！", 'success')
                self.unlock_achievement("冰雕大师")
            else:
                self.player.add_item("参与奖", 1)
                self.add_message("你参加了比赛，获得了参与奖。", 'info')
        
        elif action == "寻找雪精灵":
            if random.random() < 0.4:
                self.player.add_item("雪精灵的祝福", 1)
                self.player.max_hp += 10
                self.add_message("雪精灵赐予你祝福，你的最大生命值永久增加10点！", 'success')
            else:
                self.add_message("雪精灵隐藏得很好，你没有找到它们。", 'info')
        
        elif action == "攀登冰峰":
            if self.player.level >= 25:
                self.player.add_item("冰峰之顶的宝石", 1)
                self.add_message("你成功攀登到冰峰之顶，获得了传说中的宝石！", 'success')
                self.unlock_achievement("登山家")
            else:
                damage = random.randint(20, 40)
                self.player.hp = max(1, self.player.hp - damage)
                self.add_message(f"冰峰太陡峭了，你滑倒受伤，受到 {damage} 点伤害。", 'error')
        
        elif action == "参加神圣仪式":
            if random.random() < 0.7:
                self.player.add_item("神圣光环", 1)
                self.player.defense += 5
                self.add_message("神圣仪式增强了你的防御力，永久增加5点！", 'success')
            else:
                self.add_message("仪式过程中出现了一些小意外，没有获得特殊效果。", 'info')
        
        elif action == "学习飞行":
            if random.random() < 0.6:
                self.player.add_item("飞行药水", 2)
                self.add_message("你学会了基础的飞行技巧，获得2瓶飞行药水！", 'success')
            else:
                self.add_message("飞行学习比你想象的要困难，还需要更多练习。", 'info')
        
        elif action == "与天使交流":
            if random.random() < 0.5:
                self.player.gain_exp(50)
                self.add_message("天使的智慧启迪了你，获得50点经验值！", 'info')
            else:
                self.add_message("天使似乎有更重要的事情要做，只是简单地和你打了个招呼。", 'info')
        
        elif action == "潜水探索":
            if random.random() < 0.6:
                treasure = random.choice(["珍珠", "深海宝石", "古代金币"])
                self.player.add_item(treasure, random.randint(1, 3))
                self.add_message(f"你在水下发现了 {treasure}！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 15)
                self.add_message("你在水下遇到了危险的暗流，勉强逃脱但受了伤。", 'error')
        
        elif action == "解读古代文字":
            if random.random() < 0.4:
                self.player.add_item("古代知识卷轴", 1)
                self.add_message("你成功解读了古代文字，获得了珍贵的知识卷轴！", 'success')
            else:
                self.add_message("这些文字太古老了，你只能辨认出一些片段。", 'info')
        
        elif action == "与海洋生物交流":
            if random.random() < 0.5:
                self.player.add_item("海洋之心", 1)
                self.add_message("海洋生物对你表示友好，赠予你海洋之心！", 'success')
            else:
                self.add_message("海洋生物对你保持警惕，迅速游走了。", 'info')
        
        elif action == "参加幽灵舞会":
            if random.random() < 0.6:
                self.player.add_item("幽灵礼服", 1)
                self.add_message("幽灵们欢迎你的加入，赠予你一件幽灵礼服！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("舞会中有些幽灵表现得很不友好，你被阴气所伤。", 'error')
        
        elif action == "解开诅咒":
            if random.random() < 0.3:
                self.player.add_item("净化之石", 1)
                self.add_message("你成功解开了一部分诅咒，获得了净化之石！", 'success')
                self.unlock_achievement("驱魔师")
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("诅咒的力量比你想象的更强大，你受到了反噬。", 'error')
        
        elif action == "与亡灵对话":
            if random.random() < 0.5:
                self.player.add_item("亡灵的记忆", 1)
                self.add_message("亡灵向你透露了一些秘密，获得了亡灵的记忆！", 'success')
            else:
                self.add_message("亡灵似乎有太多的怨恨，不愿意与你交流。", 'info')
        
        elif action == "参加拍卖":
            if self.player.gold >= 50:
                self.player.gold -= 50
                item = random.choice(["稀有商品", "魔法水晶", "飞行药水"])
                self.player.add_item(item, 1)
                self.add_message(f"你在拍卖会上拍到了 {item}，花费了50金币。", 'success')
            else:
                self.add_message("你没有足够的金币参加拍卖。", 'warning')
        
        elif action == "走私交易":
            if random.random() < 0.7:
                self.player.gold += random.randint(50, 150)
                self.add_message("走私交易成功，获得了丰厚的利润！", 'success')
            else:
                self.player.gold = max(0, self.player.gold - 30)
                self.add_message("交易被守卫发现了，你不得不交出一部分金币才得以脱身。", 'error')
        
        elif action == "寻找稀有商品":
            if random.random() < 0.4:
                rare_item = random.choice(["异世界物品", "时间碎片", "龙鳞"])
                self.player.add_item(rare_item, 1)
                self.add_message(f"你找到了极其稀有的 {rare_item}！", 'success')
            else:
                self.add_message("今天的运气不太好，没有找到特别稀有的商品。", 'info')
        
        elif action == "学习锻造":
            if random.random() < 0.6:
                self.player.add_item("矮人锻造手册", 1)
                self.add_message("矮人铁匠教会了你一些锻造技巧，获得锻造手册！", 'success')
            else:
                self.add_message("锻造比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "打造神器":
            if self.player.gold >= 100 and "稀有金属" in self.player.inventory:
                self.player.gold -= 100
                self.player.remove_item("稀有金属", 1)
                weapon = random.choice(["烈焰剑", "雷霆斧", "冰霜匕首"])
                self.player.add_item(weapon, 1)
                self.add_message(f"你成功打造了 {weapon}！", 'success')
            else:
                self.add_message("你缺少必要的材料和金币来打造神器。", 'warning')
        
        elif action == "参加锻造比赛":
            if random.random() < 0.5:
                self.player.gold += 80
                self.player.add_item("锻造大赛奖牌", 1)
                self.add_message("你在锻造比赛中获得了优胜，获得80金币和奖牌！", 'success')
            else:
                self.add_message("比赛竞争很激烈，你没有获得名次。", 'info')
        
        elif action == "与书籍对话":
            if random.random() < 0.5:
                self.player.gain_exp(random.randint(30, 60))
                self.add_message("会说话的书籍教给了你很多知识，获得经验值！", 'info')
            else:
                self.add_message("这些书籍今天似乎不太愿意交谈。", 'info')
        
        elif action == "进入书中世界":
            if random.random() < 0.4:
                self.player.add_item("书中世界的纪念品", 1)
                self.player.gain_exp(40)
                self.add_message("你在书中世界的冒险让你收获颇丰！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("书中世界的冒险充满危险，你受了一些伤。", 'error')
        
        elif action == "学习禁书知识":
            if random.random() < 0.3:
                self.player.add_item("禁书", 1)
                self.player.attack += 8
                self.add_message("禁书知识增强了你的攻击力，永久增加8点！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("禁书的黑暗力量反噬了你，受到30点伤害。", 'error')
        
        elif action == "破解机关":
            if random.random() < 0.5:
                self.player.add_item("机关图纸", 1)
                self.add_message("你成功破解了神庙机关，获得了机关图纸！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("机关触发了陷阱，你勉强逃脱但受了伤。", 'error')
        
        elif action == "寻找宝藏":
            if random.random() < 0.2:
                self.player.gold += random.randint(200, 500)
                self.player.add_item("神秘宝物", 1)
                self.add_message("你找到了传说中的宝藏！获得大量金币和神秘宝物！", 'success')
                self.unlock_achievement("宝藏猎人")
            else:
                self.add_message("你搜索了很久，但宝藏似乎被藏在了更隐蔽的地方。", 'info')
        
        elif action == "接受神的试炼":
            if self.player.level >= 15:
                self.player.gain_exp(100)
                self.player.add_item("神的祝福", 1)
                self.add_message("你通过了神的试炼，获得100点经验值和神的祝福！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 50)
                self.add_message("试炼太困难了，你失败了并受到了严重的伤害。", 'error')
        
        elif action == "接受龙的试炼":
            if self.player.level >= 30:
                self.player.add_item("龙骑士徽章", 1)
                self.player.attack += 10
                self.player.defense += 5
                self.add_message("你通过了龙的试炼，成为了一名龙骑士！攻击+10，防御+5！", 'success')
                self.unlock_achievement("龙骑士")
            else:
                self.player.hp = max(1, self.player.hp - 60)
                self.add_message("龙的试炼极其危险，你被龙焰烧伤，受到60点伤害。", 'error')
        
        elif action == "学习龙语":
            if random.random() < 0.4:
                self.player.add_item("龙语词典", 1)
                self.add_message("你学会了基础的龙语，获得龙语词典！", 'success')
            else:
                self.add_message("龙语比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "与龙签订契约":
            if random.random() < 0.1:
                self.player.add_item("龙伙伴", 1)
                self.add_message("你成功与一条龙签订了契约，获得了龙伙伴！", 'success')
                self.unlock_achievement("驯龙高手")
            else:
                self.add_message("龙对你的实力还不够认可，拒绝了契约请求。", 'info')
        
        elif action == "发明创造":
            if random.random() < 0.5:
                invention = random.choice(["机械宠物", "蒸汽引擎", "自动装置"])
                self.player.add_item(invention, 1)
                self.add_message(f"你的发明成功了！创造了 {invention}！", 'success')
            else:
                self.add_message("发明过程中出现了一些小问题，这次尝试失败了。", 'info')
        
        elif action == "改造机械":
            if "机械零件" in self.player.inventory:
                self.player.remove_item("机械零件", 1)
                self.player.add_item("强化机械装置", 1)
                self.add_message("你成功改造了机械装置，使其更加强大！", 'success')
            else:
                self.add_message("你缺少改造所需的机械零件。", 'warning')
        
        elif action == "参加科学竞赛":
            if random.random() < 0.4:
                self.player.gold += 120
                self.player.add_item("科学奖杯", 1)
                self.add_message("你在科学竞赛中获得了冠军，获得120金币和奖杯！", 'success')
            else:
                self.add_message("竞赛中高手如云，你没有获得名次。", 'info')
        
        elif action == "采集毒草":
            if random.random() < 0.6:
                self.player.add_item("毒草", random.randint(1, 3))
                self.add_message("你成功采集了一些毒草！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 15)
                self.add_message("你不小心被毒草划伤，中毒了，受到15点伤害。", 'error')
        
        elif action == "制作毒药":
            if "毒草" in self.player.inventory:
                self.player.remove_item("毒草", 1)
                self.player.add_item("强力毒药", 1)
                self.add_message("你成功制作了一瓶强力毒药！", 'success')
            else:
                self.add_message("你需要毒草才能制作毒药。", 'warning')
        
        elif action == "参加园艺比赛":
            if random.random() < 0.5:
                self.player.gold += 60
                self.player.add_item("园艺大师证书", 1)
                self.add_message("你在园艺比赛中表现出色，获得60金币和证书！", 'success')
            else:
                self.add_message("其他参赛者的作品更加出色，你没有获得名次。", 'info')
        
        elif action == "观测星空":
            if random.random() < 0.5:
                self.player.add_item("星象图", 1)
                self.add_message("你观测到了一些特殊的星象，记录在了星象图上！", 'success')
            else:
                self.add_message("今天的天气不太好，看不到太多星星。", 'info')
        
        elif action == "占卜命运":
            if random.random() < 0.4:
                self.player.add_item("命运水晶", 1)
                self.add_message("占卜结果显示你的命运将会非常精彩，获得命运水晶！", 'success')
            else:
                self.add_message("占卜结果有些模糊，需要更多的信息才能确定。", 'info')
        
        elif action == "穿越时空":
            if random.random() < 0.3:
                self.player.gain_exp(100)
                self.player.add_item("时空碎片", 1)
                self.add_message("时空穿越让你获得了宝贵的经验，获得100点经验值和时空碎片！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 40)
                self.add_message("时空穿越过程中出现了异常，你受到了时空乱流的伤害。", 'error')
        
        elif action == "学习黑魔法":
            if random.random() < 0.4:
                self.player.add_item("黑暗法术书", 1)
                self.player.attack += 7
                self.add_message("你学会了强大的黑魔法，攻击永久增加7点！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("黑魔法的学习过程充满危险，你受到了黑暗能量的反噬。", 'error')
        
        elif action == "参加黑暗仪式":
            if random.random() < 0.3:
                self.player.add_item("黑暗祭坛", 1)
                self.add_message("黑暗仪式增强了你的力量，获得黑暗祭坛！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 35)
                self.add_message("仪式过程中出现了意外，你受到了黑暗力量的伤害。", 'error')
        
        elif action == "探索学院秘密":
            if random.random() < 0.2:
                self.player.add_item("学院机密卷轴", 1)
                self.add_message("你发现了学院隐藏已久的秘密，获得机密卷轴！", 'success')
            else:
                self.add_message("学院的守卫非常严密，你只能探索到一些表面的信息。", 'info')
        
        elif action == "湖中沐浴":
            if random.random() < 0.7:
                self.player.hp = self.player.max_hp
                self.add_message("湖水具有神奇的治愈力量，你的生命值完全恢复了！", 'success')
            else:
                self.add_message("今天的湖水似乎没有特别的效果，只是一次普通的沐浴。", 'info')
        
        elif action == "水晶冥想":
            if random.random() < 0.6:
                self.player.gain_exp(30)
                self.add_message("水晶冥想让你的精神得到了升华，获得30点经验值！", 'info')
            else:
                self.add_message("冥想过程中你总是分心，没有获得预期的效果。", 'info')
        
        elif action == "与精灵共舞":
            if random.random() < 0.5:
                self.player.add_item("精灵之舞的祝福", 1)
                self.add_message("精灵们欢迎你的加入，赠予你舞蹈的祝福！", 'success')
            else:
                self.add_message("精灵们似乎今天没有跳舞的心情。", 'info')
        
        elif action == "参加比赛":
            if random.random() < 0.4:
                self.player.gold += 150
                self.player.add_item("冠军奖杯", 1)
                self.add_message("你在飞行比赛中获得了冠军，获得150金币和冠军奖杯！", 'success')
                self.unlock_achievement("飞行冠军")
            else:
                self.player.gold += 20
                self.add_message("你获得了参与奖，获得20金币。", 'info')
        
        elif action == "训练飞行":
            if random.random() < 0.6:
                self.player.add_item("飞行技巧指南", 1)
                self.add_message("飞行训练提高了你的技巧，获得飞行技巧指南！", 'success')
            else:
                self.add_message("今天的训练效果不太理想，还需要更多练习。", 'info')
        
        elif action == "下注赌博":
            if self.player.gold >= 20:
                self.player.gold -= 20
                if random.random() < 0.5:
                    win_gold = random.randint(40, 100)
                    self.player.gold += win_gold
                    self.add_message(f"恭喜你赢了！获得 {win_gold} 金币！", 'success')
                else:
                    self.add_message("很遗憾，你输了这次赌博。", 'warning')
            else:
                self.add_message("你没有足够的金币进行赌博。", 'warning')
        
        elif action == "改变历史":
            if random.random() < 0.1:
                self.player.add_item("历史修改器", 1)
                self.add_message("你成功地对历史做出了微小的改变，获得历史修改器！", 'success')
                self.unlock_achievement("时间旅行者")
            else:
                self.player.hp = max(1, self.player.hp - 50)
                self.add_message("改变历史的尝试失败了，时间的反噬让你受到了严重伤害。", 'error')
        
        elif action == "预见未来":
            if random.random() < 0.4:
                self.player.add_item("未来水晶球", 1)
                self.add_message("你看到了一些未来的片段，获得未来水晶球！", 'success')
            else:
                self.add_message("未来的迷雾太浓厚了，你只能看到一些模糊的影像。", 'info')
        
        elif action == "学习精灵魔法":
            if random.random() < 0.5:
                self.player.add_item("精灵魔法书", 1)
                self.add_message("你学会了基础的精灵魔法，获得精灵魔法书！", 'success')
            else:
                self.add_message("精灵魔法比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "参加精灵舞会":
            if random.random() < 0.6:
                self.player.add_item("精灵礼服", 1)
                self.add_message("精灵们欢迎你的加入，赠予你一件精灵礼服！", 'success')
            else:
                self.add_message("精灵们今天似乎更愿意和自己的同类跳舞。", 'info')
        
        elif action == "与自然沟通":
            if random.random() < 0.5:
                self.player.add_item("自然之语", 1)
                self.add_message("你学会了与自然沟通的方法，获得自然之语！", 'success')
            else:
                self.add_message("大自然似乎今天不太愿意与你交流。", 'info')
        
        elif action == "灵魂审判":
            if random.random() < 0.3:
                self.player.add_item("审判之剑", 1)
                self.add_message("你的审判公正无私，获得了审判之剑！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("审判过程中出现了意外，你受到了灵魂的反击。", 'error')
        
        elif action == "冥界探险":
            if random.random() < 0.4:
                treasure = random.choice(["灵魂石", "冥界之火", "死亡契约"])
                self.player.add_item(treasure, 1)
                self.add_message(f"你在冥界深处发现了 {treasure}！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("冥界充满了危险，你遇到了一些不友好的亡灵。", 'error')
        
        elif action == "与亡灵交易":
            if random.random() < 0.5:
                self.player.add_item("亡灵的礼物", 1)
                self.add_message("亡灵接受了你的交易，赠予你一件神秘的礼物！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("亡灵对你的提议不感兴趣，甚至对你发起了攻击。", 'error')
        
        elif action == "制造云朵":
            if random.random() < 0.6:
                self.player.add_item("云朵精华", random.randint(1, 3))
                self.add_message("你成功制造了一些云朵，获得云朵精华！", 'success')
            else:
                self.add_message("云朵制造过程中出现了一些小问题，这次尝试失败了。", 'info')
        
        elif action == "改变天气":
            if random.random() < 0.3:
                self.player.add_item("天气控制器", 1)
                self.add_message("你成功地改变了局部天气，获得天气控制器！", 'success')
            else:
                self.add_message("天气变化比你想象的要复杂，这次尝试没有明显效果。", 'info')
        
        elif action == "乘坐云朵":
            if random.random() < 0.7:
                self.player.add_item("飞行云朵", 1)
                self.add_message("你学会了如何控制云朵飞行，获得飞行云朵！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 15)
                self.add_message("云朵突然消散了，你从空中摔了下来，受了轻伤。", 'error')
        
        elif action == "随机商品购买":
            random_items = [
                {"name": "高级治疗药水", "price": 200, "effect": "恢复满血"},
                {"name": "力量药水", "price": 300, "effect": "攻击+5"},
                {"name": "防御护符", "price": 350, "effect": "防御+5"},
                {"name": "经验水晶", "price": 400, "effect": "获得50经验值"},
                {"name": "幸运符", "price": 250, "effect": "掉落率提升"}
            ]
            
            item = random.choice(random_items)
            self.add_message(f"🎪 商人向你推荐：{item['name']} - {item['price']}金币 - {item['effect']}", 'info')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("购买", f"要购买 {item['name']} 吗？"):
                    self.player.gold -= item['price']
                    self.player.add_item(item['name'], 1)
                    self.add_message(f"购买成功！获得 {item['name']}", 'success')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        elif action == "珍品拍卖":
            rare_items = [
                {"name": "传说武器", "price": 800, "effect": "攻击+15"},
                {"name": "史诗护甲", "price": 1000, "effect": "防御+15"},
                {"name": "生命宝石", "price": 1200, "effect": "生命值+50"},
                {"name": "神圣护符", "price": 1500, "effect": "全属性+10"},
                {"name": "时光沙漏", "price": 2000, "effect": "立即升1级"}
            ]
            
            item = random.choice(rare_items)
            self.add_message(f"🏆 珍品拍卖：{item['name']} - 起拍价 {item['price']}金币 - {item['effect']}", 'info')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("竞拍", f"要出价 {item['price']} 金币竞拍 {item['name']} 吗？"):
                    if random.random() < 0.8:
                        self.player.gold -= item['price']
                        self.player.add_item(item['name'], 1)
                        self.add_message(f"竞拍成功！获得 {item['name']}", 'success')
                    else:
                        self.add_message("很遗憾，有人出价更高，你竞拍失败了。", 'warning')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        elif action == "黑市交易":
            black_market_items = [
                {"name": "诅咒之剑", "price": 500, "effect": "攻击+20，但每回合损失5点生命"},
                {"name": "灵魂石", "price": 800, "effect": "可以复活一次"},
                {"name": "黑暗水晶", "price": 600, "effect": "战斗中20%概率秒杀敌人"},
                {"name": "命运骰子", "price": 1000, "effect": "使用后随机获得或失去物品"},
                {"name": "神秘药水", "price": 300, "effect": "效果随机"}
            ]
            
            item = random.choice(black_market_items)
            self.add_message(f"🌑 黑市商人悄悄对你说：我有一些...特殊商品...", 'warning')
            self.add_message(f"🔪 商品：{item['name']} - {item['price']}金币 - {item['effect']}", 'warning')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("黑市交易", f"要进行黑市交易，购买 {item['name']} 吗？"):
                    self.player.gold -= item['price']
                    self.player.add_item(item['name'], 1)
                    self.add_message(f"交易完成！获得 {item['name']}", 'success')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        else:
            self.add_message(f"你尝试了{action}，但没有特别的事情发生。", 'info')
        
        self.update_game_time()
        self.gui.update_game_info()
    
    def handle_scene_selection(self, scene_key, scene_data):
        """处理场景选择"""
        if scene_key not in self.unlocked_scenes:
            unlock_cost = self.calculate_unlock_cost(scene_data)
            
            if self.player.gold < unlock_cost['gold']:
                self.add_message(f"金币不足！需要 {unlock_cost['gold']} 金币。", 'warning')
                return
            
            if messagebox.askyesno("解锁场景", f"确定花费 {unlock_cost['gold']} 金币解锁 {scene_data['name']} 吗？"):
                self.player.gold -= unlock_cost['gold']
                self.unlocked_scenes.add(scene_key)
                self.add_message(f"🎉 成功解锁 {scene_data['name']}！", 'success')
                
                if scene_data.get('enemies') and '暗影君主' in scene_data['enemies']:
                    self.add_message(f"⚠️  警告：这个区域包含最终Boss战！", 'warning')
                    self.add_message(f"建议等级：30+ | 建议装备：传说级", 'warning')
            else:
                return
        
        self.move_to_scene(scene_key, scene_data)
    
    def move_to_scene(self, scene_key, scene_data):
        """移动到新场景"""
        self.add_message(f"🚶‍♂️ 你前往了 {scene_data['name']}", 'info')
        self.add_message(f"📜 {scene_data['description']}", 'info')
        
        hours_spent = random.randint(1, 3)
        self.game_time += datetime.timedelta(hours=hours_spent)
        self.add_message(f"⏰ 花费了 {hours_spent} 小时", 'info')
        
        self.current_scene = scene_key
        
        if random.random() < 0.3 and scene_data['events']:
            event = random.choice(scene_data['events'])
            self.trigger_event(event)
        
        # 解锁成就
        if scene_key == "forest":
            self.unlock_achievement("森林探索者")
        elif scene_key == "cave":
            self.unlock_achievement("洞穴探险者")
        elif scene_key == "town":
            self.unlock_achievement("城镇朋友")
        elif scene_key == "wilderness":
            self.unlock_achievement("荒野求生")
        elif scene_key == "castle":
            self.unlock_achievement("城堡勇者")
        elif scene_key == "dungeon":
            self.unlock_achievement("地牢英雄")
        elif scene_key == "ice_cave":
            self.unlock_achievement("冰洞探索者")
        elif scene_key == "enchanted_forest":
            self.unlock_achievement("魔法森林使者")
        elif scene_key == "sky_city":
            self.unlock_achievement("天空之城访客")
        elif scene_key == "underwater_city":
            self.unlock_achievement("深海探索者")
        elif scene_key == "ghost_town":
            self.unlock_achievement("幽灵镇勇者")
        elif scene_key == "floating_island":
            self.unlock_achievement("浮空岛探险家")
        elif scene_key == "dwarven_mine":
            self.unlock_achievement("矮人矿坑挖掘者")
        elif scene_key == "ancient_library":
            self.unlock_achievement("知识追寻者")
        elif scene_key == "desert_oasis":
            self.unlock_achievement("沙漠绿洲发现者")
        elif scene_key == "dragon_lair":
            self.unlock_achievement("龙穴勇者")
        elif scene_key == "mechanical_city":
            self.unlock_achievement("机械都市访客")
        elif scene_key == "poison_marsh":
            self.unlock_achievement("毒沼幸存者")
        elif scene_key == "celestial_garden":
            self.unlock_achievement("天空园丁")
        elif scene_key == "shadow_realm":
            self.unlock_achievement("暗影界行者")
        elif scene_key == "crystal_cavern":
            self.unlock_achievement("水晶洞穴探索者")
        elif scene_key == "sky_pirates_ship":
            self.unlock_achievement("天空海盗")
        elif scene_key == "time_shrine":
            self.unlock_achievement("时光旅行者")
        elif scene_key == "fairy_kingdom":
            self.unlock_achievement("精灵王国使者")
        elif scene_key == "underworld":
            self.unlock_achievement("冥界访客")
        elif scene_key == "cloud_village":
            self.unlock_achievement("云中村民")
        
        if not hasattr(self, 'visited_scenes'):
            self.visited_scenes = set()
        self.visited_scenes.add(scene_key)
        
        if len(self.visited_scenes) == len(self.scenes):
            self.unlock_achievement("冒险家")
        
        self.gui.update_scene_display()
        self.gui.update_game_info()
    
    def calculate_unlock_cost(self, scene_data):
        """计算场景解锁成本"""
        gold_cost = scene_data.get('required_gold', 0)
        
        difficulty_multiplier = {
            'easy': 0.8,
            'normal': 1.0,
            'hard': 1.2,
            'extreme': 1.5,
            'ultimate': 2.0
        }.get(self.config['difficulty'], 1.0)
        
        return {'gold': int(gold_cost * difficulty_multiplier)}
    
    def get_save_files(self):
        """获取所有存档文件"""
        saves = []
        
        try:
            if not os.path.exists(self.saves_dir):
                os.makedirs(self.saves_dir)
            
            for file in os.listdir(self.saves_dir):
                if file.startswith("save_"):
                    file_path = os.path.join(self.saves_dir, file)
                    try:
                        with open(file_path, 'r') as f:
                            first_line = f.readline().strip()
                            if "RETRO RPG SAVE FILE" in first_line:
                                timestamp = "未知"
                                player_name = "未知角色"
                                
                                for line in f:
                                    line = line.strip()
                                    if line.startswith("TIMESTAMP:"):
                                        timestamp = line.split(":", 1)[1].strip()
                                    elif line.startswith("NAME:"):
                                        player_name = line.split(":", 1)[1].strip()
                                
                                try:
                                    date_obj = datetime.datetime.fromisoformat(timestamp)
                                    date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S")
                                except:
                                    date_str = timestamp
                                
                                saves.append({
                                    "file": file,
                                    "name": f"{player_name}",
                                    "date": date_str
                                })
                    except:
                        continue
            
            saves.sort(key=lambda x: x['date'], reverse=True)
            
        except Exception as e:
            print(f"读取存档列表失败: {e}")
        
        return saves
    
    def save_game(self, slot=None):
        """保存游戏"""
        if not self.player:
            return False
        
        if slot is not None:
            save_name = f"save_slot_{slot}"
        else:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"save_{timestamp}"
        
        save_path = os.path.join(self.saves_dir, save_name)
        
        try:
            with open(save_path, 'w') as f:
                f.write("=== RETRO RPG SAVE FILE ===\n")
                f.write(f"VERSION: 1.0\n")
                f.write(f"TIMESTAMP: {datetime.datetime.now().isoformat()}\n")
                f.write("\n=== PLAYER DATA ===\n")
                f.write(f"NAME: {self.player.name}\n")
                f.write(f"LEVEL: {self.player.level}\n")
                f.write(f"EXP: {self.player.exp}\n")
                f.write(f"HP: {self.player.hp}\n")
                f.write(f"MAX_HP: {self.player.max_hp}\n")
                f.write(f"ATTACK: {self.player.attack}\n")
                f.write(f"DEFENSE: {self.player.defense}\n")
                f.write(f"GOLD: {self.player.gold}\n")
                f.write(f"MAGIC_AFFINITY: {self.player.magic_affinity}\n")
                f.write(f"MAGIC_POWER: {self.player.magic_power}\n")
                
                f.write("\n=== INVENTORY ===\n")
                for item, quantity in self.player.inventory.items():
                    f.write(f"{item}:{quantity}\n")
                
                f.write("\n=== EQUIPPED ===\n")
                for slot, item in self.player.equipped.items():
                    if item:
                        f.write(f"{slot}:{item}\n")
                
                f.write("\n=== GAME STATE ===\n")
                f.write(f"CURRENT_SCENE: {self.current_scene}\n")
                f.write(f"GAME_TIME: {self.game_time.isoformat()}\n")
                f.write(f"DAY_COUNT: {self.day_count}\n")
                
                f.write("\n=== ACHIEVEMENTS ===\n")
                for achievement in self.achievements:
                    f.write(f"{achievement}\n")
                
                f.write("\n=== QUESTS ===\n")
                for quest_name, quest_data in self.quests.items():
                    f.write(f"QUEST:{quest_name}\n")
                    for key, value in quest_data.items():
                        if key == 'target':
                            f.write(f"TARGET:{str(value)}\n")
                        elif key == 'reward':
                            f.write(f"REWARD:{str(value)}\n")
                        else:
                            f.write(f"{key.upper()}:{value}\n")
                    f.write("---\n")
            
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
    
    def load_save_game(self, save_file):
        """从文件加载游戏"""
        try:
            save_path = os.path.join(self.saves_dir, save_file)
            
            with open(save_path, 'r') as f:
                lines = f.readlines()
            
            save_data = {
                "player": {},
                "game_state": {},
                "quests": {},
                "version": "1.0"
            }
            
            current_section = None
            current_quest = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith("==="):
                    if "PLAYER DATA" in line:
                        current_section = "player"
                    elif "INVENTORY" in line:
                        current_section = "inventory"
                        save_data["player"]["inventory"] = {}
                    elif "EQUIPPED" in line:
                        current_section = "equipped"
                        save_data["player"]["equipped"] = {"weapon": None, "armor": None, "accessory": None}
                    elif "GAME STATE" in line:
                        current_section = "game_state"
                    elif "ACHIEVEMENTS" in line:
                        current_section = "achievements"
                        save_data["game_state"]["achievements"] = []
                    elif "QUESTS" in line:
                        current_section = "quests"
                    continue
                
                if current_section == "player":
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key in ["level", "exp", "hp", "max_hp", "attack", "defense", "gold", "magic_power"]:
                            save_data["player"][key] = int(value)
                        else:
                            save_data["player"][key] = value
                
                elif current_section == "inventory":
                    if ":" in line:
                        item, quantity = line.split(":", 1)
                        save_data["player"]["inventory"][item.strip()] = int(quantity.strip())
                
                elif current_section == "equipped":
                    if ":" in line:
                        slot, item = line.split(":", 1)
                        save_data["player"]["equipped"][slot.strip()] = item.strip() if item.strip() else None
                
                elif current_section == "game_state":
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == "day_count":
                            save_data["game_state"][key] = int(value)
                        else:
                            save_data["game_state"][key] = value
                
                elif current_section == "achievements":
                    save_data["game_state"]["achievements"].append(line)
                
                elif current_section == "quests":
                    if line.startswith("QUEST:"):
                        current_quest = line[6:].strip()
                        save_data["quests"][current_quest] = {}
                    elif line == "---":
                        current_quest = None
                    elif current_quest and ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower()
                        value = value.strip()
                        
                        if key == "target":
                            save_data["quests"][current_quest][key] = eval(value)
                        elif key == "reward":
                            save_data["quests"][current_quest][key] = eval(value)
                        elif key in ["status", "type", "description"]:
                            save_data["quests"][current_quest][key] = value
            
            self.player = Player(
                save_data["player"]["name"],
                save_data["player"]["max_hp"],
                save_data["player"]["attack"],
                save_data["player"]["defense"]
            )
            self.player.level = save_data["player"]["level"]
            self.player.exp = save_data["player"]["exp"]
            self.player.hp = save_data["player"]["hp"]
            self.player.gold = save_data["player"]["gold"]
            self.player.inventory = save_data["player"]["inventory"]
            self.player.equipped = save_data["player"]["equipped"]
            self.player.magic_affinity = save_data["player"]["magic_affinity"]
            self.player.magic_power = save_data["player"]["magic_power"]
            
            self.current_scene = save_data["game_state"]["current_scene"]
            self.game_time = datetime.datetime.fromisoformat(save_data["game_state"]["game_time"])
            self.day_count = save_data["game_state"]["day_count"]
            self.achievements = set(save_data["game_state"]["achievements"])
            self.quests = save_data["quests"]
            
            return True
            
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def update_quest_progress(self, target, quantity):
        """更新任务进度"""
        for quest_name, quest_data in self.quests.items():
            if quest_data['status'] == 'active' and 'target' in quest_data:
                if target in quest_data['target']:
                    if target in self.player.inventory:
                        current = self.player.inventory[target]
                        required = quest_data['target'][target]
                        
                        if current >= required:
                            self.add_message(f"🎉 任务进度更新: {quest_name}", 'success')
                            self.add_message(f"你已经收集了足够的 {target}！", 'success')
    
    def is_quest_completable(self, quest_data):
        """检查任务是否可完成"""
        if 'target' not in quest_data:
            return False
        
        for target, required in quest_data['target'].items():
            if target in self.player.inventory:
                if self.player.inventory[target] < required:
                    return False
            else:
                return False
        
        return True
    
    def format_reward(self, reward):
        """格式化奖励信息"""
        parts = []
        
        if 'exp' in reward:
            parts.append(f"{reward['exp']} 经验值")
        if 'gold' in reward:
            parts.append(f"{reward['gold']} 金币")
        if 'items' in reward:
            parts.append(f"物品: {', '.join(reward['items'])}")
        
        return ", ".join(parts)
    
    def unlock_achievement(self, achievement_name):
        """解锁成就"""
        if achievement_name in self.achievements_list and achievement_name not in self.achievements:
            self.achievements.add(achievement_name)
            self.add_message(f"🏆 成就解锁: {achievement_name}！", 'gold')
            return True
        return False


class Player:
    """玩家类，管理角色属性和状态"""
    
    def __init__(self, name, hp, attack, defense):
        """初始化玩家角色"""
        self.name = name
        self.level = 1
        self.exp = 0
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.gold = 50
        self.inventory = {}
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        self.magic_affinity = None
        self.magic_power = 0
        self.magic_exp = 0
        self.magic_level = 1
        self.fragment = 0
        
        self.magic_config = {
            "fire": {
                "name": "火属性",
                "base_damage": 10,
                "growth_rate": 1.2,
                "description": "造成高额单体伤害",
                "effect": "燃烧：每回合额外造成10%伤害，持续3回合"
            },
            "water": {
                "name": "水属性",
                "base_damage": 8,
                "growth_rate": 1.1,
                "description": "降低敌人攻击力",
                "effect": "冰冻：有20%概率冻结敌人一回合"
            },
            "wind": {
                "name": "风属性",
                "base_damage": 7,
                "growth_rate": 1.0,
                "description": "增加自身闪避",
                "effect": "旋风：攻击所有敌人，伤害为单体的60%"
            },
            "earth": {
                "name": "土属性",
                "base_damage": 6,
                "growth_rate": 0.9,
                "description": "增加自身防御力",
                "effect": "石化：有15%概率使敌人防御降低20%"
            },
            "light": {
                "name": "光属性",
                "base_damage": 9,
                "growth_rate": 1.15,
                "description": "对黑暗系敌人有加成",
                "effect": "净化：有30%概率清除负面效果"
            },
            "dark": {
                "name": "暗属性",
                "base_damage": 11,
                "growth_rate": 1.25,
                "description": "高风险高回报",
                "effect": "诅咒：有25%概率使敌人每回合损失5%生命值"
            }
        }
    
    def exp_to_next_level(self):
        """计算升级所需经验值"""
        return self.level * 100
    
    def gain_exp(self, amount):
        """获得经验值"""
        self.exp += amount
        
        if amount >= 10:
            exp_bonus = amount // 10
            for _ in range(exp_bonus):
                hp_increase = random.randint(1, 3)
                attack_increase = random.randint(0, 2)
                defense_increase = random.randint(0, 2)
                
                self.max_hp += hp_increase
                self.attack += attack_increase
                self.defense += defense_increase
                
                increases = []
                if hp_increase > 0:
                    increases.append(f"生命值+{hp_increase}")
                if attack_increase > 0:
                    increases.append(f"攻击+{attack_increase}")
                if defense_increase > 0:
                    increases.append(f"防御+{defense_increase}")
                if game and increases:
                    game.add_message(f"💪 经验奖励：{', '.join(increases)}！", 'info')
        
        while self.exp >= self.exp_to_next_level():
            self.level_up()
    
    def gain_magic_exp(self, amount):
        """获得魔法经验"""
        if self.magic_affinity:
            self.magic_exp += amount
            
            while self.magic_exp >= self.magic_exp_to_next_level():
                self.magic_level_up()
    
    def magic_exp_to_next_level(self):
        """计算魔法升级所需经验"""
        return self.magic_level * 200
    
    def magic_level_up(self):
        """魔法升级"""
        self.magic_level += 1
        self.magic_exp -= self.magic_exp_to_next_level() - 200
        self.magic_power += 5
        
        config = self.magic_config[self.magic_affinity]
        if game:
            game.add_message(f"\n✨ 魔法升级！{config['name']}等级提升到 {self.magic_level}！", 'success')
            game.add_message(f"🔮 魔法强度增加到 {self.magic_power}！", 'info')
    
    def calculate_magic_damage(self, enemy_type=None):
        """计算魔法伤害"""
        if not self.magic_affinity:
            return 0
        
        config = self.magic_config[self.magic_affinity]
        base_damage = config['base_damage']
        magic_power_int = int(self.magic_power)
        
        damage = base_damage + magic_power_int
        damage *= (1 + (self.magic_level - 1) * 0.1)
        
        if enemy_type:
            if (self.magic_affinity == "light" and enemy_type == "dark") or \
               (self.magic_affinity == "dark" and enemy_type == "light"):
                damage *= 1.5
                if game:
                    game.add_message(f"✨ 属系克制！伤害提升50%！", 'success')
        
        return int(damage)
    
    def level_up(self):
        """角色升级"""
        self.level += 1
        self.exp -= self.exp_to_next_level() - 100
        
        hp_increase = random.randint(5, 15)
        attack_increase = random.randint(2, 5)
        defense_increase = random.randint(1, 4)
        
        self.max_hp += hp_increase
        self.hp = self.max_hp
        self.attack += attack_increase
        self.defense += defense_increase
        
        if game:
            game.add_message(f"\n🎉 {self.name} 升级了！现在是 {self.level} 级！", 'success')
            game.add_message(f"生命值 +{hp_increase}, 攻击力 +{attack_increase}, 防御力 +{defense_increase}", 'info')
        
        if self.level >= 20 and game:
            game.unlock_achievement("等级达人")
    
    def add_item(self, item_name, quantity=1):
        """添加物品到背包"""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
        
        unique_items = len(self.inventory)
        if unique_items >= 50 and game:
            game.unlock_achievement("收集家")
    
    def remove_item(self, item_name, quantity=1):
        """从背包移除物品"""
        if item_name in self.inventory:
            self.inventory[item_name] -= quantity
            
            if self.inventory[item_name] <= 0:
                del self.inventory[item_name]
    
    def use_item(self, item_name):
        """使用物品"""
        if item_name in self.inventory and self.inventory[item_name] > 0:
            self.remove_item(item_name, 1)
            return True
        return False


# 创建全局game变量，供Player类使用
game = None

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = GameGUI(root)
        game = app.game  # 设置全局game变量
        root.mainloop()
    except Exception as e:
        print(f"游戏发生错误: {e}")
        input("按回车键退出...")