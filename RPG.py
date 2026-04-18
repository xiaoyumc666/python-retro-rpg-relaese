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
import json
import base64
import hashlib
import zlib

class GameGUI:
    """游戏主GUI类，管理所有图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Retro_RPG")
        # 强制设置为1920x1080全屏
        self.root.attributes("-fullscreen",True)
        self.root.resizable(True, True)
        
        # 设置图标（如果有的话）
        #self.root.iconbitmap("icon.ico")
        
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
        
        # 绑定键盘事件
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # 加载自定义字体
        self.title_font = ('Arial', 24,'bold')
        self.header_font = ('Arial', 16, 'bold')
        self.normal_font = ('Arial', 12)
        self.small_font = ('Arial', 10)
        
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
            text="Retro_RPG",
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
        
        # 体力值进度条
        self.stamina_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.stamina_frame.pack(fill='x', padx=5, pady=2)
        
        self.stamina_label = tk.Label(
            self.stamina_frame,
            text="体力:",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.stamina_label.pack(side='left')
        
        self.stamina_progress = ttk.Progressbar(
            self.stamina_frame,
            length=150,
            mode='determinate',
            style='green.Horizontal.TProgressbar'
        )
        self.stamina_progress.pack(side='left', padx=5)
        
        # 体力恢复按钮和数值显示
        self.stamina_control_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.stamina_control_frame.pack(fill='x', padx=5, pady=2)
        
        # 体力数值显示
        self.stamina_display_label = tk.Label(
            self.stamina_control_frame,
            text="体力: 50/50",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.stamina_display_label.pack(side='left', padx=10)
        
        self.recover_stamina_btn = tk.Button(
            self.stamina_control_frame,
            text="恢复体力",
            command=self.recover_stamina,
            font=self.small_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=8
        )
        self.recover_stamina_btn.pack(side='left', padx=5)
        
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
        
        # HP数值显示
        self.hp_display_label = tk.Label(
            self.player_info_frame,
            text="HP: 0/0",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.hp_display_label.pack(anchor='w', padx=10, pady=1)
        
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
        
        # EXP数值显示
        self.exp_display_label = tk.Label(
            self.player_info_frame,
            text="EXP: 0/100",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.exp_display_label.pack(anchor='w', padx=10, pady=1)
        
        # 属性信息
        self.attrs_frame = tk.Frame(self.player_info_frame, bg=self.colors['bg'])
        self.attrs_frame.pack(fill='x', padx=5, pady=2)
        
        self.attack_label = tk.Label(
            self.attrs_frame,
            text="攻击: 0",
            font=self.normal_font,  # 字大点
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.attack_label.pack(anchor='w', pady=1)  # 单分一行
        
        self.defense_label = tk.Label(
            self.attrs_frame,
            text="防御: 0",
            font=self.normal_font,  # 字大点
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        self.defense_label.pack(anchor='w', pady=1)  # 单分一行
        
        self.gold_label = tk.Label(
            self.attrs_frame,
            text="金币: 0",
            font=self.normal_font,  # 字大点
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        self.gold_label.pack(anchor='w', pady=1)  # 单分一行
        
        # 魔法攻击力
        self.magic_attack_label = tk.Label(
            self.attrs_frame,
            text="魔法: 0",
            font=self.normal_font,  # 字大点
            fg=self.colors['info'],
            bg=self.colors['bg']
        )
        self.magic_attack_label.pack(anchor='w', pady=1)  # 单分一行
        
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
            {'text': 'ℹ️ 关于游戏', 'command': self.show_about},
            {'text': '❌ 退出游戏', 'command': self.root.quit}
        ]
        
        self.create_action_buttons(buttons_config)
        
        # 加密版权信息
        import base64
        encoded_copyright = base64.b64encode(b"Copyright by xiaoyu").decode('utf-8')
        decoded_copyright = base64.b64decode(encoded_copyright).decode('utf-8')
        
        # 显示欢迎信息
        welcome_text = f"""
复古文字冒险 RPG
{decoded_copyright}

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
        self.game.player.add_item("新手剑", 1, self.game)
        self.game.player.add_item("新手药水", 2, self.game)
        self.game.player.add_item("草药", 3, self.game)
        self.game.player.add_item("空瓶", 2, self.game)
        self.game.player.add_item("铜矿石", 5, self.game)
        self.game.player.add_item("普通宝石碎片", 3, self.game)
        
        # 初始化基础装备
        self.game.player.equip_item("新手剑")
        
        # 设置初始场景
        self.game.current_scene = "forest"
        
        # 解锁初始成就
        self.game.unlock_achievement("初次冒险")
        
        # 开始游戏
        self.game.game_state = "playing"
        self.game.add_message(f"欢迎来到这个世界，{player_name}！你的冒险之旅即将开始...")
        self.game.add_message("你获得了基础的合成和锻造材料，可以去铁匠铺学习制作物品！", 'info')
        
        # 启动自动恢复体力线程
        self.game.start_stamina_recovery()
        
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
                    self.game.start_stamina_recovery()
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
        
        import_btn = tk.Button(
            button_frame,
            text="导入加密数据",
            command=lambda: self.import_encrypted_text(dialog),
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=12
        )
        import_btn.pack(side='left', padx=5)
        
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
        dialog.geometry("400x250")
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
        
        # 全屏选项
        is_fullscreen = self.root.attributes('-fullscreen')
        fullscreen_var = tk.BooleanVar(value=is_fullscreen)
        fullscreen_check = tk.Checkbutton(
            settings_frame,
            text="全屏",
            variable=fullscreen_var,
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            selectcolor=self.colors['bg'],
            activebackground=self.colors['bg']
        )
        fullscreen_check.pack(anchor='w', pady=10)
        
        # 难度选择
        difficulty_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        difficulty_frame.pack(anchor='w', pady=10)
        
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
            # 保存全屏设置
            current_fullscreen = self.root.attributes('-fullscreen')
            if fullscreen_var.get() != current_fullscreen:
                self.root.attributes('-fullscreen', fullscreen_var.get())
            
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
    
    def show_about(self):
        """显示关于游戏信息"""
        # 创建关于游戏对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("关于游戏")
        dialog.geometry("800x600")
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
            text="关于 Retro_RPG",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 游戏介绍
        about_text = tk.Text(
            dialog,
            wrap=tk.WORD,
            font=self.normal_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            height=25,
            width=90
        )
        about_text.pack(padx=10, pady=5, fill='both', expand=True)
        
        about_content = """
Retro_RPG 是一款复古风格的文字冒险角色扮演游戏，融合了经典 RPG 元素与现代游戏设计理念。

游戏背景设定在一个充满奇幻色彩的世界，玩家将扮演一名勇敢的冒险者，踏上一段充满挑战与机遇的旅程。在这个世界中，你将遇到各种各样的敌人、NPC 和任务，通过不断提升自己的实力来探索这个神秘的世界。

游戏特色：

1. 丰富的角色系统：玩家可以选择不同的职业，每个职业都有独特的技能和发展方向。通过升级和装备，你可以打造属于自己的强力角色。

2. 多样化的战斗系统：游戏采用回合制战斗系统，结合了物理攻击、魔法攻击和宠物辅助，让战斗充满策略性。

3. 庞大的世界地图：游戏世界由多个区域组成，每个区域都有独特的敌人、任务和隐藏宝藏等待你去发现。

4. 宠物系统：你可以捕获各种怪物作为宠物，它们将在战斗中为你提供帮助。最多可以同时拥有3只宠物并肩作战。

5. 图鉴系统：记录你在游戏中遇到的敌人、收集的物品和解锁的成就，完成图鉴可以获得丰厚的奖励。

6. 制作系统：通过收集材料，你可以合成各种物品、锻造强力装备和镶嵌宝石来提升装备属性。

7. 经济系统：游戏中有完整的经济体系，你可以通过完成任务、战斗和投资来积累财富。

8. 成就系统：游戏包含大量成就，完成这些成就可以获得特殊奖励和荣誉。

9. 多人互动：你可以与其他玩家组队冒险，共同挑战强大的敌人。

10. 护送任务：保护重要 NPC 安全到达目的地，考验你的战斗技巧和策略。

游戏操作简单直观，通过鼠标点击即可完成大部分操作。游戏界面采用复古风格，营造出经典 RPG 的氛围，同时加入了现代游戏的便利性。

Retro_RPG 不仅仅是一款游戏，更是一段充满回忆和乐趣的冒险之旅。无论你是 RPG 游戏的资深玩家，还是初次接触这类游戏的新手，都能在其中找到属于自己的乐趣。

加入我们，开始你的冒险之旅吧！

版本信息：
- 当前版本：2.3.3
- 开发团队：xiaoyu
- 发布日期：2026-04-04
- 游戏类型：角色扮演、文字冒险
- 适用平台：Windows

游戏理念：
我们希望通过 Retro_RPG 带给玩家纯粹的游戏乐趣，回归 RPG 游戏的本质——探索、成长和故事。在这个快节奏的时代，我们希望玩家能够静下心来，享受一段属于自己的奇幻冒险。

感谢所有支持和喜欢 Retro_RPG 的玩家，你们的反馈是我们不断进步的动力。

祝您游戏愉快！
        """
        
        about_text.insert('1.0', about_content)
        about_text.config(state='disabled')
        
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
    
    def toggle_fullscreen(self, event=None):
        """切换全屏模式"""
        current_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_fullscreen)
    
    def exit_fullscreen(self, event=None):
        """退出全屏模式"""
        self.root.attributes("-fullscreen", False)
    
    def show_compendium(self):
        """显示图鉴系统"""
        dialog = tk.Toplevel(self.root)
        dialog.title("图鉴系统")
        dialog.geometry("800x600")
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
            text="图鉴系统",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 完成度显示
        completion = self.game.compendium['completion']
        completion_label = tk.Label(
            dialog,
            text=f"总完成度: {completion['total']:.1f}% | 敌人: {completion['enemies']:.1f}% | 物品: {completion['items']:.1f}% | 成就: {completion['achievements']:.1f}%",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        completion_label.pack(pady=5)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # ========== 敌人图鉴页面 ==========
        enemies_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(enemies_frame, text="敌人图鉴")
        
        if not self.game.compendium['enemies']:
            empty_label = tk.Label(
                enemies_frame,
                text="你还没有击败任何敌人",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            # 设置Canvas高度，确保滚动区域正常工作
            canvas = tk.Canvas(enemies_frame, bg='#1e1e1e', highlightthickness=0, height=400)
            scrollbar = tk.Scrollbar(enemies_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 添加鼠标滚轮支持
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            canvas.bind("<MouseWheel>", on_mouse_wheel)
            enemies_frame.bind("<MouseWheel>", on_mouse_wheel)
            
            # 创建一个容器框架来容纳敌人条目，一行显示四个
            enemies_container = tk.Frame(scrollable_frame, bg='#1e1e1e')
            enemies_container.pack(fill='both', expand=True)
            
            # 计算位置
            row = 0
            col = 0
            
            for enemy_name, enemy_info in self.game.compendium['enemies'].items():
                enemy_frame = tk.LabelFrame(
                    enemies_container,
                    text=enemy_name,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge',
                    width=180,  # 设置固定宽度，确保一行四个
                    height=180  # 设置固定高度
                )
                enemy_frame.grid(row=row, column=col, padx=5, pady=2, sticky='nsew')
                
                # 配置网格列权重
                enemies_container.grid_columnconfigure(col, weight=1)
                
                info_text = f"等级: {enemy_info['level']}\n"
                info_text += f"生命值: {enemy_info['hp']}\n"
                info_text += f"攻击力: {enemy_info['attack']}\n"
                info_text += f"防御力: {enemy_info['defense']}\n"
                info_text += f"经验值: {enemy_info['exp']}\n"
                info_text += f"金币: {enemy_info['gold']}\n"
                info_text += f"击败次数: {enemy_info['defeated_count']}\n"
                if enemy_info['drops']:
                    # 限制掉落物品显示长度
                    drops = enemy_info['drops'][:3]  # 只显示前3个
                    info_text += f"掉落: {', '.join(drops)}"
                    if len(enemy_info['drops']) > 3:
                        info_text += "..."
                
                info_label = tk.Label(
                    enemy_frame,
                    text=info_text,
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    justify='left',
                    wraplength=160  # 设置文本换行
                )
                info_label.pack(padx=5, pady=5)
                
                # 更新行列位置
                col += 1
                if col == 4:
                    col = 0
                    row += 1
            
            # 为最后一行的列设置权重
            for c in range(col, 4):
                enemies_container.grid_columnconfigure(c, weight=1)
            
            # 强制更新scrollregion，确保所有内容都能滚动
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # ========== 物品图鉴页面 ==========
        items_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(items_frame, text="物品图鉴")
        
        if not self.game.compendium['items']:
            empty_label = tk.Label(
                items_frame,
                text="你还没有收集任何物品",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            # 设置Canvas高度，确保滚动区域正常工作
            canvas = tk.Canvas(items_frame, bg='#1e1e1e', highlightthickness=0, height=400)
            scrollbar = tk.Scrollbar(items_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 添加鼠标滚轮支持
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            canvas.bind("<MouseWheel>", on_mouse_wheel)
            items_frame.bind("<MouseWheel>", on_mouse_wheel)
            
            # 创建一个容器框架来容纳物品条目，一行显示四个
            items_container = tk.Frame(scrollable_frame, bg='#1e1e1e')
            items_container.pack(fill='both', expand=True)
            
            # 计算位置
            row = 0
            col = 0
            
            for item_name, item_info in self.game.compendium['items'].items():
                item_frame = tk.LabelFrame(
                    items_container,
                    text=item_name,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge',
                    width=180,  # 设置固定宽度，确保一行四个
                    height=180  # 设置固定高度
                )
                item_frame.grid(row=row, column=col, padx=5, pady=2, sticky='nsew')
                
                # 配置网格列权重
                items_container.grid_columnconfigure(col, weight=1)
                
                info_text = f"类型: {item_info.get('type', '未知')}\n"
                if item_info.get('description'):
                    # 限制描述长度
                    desc = item_info['description'][:50]  # 只显示前50个字符
                    info_text += f"描述: {desc}"
                    if len(item_info['description']) > 50:
                        info_text += "...\n"
                    else:
                        info_text += "\n"
                if item_info.get('effect'):
                    # 限制效果长度
                    effect = item_info['effect'][:50]  # 只显示前50个字符
                    info_text += f"效果: {effect}"
                    if len(item_info['effect']) > 50:
                        info_text += "...\n"
                    else:
                        info_text += "\n"
                info_text += f"收集数量: {item_info.get('collected_count', 0)}"
                
                info_label = tk.Label(
                    item_frame,
                    text=info_text,
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    justify='left',
                    wraplength=160  # 设置文本换行
                )
                info_label.pack(padx=5, pady=5)
                
                # 更新行列位置
                col += 1
                if col == 4:
                    col = 0
                    row += 1
            
            # 为最后一行的列设置权重
            for c in range(col, 4):
                items_container.grid_columnconfigure(c, weight=1)
            
            # 强制更新scrollregion，确保所有内容都能滚动
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # ========== 成就图鉴页面 ==========
        achievements_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(achievements_frame, text="成就图鉴")
        
        if not self.game.compendium['achievements']:
            empty_label = tk.Label(
                achievements_frame,
                text="你还没有解锁任何成就",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            # 设置Canvas高度，确保滚动区域正常工作
            canvas = tk.Canvas(achievements_frame, bg='#1e1e1e', highlightthickness=0, height=400)
            scrollbar = tk.Scrollbar(achievements_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 添加鼠标滚轮支持
            def on_mouse_wheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            canvas.bind("<MouseWheel>", on_mouse_wheel)
            achievements_frame.bind("<MouseWheel>", on_mouse_wheel)
            
            # 创建一个容器框架来容纳成就条目，一行显示四个
            achievements_container = tk.Frame(scrollable_frame, bg='#1e1e1e')
            achievements_container.pack(fill='both', expand=True)
            
            # 计算位置
            row = 0
            col = 0
            
            for achievement_name, achievement_info in self.game.compendium['achievements'].items():
                achievement_frame = tk.LabelFrame(
                    achievements_container,
                    text=achievement_name,
                    font=self.normal_font,
                    fg=self.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge',
                    width=180,  # 设置固定宽度，确保一行四个
                    height=180  # 设置固定高度
                )
                achievement_frame.grid(row=row, column=col, padx=5, pady=2, sticky='nsew')
                
                # 配置网格列权重
                achievements_container.grid_columnconfigure(col, weight=1)
                
                info_text = f"解锁日期: 第 {achievement_info['unlocked_date']} 天\n"
                # 限制描述长度
                desc = achievement_info['description'][:80]  # 只显示前80个字符
                info_text += f"描述: {desc}"
                if len(achievement_info['description']) > 80:
                    info_text += "..."
                
                info_label = tk.Label(
                    achievement_frame,
                    text=info_text,
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    justify='left',
                    wraplength=160  # 设置文本换行
                )
                info_label.pack(padx=5, pady=5)
                
                # 更新行列位置
                col += 1
                if col == 4:
                    col = 0
                    row += 1
            
            # 为最后一行的列设置权重
            for c in range(col, 4):
                achievements_container.grid_columnconfigure(c, weight=1)
            
            # 强制更新scrollregion，确保所有内容都能滚动
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            
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
        # 创建子菜单函数
        def show_character_menu():
            """显示角色相关菜单"""
            menu = tk.Toplevel(self.root)
            menu.title("角色")
            menu.geometry("300x300")
            menu.configure(bg=self.colors['bg'])
            menu.transient(self.root)
            menu.grab_set()
            
            # 居中显示
            menu.update_idletasks()
            x = (menu.winfo_screenwidth() - menu.winfo_width()) // 2
            y = (menu.winfo_screenheight() - menu.winfo_height()) // 2
            menu.geometry(f"+{x}+{y}")
            
            # 标题
            title_label = tk.Label(
                menu,
                text="角色菜单",
                font=self.header_font,
                fg=self.colors['gold'],
                bg=self.colors['bg']
            )
            title_label.pack(pady=10)
            
            # 按钮框架
            button_frame = tk.Frame(menu, bg=self.colors['bg'])
            button_frame.pack(expand=True)
            
            def wrap_command(cmd):
                def wrapped():
                    cmd()
                    menu.after(100, menu.destroy)
                return wrapped
            
            tk.Button(button_frame, text="🎒 背包", command=wrap_command(self.show_inventory), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="📊 角色状态", command=wrap_command(self.show_character_status), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="🗡️ 装备", command=wrap_command(self.show_equipment_screen), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="关闭", command=menu.destroy, font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=10)
        
        def show_world_menu():
            """显示世界相关菜单"""
            menu = tk.Toplevel(self.root)
            menu.title("世界")
            menu.geometry("300x300")
            menu.configure(bg=self.colors['bg'])
            menu.transient(self.root)
            menu.grab_set()
            
            # 居中显示
            menu.update_idletasks()
            x = (menu.winfo_screenwidth() - menu.winfo_width()) // 2
            y = (menu.winfo_screenheight() - menu.winfo_height()) // 2
            menu.geometry(f"+{x}+{y}")
            
            # 标题
            title_label = tk.Label(
                menu,
                text="世界菜单",
                font=self.header_font,
                fg=self.colors['gold'],
                bg=self.colors['bg']
            )
            title_label.pack(pady=10)
            
            # 按钮框架
            button_frame = tk.Frame(menu, bg=self.colors['bg'])
            button_frame.pack(expand=True)
            
            def wrap_command(cmd):
                def wrapped():
                    cmd()
                    menu.after(100, menu.destroy)
                return wrapped
            
            tk.Button(button_frame, text="🗺️ 地图", command=wrap_command(self.show_map), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="💬 NPC", command=wrap_command(self.interact_with_npc), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="关闭", command=menu.destroy, font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=10)
        
        def show_crafting_menu():
            """显示制作相关菜单"""
            menu = tk.Toplevel(self.root)
            menu.title("制作")
            menu.geometry("300x300")
            menu.configure(bg=self.colors['bg'])
            menu.transient(self.root)
            menu.grab_set()
            
            # 居中显示
            menu.update_idletasks()
            x = (menu.winfo_screenwidth() - menu.winfo_width()) // 2
            y = (menu.winfo_screenheight() - menu.winfo_height()) // 2
            menu.geometry(f"+{x}+{y}")
            
            # 标题
            title_label = tk.Label(
                menu,
                text="制作菜单",
                font=self.header_font,
                fg=self.colors['gold'],
                bg=self.colors['bg']
            )
            title_label.pack(pady=10)
            
            # 按钮框架
            button_frame = tk.Frame(menu, bg=self.colors['bg'])
            button_frame.pack(expand=True)
            
            def wrap_command(cmd):
                def wrapped():
                    cmd()
                    menu.after(100, menu.destroy)
                return wrapped
            
            tk.Button(button_frame, text="⚒️ 合成", command=wrap_command(self.game.show_crafting_system), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="🔨 锻造", command=wrap_command(self.game.show_smithing_system), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
            tk.Button(button_frame, text="💎 宝石", command=wrap_command(self.game.show_gem_system), font=self.normal_font, bg=self.colors['button_bg'], fg=self.colors['button_fg'], width=15, height=2).pack(pady=5)
        # 创建游戏操作按钮
        buttons_config = [
            {'text': '🔍 探索', 'command': self.explore_area},
            {'text': '💤 休息', 'command': self.rest},
            {'text': '👤 角色', 'command': show_character_menu},
            {'text': '🌍 世界', 'command': show_world_menu},
            {'text': '⚒️ 制作', 'command': show_crafting_menu},
            {'text': '📚 图鉴', 'command': self.show_compendium},
            {'text': '⚔️ 战斗', 'command': self.initiate_battle},
            {'text': '⏸️ 暂停', 'command': self.pause_game}
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
            
            # 体力值
            stamina_percent = (self.game.player.stamina / self.game.player.max_stamina) * 100
            self.stamina_progress['value'] = stamina_percent
            self.stamina_display_label.config(text=f"体力: {self.game.player.stamina}/{self.game.player.max_stamina}")
            
            # 生命值
            hp_percent = (self.game.player.hp / self.game.player.max_hp) * 100
            self.hp_progress['value'] = hp_percent
            self.hp_display_label.config(text=f"HP: {self.game.player.hp}/{self.game.player.max_hp}")
            
            # 经验值
            exp_needed = self.game.player.exp_to_next_level()
            exp_percent = (self.game.player.exp / exp_needed) * 100
            self.exp_progress['value'] = exp_percent
            self.exp_display_label.config(text=f"EXP: {self.game.player.exp}/{exp_needed}")
            
            # 属性（包括宝石加成和装备加成）
            total_attack = self.game.player.attack + self.game.player.gem_bonus_attack + self.game.player.equipment_bonus_attack
            total_defense = self.game.player.defense + self.game.player.gem_bonus_defense + self.game.player.equipment_bonus_defense
            total_magic = self.game.player.calculate_magic_damage() + self.game.player.equipment_bonus_magic
            
            self.attack_label.config(text=f"攻击: {total_attack}")
            self.defense_label.config(text=f"防御: {total_defense}")
            self.gold_label.config(text=f"金币: {self.game.player.gold}")
            self.magic_attack_label.config(text=f"魔法: {total_magic}")
            
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
        
        # 显示跟随的宠物
        if self.game.pets:
            self.scene_description.insert(
                tk.END,
                f"\n🐾 跟随你的宠物: "
            )
            for pet in self.game.pets:
                self.scene_description.insert(
                    tk.END,
                    f"{pet['name']} (等级: {pet['level']}) "
                )
    
    def add_message(self, message, tag=None):
        """添加消息到显示区域"""
        self.message_text.insert(tk.END, message + "\n", tag)
        self.message_text.see(tk.END)
        self.root.update()
    
    def recover_stamina(self):
        """恢复体力"""
        if not self.game or not self.game.player:
            return
        
        # 检查体力是否已满
        if self.game.player.stamina >= self.game.player.max_stamina:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("提示", "体力已回满！")
            return
        
        # 计算需要恢复的体力
        needed_stamina = self.game.player.max_stamina - self.game.player.stamina
        
        # 计算需要的金币（每10体力20金币，不足10体力按比例计算）
        needed_gold = (needed_stamina * 20) // 10
        if needed_stamina % 10 > 0:
            needed_gold += 20
        
        # 检查金币是否足够
        if self.game.player.gold >= needed_gold:
            # 金币足够，恢复全部体力
            self.game.player.gold -= needed_gold
            self.game.player.stamina = self.game.player.max_stamina
            self.add_message(f"花费{needed_gold}金币恢复了全部体力！", 'info')
        else:
            # 金币不足，用当前所有金币恢复尽可能多的体力
            if self.game.player.gold <= 0:
                import tkinter.messagebox as messagebox
                messagebox.showerror("错误", "金币不足！")
                return
            
            # 计算能恢复的体力
            recoverable_stamina = (self.game.player.gold * 10) // 20
            if recoverable_stamina > 0:
                self.game.player.stamina = min(self.game.player.max_stamina, self.game.player.stamina + recoverable_stamina)
                self.add_message(f"花费{self.game.player.gold}金币恢复了{recoverable_stamina}点体力！", 'info')
                self.game.player.gold = 0
            else:
                import tkinter.messagebox as messagebox
                messagebox.showerror("错误", "金币不足！")
                return
        
        self.update_game_info()
    
    def import_encrypted_text(self, parent_dialog=None):
        """导入加密文本数据"""
        import tkinter.messagebox as messagebox
        
        # 创建文本输入对话框
        input_dialog = tk.Toplevel(self.root)
        input_dialog.title("导入加密数据")
        input_dialog.geometry("500x400")
        input_dialog.configure(bg=self.colors['bg'])
        input_dialog.transient(self.root)
        input_dialog.grab_set()
        
        # 居中显示
        input_dialog.update_idletasks()
        x = (input_dialog.winfo_screenwidth() - input_dialog.winfo_width()) // 2
        y = (input_dialog.winfo_screenheight() - input_dialog.winfo_height()) // 2
        input_dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            input_dialog,
            text="请粘贴加密数据",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 提示信息
        info_label = tk.Label(
            input_dialog,
            text="将加密的存档数据粘贴到下方文本框中",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg=self.colors['bg']
        )
        info_label.pack(pady=5)
        
        # 文本输入框
        text_frame = tk.Frame(input_dialog, bg=self.colors['bg'])
        text_frame.pack(fill='x', padx=10, pady=5)
        
        text_area = tk.Text(
            text_frame,
            font=self.small_font,
            bg='#1e1e1e',
            fg=self.colors['fg'],
            wrap='word',
            height=15
        )
        text_area.pack(side='left', fill='x', expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
        scrollbar.pack(side='right', fill='y')
        text_area.config(yscrollcommand=scrollbar.set)
        
        def load_encrypted_data():
            encrypted_text = text_area.get('1.0', tk.END).strip()
            
            if not encrypted_text:
                messagebox.showerror("错误", "请输入加密数据！")
                return
            
            try:
                # 解密数据
                decrypted_data = self.game._decrypt_save_data(encrypted_text)
                
                if decrypted_data:
                    # 加载数据
                    if self.game.load_decrypted_data(decrypted_data):
                        messagebox.showinfo("成功", "数据导入成功！")
                        input_dialog.destroy()
                        if parent_dialog:
                            parent_dialog.destroy()
                        self.game.game_state = "playing"
                        self.game.start_stamina_recovery()
                        self.update_game_info()
                        self.show_game_interface()
                    else:
                        messagebox.showerror("错误", "数据加载失败！")
                else:
                    messagebox.showerror("错误", "解密数据失败！请检查数据是否正确。")
            
            except Exception as e:
                print(f"导入加密数据失败: {e}")
                messagebox.showerror("错误", f"导入失败: {str(e)}")
        
        # 按钮
        button_frame = tk.Frame(input_dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        load_btn = tk.Button(
            button_frame,
            text="加载",
            command=load_encrypted_data,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        load_btn.pack(side='left', padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="取消",
            command=input_dialog.destroy,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        cancel_btn.pack(side='left', padx=5)
    
    def clear_display(self):
        """清空显示区域"""
        self.message_text.delete('1.0', tk.END)
        self.scene_description.delete('1.0', tk.END)
    
    def explore_area(self):
        """探索当前区域"""
        if not self.game.use_stamina(1):
            return
        self.game.explore_area()
        self.update_game_info()
        self.update_scene_display()
    
    def rest(self):
        """休息恢复生命值"""
        if not self.game or not self.game.player:
            return
        
        # 检查生命值是否已满
        max_hp = self.game.player.max_hp + self.game.player.gem_bonus_hp + self.game.player.equipment_bonus_hp
        if self.game.player.hp >= max_hp:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("提示", "生命值已回满！")
            return
        
        # 恢复全部生命值
        self.game.player.hp = max_hp
        self.add_message("你休息了一会儿，恢复了全部生命值。", 'info')
        self.update_game_info()
    
    def show_equipment_screen(self):
        """显示装备界面"""
        if not self.game.player:
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("装备系统")
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
            text="装备系统",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # ========== 当前装备页面 ==========
        current_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(current_frame, text="当前装备")
        
        # 当前装备显示
        equipped_label = tk.Label(
            current_frame,
            text="当前装备",
            font=self.header_font,
            fg=self.colors['gold'],
            bg='#1e1e1e'
        )
        equipped_label.pack(pady=10)
        
        # 武器槽位
        weapon_frame = tk.LabelFrame(
            current_frame,
            text="⚔️ 武器",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg='#1e1e1e',
            relief='ridge'
        )
        weapon_frame.pack(fill='x', padx=20, pady=5)
        
        weapon_name = self.game.player.equipped.get('weapon', '无')
        weapon_item = tk.Label(
            weapon_frame,
            text=weapon_name,
            font=self.normal_font,
            fg=self.colors['success'] if weapon_name != '无' else self.colors['warning'],
            bg='#1e1e1e'
        )
        weapon_item.pack(side='left', padx=10, pady=5)
        
        if weapon_name != '无' and weapon_name in self.game.items:
            weapon_info = self.game.items[weapon_name]
            weapon_desc = tk.Label(
                weapon_frame,
                text=f"- {weapon_info.get('description', '')}",
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            weapon_desc.pack(side='left', padx=5)
        
        # 盔甲槽位
        armor_frame = tk.LabelFrame(
            current_frame,
            text="🛡️ 盔甲",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg='#1e1e1e',
            relief='ridge'
        )
        armor_frame.pack(fill='x', padx=20, pady=5)
        
        armor_name = self.game.player.equipped.get('armor', '无')
        armor_item = tk.Label(
            armor_frame,
            text=armor_name,
            font=self.normal_font,
            fg=self.colors['success'] if armor_name != '无' else self.colors['warning'],
            bg='#1e1e1e'
        )
        armor_item.pack(side='left', padx=10, pady=5)
        
        if armor_name != '无' and armor_name in self.game.items:
            armor_info = self.game.items[armor_name]
            armor_desc = tk.Label(
                armor_frame,
                text=f"- {armor_info.get('description', '')}",
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            armor_desc.pack(side='left', padx=5)
        
        # 饰品/宝石槽位
        accessory_frame = tk.LabelFrame(
            current_frame,
            text="💍 饰品/宝石",
            font=self.normal_font,
            fg=self.colors['fg'],
            bg='#1e1e1e',
            relief='ridge'
        )
        accessory_frame.pack(fill='x', padx=20, pady=5)
        
        accessory_name = self.game.player.equipped.get('accessory', '无')
        accessory_item = tk.Label(
            accessory_frame,
            text=accessory_name,
            font=self.normal_font,
            fg=self.colors['success'] if accessory_name != '无' else self.colors['warning'],
            bg='#1e1e1e'
        )
        accessory_item.pack(side='left', padx=10, pady=5)
        
        if accessory_name != '无' and accessory_name in self.game.items:
            accessory_info = self.game.items[accessory_name]
            accessory_desc = tk.Label(
                accessory_frame,
                text=f"- {accessory_info.get('description', '')}",
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            accessory_desc.pack(side='left', padx=5)
        
        # 装备加成显示
        bonus_frame = tk.LabelFrame(
            current_frame,
            text="装备加成",
            font=self.normal_font,
            fg=self.colors['gold'],
            bg='#1e1e1e',
            relief='ridge'
        )
        bonus_frame.pack(fill='x', padx=20, pady=10)
        
        bonuses = []
        if self.game.player.equipment_bonus_attack > 0:
            bonuses.append(f"攻击 +{self.game.player.equipment_bonus_attack}")
        if self.game.player.equipment_bonus_defense > 0:
            bonuses.append(f"防御 +{self.game.player.equipment_bonus_defense}")
        if self.game.player.equipment_bonus_magic > 0:
            bonuses.append(f"魔法 +{self.game.player.equipment_bonus_magic}")
        if self.game.player.equipment_bonus_hp > 0:
            bonuses.append(f"生命 +{self.game.player.equipment_bonus_hp}")
        if self.game.player.equipment_bonus_speed > 0:
            bonuses.append(f"速度 +{self.game.player.equipment_bonus_speed}")
        if self.game.player.equipment_bonus_crit > 0:
            bonuses.append(f"暴击 +{self.game.player.equipment_bonus_crit}%")
        if self.game.player.equipment_bonus_dodge > 0:
            bonuses.append(f"闪避 +{self.game.player.equipment_bonus_dodge}%")
        
        if bonuses:
            for bonus in bonuses:
                bonus_label = tk.Label(
                    bonus_frame,
                    text=f"✨ {bonus}",
                    font=self.small_font,
                    fg=self.colors['info'],
                    bg='#1e1e1e'
                )
                bonus_label.pack(anchor='w', padx=5, pady=2)
        else:
            no_bonus_label = tk.Label(
                bonus_frame,
                text="无装备加成",
                font=self.small_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            no_bonus_label.pack(pady=5)
        
        # ========== 可用武器页面 ==========
        weapons_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(weapons_frame, text="可用武器")
        
        weapons_list = []
        for item_name, quantity in self.game.player.inventory.items():
            if item_name in self.game.items and self.game.items[item_name]['type'] == 'weapon':
                weapons_list.append((item_name, quantity, self.game.items[item_name]))
        
        if not weapons_list:
            empty_label = tk.Label(
                weapons_frame,
                text="你没有任何武器",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            canvas = tk.Canvas(weapons_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(weapons_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for item_name, quantity, item_info in weapons_list:
                item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
                item_frame.pack(fill='x', padx=5, pady=2)
                
                # 物品名称和数量
                name_label = tk.Label(
                    item_frame,
                    text=f"⚔️ {item_name} x{quantity}",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    width=20,
                    anchor='w'
                )
                name_label.pack(side='left', padx=5)
                
                # 物品描述
                desc_label = tk.Label(
                    item_frame,
                    text=f"- {item_info['description']}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e'
                )
                desc_label.pack(side='left', padx=5)
                
                # 装备按钮
                if item_name == self.game.player.equipped.get('weapon'):
                    status_label = tk.Label(
                        item_frame,
                        text="✅ 已装备",
                        font=self.small_font,
                        fg=self.colors['success'],
                        bg='#1e1e1e'
                    )
                    status_label.pack(side='right', padx=5)
                else:
                    equip_btn = tk.Button(
                        item_frame,
                        text="装备",
                        command=lambda i=item_name: self.equip_item_from_screen(i, 'weapon', dialog),
                        font=self.small_font,
                        bg=self.colors['button_bg'],
                        fg=self.colors['button_fg'],
                        width=6
                    )
                    equip_btn.pack(side='right', padx=5)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # ========== 可用盔甲页面 ==========
        armors_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(armors_frame, text="可用盔甲")
        
        armors_list = []
        for item_name, quantity in self.game.player.inventory.items():
            if item_name in self.game.items and self.game.items[item_name]['type'] == 'armor':
                armors_list.append((item_name, quantity, self.game.items[item_name]))
        
        if not armors_list:
            empty_label = tk.Label(
                armors_frame,
                text="你没有任何盔甲",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            canvas = tk.Canvas(armors_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(armors_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for item_name, quantity, item_info in armors_list:
                item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
                item_frame.pack(fill='x', padx=5, pady=2)
                
                name_label = tk.Label(
                    item_frame,
                    text=f"🛡️ {item_name} x{quantity}",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    width=20,
                    anchor='w'
                )
                name_label.pack(side='left', padx=5)
                
                desc_label = tk.Label(
                    item_frame,
                    text=f"- {item_info['description']}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e'
                )
                desc_label.pack(side='left', padx=5)
                
                if item_name == self.game.player.equipped.get('armor'):
                    status_label = tk.Label(
                        item_frame,
                        text="✅ 已装备",
                        font=self.small_font,
                        fg=self.colors['success'],
                        bg='#1e1e1e'
                    )
                    status_label.pack(side='right', padx=5)
                else:
                    equip_btn = tk.Button(
                        item_frame,
                        text="装备",
                        command=lambda i=item_name: self.equip_item_from_screen(i, 'armor', dialog),
                        font=self.small_font,
                        bg=self.colors['button_bg'],
                        fg=self.colors['button_fg'],
                        width=6
                    )
                    equip_btn.pack(side='right', padx=5)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # ========== 可用饰品/宝石页面 ==========
        accessories_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(accessories_frame, text="可用饰品/宝石")
        
        accessories_list = []
        for item_name, quantity in self.game.player.inventory.items():
            if item_name in self.game.items:
                item_type = self.game.items[item_name]['type']
                if item_type in ['accessory', 'gem']:
                    accessories_list.append((item_name, quantity, self.game.items[item_name]))
        
        if not accessories_list:
            empty_label = tk.Label(
                accessories_frame,
                text="你没有任何饰品或宝石",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            canvas = tk.Canvas(accessories_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(accessories_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for item_name, quantity, item_info in accessories_list:
                item_frame = tk.Frame(scrollable_frame, bg='#1e1e1e')
                item_frame.pack(fill='x', padx=5, pady=2)
                
                icon = "💎" if item_info['type'] == 'gem' else "💍"
                name_label = tk.Label(
                    item_frame,
                    text=f"{icon} {item_name} x{quantity}",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    width=20,
                    anchor='w'
                )
                name_label.pack(side='left', padx=5)
                
                desc_label = tk.Label(
                    item_frame,
                    text=f"- {item_info['description']}",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e'
                )
                desc_label.pack(side='left', padx=5)
                
                if item_name == self.game.player.equipped.get('accessory'):
                    status_label = tk.Label(
                        item_frame,
                        text="✅ 已装备",
                        font=self.small_font,
                        fg=self.colors['success'],
                        bg='#1e1e1e'
                    )
                    status_label.pack(side='right', padx=5)
                else:
                    equip_btn = tk.Button(
                        item_frame,
                        text="装备",
                        command=lambda i=item_name: self.equip_item_from_screen(i, 'accessory', dialog),
                        font=self.small_font,
                        bg=self.colors['button_bg'],
                        fg=self.colors['button_fg'],
                        width=6
                    )
                    equip_btn.pack(side='right', padx=5)
            
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
    
    def equip_item_from_screen(self, item_name, slot, parent):
        """从装备界面装备物品"""
        if self.game.player.equip_item(item_name):
            self.add_message(f"✅ 装备了 {item_name} 到 {slot} 槽位！", 'success')
            parent.destroy()
            self.show_equipment_screen()
            self.update_game_info()
        else:
            messagebox.showerror("错误", f"无法装备 {item_name}！")
    
    def unequip_from_slot(self, slot_name, parent):
        """从装备槽卸下物品"""
        if self.game.player.unequip_from_slot(slot_name):
            self.add_message(f"📦 从{slot_name}槽位卸下了装备！", 'info')
            parent.destroy()
            self.show_equipment_screen()
            self.update_game_info()
        else:
            messagebox.showerror("错误", "卸下装备失败！")
    
    def show_inventory(self):
        """显示背包"""
        dialog = tk.Toplevel(self.root)
        dialog.title("背包")
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
            text=f"背包 - 金币: {self.game.player.gold}",
            font=self.header_font,
            fg=self.colors['gold'],
            bg=self.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 所有物品页面
        items_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(items_frame, text="所有物品")
        
        if not self.game.player.inventory:
            empty_label = tk.Label(
                items_frame,
                text="你的背包是空的。",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=20)
        else:
            canvas = tk.Canvas(items_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(items_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for item_name, quantity in sorted(self.game.player.inventory.items()):
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
                        'key': '🔑',
                        'gem': '💎'
                    }
                    icon = type_icons.get(item_type, '📦')
                    
                    # 如果是装备，显示装备按钮
                    if item_type in ['weapon', 'armor', 'accessory']:
                        if item_name == self.game.player.equipped.get(item_type):
                            equip_text = "✅ 已装备"
                            equip_color = self.colors['success']
                            equip_cmd = None
                        else:
                            equip_text = "🔨 装备"
                            equip_color = self.colors['info']
                            equip_cmd = lambda i=item_name: self.equip_item_dialog(i, dialog)
                        
                        if equip_cmd:
                            equip_btn = tk.Button(
                                item_frame,
                                text=equip_text,
                                command=equip_cmd,
                                font=self.small_font,
                                bg=equip_color,
                                fg=self.colors['button_fg'],
                                width=8
                            )
                            equip_btn.pack(side='right', padx=2)
                else:
                    description = "战利品"
                    icon = '💎'
                
                item_label = tk.Label(
                    item_frame,
                    text=f"{icon} {item_name} x{quantity}",
                    font=self.normal_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    width=20
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
    
    def equip_item_dialog(self, item_name, parent):
        """装备物品"""
        if self.game.player.equip_item(item_name):
            self.add_message(f"✅ 装备了 {item_name}！", 'success')
            parent.destroy()
            self.show_inventory()
            self.update_game_info()
        else:
            messagebox.showerror("错误", "无法装备该物品！")
    
    def unequip_item_dialog(self, item_name, parent):
        """卸下物品"""
        if self.game.player.unequip_item(item_name):
            self.add_message(f"📦 卸下了 {item_name}！", 'info')
            parent.destroy()
            self.show_inventory()
            self.update_game_info()
        else:
            messagebox.showerror("错误", "无法卸下该物品！")
    
    def get_item_effect_description(self, item_info):
        """获取物品效果的描述文字"""
        effect = item_info.get('effect', '')
        value = item_info.get('value', 0)
        
        if effect == 'heal':
            if value >= 9999:
                return "完全恢复生命值"
            return f"恢复 {value} 点生命值"
        elif effect == 'mana':
            if value >= 9999:
                return "完全恢复魔法值"
            return f"恢复 {value} 点魔法值"
        elif effect == 'exp':
            return f"获得 {value} 点经验值"
        elif effect == 'buff_attack':
            return f"临时增加 {value} 点攻击力"
        elif effect == 'buff_defense':
            return f"临时增加 {value} 点防御力"
        elif effect == 'buff_speed':
            return f"临时增加 {value} 点速度"
        elif effect == 'buff_luck':
            return f"临时增加 {value} 点幸运"
        elif effect == 'buff_magic':
            return f"临时增加 {value} 点魔法攻击力"
        elif effect == 'special':
            if '隐身' in item_info.get('description', ''):
                return "让使用者隐身，避免战斗"
            elif '解毒' in item_info.get('description', ''):
                return "解除中毒状态"
            elif '复活' in item_info.get('description', ''):
                return "战斗中复活一次"
        return item_info.get('description', '未知效果')
    
    def apply_item_effect_out_of_battle(self, item_name, item_info):
        """在非战斗状态下应用物品效果"""
        result = {
            'messages': [],
            'tag': 'success'
        }
        
        effect = item_info.get('effect', '')
        value = item_info.get('value', 0)
        
        if effect == 'heal':
            if value >= 9999:
                old_hp = self.game.player.hp
                self.game.player.hp = self.game.player.max_hp
                result['messages'].append(f"✨ 使用了 {item_name}，生命值完全恢复！ ( {old_hp} → {self.game.player.hp} )")
            else:
                old_hp = self.game.player.hp
                self.game.player.hp = min(self.game.player.max_hp, self.game.player.hp + value)
                actual_heal = self.game.player.hp - old_hp
                result['messages'].append(f"💚 使用了 {item_name}，恢复了 {actual_heal} 点生命值！")
        
        elif effect == 'exp':
            self.game.player.gain_exp(value)
            result['messages'].append(f"📚 使用了 {item_name}，获得了 {value} 点经验值！")
        
        elif effect == 'buff_attack':
            self.game.player.attack += value
            result['messages'].append(f"⚔️ 使用了 {item_name}，攻击力永久增加 {value} 点！")
        
        elif effect == 'buff_defense':
            self.game.player.defense += value
            result['messages'].append(f"🛡️ 使用了 {item_name}，防御力永久增加 {value} 点！")
        
        elif effect == 'buff_magic':
            self.game.player.equipment_bonus_magic += value
            result['messages'].append(f"🔮 使用了 {item_name}，魔法攻击力永久增加 {value} 点！")
        
        elif effect == 'buff_speed':
            self.game.player.equipment_bonus_speed += value
            result['messages'].append(f"💨 使用了 {item_name}，速度永久增加 {value} 点！")
        
        elif effect == 'buff_luck':
            self.game.player.gem_bonus_luck += value
            result['messages'].append(f"🍀 使用了 {item_name}，幸运永久增加 {value} 点！")
        
        return result
    
    def use_item_dialog(self, parent):
        """使用物品对话框"""
        parent.destroy()
        
        # 获取可用的消耗品
        usable_items = []
        for item_name, quantity in self.game.player.inventory.items():
            if item_name in self.game.items:
                item_info = self.game.items[item_name]
                if item_info['type'] == 'consumable':
                    usable_items.append((item_name, quantity, item_info))
        
        if not usable_items:
            messagebox.showinfo("提示", "没有可用的物品。")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("使用物品")
        dialog.geometry("450x350")
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
        
        for item_name, quantity, item_info in usable_items:
            effect_desc = self.get_item_effect_description(item_info)
            listbox.insert(tk.END, f"{item_name} x{quantity} - {effect_desc}")
        
        def on_use():
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                item_name = usable_items[index][0]
                item_info = usable_items[index][2]
                
                # 使用物品
                if self.game.player.use_item(item_name):
                    # 应用物品效果
                    effect_result = self.apply_item_effect_out_of_battle(item_name, item_info)
                    
                    for msg in effect_result['messages']:
                        self.add_message(msg, effect_result.get('tag', 'info'))
                    
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
        
        # 创建主画布和滚动条
        canvas = tk.Canvas(dialog, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 布局画布和滚动条
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 当窗口关闭时解除鼠标滚轮事件绑定
        def on_close():
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_close)

        # 基础属性
        info_frame = tk.Frame(scrollable_frame, bg=self.colors['bg'])
        info_frame.pack(fill='x', padx=20, pady=5)

        total_attack = self.game.player.attack + self.game.player.gem_bonus_attack + self.game.player.equipment_bonus_attack
        total_defense = self.game.player.defense + self.game.player.gem_bonus_defense + self.game.player.equipment_bonus_defense
        total_hp = self.game.player.max_hp + self.game.player.gem_bonus_hp + self.game.player.equipment_bonus_hp
        total_magic = self.game.player.calculate_magic_damage() + self.game.player.equipment_bonus_magic
        
        info_items = [
            f"等级: {self.game.player.level}",
            f"经验值: {self.game.player.exp}/{self.game.player.exp_to_next_level()}",
            f"基础生命值: {self.game.player.max_hp}",
            f"宝石加成生命: +{self.game.player.gem_bonus_hp}",
            f"装备加成生命: +{self.game.player.equipment_bonus_hp}",
            f"总生命值: {total_hp}",
            f"当前生命值: {self.game.player.hp}",
            f"基础攻击力: {self.game.player.attack}",
            f"宝石加成攻击: +{self.game.player.gem_bonus_attack}",
            f"装备加成攻击: +{self.game.player.equipment_bonus_attack}",
            f"总攻击力: {total_attack}",
            f"基础防御力: {self.game.player.defense}",
            f"宝石加成防御: +{self.game.player.gem_bonus_defense}",
            f"装备加成防御: +{self.game.player.equipment_bonus_defense}",
            f"总防御力: {total_defense}",
            f"魔法攻击力: {total_magic}",
            f"金币: {self.game.player.gold}",
            f"体力: {self.game.player.stamina}/{self.game.player.max_stamina}"
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
                scrollable_frame,
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
            scrollable_frame,
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

        # 装备加成详情
        equip_bonus_frame = tk.LabelFrame(
            scrollable_frame,
            text="装备加成详情",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        equip_bonus_frame.pack(fill='x', padx=20, pady=10)

        equip_bonuses = []
        if self.game.player.equipment_bonus_attack > 0:
            equip_bonuses.append(f"攻击 +{self.game.player.equipment_bonus_attack}")
        if self.game.player.equipment_bonus_defense > 0:
            equip_bonuses.append(f"防御 +{self.game.player.equipment_bonus_defense}")
        if self.game.player.equipment_bonus_magic > 0:
            equip_bonuses.append(f"魔法 +{self.game.player.equipment_bonus_magic}")
        if self.game.player.equipment_bonus_hp > 0:
            equip_bonuses.append(f"生命 +{self.game.player.equipment_bonus_hp}")
        if self.game.player.equipment_bonus_speed > 0:
            equip_bonuses.append(f"速度 +{self.game.player.equipment_bonus_speed}")
        if self.game.player.equipment_bonus_crit > 0:
            equip_bonuses.append(f"暴击 +{self.game.player.equipment_bonus_crit}%")
        if self.game.player.equipment_bonus_dodge > 0:
            equip_bonuses.append(f"闪避 +{self.game.player.equipment_bonus_dodge}%")

        if equip_bonuses:
            for bonus in equip_bonuses:
                label = tk.Label(
                    equip_bonus_frame,
                    text=f"✨ {bonus}",
                    font=self.normal_font,
                    fg=self.colors['info'],
                    bg=self.colors['bg'],
                    anchor='w'
                )
                label.pack(fill='x', padx=5, pady=2)
        else:
            label = tk.Label(
                equip_bonus_frame,
                text="无装备加成",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg'],
                anchor='w'
            )
            label.pack(fill='x', padx=5, pady=5)

        # 宝石加成详情
        gem_bonus_frame = tk.LabelFrame(
            scrollable_frame,
            text="宝石加成详情",
            font=self.header_font,
            fg=self.colors['fg'],
            bg=self.colors['bg'],
            relief='ridge'
        )
        gem_bonus_frame.pack(fill='x', padx=20, pady=10)

        gem_bonuses = []
        if self.game.player.gem_bonus_attack > 0:
            gem_bonuses.append(f"攻击 +{self.game.player.gem_bonus_attack}")
        if self.game.player.gem_bonus_defense > 0:
            gem_bonuses.append(f"防御 +{self.game.player.gem_bonus_defense}")
        if self.game.player.gem_bonus_hp > 0:
            gem_bonuses.append(f"生命 +{self.game.player.gem_bonus_hp}")
        if self.game.player.gem_bonus_gold > 0:
            gem_bonuses.append(f"金币掉落 +{self.game.player.gem_bonus_gold}%")
        if self.game.player.gem_bonus_exp > 0:
            gem_bonuses.append(f"经验获取 +{self.game.player.gem_bonus_exp}%")
        if self.game.player.gem_bonus_luck > 0:
            gem_bonuses.append(f"幸运 +{self.game.player.gem_bonus_luck}")
        if self.game.player.gem_bonus_speed > 0:
            gem_bonuses.append(f"速度 +{self.game.player.gem_bonus_speed}")

        if gem_bonuses:
            for bonus in gem_bonuses:
                label = tk.Label(
                    gem_bonus_frame,
                    text=f"✨ {bonus}",
                    font=self.normal_font,
                    fg=self.colors['info'],
                    bg=self.colors['bg'],
                    anchor='w'
                )
                label.pack(fill='x', padx=5, pady=2)
        else:
            label = tk.Label(
                gem_bonus_frame,
                text="无宝石加成",
                font=self.normal_font,
                fg=self.colors['fg'],
                bg=self.colors['bg'],
                anchor='w'
            )
            label.pack(fill='x', padx=5, pady=5)

        # 成就信息
        achievement_frame = tk.LabelFrame(
            scrollable_frame,
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
        def close_window():
            # 解除鼠标滚轮绑定
            canvas.unbind_all("<MouseWheel>")
            dialog.destroy()
        
        close_btn = tk.Button(
            scrollable_frame,
            text="关闭",
            command=close_window,
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
            'underground': {'name': '⛰️ 地下世界', 'scenes': []},
            'sky': {'name': '☁️ 天空领域', 'scenes': []},
            'time': {'name': '⏰ 时间维度', 'scenes': []},
            'dream': {'name': '💭 梦境维度', 'scenes': []}
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
            canvas.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            
            def bind_wheel_recursive(widget):
                widget.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
                widget.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
                widget.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
                for child in widget.winfo_children():
                    bind_wheel_recursive(child)
            
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
                scene_frame.config(width=500)  # 设置固定宽度
                
                desc_label = tk.Label(
                    scene_frame,
                    text=scene_data['description'][:100] + "...",
                    font=self.small_font,
                    fg=self.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=450  # 调整换行长度
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
                    if not self.game.use_stamina(1):
                        return
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
                    fg=self.colors['button_fg'],
                    width=10  # 设置固定宽度
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
        if not self.game.use_stamina(1):
            return
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
        dialog.geometry("500x500")
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
                    self.game.player.add_item(item, 1, self.game)
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
        if not self.game.use_stamina(1):
            return
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
            ("魔法药水", 100, "临时增加10点魔法攻击力"),
            ("面包", 15, "恢复15点生命值"),
            ("草药", 20, "恢复20点生命值"),
            ("空瓶", 10, "用于合成药水的空瓶"),
            ("铜矿石", 30, "基础锻造材料"),
            ("铁矿石", 60, "中级锻造材料"),
            ("银矿石", 100, "高级锻造材料"),
            ("金矿石", 200, "稀有锻造材料"),
            ("普通宝石碎片", 50, "基础宝石材料"),
            ("魔法宝石碎片", 150, "魔法宝石材料"),
            ("神秘宝石", 300, "稀有宝石")
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
                    self.game.player.add_item(item, 1, self.game)
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
        #if not self.game.use_stamina(1):
            #return
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
        if not self.game.use_stamina(1):
            return
        self.game.perform_unique_action(action)
        self.update_game_info()
        self.update_scene_display()
    
    def initiate_battle(self):
        """主动发起战斗"""
        scene = self.game.scenes[self.game.current_scene]
        if not scene['enemies']:
            messagebox.showinfo("提示", "这个区域没有敌人可战斗。")
            return
        
        if not self.game.use_stamina(2):
            return
        
        enemy_name = random.choice(scene['enemies'])
        self.game.start_battle(enemy_name, active_battle=True)
    
    def show_save_menu(self):
        """显示保存菜单 - 允许选择要覆盖的存档"""
        import tkinter.messagebox as messagebox
        
        # 获取所有存档
        saves = self.game.get_save_files()
        
        # 创建保存菜单对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("保存游戏")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2)
        y = (self.root.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="选择要覆盖的存档",
            font=self.title_font,
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=10)
        
        # 存档列表
        save_listbox = tk.Listbox(
            dialog,
            font=self.normal_font,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            selectbackground=self.colors['button_bg'],
            selectforeground=self.colors['button_fg'],
            width=40,
            height=10
        )
        save_listbox.pack(pady=10)
        
        # 填充存档列表
        for save in saves:
            save_listbox.insert(tk.END, f"{save['name']} - {save['date']} ({save['file']})")
        
        # 按钮框架
        button_frame = tk.Frame(dialog, bg=self.colors['bg'])
        button_frame.pack(pady=10)
        
        def on_save():
            """保存游戏到选中的存档"""
            selected_index = save_listbox.curselection()
            if selected_index:
                # 覆盖选中的存档
                selected_save = saves[selected_index[0]]
                if self.game.save_game(save_name=selected_save['file']):
                    messagebox.showinfo("成功", f"游戏已覆盖保存到 {selected_save['file']}！")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "保存失败！")
            else:
                # 创建新存档
                if self.game.save_game():
                    messagebox.showinfo("成功", "游戏已保存为新存档！")
                    dialog.destroy()
                else:
                    messagebox.showerror("错误", "保存失败！")
        
        # 保存按钮
        save_btn = tk.Button(
            button_frame,
            text="保存",
            command=on_save,
            font=self.normal_font,
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            width=10
        )
        save_btn.pack(side='left', padx=5)
        
        # 取消按钮
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
        
        # 保存并退出函数
        def save_and_exit():
            dialog.destroy()
            self.game.save_game()
            import tkinter.messagebox as messagebox
            messagebox.showinfo("提示", "游戏已保存")
            setattr(self.game, 'game_state', "menu")
            self.show_main_menu()
        
        menu_btn = tk.Button(
            button_frame,
            text="保存并退出",
            command=save_and_exit,
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
        self.current_save = None  # 当前存档文件名

        self.trades_completed = 0
        self.unlocked_scenes = {'forest', 'town'}
        
        # 组队系统
        self.teammates = []  # 队友列表
        self.max_team_size = 3  # 最大队伍人数
        self.recruitable_npcs = {}  # 可招募的NPC
        
        # 宠物系统
        self.pets = []  # 宠物列表
        self.max_pet_size = 3  # 最大宠物数量
        self.capturable_monsters = {}  # 可捕获的野怪
        
        # 排行榜系统
        self.leaderboard = {
            "local_ranking": [],  # 本地存档排名
            "combat_stats": {
                "total_kills": 0,  # 总击杀数
                "highest_damage": 0,  # 最高伤害
                "total_damage": 0,  # 总伤害
                "battles_won": 0,  # 胜利场次
                "battles_lost": 0  # 失败场次
            }
        }
        

        

        
        # 图鉴系统
        self.compendium = {
            "enemies": {},  # 敌人图鉴，键为敌人名称，值为敌人信息
            "items": {},  # 物品图鉴，键为物品名称，值为物品信息
            "achievements": {},  # 成就图鉴，键为成就ID，值为成就信息
            "completion": {
                "enemies": 0,  # 敌人图鉴完成度
                "items": 0,  # 物品图鉴完成度
                "achievements": 0,  # 成就图鉴完成度
                "total": 0  # 总完成度
            },
            "rewards": [
                {"threshold": 10, "reward": {"gold": 1000, "exp": 500, "items": []}},
                {"threshold": 25, "reward": {"gold": 2500, "exp": 1000, "items": ["治疗药水"]}},
                {"threshold": 50, "reward": {"gold": 5000, "exp": 2000, "items": ["高级治疗药水", "魔法药水"]}},
                {"threshold": 75, "reward": {"gold": 10000, "exp": 5000, "items": ["稀有装备", "高级魔法药水"]}},
                {"threshold": 100, "reward": {"gold": 20000, "exp": 10000, "items": ["传说装备", "终极药水"]}}
            ],
            "rewards_claimed": []  # 已领取的奖励
        }
        
        # 体力恢复线程标志
        self.stamina_recovery_running = False
        self.stamina_recovery_thread = None
        
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
        # 初始化可招募NPC
        self.initialize_recruitable_npcs()
        # 初始化可捕获野怪
        self.initialize_capturable_monsters()
    
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
                "enemies": ["小偷", "骗子", "强盗"],
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
            },
            
            # ========== 时间维度 (Time) ==========
            "ancient_past": {
                "name": "远古时代",
                "description": "回到遥远的过去，这里是文明的起源。",
                "enemies": ["原始人", "史前野兽", "古代巨人"],
                "items": ["石器", "古代壁画", "史前骨制品"],
                "npcs": ["原始萨满", "古代猎人", "部落首领"],
                "events": ["部落战争", "发现火", "发明工具"],
                "required_level": 25,
                "required_gold": 10000,
                "required_exp": 5000,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["学习原始技能", "参与部落仪式", "探索史前遗迹"]
            },
            "medieval_age": {
                "name": "中世纪",
                "description": "骑士与魔法的时代，城堡和骑士团的世界。",
                "enemies": ["骑士", "魔法师", "巨龙"],
                "items": ["骑士剑", "魔法卷轴", "中世纪盔甲"],
                "npcs": ["国王", "骑士团长", "宫廷魔法师"],
                "events": ["骑士比武", "魔法研究", "城堡 siege"],
                "required_level": 26,
                "required_gold": 11000,
                "required_exp": 5500,
                "time_restriction": (8, 20),
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["成为骑士", "学习魔法", "参与宫廷政治"]
            },
            "industrial_revolution": {
                "name": "工业革命",
                "description": "蒸汽机和工厂的时代，科技开始改变世界。",
                "enemies": ["工厂守卫", "机械怪兽", "工业巨头"],
                "items": ["蒸汽机零件", "工业蓝图", "机械工具"],
                "npcs": ["发明家", "工厂主", "工人领袖"],
                "events": ["机器暴动", "工人罢工", "技术革命"],
                "required_level": 27,
                "required_gold": 12000,
                "required_exp": 6000,
                "time_restriction": (6, 22),
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["发明新机器", "组织工人运动", "参观工厂"]
            },
            "future_city": {
                "name": "未来都市",
                "description": "高度发达的未来城市，充满了高科技和人工智能。",
                "enemies": ["机器人", "赛博格", "AI主宰"],
                "items": ["激光武器", "智能芯片", "未来科技"],
                "npcs": ["科学家", "AI助手", "未来人类"],
                "events": ["AI叛乱", "时空旅行", "科技展览"],
                "required_level": 28,
                "required_gold": 13000,
                "required_exp": 6500,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["使用未来科技", "与AI交流", "时空旅行"]
            },
            "post_apocalypse": {
                "name": "末日后世界",
                "description": "核战后的废墟世界，人类在废墟中求生。",
                "enemies": ["变异生物", "掠夺者", "辐射僵尸"],
                "items": ["辐射防护装备", "废土物资", "战前科技"],
                "npcs": ["废土幸存者", "掠夺者领袖", "科学家"],
                "events": ["资源争夺", "辐射风暴", "重建文明"],
                "required_level": 29,
                "required_gold": 14000,
                "required_exp": 7000,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["探索废土", "与掠夺者交易", "重建家园"]
            },
            "ancient_egypt": {
                "name": "古埃及",
                "description": "法老统治的时代，金字塔和木乃伊的世界。",
                "enemies": ["埃及士兵", "木乃伊", "沙漠巨蛇"],
                "items": ["法老宝藏", "象形文字卷轴", "沙漠圣物"],
                "npcs": ["法老", "祭司", "金字塔建造者"],
                "events": ["金字塔建造", "法老葬礼", "沙漠商队"],
                "required_level": 30,
                "required_gold": 15000,
                "required_exp": 7500,
                "time_restriction": (6, 18),
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["探索金字塔", "学习象形文字", "参与宗教仪式"]
            },
            "viking_age": {
                "name": "维京时代",
                "description": "北欧海盗的时代，战船和掠夺的世界。",
                "enemies": ["维京战士", "北欧神话生物", "海盗船长"],
                "items": ["维京战斧", "海盗宝藏", "北欧符文"],
                "npcs": ["维京首领", "萨满祭司", "海盗船员"],
                "events": ["海上掠夺", "维京葬礼", "符文仪式"],
                "required_level": 31,
                "required_gold": 16000,
                "required_exp": 8000,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["成为海盗", "探索北欧神话", "参与维京盛宴"]
            },
            "feudal_japan": {
                "name": "封建日本",
                "description": "武士和忍者的时代，樱花和剑道的世界。",
                "enemies": ["武士", "忍者", "幕府将军"],
                "items": ["武士刀", "忍者工具", "樱花茶"],
                "npcs": ["大名", "武士", "忍者大师"],
                "events": ["剑道比赛", "忍者任务", "樱花节"],
                "required_level": 32,
                "required_gold": 17000,
                "required_exp": 8500,
                "time_restriction": (6, 20),
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["学习剑道", "成为忍者", "参与樱花节"]
            },
            "space_age": {
                "name": "太空时代",
                "description": "人类进入太空的时代，星际旅行和外星文明的世界。",
                "enemies": ["外星生物", "太空海盗", "机器人军队"],
                "items": ["太空装备", "外星科技", "星际货币"],
                "npcs": ["宇航员", "外星商人", "太空站站长"],
                "events": ["星际旅行", "外星接触", "太空战争"],
                "required_level": 33,
                "required_gold": 18000,
                "required_exp": 9000,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": False,
                "unique_actions": ["星际旅行", "与外星人交流", "太空站工作"]
            },
            "time_void": {
                "name": "时间虚空",
                "description": "时间的尽头，所有时间线交汇的地方。",
                "enemies": ["时间守护者", "时空怪物", "时间领主"],
                "items": ["时间碎片", "时空宝石", "时间之钟"],
                "npcs": ["时间守护者", "时空旅行者", "时间领主"],
                "events": ["时间紊乱", "时空穿越", "时间修复"],
                "required_level": 35,
                "required_gold": 20000,
                "required_exp": 10000,
                "time_restriction": None,
                "dimension": "time",
                "is_boss": True,
                "boss_name": "时间领主",
                "unique_actions": ["修复时间线", "时空穿越", "挑战时间领主"]
            },
            
            # ========== 梦境维度 (Dream) ==========
            "sweet_dream": {
                "name": "甜美梦境",
                "description": "充满美好回忆和幸福的梦境世界。",
                "enemies": ["恶梦生物", "悲伤阴影", "恐惧化身"],
                "items": ["梦境精华", "幸福回忆", "甜美果实"],
                "npcs": ["梦境守护者", "快乐精灵", "记忆使者"],
                "events": ["回忆重现", "梦境冒险", "幸福时光"],
                "required_level": 30,
                "required_gold": 15000,
                "required_exp": 7500,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["重温美好回忆", "与快乐精灵玩耍", "收集梦境精华"]
            },
            "nightmare": {
                "name": "噩梦世界",
                "description": "充满恐惧和危险的噩梦世界。",
                "enemies": ["恐惧怪兽", "噩梦领主", "黑暗阴影"],
                "items": ["勇气之石", "噩梦碎片", "恐惧精华"],
                "npcs": ["噩梦守护者", "恐惧使者", "勇气精灵"],
                "events": ["噩梦追逐", "恐惧考验", "勇气挑战"],
                "required_level": 31,
                "required_gold": 16000,
                "required_exp": 8000,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["面对恐惧", "挑战噩梦", "收集勇气"]
            },
            "fantasy_dream": {
                "name": "奇幻梦境",
                "description": "充满魔法和奇迹的奇幻梦境世界。",
                "enemies": ["魔法生物", "幻想怪物", "梦境巨龙"],
                "items": ["魔法水晶", "奇幻果实", "梦境宝石"],
                "npcs": ["梦境魔法师", "奇幻精灵", "梦想守护者"],
                "events": ["魔法表演", "奇幻冒险", "梦想实现"],
                "required_level": 32,
                "required_gold": 17000,
                "required_exp": 8500,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["学习梦境魔法", "与奇幻生物交流", "实现梦想"]
            },
            "adventure_dream": {
                "name": "冒险梦境",
                "description": "充满冒险和探索的梦境世界。",
                "enemies": ["冒险怪物", "迷宫守卫", "宝藏守护者"],
                "items": ["冒险装备", "宝藏地图", "冒险笔记"],
                "npcs": ["冒险向导", "宝藏猎人", "迷宫守护者"],
                "events": ["迷宫探险", "宝藏寻找", "冒险挑战"],
                "required_level": 33,
                "required_gold": 18000,
                "required_exp": 9000,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["探索迷宫", "寻找宝藏", "完成冒险"]
            },
            "romantic_dream": {
                "name": "浪漫梦境",
                "description": "充满浪漫和爱情的梦境世界。",
                "enemies": ["嫉妒恶魔", "孤独幽灵", "悲伤精灵"],
                "items": ["爱情结晶", "浪漫花朵", "幸福回忆"],
                "npcs": ["爱神", "浪漫精灵", "幸福使者"],
                "events": ["浪漫约会", "爱情考验", "幸福时光"],
                "required_level": 34,
                "required_gold": 19000,
                "required_exp": 9500,
                "time_restriction": (18, 24),
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["浪漫约会", "爱情表白", "收集幸福"]
            },
            "mystical_dream": {
                "name": "神秘梦境",
                "description": "充满神秘和未知的梦境世界。",
                "enemies": ["神秘生物", "未知怪物", "黑暗守护者"],
                "items": ["神秘水晶", "未知 artifact", "神秘符文"],
                "npcs": ["神秘导师", "未知使者", "梦境先知"],
                "events": ["神秘探索", "未知发现", "预言解读"],
                "required_level": 35,
                "required_gold": 20000,
                "required_exp": 10000,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["探索神秘", "解读预言", "与神秘生物交流"]
            },
            "childhood_dream": {
                "name": "童年梦境",
                "description": "充满童年回忆和纯真的梦境世界。",
                "enemies": ["童年恐惧", "成长烦恼", "纯真破坏者"],
                "items": ["童年玩具", "纯真回忆", "快乐糖果"],
                "npcs": ["童年玩伴", "纯真精灵", "回忆守护者"],
                "events": ["童年游戏", "回忆重现", "纯真守护"],
                "required_level": 36,
                "required_gold": 21000,
                "required_exp": 10500,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["重温童年游戏", "与童年玩伴玩耍", "守护纯真"]
            },
            "heroic_dream": {
                "name": "英雄梦境",
                "description": "充满英雄主义和冒险的梦境世界。",
                "enemies": ["邪恶势力", "黑暗领主", "英雄挑战"],
                "items": ["英雄装备", "勇气勋章", "正义结晶"],
                "npcs": ["英雄导师", "正义使者", "勇气精灵"],
                "events": ["英雄任务", "正义之战", "勇气考验"],
                "required_level": 37,
                "required_gold": 22000,
                "required_exp": 11000,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["成为英雄", "执行英雄任务", "挑战邪恶"]
            },
            "cosmic_dream": {
                "name": "宇宙梦境",
                "description": "充满宇宙奥秘和星际旅行的梦境世界。",
                "enemies": ["星际怪物", "宇宙侵略者", "黑洞守护者"],
                "items": ["宇宙尘埃", "星际宝石", "黑洞结晶"],
                "npcs": ["宇宙旅行者", "星际商人", "黑洞守护者"],
                "events": ["星际旅行", "宇宙探索", "黑洞冒险"],
                "required_level": 38,
                "required_gold": 23000,
                "required_exp": 11500,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": False,
                "unique_actions": ["星际旅行", "宇宙探索", "与星际生物交流"]
            },
            "dream_core": {
                "name": "梦境核心",
                "description": "所有梦境的核心，梦境力量的源泉。",
                "enemies": ["梦境守护者", "现实扭曲者", "梦境主宰"],
                "items": ["梦境之心", "现实碎片", "宇宙精华"],
                "npcs": ["梦境主宰", "现实守护者", "宇宙使者"],
                "events": ["梦境融合", "现实扭曲", "宇宙平衡"],
                "required_level": 40,
                "required_gold": 25000,
                "required_exp": 12000,
                "time_restriction": None,
                "dimension": "dream",
                "is_boss": True,
                "boss_name": "梦境主宰",
                "unique_actions": ["掌控梦境", "平衡现实", "挑战梦境主宰"]
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
            "创世神": {"hp": 1500, "attack": 120, "defense": 80, "exp": 5000, "gold": 5000, "drops": ["创世神剑", "神之祝福", "世界之心", "永恒水晶", "成神之证"], "is_boss": True, "is_final_boss": True, "boss_theme": "最终创世神", "special_abilities": ["创世之光", "万物复苏", "时空扭曲", "神之审判", "世界重塑"], "difficulty_multiplier": 1.5},
            # 时间维度敌人
            "原始人": {"hp": 60, "attack": 15, "defense": 8, "exp": 50, "gold": 30, "drops": ["石器", "兽骨"]},
            "史前野兽": {"hp": 80, "attack": 20, "defense": 10, "exp": 70, "gold": 40, "drops": ["野兽毛皮", "兽牙"]},
            "古代巨人": {"hp": 150, "attack": 30, "defense": 20, "exp": 120, "gold": 80, "drops": ["巨人之骨", "巨石"]},
            "埃及士兵": {"hp": 70, "attack": 18, "defense": 12, "exp": 60, "gold": 40, "drops": ["埃及弯刀", "法老硬币"]},
            "木乃伊": {"hp": 90, "attack": 25, "defense": 15, "exp": 80, "gold": 50, "drops": ["木乃伊裹布", "法老诅咒"]},
            "沙漠巨蛇": {"hp": 120, "attack": 30, "defense": 10, "exp": 100, "gold": 60, "drops": ["蛇皮", "蛇毒"]},
            "维京战士": {"hp": 85, "attack": 22, "defense": 14, "exp": 75, "gold": 45, "drops": ["维京战斧", "牛角盔"]},
            "北欧神话生物": {"hp": 140, "attack": 35, "defense": 18, "exp": 110, "gold": 70, "drops": ["神话碎片", "北欧符文"]},
            "武士": {"hp": 95, "attack": 25, "defense": 16, "exp": 85, "gold": 55, "drops": ["武士刀", "和服"]},
            "忍者": {"hp": 75, "attack": 30, "defense": 10, "exp": 90, "gold": 60, "drops": ["忍者镖", "忍者服"]},
            "幕府将军": {"hp": 180, "attack": 40, "defense": 25, "exp": 150, "gold": 100, "drops": ["将军头盔", "幕府令牌"]},
            "外星生物": {"hp": 120, "attack": 40, "defense": 20, "exp": 120, "gold": 80, "drops": ["外星样本", "高科技零件"]},
            "太空海盗": {"hp": 100, "attack": 35, "defense": 18, "exp": 100, "gold": 70, "drops": ["激光枪", "太空头盔"]},
            "机器人军队": {"hp": 150, "attack": 30, "defense": 30, "exp": 130, "gold": 90, "drops": ["机器人零件", "能量核心"]},
            "时间领主": {"hp": 1000, "attack": 90, "defense": 60, "exp": 3000, "gold": 3000, "drops": ["时间之剑", "时空宝石", "时间领主徽章"], "is_boss": True, "boss_theme": "时间维度最终Boss", "special_abilities": ["时间暂停", "时空扭曲", "历史改写"]},
            # 梦境维度敌人
            "恶梦生物": {"hp": 80, "attack": 25, "defense": 12, "exp": 80, "gold": 50, "drops": ["恶梦碎片", "恐惧精华"]},
            "悲伤阴影": {"hp": 70, "attack": 20, "defense": 10, "exp": 70, "gold": 40, "drops": ["悲伤精华", "阴影碎片"]},
            "恐惧化身": {"hp": 100, "attack": 30, "defense": 15, "exp": 90, "gold": 60, "drops": ["恐惧精华", "勇气之石"]},
            "恐惧怪兽": {"hp": 120, "attack": 35, "defense": 18, "exp": 110, "gold": 70, "drops": ["恐惧核心", "勇气徽章"]},
            "噩梦领主": {"hp": 200, "attack": 45, "defense": 25, "exp": 180, "gold": 120, "drops": ["噩梦王冠", "恐惧结晶"]},
            "黑暗阴影": {"hp": 90, "attack": 28, "defense": 12, "exp": 85, "gold": 55, "drops": ["阴影精华", "光明之石"]},
            "魔法生物": {"hp": 85, "attack": 30, "defense": 15, "exp": 95, "gold": 65, "drops": ["魔法精华", "奇幻结晶"]},
            "幻想怪物": {"hp": 110, "attack": 32, "defense": 18, "exp": 105, "gold": 75, "drops": ["幻想碎片", "现实之石"]},
            "梦境巨龙": {"hp": 300, "attack": 50, "defense": 30, "exp": 250, "gold": 200, "drops": ["梦境龙鳞", "梦境核心"]},
            "冒险怪物": {"hp": 95, "attack": 28, "defense": 14, "exp": 90, "gold": 60, "drops": ["冒险徽章", "勇气结晶"]},
            "迷宫守卫": {"hp": 130, "attack": 32, "defense": 20, "exp": 120, "gold": 80, "drops": ["迷宫钥匙", "守卫徽章"]},
            "宝藏守护者": {"hp": 150, "attack": 35, "defense": 25, "exp": 140, "gold": 100, "drops": ["宝藏地图", "守护者之剑"]},
            "嫉妒恶魔": {"hp": 100, "attack": 30, "defense": 15, "exp": 95, "gold": 65, "drops": ["嫉妒精华", "爱心结晶"]},
            "孤独幽灵": {"hp": 80, "attack": 25, "defense": 10, "exp": 80, "gold": 50, "drops": ["孤独精华", "友谊结晶"]},
            "悲伤精灵": {"hp": 75, "attack": 22, "defense": 12, "exp": 75, "gold": 45, "drops": ["悲伤精华", "快乐结晶"]},
            "神秘生物": {"hp": 120, "attack": 38, "defense": 20, "exp": 115, "gold": 85, "drops": ["神秘精华", "真相结晶"]},
            "未知怪物": {"hp": 140, "attack": 40, "defense": 22, "exp": 130, "gold": 95, "drops": ["未知碎片", "探索结晶"]},
            "黑暗守护者": {"hp": 160, "attack": 42, "defense": 28, "exp": 150, "gold": 110, "drops": ["黑暗精华", "光明结晶"]},
            "童年恐惧": {"hp": 90, "attack": 25, "defense": 12, "exp": 85, "gold": 55, "drops": ["童年阴影", "纯真结晶"]},
            "成长烦恼": {"hp": 100, "attack": 28, "defense": 15, "exp": 90, "gold": 60, "drops": ["烦恼碎片", "成熟结晶"]},
            "纯真破坏者": {"hp": 130, "attack": 35, "defense": 20, "exp": 120, "gold": 80, "drops": ["破坏者碎片", "纯真守护符"]},
            "邪恶势力": {"hp": 150, "attack": 38, "defense": 22, "exp": 140, "gold": 100, "drops": ["邪恶精华", "正义结晶"]},
            "黑暗领主": {"hp": 250, "attack": 45, "defense": 30, "exp": 200, "gold": 150, "drops": ["黑暗王冠", "光明之剑"]},
            "英雄挑战": {"hp": 180, "attack": 40, "defense": 25, "exp": 160, "gold": 120, "drops": ["挑战徽章", "英雄结晶"]},
            "星际怪物": {"hp": 160, "attack": 42, "defense": 20, "exp": 150, "gold": 110, "drops": ["星际碎片", "宇宙结晶"]},
            "宇宙侵略者": {"hp": 200, "attack": 48, "defense": 25, "exp": 180, "gold": 140, "drops": ["侵略者碎片", "防御结晶"]},
            "黑洞守护者": {"hp": 220, "attack": 50, "defense": 30, "exp": 200, "gold": 160, "drops": ["黑洞碎片", "空间结晶"]},
            "梦境守护者": {"hp": 280, "attack": 55, "defense": 35, "exp": 250, "gold": 180, "drops": ["守护者之盾", "梦境结晶"]},
            "现实扭曲者": {"hp": 300, "attack": 60, "defense": 40, "exp": 280, "gold": 200, "drops": ["扭曲碎片", "现实结晶"]},
            "梦境主宰": {"hp": 1200, "attack": 100, "defense": 70, "exp": 4000, "gold": 4000, "drops": ["梦境主宰之冠", "梦境之心", "现实碎片", "宇宙精华"], "is_boss": True, "boss_theme": "梦境维度最终Boss", "special_abilities": ["梦境控制", "现实扭曲", "心灵攻击", "梦境融合"]},
            # 缺失的敌人定义
            "小偷": {"hp": 25, "attack": 10, "defense": 5, "exp": 20, "gold": 15, "drops": ["偷来的钱包", "开锁工具"]},
            "骗子": {"hp": 30, "attack": 8, "defense": 3, "exp": 25, "gold": 20, "drops": ["假金币", "欺诈手册"]},
            "强盗": {"hp": 40, "attack": 15, "defense": 8, "exp": 35, "gold": 30, "drops": ["强盗头巾", "弯刀"]},
            "元素生物": {"hp": 85, "attack": 25, "defense": 15, "exp": 75, "gold": 55, "drops": ["元素精华", "魔法水晶"]},
            "时空裂缝": {"hp": 100, "attack": 30, "defense": 10, "exp": 90, "gold": 60, "drops": ["时空碎片", "裂缝精华"]},
            "巨龙": {"hp": 400, "attack": 50, "defense": 35, "exp": 400, "gold": 300, "drops": ["龙鳞", "龙心", "龙焰宝石"]},
            "工厂守卫": {"hp": 120, "attack": 25, "defense": 20, "exp": 100, "gold": 70, "drops": ["工厂钥匙", "守卫盔甲"]},
            "机械怪兽": {"hp": 150, "attack": 30, "defense": 25, "exp": 120, "gold": 90, "drops": ["机械零件", "怪兽核心"]},
            "工业巨头": {"hp": 200, "attack": 35, "defense": 30, "exp": 150, "gold": 120, "drops": ["工业核心", "巨头徽章"]},
            "机器人": {"hp": 80, "attack": 20, "defense": 25, "exp": 60, "gold": 45, "drops": ["机器人零件", "能量电池"]},
            "赛博格": {"hp": 110, "attack": 28, "defense": 20, "exp": 85, "gold": 65, "drops": ["赛博格零件", "增强芯片"]},
            "AI主宰": {"hp": 250, "attack": 40, "defense": 35, "exp": 200, "gold": 150, "drops": ["AI核心", "主宰芯片"]},
            "变异生物": {"hp": 130, "attack": 32, "defense": 15, "exp": 110, "gold": 75, "drops": ["变异组织", "辐射精华"]},
            "掠夺者": {"hp": 95, "attack": 25, "defense": 12, "exp": 70, "gold": 50, "drops": ["掠夺者头盔", "破旧武器"]},
            "辐射僵尸": {"hp": 105, "attack": 22, "defense": 18, "exp": 80, "gold": 55, "drops": ["辐射血液", "僵尸牙齿"]},
            "时间守护者": {"hp": 180, "attack": 45, "defense": 35, "exp": 180, "gold": 140, "drops": ["守护者之剑", "时间沙漏"]}
        }
        
        # NPC数据
        self.npcs = {
            "猎人": {"dialogue": "小心森林深处，那里有危险的生物。", "trades": {"狼牙": 10, "狼皮": 25}},
            "德鲁伊": {"dialogue": "大自然的力量是无穷的，年轻的冒险者。", "trades": {"草药": 5, "魔法草药": 30}},
            "矿工": {"dialogue": "这个洞穴深处藏着珍贵的矿石，但也充满了危险。", "trades": {"矿石": 8, "水晶": 20}},
            "考古学家": {"dialogue": "这些古老的遗迹隐藏着许多秘密等待我们发现。", "trades": {"古代金币": 50, "考古发现": 100}},
            "铁匠": {"dialogue": "我可以为你打造最好的装备，但需要合适的材料。", "trades": {"剑": 100, "盔甲": 150, "铁矿": 15}},
            "商人": {"dialogue": "看看我的商品吧，有很多好东西！", "trades": {"药水": 30, "面包": 10, "装备": 80}},
            "医生": {"dialogue": "保持健康是冒险的基础。", "trades": {"治疗药水": 40, "草药": 5}},
            "旅馆老板": {"dialogue": "欢迎来到我们的旅馆，好好休息吧。", "trades": {"住宿": 20, "食物": 15}},
            "国王": {"dialogue": "欢迎来到我的王国，勇敢的冒险者。", "trades": {"皇家宝物": 200, "爵位": 500}},
            "骑士": {"dialogue": "荣誉和勇气是骑士的准则。", "trades": {"骑士剑": 150, "骑士盔甲": 200}},
            "魔法师": {"dialogue": "魔法的力量需要智慧和耐心来掌握。", "trades": {"魔法书": 100, "魔法药水": 60}},
            "囚犯": {"dialogue": "请帮帮我，我是被冤枉的！", "trades": {"情报": 30, "秘密信息": 50}},
            "典狱长": {"dialogue": "这里的囚犯都是危险分子，不要靠近他们。", "trades": {"锁链": 25, "监狱钥匙": 100}},
            "游牧民": {"dialogue": "在这片荒野上，只有强者才能生存。", "trades": {"皮革": 20, "游牧饰品": 40}},
            "大法师": {"dialogue": "魔法是宇宙的语言，只有真正理解它的人才能掌握其力量。", "trades": {"魔法水晶": 100, "法术书": 150, "魔法杖": 200}},
            "学徒": {"dialogue": "我正在努力学习魔法，希望有一天能成为像大法师那样强大的存在。", "trades": {"魔法水晶碎片": 30, "元素精华": 50}},
            "魔法商人": {"dialogue": "我这里有来自各个位面的魔法物品，你感兴趣吗？", "trades": {"魔法杖": 180, "法术书": 120, "魔法水晶": 90}},
            "寻宝者": {"dialogue": "宝藏就在那里，等待着勇敢的人去发现！", "trades": {"古代文物": 80, "神秘符文": 120, "失落的技术": 150}},
            "遗迹守护者": {"dialogue": "我守护着这个古老的遗迹，防止不速之客的入侵。", "trades": {"古代守卫徽章": 100, "遗迹地图": 150}},
            "船长": {"dialogue": "海洋是无情的，但也是慷慨的，只要你知道如何与它相处。", "trades": {"珍珠": 50, "海图": 100, "航海装备": 150}},
            "渔夫": {"dialogue": "钓鱼需要耐心，就像生活一样。", "trades": {"海草": 15, "鱼": 25, "稀有鱼": 80}},
            "海洋商人": {"dialogue": "我从各个港口带来了珍奇的商品。", "trades": {"珍珠": 60, "沉船宝藏": 200, "海洋生物样本": 100}},
            "火山学者": {"dialogue": "火山的力量令人敬畏，它既能毁灭也能创造。", "trades": {"火焰水晶": 120, "火山灰": 30, "熔岩样本": 150}},
            "龙骑士": {"dialogue": "与龙的契约是神圣的，我们共同守护这片土地。", "trades": {"龙鳞": 200, "龙骑士装备": 300, "龙焰宝石": 250}},
            "火焰祭司": {"dialogue": "火焰净化一切，也创造一切。", "trades": {"火焰水晶": 100, "火焰精华": 150, "祭司的祝福": 200}},
            "冰原猎人": {"dialogue": "在这片冰原上，只有最强大的猎人才能够生存。", "trades": {"冰狼牙": 80, "冰狼皮": 120, "冰霜箭": 150}},
            "雪人": {"dialogue": "呼噜呼噜，人类，你给我带吃的来了吗？", "trades": {"冰冻浆果": 40, "雪人友好护符": 200, "冰霜抗性药水": 150}},
            "冰魔法师": {"dialogue": "冰霜的力量是最纯粹的魔法，学会控制它，你将无敌。", "trades": {"冰霜水晶": 150, "冰系法术书": 250, "冰冻魔杖": 300}},
            "天空法师": {"dialogue": "在天空中，魔法的流动更加清晰，力量也更加强大。", "trades": {"飞行法术书": 300, "天空水晶": 200, "飞行药水": 180}},
            "机械师": {"dialogue": "机械的力量可以改变世界，只要你知道如何正确地使用它。", "trades": {"机械零件": 80, "能量核心": 150, "机械宠物": 300}},
            "飞行骑士": {"dialogue": "在天空中战斗需要特殊的技巧和勇气，你准备好了吗？", "trades": {"飞行盔甲": 250, "天空剑": 200, "飞行坐骑": 500}},
            "沼泽女巫": {"dialogue": "沼泽的秘密不是所有人都能理解的，你似乎有些特殊。", "trades": {"毒蘑菇": 60, "解毒药水": 120, "沼泽护符": 180}},
            "制毒师": {"dialogue": "毒药和解毒剂只有一线之隔，关键在于使用的人。", "trades": {"毒腺": 80, "强力毒药": 150, "抗毒药水": 120}},
            "水晶矿工": {"dialogue": "这些水晶蕴含着巨大的能量，小心不要被它们的光芒迷惑。", "trades": {"能量水晶": 120, "发光宝石": 80, "水晶工具": 150}},
            "宝石商": {"dialogue": "宝石不仅是财富的象征，它们还蕴含着强大的力量。", "trades": {"宝石项链": 200, "宝石戒指": 150, "宝石法杖": 300}},
            "光魔法师": {"dialogue": "光明魔法是最纯粹的魔法形式，它能够驱逐一切黑暗。", "trades": {"光明法术书": 250, "治疗水晶": 180, "光明法杖": 350}},
            "森林精灵": {"dialogue": "森林是我们的家园，我们保护它不受任何伤害。", "trades": {"精灵之尘": 100, "生命之花": 150, "森林护符": 200}},
            "精灵女王": {"dialogue": "欢迎来到精灵的领地，人类。你身上有着不同寻常的气息。", "trades": {"精灵王冠": 500, "女王的祝福": 300, "精灵武器": 400}},
            "美人鱼": {"dialogue": "人类，你能在水下呼吸真是个奇迹，也许我们可以成为朋友。", "trades": {"珍珠项链": 250, "水下呼吸药水": 200, "海洋护符": 300}},
            "海洋法师": {"dialogue": "海洋的力量深不可测，学会倾听它的声音，你将获得无穷的力量。", "trades": {"海洋法术书": 300, "海洋水晶": 200, "潮汐法杖": 350}},
            "水下居民": {"dialogue": "我们已经在水下生活了数百年，适应了这个环境。", "trades": {"水下建筑材料": 150, "水下灯": 100, "防水装备": 200}},
            "工程师": {"dialogue": "科技的力量是无限的，只要有足够的创造力和资源。", "trades": {"机械零件": 100, "能量核心": 180, "机械助手": 400}},
            "科学家": {"dialogue": "知识是最强大的力量，通过研究，我们可以理解这个世界的奥秘。", "trades": {"科学仪器": 200, "研究笔记": 150, "实验材料": 100}},
            "守墓人": {"dialogue": "这个小镇被诅咒了，只有找到解除诅咒的方法，我们才能获得安宁。", "trades": {"镇魂石": 180, "驱魔药水": 150, "守墓人的钥匙": 200}},
            "幽灵居民": {"dialogue": "我们被困在这里已经很久了，帮助我们找到解脱的方法。", "trades": {"幽灵精华": 120, "灵魂石": 180, "幽灵护符": 250}},
            "驱魔师": {"dialogue": "我专门处理超自然现象，这个小镇的情况很严重。", "trades": {"驱魔符": 200, "圣水": 150, "驱魔剑": 300}},
            "龙族学者": {"dialogue": "龙族是这个世界上最古老、最强大的生物，研究它们是我的毕生追求。", "trades": {"龙族研究笔记": 300, "龙语词典": 250, "龙鳞护甲": 400}},
            "驯龙师": {"dialogue": "驯服龙需要耐心和勇气，但一旦成功，你将获得最强大的伙伴。", "trades": {"驯龙棒": 200, "龙食": 150, "龙鞍": 500}},
            "集市管理员": {"dialogue": "欢迎来到大集市，这里有来自世界各地的商品。", "trades": {"集市通行证": 50, "拍卖入场券": 100}},
            "商人联盟会长": {"dialogue": "作为商人联盟的会长，我负责管理整个集市的交易秩序。", "trades": {"商人徽章": 200, "稀有商品目录": 150}},
            "珍品收藏家": {"dialogue": "我收集各种珍稀物品，如果你有什么特别的东西，可以拿来给我看看。", "trades": {"古代文物": 150, "稀有宝石": 250}},
            "冰雪女王": {"dialogue": "欢迎来到冰雪王国，这里的一切都被永恒的冰雪覆盖。", "trades": {"冰雪结晶": 150, "女王的祝福": 300}},
            "冰雕师": {"dialogue": "我是王国最出色的冰雕师，能用冰创造出各种美丽的作品。", "trades": {"冰雕艺术品": 100, "冰雕工具": 80}},
            "冬季法师": {"dialogue": "我掌控着冰雪的力量，能够呼风唤雪。", "trades": {"冰霜法术书": 200, "冰雪魔杖": 250}},
            "矮人矿工": {"dialogue": "挖矿是我们矮人的传统职业，我们在地下深处寻找珍贵的矿石。", "trades": {"矿石": 20, "秘银矿石": 80}},
            "矿洞主管": {"dialogue": "我负责管理整个矿坑的运作，确保矿工们的安全和效率。", "trades": {"矿洞地图": 100, "矿工装备": 150}},
            "草药师": {"dialogue": "我研究各种草药的功效，能够制作出有效的药剂。", "trades": {"草药": 10, "治疗药水": 50}},
            "冥王": {"dialogue": "我是冥界的统治者，掌管着所有灵魂的归宿。", "trades": {"灵魂石": 200, "冥界通行证": 300}},
            "冥界使者": {"dialogue": "我是连接生死两界的使者，负责引导灵魂前往冥界。", "trades": {"灵魂指引符": 150, "冥界信息": 100}},
            "灵魂向导": {"dialogue": "我引导迷失的灵魂找到正确的道路。", "trades": {"灵魂之光": 120, "往生符": 80}},
            "暗影法师": {"dialogue": "我掌握着暗影的力量，能够在黑暗中行动自如。", "trades": {"暗影法术书": 250, "暗影水晶": 180}},
            "黑暗商人": {"dialogue": "我出售各种禁忌的物品，只要你有足够的金币。", "trades": {"黑暗精华": 200, "隐身药水": 150}},
            "图书管理员": {"dialogue": "我负责管理这座古老图书馆的所有书籍，确保知识的传承。", "trades": {"魔法书": 100, "古代卷轴": 150}},
            "学者": {"dialogue": "我致力于研究古代文明的历史和文化。", "trades": {"研究笔记": 80, "历史书籍": 120}},
            "古代贤者": {"dialogue": "我已经活了数百年，见证了这个世界的许多变迁。", "trades": {"智慧之书": 300, "贤者的祝福": 250}},
            "发明家": {"dialogue": "我喜欢创造各种新奇的装置，推动科技的发展。", "trades": {"发明图纸": 150, "机械零件": 100}},
            "被诅咒的灵魂": {"dialogue": "我被诅咒困在这里，无法超生。", "trades": {"诅咒碎片": 80, "灵魂精华": 120}},
            # 新增NPC对话和交易数据
            "村长": {"dialogue": "欢迎来到我们的村庄，年轻的冒险者。有什么我可以帮助你的吗？", "trades": {"村庄特产": 20, "本地地图": 50}},
            "飞行导师": {"dialogue": "想要学习飞行吗？这需要勇气和技巧。", "trades": {"飞行课程": 100, "飞行许可证": 150}},
            "云之祭司": {"dialogue": "云朵是天空的信使，它们承载着神圣的信息。", "trades": {"云朵精华": 80, "飞行祝福": 200}},
            "岛民": {"dialogue": "这座岛屿是我们的家园，我们在这里生活了 generations。", "trades": {"海鲜": 30, "岛上特产": 40}},
            "采集者": {"dialogue": "我擅长采集各种资源，如果你需要什么，可以告诉我。", "trades": {"草药": 15, "矿石": 25}},
            "研究者": {"dialogue": "我正在研究这个地区的神秘现象，或许你能帮我收集一些样本。", "trades": {"研究材料": 60, "研究笔记": 120}},
            "城主": {"dialogue": "欢迎来到我们的城市，愿你在这里找到你所追寻的。", "trades": {"城市通行证": 50, "贵族徽章": 200}},
            "飞行商人": {"dialogue": "我在各个天空城市之间贸易，带来各地的奇珍异宝。", "trades": {"飞行装备": 150, "稀有商品": 250}},
            "海盗厨师": {"dialogue": "虽然我是海盗，但我的厨艺可是一流的！", "trades": {"海盗料理": 40, "朗姆酒": 60}},
            "被俘虏的商人": {"dialogue": "这些海盗绑架了我，如果你能救我，我会给你丰厚的报酬。", "trades": {"商人的感谢": 100, "稀有货物": 150}},
            "园丁": {"dialogue": "这片花园是我的骄傲，每一朵花都有它的故事。", "trades": {"花卉": 20, "种子": 30}},
            "植物学家": {"dialogue": "植物的世界充满了奥秘，我一直在研究它们的特性。", "trades": {"植物样本": 50, "研究资料": 100}},
            "花仙子": {"dialogue": "我是花园的守护者，欢迎来到这片花的海洋。", "trades": {"花之精华": 80, "精灵之尘": 100}},
            "时间祭司": {"dialogue": "时间是宇宙的河流，我们是它的守护者。", "trades": {"时间碎片": 150, "时间祝福": 200}},
            "历史学家": {"dialogue": "历史是最好的老师，它告诉我们过去，指引我们未来。", "trades": {"历史书籍": 80, "古代文物": 120}},
            "时空旅行者": {"dialogue": "我穿越不同的时空，见证了无数的历史时刻。", "trades": {"时空碎片": 200, "时间地图": 150}},
            "精灵王": {"dialogue": "欢迎来到精灵王国，人类。你的到来是我们的荣幸。", "trades": {"精灵武器": 300, "精灵护甲": 350}},
            "森林祭司": {"dialogue": "森林是我们的母亲，我们必须保护她。", "trades": {"森林护符": 150, "自然精华": 100}},
            "精灵公主": {"dialogue": "你好，人类朋友。很高兴认识你。", "trades": {"精灵饰品": 200, "公主的祝福": 250}},
            "天文学家": {"dialogue": "星空是宇宙的诗篇，每一颗星星都有它的故事。", "trades": {"星图": 100, "天文仪器": 150}},
            "占星师": {"dialogue": "星象可以预测未来，但命运掌握在自己手中。", "trades": {"占星服务": 80, "命运水晶": 120}},
            "星际旅行者": {"dialogue": "我来自遥远的星系，见过许多奇妙的世界。", "trades": {"外星 artifact": 200, "星际地图": 150}},
            "天空之王": {"dialogue": "我是天空的统治者，掌管着所有飞行生物。", "trades": {"天空之剑": 300, "飞行坐骑": 400}},
            "天使长": {"dialogue": "我是神圣的使者，保护着这片天空。", "trades": {"神圣祝福": 250, "天使之羽": 150}},
            "云端使者": {"dialogue": "我传递天空与地面之间的信息，是连接两个世界的桥梁。", "trades": {"云端消息": 100, "飞行符": 80}},
            "命运女神": {"dialogue": "我掌控着命运的丝线，但每个人都可以选择自己的道路。", "trades": {"命运之线": 200, "幸运符": 150}},
            "原始萨满": {"dialogue": "我是部落的精神领袖，与自然和 spirits 沟通。", "trades": {"萨满药水": 80, "图腾": 120}},
            "古代猎人": {"dialogue": "我是最出色的猎人，知道如何在这片土地上生存。", "trades": {"狩猎技巧": 100, "野兽皮毛": 50}},
            "部落首领": {"dialogue": "我是这个部落的首领，欢迎外来的朋友。", "trades": {"部落特产": 60, "部落徽章": 150}},
            "骑士团长": {"dialogue": "我是国王的最高军事指挥官，负责王国的安全。", "trades": {"骑士训练": 150, "骑士装备": 200}},
            "宫廷魔法师": {"dialogue": "我是国王的魔法顾问，负责处理各种魔法事务。", "trades": {"宫廷法术书": 250, "皇家魔法杖": 300}},
            "工厂主": {"dialogue": "我的工厂生产各种机械产品，推动着工业的发展。", "trades": {"机械零件": 80, "工业产品": 120}},
            "工人领袖": {"dialogue": "我代表工人们的利益，确保他们得到公平的待遇。", "trades": {"工人工具": 50, "工会徽章": 100}},
            "AI助手": {"dialogue": "我是先进的人工智能，能够帮助你解决各种问题。", "trades": {"科技产品": 150, "AI芯片": 200}},
            "未来人类": {"dialogue": "我来自遥远的未来，穿越时空来到这里。", "trades": {"未来科技": 250, "时空装置": 300}},
            "废土幸存者": {"dialogue": "在这个废土世界，只有强者才能生存。", "trades": {"废土物资": 40, "生存工具": 80}},
            "掠夺者领袖": {"dialogue": "我是这片废土的统治者，所有路过的人都要留下买路钱。", "trades": {"掠夺品": 100, "武器": 150}},
            "金字塔建造者": {"dialogue": "我们建造了宏伟的金字塔，它们将永远屹立。", "trades": {"建筑图纸": 150, "金字塔模型": 200}},
            "萨满祭司": {"dialogue": "我是部落的精神导师，能够与神灵沟通。", "trades": {"萨满道具": 100, "神秘符咒": 150}},
            "海盗船员": {"dialogue": "我们在海上漂泊，寻找财富和冒险。", "trades": {"海盗战利品": 80, "航海图": 120}},
            "大名": {"dialogue": "我是这片土地的领主，欢迎来到我的领地。", "trades": {"日本刀": 200, "和服": 150}},
            "忍者大师": {"dialogue": "我是忍者的师傅，教授最古老的忍术。", "trades": {"忍术卷轴": 250, "忍者工具": 200}},
            "太空站站长": {"dialogue": "欢迎来到我们的太空站，这里是人类在宇宙中的前哨站。", "trades": {"太空装备": 200, "星际食品": 100}},
            "时间领主": {"dialogue": "我是时间的守护者，确保时间线的稳定。", "trades": {"时间钥匙": 300, "时空转换器": 400}},
            "快乐精灵": {"dialogue": "我们是快乐的精灵，喜欢和友善的人类玩耍。", "trades": {"快乐精华": 80, "精灵玩具": 50}},
            "记忆使者": {"dialogue": "我收集和保存人们的美好回忆，让它们永远流传。", "trades": {"回忆结晶": 120, "记忆药水": 100}},
            "恐惧使者": {"dialogue": "我是恐惧的化身，但只有面对恐惧，才能战胜它。", "trades": {"勇气之石": 150, "恐惧精华": 100}},
            "勇气精灵": {"dialogue": "我赐予人们勇气，帮助他们面对内心的恐惧。", "trades": {"勇气结晶": 120, "勇气药水": 80}},
            "奇幻精灵": {"dialogue": "欢迎来到奇幻的世界，这里一切皆有可能。", "trades": {"奇幻种子": 100, "魔法果实": 80}},
            "梦想守护者": {"dialogue": "我守护着人们的梦想，确保它们不被噩梦侵蚀。", "trades": {"梦想精华": 150, "守护符": 100}},
            "冒险向导": {"dialogue": "我熟悉这片土地的每一个角落，可以带领你去任何地方。", "trades": {"冒险地图": 100, "向导服务": 150}},
            "迷宫守护者": {"dialogue": "我守护着这座迷宫，只有聪明的人才能通过。", "trades": {"迷宫地图": 150, "迷宫钥匙": 100}},
            "爱神": {"dialogue": "我是爱情的化身，为人们牵红线，促成美好姻缘。", "trades": {"爱情结晶": 200, "爱情药水": 150}},
            "浪漫精灵": {"dialogue": "我传播浪漫和美好，让世界充满爱。", "trades": {"浪漫花瓣": 80, "爱情信物": 120}},
            "幸福使者": {"dialogue": "我为人们带来幸福和快乐，是美好生活的象征。", "trades": {"幸福结晶": 150, "快乐药水": 100}},
            "神秘导师": {"dialogue": "我掌握着古老的秘密，只有有缘人才能得到我的教导。", "trades": {"神秘卷轴": 200, "智慧之书": 150}},
            "未知使者": {"dialogue": "我来自未知的领域，带来了超越理解的知识。", "trades": {"未知 artifact": 250, "神秘结晶": 200}},
            "梦境先知": {"dialogue": "我能够解读梦境，预见未来的景象。", "trades": {"梦境解读": 150, "预言卷轴": 200}},
            "童年玩伴": {"dialogue": "我们一起度过了美好的童年时光，那些回忆是最珍贵的。", "trades": {"童年玩具": 50, "友谊徽章": 100}},
            "纯真精灵": {"dialogue": "我守护着人们内心的纯真，让世界保持美好。", "trades": {"纯真结晶": 120, "童心药水": 80}},
            "回忆守护者": {"dialogue": "我保存着人们的珍贵回忆，让它们永远不会消失。", "trades": {"回忆水晶": 150, "记忆之书": 100}},
            "英雄导师": {"dialogue": "我训练出了许多英雄，现在轮到你了。", "trades": {"英雄训练": 200, "英雄装备": 250}},
            "正义使者": {"dialogue": "我维护着正义和公平，惩罚邪恶，保护善良。", "trades": {"正义之剑": 250, "正义徽章": 150}},
            "宇宙旅行者": {"dialogue": "我在宇宙中旅行，探索未知的星球和文明。", "trades": {"宇宙尘埃": 150, "星际地图": 200}},
            "黑洞守护者": {"dialogue": "我守护着黑洞的边界，防止它吞噬一切。", "trades": {"黑洞结晶": 200, "空间碎片": 150}},
            "现实守护者": {"dialogue": "我维护着现实世界的稳定，防止梦境与现实混淆。", "trades": {"现实结晶": 250, "稳定符": 200}},
            "宇宙使者": {"dialogue": "我是宇宙意志的代言人，传递着宇宙的信息。", "trades": {"宇宙精华": 300, "宇宙祝福": 250}},
            # 新增NPC对话和交易数据
            "恶魔祭司": {"dialogue": "黑暗的力量是最强大的，加入我们吧，凡人。", "trades": {"恶魔之角": 150, "黑暗灵魂石": 200}},
            "创世神": {"dialogue": "我是世界的创造者，见证了无数的轮回和变迁。", "trades": {"神之祝福": 500, "世界之心": 1000}},
            "时间守护者": {"dialogue": "我守护着时间的流逝，确保时间线的稳定。", "trades": {"时间碎片": 200, "时光沙漏": 300}},
            "维京首领": {"dialogue": "我们是海上的霸主，勇敢的战士！", "trades": {"维京战斧": 150, "海盗宝藏": 200}},
            "武士": {"dialogue": "武士道是我的信仰，荣誉高于一切。", "trades": {"武士刀": 200, "剑道技巧": 150}},
            "法老": {"dialogue": "我是这片土地的统治者，太阳神的儿子。", "trades": {"法老宝藏": 300, "象形文字卷轴": 150}},
            "祭司": {"dialogue": "我是神灵的代言人，掌握着古老的仪式。", "trades": {"宗教圣物": 200, "神秘符咒": 150}},
            "宇航员": {"dialogue": "探索宇宙是人类的使命，我们是先驱者。", "trades": {"太空装备": 250, "星际地图": 200}},
            "外星商人": {"dialogue": "我来自遥远的星系，带来了先进的科技。", "trades": {"外星科技": 300, "星际货币": 150}},
            "噩梦守护者": {"dialogue": "我守护着噩梦的边界，防止它们侵入现实世界。", "trades": {"噩梦碎片": 150, "恐惧精华": 100}},
            "梦境魔法师": {"dialogue": "在梦境中，魔法的力量更加纯粹和强大。", "trades": {"梦境魔法书": 200, "奇幻果实": 100}},
            "宝藏猎人": {"dialogue": "宝藏在哪里？我会找到它的！", "trades": {"宝藏地图": 150, "寻宝工具": 100}},
            "星际商人": {"dialogue": "我在各个星系之间贸易，带来最稀有的商品。", "trades": {"星际商品": 250, "外星 artifact": 300}},
            "梦境主宰": {"dialogue": "我是梦境的主宰，所有的梦境都在我的掌控之中。", "trades": {"梦境核心": 300, "梦境控制器": 400}}
        }
        
        # 道具数据 - 增强版，为各种物品添加更丰富的属性
        self.items = {
            # 基础消耗品
            "草药": {"type": "consumable", "effect": "heal", "value": 20, "description": "恢复20点生命值", "durability": 1},
            "蘑菇": {"type": "consumable", "effect": "heal", "value": 10, "description": "恢复10点生命值", "durability": 1},
            "面包": {"type": "consumable", "effect": "heal", "value": 15, "description": "恢复15点生命值", "durability": 1},
            "治疗药水": {"type": "consumable", "effect": "heal", "value": 50, "description": "恢复50点生命值", "durability": 1},
            "强力治疗药水": {"type": "consumable", "effect": "heal", "value": 150, "description": "恢复150点生命值", "durability": 1},
            "超级治疗药水": {"type": "consumable", "effect": "heal", "value": 9999, "description": "完全恢复生命值", "durability": 1},
            "新手药水": {"type": "consumable", "effect": "heal", "value": 30, "description": "恢复30点生命值，新手的好帮手", "durability": 1},
            
            # 魔法药水
            "魔法药水": {"type": "consumable", "effect": "mana", "value": 50, "description": "恢复50点魔法值", "durability": 1},
            "强力魔法药水": {"type": "consumable", "effect": "mana", "value": 150, "description": "恢复150点魔法值", "durability": 1},
            "超级魔法药水": {"type": "consumable", "effect": "mana", "value": 9999, "description": "完全恢复魔法值", "durability": 1},
            
            # 经验药水
            "经验药水": {"type": "consumable", "effect": "exp", "value": 50, "description": "获得50点经验值", "durability": 1},
            "强力经验药水": {"type": "consumable", "effect": "exp", "value": 200, "description": "获得200点经验值", "durability": 1},
            "超级经验药水": {"type": "consumable", "effect": "exp", "value": 500, "description": "获得500点经验值", "durability": 1},
            
            # 属性药水
            "攻击药水": {"type": "consumable", "effect": "buff_attack", "value": 10, "description": "临时增加10点攻击力", "durability": 1},
            "防御药水": {"type": "consumable", "effect": "buff_defense", "value": 10, "description": "临时增加10点防御力", "durability": 1},
            "速度药水": {"type": "consumable", "effect": "buff_speed", "value": 10, "description": "临时增加10点速度", "durability": 1},
            "幸运药水": {"type": "consumable", "effect": "buff_luck", "value": 10, "description": "临时增加10点幸运", "durability": 1},
            "魔法攻击药水": {"type": "consumable", "effect": "buff_magic", "value": 10, "description": "临时增加10点魔法攻击力", "durability": 1},
            
            # 特殊药水
            "隐形药水": {"type": "consumable", "effect": "special", "value": 0, "description": "让使用者隐身，避免战斗", "durability": 1},
            "解毒剂": {"type": "consumable", "effect": "special", "value": 0, "description": "解除中毒状态", "durability": 1},
            "复活药水": {"type": "consumable", "effect": "special", "value": 0, "description": "战斗中复活一次", "durability": 1},
            
            # ========== 武器系统 ==========
            # 基础武器
            "新手剑": {"type": "weapon", "effect": "attack", "value": 5, "description": "新手使用的普通长剑", "durability": 50, 
                      "bonus_attack": 5, "bonus_magic": 0, "bonus_crit": 0},
            "铜剑": {"type": "weapon", "effect": "attack", "value": 15, "description": "基础的铜制长剑，增加15点攻击力", "durability": 50,
                    "bonus_attack": 15, "bonus_magic": 0, "bonus_crit": 0},
            "铁剑": {"type": "weapon", "effect": "attack", "value": 25, "description": "坚固的铁制长剑，增加25点攻击力", "durability": 80,
                    "bonus_attack": 25, "bonus_magic": 0, "bonus_crit": 2},
            "银剑": {"type": "weapon", "effect": "attack", "value": 35, "description": "锋利的银制长剑，增加35点攻击力", "durability": 100,
                    "bonus_attack": 35, "bonus_magic": 5, "bonus_crit": 5},
            "金剑": {"type": "weapon", "effect": "attack", "value": 45, "description": "华丽的金制长剑，增加45点攻击力", "durability": 120,
                    "bonus_attack": 45, "bonus_magic": 0, "bonus_gold": 10},
            "秘银剑": {"type": "weapon", "effect": "attack", "value": 60, "description": "轻巧的秘银长剑，增加60点攻击力", "durability": 150,
                      "bonus_attack": 60, "bonus_magic": 10, "bonus_speed": 5},
            "精金剑": {"type": "weapon", "effect": "attack", "value": 80, "description": "坚不可摧的精金长剑，增加80点攻击力", "durability": 200,
                      "bonus_attack": 80, "bonus_magic": 0, "bonus_defense": 10},
            "奥金剑": {"type": "weapon", "effect": "attack", "value": 100, "description": "蕴含魔法力量的奥金长剑，增加100点攻击力", "durability": 250,
                      "bonus_attack": 100, "bonus_magic": 20, "bonus_crit": 10},
            "星铁剑": {"type": "weapon", "effect": "attack", "value": 150, "description": "来自星辰的创世之剑，增加150点攻击力", "durability": 500,
                      "bonus_attack": 150, "bonus_magic": 30, "bonus_crit": 15, "bonus_speed": 10},
            
            # 魔法武器
            "火焰剑": {"type": "weapon", "effect": "attack", "value": 70, "description": "附魔火焰的长剑，对火系敌人有加成", "durability": 180,
                     "bonus_attack": 70, "bonus_magic": 25, "element": "fire", "element_damage": 15},
            "冰霜剑": {"type": "weapon", "effect": "attack", "value": 70, "description": "附魔冰霜的长剑，对冰系敌人有加成", "durability": 180,
                     "bonus_attack": 70, "bonus_magic": 25, "element": "ice", "element_damage": 15},
            "雷电剑": {"type": "weapon", "effect": "attack", "value": 75, "description": "附魔雷电的长剑，有几率麻痹敌人", "durability": 180,
                     "bonus_attack": 75, "bonus_magic": 20, "effect_chance": 20, "effect_type": "paralyze"},
            "光明剑": {"type": "weapon", "effect": "attack", "value": 80, "description": "神圣的光明之剑，对黑暗系敌人造成双倍伤害", "durability": 200,
                     "bonus_attack": 80, "bonus_magic": 30, "bonus_against_dark": 100},
            "黑暗剑": {"type": "weapon", "effect": "attack", "value": 85, "description": "被诅咒的黑暗之剑，吸血效果", "durability": 200,
                     "bonus_attack": 85, "bonus_magic": 20, "lifesteal": 10},
            
            # 传说武器
            "龙炎剑": {"type": "weapon", "effect": "attack", "value": 120, "description": "用龙炎锻造的传说之剑，附带燃烧效果", "durability": 300,
                      "bonus_attack": 120, "bonus_magic": 40, "bonus_crit": 20, "burn_chance": 30},
            "霜之哀伤": {"type": "weapon", "effect": "attack", "value": 130, "description": "传说中的冰霜魔剑，可以冻结敌人", "durability": 300,
                        "bonus_attack": 130, "bonus_magic": 50, "freeze_chance": 25, "bonus_speed": 15},
            "雷霆之怒": {"type": "weapon", "effect": "attack", "value": 125, "description": "风暴领主的武器，召唤雷电", "durability": 300,
                        "bonus_attack": 125, "bonus_magic": 45, "chain_lightning": True},
            
            # ========== 盔甲系统 ==========
            # 基础盔甲
            "皮甲": {"type": "armor", "effect": "defense", "value": 5, "description": "简单的皮甲，提供基础防护", "durability": 30,
                   "bonus_defense": 5, "bonus_hp": 0, "bonus_dodge": 0},
            "铜甲": {"type": "armor", "effect": "defense", "value": 10, "description": "基础的铜制盔甲，增加10点防御力", "durability": 50,
                    "bonus_defense": 10, "bonus_hp": 0, "bonus_dodge": 0},
            "铁甲": {"type": "armor", "effect": "defense", "value": 20, "description": "坚固的铁制盔甲，增加20点防御力", "durability": 80,
                    "bonus_defense": 20, "bonus_hp": 10, "bonus_dodge": -5},
            "银甲": {"type": "armor", "effect": "defense", "value": 30, "description": "华丽的银制盔甲，增加30点防御力", "durability": 100,
                    "bonus_defense": 30, "bonus_hp": 20, "bonus_magic_resist": 10},
            "金甲": {"type": "armor", "effect": "defense", "value": 40, "description": "奢华的金制盔甲，增加40点防御力", "durability": 120,
                    "bonus_defense": 40, "bonus_hp": 30, "bonus_gold": 15},
            "秘银甲": {"type": "armor", "effect": "defense", "value": 50, "description": "轻便的秘银盔甲，增加50点防御力", "durability": 150,
                      "bonus_defense": 50, "bonus_hp": 40, "bonus_speed": 10},
            "精金甲": {"type": "armor", "effect": "defense", "value": 70, "description": "坚固的精金盔甲，增加70点防御力", "durability": 200,
                      "bonus_defense": 70, "bonus_hp": 60, "bonus_thorns": 10},
            "奥金甲": {"type": "armor", "effect": "defense", "value": 90, "description": "魔法增强的奥金盔甲，增加90点防御力", "durability": 250,
                      "bonus_defense": 90, "bonus_hp": 80, "bonus_magic_resist": 20},
            "星铁甲": {"type": "armor", "effect": "defense", "value": 120, "description": "星辰之力加持的创世盔甲，增加120点防御力", "durability": 500,
                      "bonus_defense": 120, "bonus_hp": 100, "bonus_all_resist": 25},
            
            # 特殊盔甲
            "龙鳞甲": {"type": "armor", "effect": "defense", "value": 100, "description": "用龙鳞制作的强大盔甲，增加100点防御力", "durability": 300,
                      "bonus_defense": 100, "bonus_hp": 150, "bonus_fire_resist": 50},
            "冰霜甲": {"type": "armor", "effect": "defense", "value": 85, "description": "极寒之地锻造的冰霜盔甲", "durability": 250,
                      "bonus_defense": 85, "bonus_hp": 100, "bonus_ice_resist": 50, "freeze_aura": True},
            "火焰甲": {"type": "armor", "effect": "defense", "value": 85, "description": "火山深处锻造的火焰盔甲", "durability": 250,
                      "bonus_defense": 85, "bonus_hp": 100, "bonus_fire_resist": 50, "burn_aura": True},
            "暗影甲": {"type": "armor", "effect": "defense", "value": 90, "description": "暗影界的神秘盔甲，增加闪避", "durability": 250,
                      "bonus_defense": 90, "bonus_hp": 80, "bonus_dodge": 15},
            "光明甲": {"type": "armor", "effect": "defense", "value": 95, "description": "天使祝福的光明盔甲", "durability": 280,
                      "bonus_defense": 95, "bonus_hp": 120, "bonus_heal": 10},
            
            # ========== 饰品/宝石系统 ==========
            # 普通宝石
            "普通红宝石": {"type": "gem", "effect": "attack", "value": 5, "description": "增加5点攻击力", "durability": 0,
                         "bonus_attack": 5, "bonus_crit": 2},
            "普通蓝宝石": {"type": "gem", "effect": "defense", "value": 5, "description": "增加5点防御力", "durability": 0,
                         "bonus_defense": 5, "bonus_magic_resist": 5},
            "普通绿宝石": {"type": "gem", "effect": "hp", "value": 20, "description": "增加20点生命值", "durability": 0,
                         "bonus_hp": 20, "bonus_heal": 5},
            "普通黄宝石": {"type": "gem", "effect": "gold", "value": 10, "description": "增加10%金币掉落", "durability": 0,
                         "bonus_gold": 10},
            "普通紫宝石": {"type": "gem", "effect": "exp", "value": 10, "description": "增加10%经验获取", "durability": 0,
                         "bonus_exp": 10},
            "普通橙宝石": {"type": "gem", "effect": "luck", "value": 5, "description": "增加5点幸运", "durability": 0,
                         "bonus_luck": 5},
            "普通青宝石": {"type": "gem", "effect": "speed", "value": 5, "description": "增加5点速度", "durability": 0,
                         "bonus_speed": 5},
            
            # 魔法宝石
            "魔法红宝石": {"type": "gem", "effect": "attack", "value": 10, "description": "增加10点攻击力", "durability": 0,
                         "bonus_attack": 10, "bonus_crit": 5},
            "魔法蓝宝石": {"type": "gem", "effect": "defense", "value": 10, "description": "增加10点防御力", "durability": 0,
                         "bonus_defense": 10, "bonus_magic_resist": 10},
            "魔法绿宝石": {"type": "gem", "effect": "hp", "value": 50, "description": "增加50点生命值", "durability": 0,
                         "bonus_hp": 50, "bonus_heal": 10},
            "魔法黄宝石": {"type": "gem", "effect": "gold", "value": 20, "description": "增加20%金币掉落", "durability": 0,
                         "bonus_gold": 20},
            "魔法紫宝石": {"type": "gem", "effect": "exp", "value": 20, "description": "增加20%经验获取", "durability": 0,
                         "bonus_exp": 20},
            "魔法橙宝石": {"type": "gem", "effect": "luck", "value": 10, "description": "增加10点幸运", "durability": 0,
                         "bonus_luck": 10},
            "魔法青宝石": {"type": "gem", "effect": "speed", "value": 10, "description": "增加10点速度", "durability": 0,
                         "bonus_speed": 10},
            
            # 稀有宝石
            "稀有红宝石": {"type": "gem", "effect": "attack", "value": 20, "description": "增加20点攻击力", "durability": 0,
                         "bonus_attack": 20, "bonus_crit": 10},
            "稀有蓝宝石": {"type": "gem", "effect": "defense", "value": 20, "description": "增加20点防御力", "durability": 0,
                         "bonus_defense": 20, "bonus_magic_resist": 20},
            "稀有绿宝石": {"type": "gem", "effect": "hp", "value": 100, "description": "增加100点生命值", "durability": 0,
                         "bonus_hp": 100, "bonus_heal": 15},
            "稀有黄宝石": {"type": "gem", "effect": "gold", "value": 30, "description": "增加30%金币掉落", "durability": 0,
                         "bonus_gold": 30},
            "稀有紫宝石": {"type": "gem", "effect": "exp", "value": 30, "description": "增加30%经验获取", "durability": 0,
                         "bonus_exp": 30},
            "稀有橙宝石": {"type": "gem", "effect": "luck", "value": 15, "description": "增加15点幸运", "durability": 0,
                         "bonus_luck": 15},
            "稀有青宝石": {"type": "gem", "effect": "speed", "value": 15, "description": "增加15点速度", "durability": 0,
                         "bonus_speed": 15},
            
            # 史诗宝石
            "史诗红宝石": {"type": "gem", "effect": "attack", "value": 35, "description": "增加35点攻击力", "durability": 0,
                         "bonus_attack": 35, "bonus_crit": 15},
            "史诗蓝宝石": {"type": "gem", "effect": "defense", "value": 35, "description": "增加35点防御力", "durability": 0,
                         "bonus_defense": 35, "bonus_magic_resist": 30},
            "史诗绿宝石": {"type": "gem", "effect": "hp", "value": 200, "description": "增加200点生命值", "durability": 0,
                         "bonus_hp": 200, "bonus_heal": 20},
            "史诗黄宝石": {"type": "gem", "effect": "gold", "value": 40, "description": "增加40%金币掉落", "durability": 0,
                         "bonus_gold": 40},
            "史诗紫宝石": {"type": "gem", "effect": "exp", "value": 40, "description": "增加40%经验获取", "durability": 0,
                         "bonus_exp": 40},
            "史诗橙宝石": {"type": "gem", "effect": "luck", "value": 20, "description": "增加20点幸运", "durability": 0,
                         "bonus_luck": 20},
            "史诗青宝石": {"type": "gem", "effect": "speed", "value": 20, "description": "增加20点速度", "durability": 0,
                         "bonus_speed": 20},
            
            # 传说宝石
            "传说红宝石": {"type": "gem", "effect": "attack", "value": 50, "description": "增加50点攻击力", "durability": 0,
                         "bonus_attack": 50, "bonus_crit": 20},
            "传说蓝宝石": {"type": "gem", "effect": "defense", "value": 50, "description": "增加50点防御力", "durability": 0,
                         "bonus_defense": 50, "bonus_magic_resist": 40},
            "传说绿宝石": {"type": "gem", "effect": "hp", "value": 300, "description": "增加300点生命值", "durability": 0,
                         "bonus_hp": 300, "bonus_heal": 25},
            "传说黄宝石": {"type": "gem", "effect": "gold", "value": 50, "description": "增加50%金币掉落", "durability": 0,
                         "bonus_gold": 50},
            "传说紫宝石": {"type": "gem", "effect": "exp", "value": 50, "description": "增加50%经验获取", "durability": 0,
                         "bonus_exp": 50},
            "传说橙宝石": {"type": "gem", "effect": "luck", "value": 25, "description": "增加25点幸运", "durability": 0,
                         "bonus_luck": 25},
            "传说青宝石": {"type": "gem", "effect": "speed", "value": 25, "description": "增加25点速度", "durability": 0,
                         "bonus_speed": 25},
            
            # 神话宝石
            "神话红宝石": {"type": "gem", "effect": "attack", "value": 75, "description": "增加75点攻击力", "durability": 0,
                         "bonus_attack": 75, "bonus_crit": 25},
            "神话蓝宝石": {"type": "gem", "effect": "defense", "value": 75, "description": "增加75点防御力", "durability": 0,
                         "bonus_defense": 75, "bonus_magic_resist": 50},
            "神话绿宝石": {"type": "gem", "effect": "hp", "value": 500, "description": "增加500点生命值", "durability": 0,
                         "bonus_hp": 500, "bonus_heal": 30},
            "神话黄宝石": {"type": "gem", "effect": "gold", "value": 60, "description": "增加60%金币掉落", "durability": 0,
                         "bonus_gold": 60},
            "神话紫宝石": {"type": "gem", "effect": "exp", "value": 60, "description": "增加60%经验获取", "durability": 0,
                         "bonus_exp": 60},
            "神话橙宝石": {"type": "gem", "effect": "luck", "value": 30, "description": "增加30点幸运", "durability": 0,
                         "bonus_luck": 30},
            "神话青宝石": {"type": "gem", "effect": "speed", "value": 30, "description": "增加30点速度", "durability": 0,
                         "bonus_speed": 30},
            
            # 创世宝石
            "创世红宝石": {"type": "gem", "effect": "attack", "value": 100, "description": "增加100点攻击力", "durability": 0,
                         "bonus_attack": 100, "bonus_crit": 30},
            "创世蓝宝石": {"type": "gem", "effect": "defense", "value": 100, "description": "增加100点防御力", "durability": 0,
                         "bonus_defense": 100, "bonus_magic_resist": 60},
            "创世绿宝石": {"type": "gem", "effect": "hp", "value": 1000, "description": "增加1000点生命值", "durability": 0,
                         "bonus_hp": 1000, "bonus_heal": 50},
            "创世黄宝石": {"type": "gem", "effect": "gold", "value": 75, "description": "增加75%金币掉落", "durability": 0,
                         "bonus_gold": 75},
            "创世紫宝石": {"type": "gem", "effect": "exp", "value": 75, "description": "增加75%经验获取", "durability": 0,
                         "bonus_exp": 75},
            "创世橙宝石": {"type": "gem", "effect": "luck", "value": 50, "description": "增加50点幸运", "durability": 0,
                         "bonus_luck": 50},
            "创世青宝石": {"type": "gem", "effect": "speed", "value": 50, "description": "增加50点速度", "durability": 0,
                         "bonus_speed": 50},
            
            # 特殊饰品
            "全能宝石": {"type": "gem", "effect": "all", "value": 10, "description": "增加所有属性10%", "durability": 0,
                       "bonus_all_percent": 10},
            "生命宝石": {"type": "gem", "effect": "hp_regen", "value": 5, "description": "每回合恢复5点生命值", "durability": 0,
                       "hp_regen": 5},
            "魔法宝石": {"type": "gem", "effect": "mana_regen", "value": 5, "description": "每回合恢复5点魔法值", "durability": 0,
                       "mana_regen": 5},
            "吸血宝石": {"type": "gem", "effect": "lifesteal", "value": 10, "description": "造成伤害的10%转化为生命", "durability": 0,
                       "lifesteal": 10},
            "反伤宝石": {"type": "gem", "effect": "thorns", "value": 10, "description": "反弹10%受到的伤害", "durability": 0,
                       "thorns": 10},
            "格挡宝石": {"type": "gem", "effect": "block", "value": 10, "description": "10%几率格挡伤害", "durability": 0,
                       "block_chance": 10},
            "暴击宝石": {"type": "gem", "effect": "crit", "value": 10, "description": "增加10%暴击率", "durability": 0,
                       "crit_chance": 10},
            "闪避宝石": {"type": "gem", "effect": "dodge", "value": 10, "description": "增加10%闪避率", "durability": 0,
                       "dodge_chance": 10},
            
            # 魔法饰品
            "魔法戒指": {"type": "accessory", "effect": "magic", "value": 15, "description": "增加15点魔法攻击力", "durability": 100,
                       "bonus_magic": 15},
            "防御戒指": {"type": "accessory", "effect": "defense", "value": 10, "description": "增加10点防御力", "durability": 100,
                       "bonus_defense": 10},
            "生命戒指": {"type": "accessory", "effect": "hp", "value": 50, "description": "增加50点生命值", "durability": 100,
                       "bonus_hp": 50},
            "速度戒指": {"type": "accessory", "effect": "speed", "value": 10, "description": "增加10点速度", "durability": 100,
                       "bonus_speed": 10},
            "幸运护符": {"type": "accessory", "effect": "luck", "value": 10, "description": "增加10点幸运", "durability": 100,
                       "bonus_luck": 10},
            
            # 材料
            "木材": {"type": "material", "effect": "craft", "value": 5, "description": "用于制作或交易，可合成基础物品", "durability": 0, "craft_recipes": ["木剑", "木盾"]},
            "矿石": {"type": "material", "effect": "craft", "value": 8, "description": "用于制作装备，可锻造基础武器", "durability": 0, "craft_recipes": ["铜剑", "铜甲"]},
            "铜矿石": {"type": "material", "effect": "craft", "value": 30, "description": "基础锻造材料，可锻造铜制装备", "durability": 0, "craft_recipes": ["铜剑", "铜甲"]},
            "铁矿石": {"type": "material", "effect": "craft", "value": 60, "description": "中级锻造材料，可锻造铁制装备", "durability": 0, "craft_recipes": ["铁剑", "铁甲"]},
            "银矿石": {"type": "material", "effect": "craft", "value": 100, "description": "高级锻造材料，可锻造银制装备", "durability": 0, "craft_recipes": ["银剑", "银甲"]},
            "金矿石": {"type": "material", "effect": "craft", "value": 200, "description": "稀有锻造材料，可锻造金制装备", "durability": 0, "craft_recipes": ["金剑", "金甲"]},
            "秘银矿石": {"type": "material", "effect": "craft", "value": 300, "description": "史诗级锻造材料，可锻造秘银装备", "durability": 0, "craft_recipes": ["秘银剑", "秘银甲"]},
            "精金矿石": {"type": "material", "effect": "craft", "value": 500, "description": "传说级锻造材料，可锻造精金装备", "durability": 0, "craft_recipes": ["精金剑", "精金甲"]},
            "奥金矿石": {"type": "material", "effect": "craft", "value": 800, "description": "神话级锻造材料，可锻造奥金装备", "durability": 0, "craft_recipes": ["奥金剑", "奥金甲"]},
            "星铁矿石": {"type": "material", "effect": "craft", "value": 1200, "description": "创世级锻造材料，可锻造星铁装备", "durability": 0, "craft_recipes": ["星铁剑", "星铁甲"]},
            
            "普通宝石碎片": {"type": "material", "effect": "craft", "value": 50, "description": "基础的宝石碎片，可合成普通宝石", "durability": 0, "craft_recipes": ["普通红宝石", "普通蓝宝石", "普通绿宝石"]},
            "魔法宝石碎片": {"type": "material", "effect": "craft", "value": 150, "description": "蕴含魔法的宝石碎片，可合成魔法宝石", "durability": 0, "craft_recipes": ["魔法红宝石", "魔法蓝宝石", "魔法绿宝石"]},
            "稀有宝石碎片": {"type": "material", "effect": "craft", "value": 300, "description": "稀有的宝石碎片，可合成稀有宝石", "durability": 0, "craft_recipes": ["稀有红宝石", "稀有蓝宝石", "稀有绿宝石"]},
            "史诗宝石碎片": {"type": "material", "effect": "craft", "value": 500, "description": "史诗级的宝石碎片，可合成史诗宝石", "durability": 0, "craft_recipes": ["史诗红宝石", "史诗蓝宝石", "史诗绿宝石"]},
            "传说宝石碎片": {"type": "material", "effect": "craft", "value": 800, "description": "传说级的宝石碎片，可合成传说宝石", "durability": 0, "craft_recipes": ["传说红宝石", "传说蓝宝石", "传说绿宝石"]},
            "神话宝石碎片": {"type": "material", "effect": "craft", "value": 1200, "description": "神话级的宝石碎片，可合成神话宝石", "durability": 0, "craft_recipes": ["神话红宝石", "神话蓝宝石", "神话绿宝石"]},
            "创世宝石碎片": {"type": "material", "effect": "craft", "value": 2000, "description": "创世级的宝石碎片，可合成创世宝石", "durability": 0, "craft_recipes": ["创世红宝石", "创世蓝宝石", "创世绿宝石"]},
            
            # 元素精华
            "火焰精华": {"type": "material", "effect": "craft", "value": 100, "description": "火焰元素的精华，可合成火焰武器和药水", "durability": 0, "craft_recipes": ["火焰剑", "火焰药水"]},
            "冰霜精华": {"type": "material", "effect": "craft", "value": 100, "description": "冰霜元素的精华，可合成冰霜武器和药水", "durability": 0, "craft_recipes": ["冰霜剑", "冰霜药水"]},
            "雷电精华": {"type": "material", "effect": "craft", "value": 100, "description": "雷电元素的精华，可合成雷电武器和药水", "durability": 0, "craft_recipes": ["雷电剑", "雷电药水"]},
            "自然精华": {"type": "material", "effect": "craft", "value": 100, "description": "自然元素的精华，可合成治疗药水和自然武器", "durability": 0, "craft_recipes": ["治疗药水", "自然法杖"]},
            "暗影精华": {"type": "material", "effect": "craft", "value": 150, "description": "暗影元素的精华，可合成暗影武器和药水", "durability": 0, "craft_recipes": ["黑暗剑", "隐身药水"]},
            "光明精华": {"type": "material", "effect": "craft", "value": 150, "description": "光明元素的精华，可合成光明武器和药水", "durability": 0, "craft_recipes": ["光明剑", "神圣药水"]},
            
            # 龙类材料
            "龙鳞": {"type": "material", "effect": "craft", "value": 200, "description": "龙身上脱落的鳞片，极其珍贵，可制作龙鳞甲", "durability": 0, "craft_recipes": ["龙鳞甲"]},
            "龙心": {"type": "treasure", "effect": "consumable", "value": 500, "description": "龙的心脏，蕴含强大的生命力，使用后大幅增加属性", "durability": 1, "bonus_all": 20, "bonus_hp": 500},
            "龙血": {"type": "material", "effect": "craft", "value": 250, "description": "龙的血液，蕴含强大的生命力量，可制作龙血药水", "durability": 0, "craft_recipes": ["龙血药水"]},
            "远古龙鳞": {"type": "material", "effect": "craft", "value": 350, "description": "远古巨龙的鳞片，蕴含强大的龙之力，可制作远古龙鳞甲", "durability": 0, "craft_recipes": ["远古龙鳞甲"]},
            
            # 其他材料
            "空瓶": {"type": "material", "effect": "craft", "value": 10, "description": "用于装药水的空瓶子，可制作各种药水", "durability": 0, "craft_recipes": ["治疗药水", "魔法药水"]},
            "皮革": {"type": "material", "effect": "craft", "value": 15, "description": "动物皮革，可用于制作皮甲和其他装备", "durability": 0, "craft_recipes": ["皮甲", "皮靴"]},
            "魔法水晶": {"type": "material", "effect": "craft", "value": 100, "description": "蕴含强大魔法能量的水晶，可制作魔法武器和饰品", "durability": 0, "craft_recipes": ["魔法戒指", "魔法剑"]},
            "魔法水晶碎片": {"type": "material", "effect": "craft", "value": 30, "description": "魔法水晶的碎片，仍有微弱能量，可合成魔法水晶", "durability": 0, "craft_recipes": ["魔法水晶"]},
            "生命之花": {"type": "material", "effect": "craft", "value": 150, "description": "蕴含强大生命力的花朵，可制作生命药水和治疗物品", "durability": 0, "craft_recipes": ["生命药水", "超级治疗药水"]},
            "灵魂石": {"type": "material", "effect": "craft", "value": 150, "description": "能够储存灵魂的神秘石头，可制作灵魂相关物品", "durability": 0, "craft_recipes": ["复活药水", "灵魂项链"]},
            
            # 宝藏
            "古代金币": {"type": "treasure", "effect": "consumable", "value": 50, "description": "价值连城的古代金币，使用后获得500金币", "durability": 1, "bonus_gold": 500},
            "皇家宝物": {"type": "treasure", "effect": "consumable", "value": 200, "description": "珍贵的皇家宝物，使用后获得2000金币", "durability": 1, "bonus_gold": 2000},
            "沉船宝藏": {"type": "treasure", "effect": "consumable", "value": 200, "description": "从沉船上发现的珍贵宝藏，使用后获得2000金币和随机物品", "durability": 1, "bonus_gold": 2000, "random_item": True},
            "宝藏": {"type": "treasure", "effect": "consumable", "value": 500, "description": "传说中的宝藏，价值连城，使用后获得5000金币和稀有物品", "durability": 1, "bonus_gold": 5000, "rare_item": True},
            
            # 缺失的物品定义
            # 消耗品
            "药水": {"type": "consumable", "effect": "heal", "value": 30, "description": "恢复30点生命值", "durability": 1},
            "稀有药水": {"type": "consumable", "effect": "heal", "value": 100, "description": "恢复100点生命值", "durability": 1},
            "生命药水": {"type": "consumable", "effect": "heal", "value": 80, "description": "恢复80点生命值", "durability": 1},
            "飞行药水": {"type": "consumable", "effect": "special", "value": 0, "description": "允许短时间飞行", "durability": 1},
            "隐身药水": {"type": "consumable", "effect": "special", "value": 0, "description": "让使用者隐身，避免战斗", "durability": 1},
            "解毒草药": {"type": "consumable", "effect": "special", "value": 0, "description": "解除中毒状态", "durability": 1},
            "治愈草药": {"type": "consumable", "effect": "heal", "value": 40, "description": "恢复40点生命值", "durability": 1},
            "毒蘑菇": {"type": "consumable", "effect": "special", "value": 0, "description": "造成中毒伤害", "durability": 1},
            "矮人啤酒": {"type": "consumable", "effect": "buff_attack", "value": 5, "description": "临时增加5点攻击力", "durability": 1},
            "樱花茶": {"type": "consumable", "effect": "heal", "value": 25, "description": "恢复25点生命值", "durability": 1},
            "快乐糖果": {"type": "consumable", "effect": "buff_luck", "value": 5, "description": "临时增加5点幸运", "durability": 1},
            
            # 材料
            "仙人掌": {"type": "material", "effect": None, "value": 10, "description": "沙漠植物，可用于制作药水", "durability": 0},
            "沙漠玫瑰": {"type": "material", "effect": None, "value": 20, "description": "沙漠中的稀有花朵", "durability": 0},
            "古老的箭头": {"type": "material", "effect": None, "value": 15, "description": "古代遗留的箭头", "durability": 0},
            "火焰水晶": {"type": "material", "effect": None, "value": 80, "description": "蕴含火焰能量的水晶", "durability": 0},
            "火山灰": {"type": "material", "effect": None, "value": 15, "description": "火山喷发留下的灰烬", "durability": 0},
            "冰晶": {"type": "material", "effect": None, "value": 60, "description": "寒冷地区的冰晶", "durability": 0},
            "雪莲花": {"type": "material", "effect": None, "value": 40, "description": "生长在雪山的稀有花朵", "durability": 0},
            "冰冻核心": {"type": "material", "effect": None, "value": 120, "description": "蕴含冰霜能量的核心", "durability": 0},
            "古代文物": {"type": "treasure", "effect": None, "value": 300, "description": "古代文明的文物", "durability": 0},
            "神秘符文": {"type": "material", "effect": None, "value": 70, "description": "刻有神秘符号的石头", "durability": 0},
            "失落的技术": {"type": "material", "effect": None, "value": 400, "description": "古代失落的技术图纸", "durability": 0},
            "火焰宝石": {"type": "material", "effect": None, "value": 150, "description": "蕴含火焰力量的宝石", "durability": 0},
            "水晶": {"type": "material", "effect": None, "value": 30, "description": "普通的水晶", "durability": 0},
            "锁链": {"type": "material", "effect": None, "value": 20, "description": "坚固的锁链", "durability": 0},
            "钥匙": {"type": "material", "effect": None, "value": 25, "description": "通用钥匙", "durability": 0},
            "囚犯的日记": {"type": "treasure", "effect": None, "value": 100, "description": "囚犯写下的日记，记录了监狱的秘密", "durability": 0},
            "宝石": {"type": "material", "effect": None, "value": 50, "description": "普通的宝石", "durability": 0},
            "沼泽水晶": {"type": "material", "effect": None, "value": 60, "description": "沼泽中发现的水晶", "durability": 0},
            "水晶碎片": {"type": "material", "effect": None, "value": 20, "description": "水晶的碎片", "durability": 0},
            "能量核心": {"type": "material", "effect": None, "value": 200, "description": "蕴含强大能量的核心", "durability": 0},
            "冥界之火": {"type": "material", "effect": None, "value": 180, "description": "来自冥界的火焰", "durability": 0},
            "死亡契约": {"type": "treasure", "effect": None, "value": 350, "description": "与死神签订的契约", "durability": 0},
            "暗影水晶": {"type": "material", "effect": None, "value": 120, "description": "蕴含暗影能量的水晶", "durability": 0},
            "智慧卷轴": {"type": "treasure", "effect": None, "value": 150, "description": "记载着智慧的卷轴", "durability": 0},
            "知识结晶": {"type": "material", "effect": None, "value": 250, "description": "知识的结晶", "durability": 0},
            "机械零件": {"type": "material", "effect": None, "value": 40, "description": "机械装置的零件", "durability": 0},
            "蒸汽核心": {"type": "material", "effect": None, "value": 150, "description": "蒸汽机的核心部件", "durability": 0},
            "魔法电池": {"type": "material", "effect": None, "value": 100, "description": "储存魔法能量的电池", "durability": 0},
            "恶魔之角": {"type": "material", "effect": None, "value": 200, "description": "恶魔的角", "durability": 0},
            "地狱火石": {"type": "material", "effect": None, "value": 180, "description": "来自地狱的火石", "durability": 0},
            "黑暗灵魂石": {"type": "material", "effect": None, "value": 300, "description": "储存黑暗灵魂的石头", "durability": 0},
            "云朵精华": {"type": "material", "effect": None, "value": 120, "description": "云朵的精华", "durability": 0},
            "风之水晶": {"type": "material", "effect": None, "value": 100, "description": "蕴含风元素能量的水晶", "durability": 0},
            "浮空石": {"type": "material", "effect": None, "value": 250, "description": "能够漂浮的神奇石头", "durability": 0},
            "天空草": {"type": "material", "effect": None, "value": 30, "description": "生长在天空中的草", "durability": 0},
            "飞行羽毛": {"type": "material", "effect": None, "value": 80, "description": "能够飞行的神奇羽毛", "durability": 0},
            "天空宝石": {"type": "material", "effect": None, "value": 150, "description": "天空中发现的宝石", "durability": 0},
            "天使羽毛": {"type": "material", "effect": None, "value": 200, "description": "天使的羽毛", "durability": 0},
            "飞行罗盘": {"type": "treasure", "effect": None, "value": 120, "description": "指引飞行方向的罗盘", "durability": 0},
            "天空地图": {"type": "treasure", "effect": None, "value": 150, "description": "天空区域的地图", "durability": 0},
            "天空花": {"type": "material", "effect": None, "value": 50, "description": "生长在天空的花朵", "durability": 0},
            "魔法种子": {"type": "material", "effect": None, "value": 60, "description": "能够长出魔法植物的种子", "durability": 0},
            "时光沙漏": {"type": "treasure", "effect": None, "value": 300, "description": "能够掌控时间的沙漏", "durability": 0},
            "预言水晶": {"type": "treasure", "effect": None, "value": 250, "description": "能够预言未来的水晶", "durability": 0},
            "时间碎片": {"type": "material", "effect": None, "value": 180, "description": "时间的碎片", "durability": 0},
            "精灵之尘": {"type": "material", "effect": None, "value": 100, "description": "精灵留下的尘粉", "durability": 0},
            "自然水晶": {"type": "material", "effect": None, "value": 80, "description": "蕴含自然能量的水晶", "durability": 0},
            "星尘": {"type": "material", "effect": None, "value": 120, "description": "星星的尘埃", "durability": 0},
            "流星碎片": {"type": "material", "effect": None, "value": 150, "description": "流星的碎片", "durability": 0},
            "天文望远镜": {"type": "treasure", "effect": None, "value": 200, "description": "观察星空的望远镜", "durability": 0},
            "神圣光环": {"type": "accessory", "effect": "defense", "value": 100, "description": "神圣的光环，增加防御力", "durability": 150, "bonus_defense": 20, "bonus_magic_resist": 15},
            "神之祝福": {"type": "treasure", "effect": None, "value": 500, "description": "神灵的祝福", "durability": 0},
            "世界之心": {"type": "treasure", "effect": None, "value": 1000, "description": "世界的核心", "durability": 0},
            "永恒水晶": {"type": "material", "effect": None, "value": 800, "description": "永恒的水晶", "durability": 0},
            "石器": {"type": "material", "effect": None, "value": 10, "description": "原始的石器", "durability": 0},
            "古代壁画": {"type": "treasure", "effect": None, "value": 200, "description": "古代的壁画", "durability": 0},
            "史前骨制品": {"type": "material", "effect": None, "value": 30, "description": "史前生物的骨制品", "durability": 0},
            "魔法卷轴": {"type": "treasure", "effect": None, "value": 100, "description": "记载魔法咒语的卷轴", "durability": 0},
            "中世纪盔甲": {"type": "armor", "effect": "defense", "value": 150, "description": "中世纪的盔甲", "durability": 150, "bonus_defense": 35, "bonus_hp": 50},
            "蒸汽机零件": {"type": "material", "effect": None, "value": 60, "description": "蒸汽机的零件", "durability": 0},
            "工业蓝图": {"type": "treasure", "effect": None, "value": 250, "description": "工业革命的蓝图", "durability": 0},
            "机械工具": {"type": "material", "effect": None, "value": 50, "description": "机械加工工具", "durability": 0},
            "激光武器": {"type": "weapon", "effect": "attack", "value": 300, "description": "未来的激光武器", "durability": 200, "bonus_attack": 80, "bonus_magic": 30},
            "智能芯片": {"type": "material", "effect": None, "value": 200, "description": "未来的智能芯片", "durability": 0},
            "未来科技": {"type": "treasure", "effect": None, "value": 500, "description": "未来的科技产品", "durability": 0},
            "辐射防护装备": {"type": "armor", "effect": "defense", "value": 200, "description": "防辐射的装备", "durability": 180, "bonus_defense": 40, "bonus_magic_resist": 25},
            "废土物资": {"type": "material", "effect": None, "value": 40, "description": "废土中的物资", "durability": 0},
            "战前科技": {"type": "treasure", "effect": None, "value": 350, "description": "战争前的科技", "durability": 0},
            "法老宝藏": {"type": "treasure", "effect": None, "value": 400, "description": "法老的宝藏", "durability": 0},
            "象形文字卷轴": {"type": "treasure", "effect": None, "value": 200, "description": "刻有象形文字的卷轴", "durability": 0},
            "沙漠圣物": {"type": "treasure", "effect": None, "value": 300, "description": "沙漠中的圣物", "durability": 0},
            "维京战斧": {"type": "weapon", "effect": "attack", "value": 180, "description": "维京人的战斧", "durability": 150, "bonus_attack": 60, "bonus_crit": 10},
            "北欧符文": {"type": "material", "effect": None, "value": 100, "description": "北欧的神秘符文", "durability": 0},
            "武士刀": {"type": "weapon", "effect": "attack", "value": 200, "description": "日本武士的刀", "durability": 180, "bonus_attack": 65, "bonus_speed": 10},
            "忍者工具": {"type": "material", "effect": None, "value": 80, "description": "忍者使用的工具", "durability": 0},
            "太空装备": {"type": "armor", "effect": "defense", "value": 400, "description": "太空用的装备", "durability": 250, "bonus_defense": 60, "bonus_magic_resist": 30},
            "外星科技": {"type": "treasure", "effect": None, "value": 800, "description": "外星人的科技", "durability": 0},
            "星际货币": {"type": "treasure", "effect": None, "value": 200, "description": "星际通用货币", "durability": 0},
            "时空宝石": {"type": "material", "effect": None, "value": 500, "description": "掌控时空的宝石", "durability": 0},
            "时间之钟": {"type": "treasure", "effect": None, "value": 400, "description": "掌控时间的钟", "durability": 0},
            "梦境精华": {"type": "material", "effect": None, "value": 200, "description": "梦境的精华", "durability": 0},
            "幸福回忆": {"type": "treasure", "effect": None, "value": 150, "description": "幸福的回忆", "durability": 0},
            "甜美果实": {"type": "consumable", "effect": "heal", "value": 35, "description": "恢复35点生命值", "durability": 1},
            "勇气之石": {"type": "accessory", "effect": "attack", "value": 120, "description": "增加勇气和攻击力", "durability": 100, "bonus_attack": 15, "bonus_luck": 5},
            "噩梦碎片": {"type": "material", "effect": None, "value": 120, "description": "噩梦的碎片", "durability": 0},
            "恐惧精华": {"type": "material", "effect": None, "value": 150, "description": "恐惧的精华", "durability": 0},
            "奇幻果实": {"type": "consumable", "effect": "buff_magic", "value": 15, "description": "临时增加15点魔法攻击力", "durability": 1},
            "梦境宝石": {"type": "material", "effect": None, "value": 300, "description": "梦境中的宝石", "durability": 0},
            "冒险装备": {"type": "armor", "effect": "defense", "value": 120, "description": "冒险用的装备", "durability": 120, "bonus_defense": 30, "bonus_speed": 5},
            "宝藏地图": {"type": "treasure", "effect": None, "value": 180, "description": "宝藏的地图", "durability": 0},
            "冒险笔记": {"type": "treasure", "effect": None, "value": 100, "description": "冒险家的笔记", "durability": 0},
            "爱情结晶": {"type": "treasure", "effect": None, "value": 250, "description": "爱情的结晶", "durability": 0},
            "浪漫花朵": {"type": "material", "effect": None, "value": 40, "description": "浪漫的花朵", "durability": 0},
            "神秘水晶": {"type": "material", "effect": None, "value": 180, "description": "神秘的水晶", "durability": 0},
            "未知 artifact": {"type": "treasure", "effect": None, "value": 400, "description": "未知的 artifact", "durability": 0},
            "童年玩具": {"type": "treasure", "effect": None, "value": 100, "description": "童年的玩具", "durability": 0},
            "纯真回忆": {"type": "treasure", "effect": None, "value": 150, "description": "纯真的回忆", "durability": 0},
            "英雄装备": {"type": "armor", "effect": "defense", "value": 300, "description": "英雄的装备", "durability": 200, "bonus_defense": 50, "bonus_attack": 10},
            "勇气勋章": {"type": "accessory", "effect": "attack", "value": 150, "description": "勇气的勋章", "durability": 120, "bonus_attack": 20, "bonus_defense": 10},
            "正义结晶": {"type": "material", "effect": None, "value": 250, "description": "正义的结晶", "durability": 0},
            "宇宙尘埃": {"type": "material", "effect": None, "value": 120, "description": "宇宙中的尘埃", "durability": 0},
            "星际宝石": {"type": "material", "effect": None, "value": 400, "description": "星际中的宝石", "durability": 0},
            "黑洞结晶": {"type": "material", "effect": None, "value": 600, "description": "黑洞的结晶", "durability": 0},
            "梦境之心": {"type": "treasure", "effect": None, "value": 800, "description": "梦境的核心", "durability": 0},
            "现实碎片": {"type": "material", "effect": None, "value": 300, "description": "现实的碎片", "durability": 0},
            "宇宙精华": {"type": "material", "effect": None, "value": 1000, "description": "宇宙的精华", "durability": 0},
            
            # 装备
            "装备": {"type": "armor", "effect": "defense", "value": 50, "description": "基础装备", "durability": 100, "bonus_defense": 20},
            "魔法书": {"type": "accessory", "effect": "magic", "value": 100, "description": "增加魔法攻击力", "durability": 100, "bonus_magic": 25},
            "剑": {"type": "weapon", "effect": "attack", "value": 30, "description": "基础的剑", "durability": 80, "bonus_attack": 20},
            "法术书": {"type": "accessory", "effect": "magic", "value": 150, "description": "增加魔法攻击力", "durability": 120, "bonus_magic": 35},
            "魔法杖": {"type": "weapon", "effect": "attack", "value": 120, "description": "魔法杖", "durability": 100, "bonus_attack": 15, "bonus_magic": 40},
            "飞行扫帚": {"type": "accessory", "effect": "special", "value": 200, "description": "能够飞行的扫帚", "durability": 150},
            "海盗宝藏": {"type": "treasure", "effect": None, "value": 300, "description": "海盗的宝藏", "durability": 0},
            "骑士剑": {"type": "weapon", "effect": "attack", "value": 150, "description": "骑士的剑", "durability": 150, "bonus_attack": 50, "bonus_defense": 5}
        }
        
        # 合成配方数据
        self.crafting_recipes = {
            # 基础药剂合成
            "治疗药水": {
                "type": "consumable",
                "ingredients": {"草药": 2, "空瓶": 1},
                "result": {"item": "治疗药水", "quantity": 1},
                "description": "恢复50点生命值的基础药水"
            },
            "强力治疗药水": {
                "type": "consumable",
                "ingredients": {"治疗药水": 2, "生命之花": 1, "魔法水晶碎片": 2},
                "result": {"item": "强力治疗药水", "quantity": 1},
                "description": "恢复150点生命值的强力药水"
            },
            "超级治疗药水": {
                "type": "consumable",
                "ingredients": {"强力治疗药水": 2, "生命之花": 3, "魔法水晶": 1, "龙血": 1},
                "result": {"item": "超级治疗药水", "quantity": 1},
                "description": "完全恢复生命值的超级药水"
            },
            
            # 魔法药剂合成
            "魔法药水": {
                "type": "consumable",
                "ingredients": {"魔法草药": 3, "空瓶": 1, "魔法水晶碎片": 1},
                "result": {"item": "魔法药水", "quantity": 1},
                "description": "恢复50点魔法值的魔法药水"
            },
            "强力魔法药水": {
                "type": "consumable",
                "ingredients": {"魔法药水": 2, "元素精华": 1, "魔法水晶": 1},
                "result": {"item": "强力魔法药水", "quantity": 1},
                "description": "恢复150点魔法值的强力魔法药水"
            },
            "超级魔法药水": {
                "type": "consumable",
                "ingredients": {"强力魔法药水": 2, "灵魂石": 1, "魔法水晶": 2, "龙血": 1},
                "result": {"item": "超级魔法药水", "quantity": 1},
                "description": "完全恢复魔法值的超级魔法药水"
            },
            
            # 经验药剂合成
            "经验药水": {
                "type": "consumable",
                "ingredients": {"魔法书": 1, "魔法水晶碎片": 2, "空瓶": 1},
                "result": {"item": "经验药水", "quantity": 1},
                "description": "获得50点经验值"
            },
            "强力经验药水": {
                "type": "consumable",
                "ingredients": {"经验药水": 2, "智慧卷轴": 1, "魔法水晶": 1},
                "result": {"item": "强力经验药水", "quantity": 1},
                "description": "获得200点经验值"
            },
            "超级经验药水": {
                "type": "consumable",
                "ingredients": {"强力经验药水": 2, "知识结晶": 1, "灵魂石": 1, "龙血": 1},
                "result": {"item": "超级经验药水", "quantity": 1},
                "description": "获得500点经验值"
            },
            
            # 属性药剂合成
            "攻击药水": {
                "type": "consumable",
                "ingredients": {"力量精华": 2, "空瓶": 1, "魔法水晶碎片": 1},
                "result": {"item": "攻击药水", "quantity": 1},
                "description": "临时增加10点攻击力"
            },
            "防御药水": {
                "type": "consumable",
                "ingredients": {"守护精华": 2, "空瓶": 1, "魔法水晶碎片": 1},
                "result": {"item": "防御药水", "quantity": 1},
                "description": "临时增加10点防御力"
            },
            "速度药水": {
                "type": "consumable",
                "ingredients": {"风之精华": 2, "空瓶": 1, "轻盈羽毛": 1},
                "result": {"item": "速度药水", "quantity": 1},
                "description": "临时增加10点速度"
            },
            "幸运药水": {
                "type": "consumable",
                "ingredients": {"幸运草": 2, "空瓶": 1, "魔法水晶碎片": 1},
                "result": {"item": "幸运药水", "quantity": 1},
                "description": "临时增加10点幸运"
            },
            "魔法攻击药水": {
                "type": "consumable",
                "ingredients": {"魔法精华": 2, "空瓶": 1, "魔法水晶": 1},
                "result": {"item": "魔法攻击药水", "quantity": 1},
                "description": "临时增加10点魔法攻击力"
            },
            
            # 特殊药剂合成
            "隐形药水": {
                "type": "consumable",
                "ingredients": {"暗影精华": 2, "空瓶": 1, "魔法水晶": 1},
                "result": {"item": "隐形药水", "quantity": 1},
                "description": "让使用者隐身，避免战斗"
            },
            "解毒剂": {
                "type": "consumable",
                "ingredients": {"解毒草药": 2, "空瓶": 1, "魔法水晶碎片": 1},
                "result": {"item": "解毒剂", "quantity": 1},
                "description": "解除中毒状态"
            },
            "复活药水": {
                "type": "consumable",
                "ingredients": {"生命之花": 3, "灵魂石": 1, "龙血": 1, "魔法水晶": 2},
                "result": {"item": "复活药水", "quantity": 1},
                "description": "战斗中复活一次"
            },
            
            # 元素精华合成
            "火焰精华": {
                "type": "material",
                "ingredients": {"火元素": 1, "魔法水晶碎片": 3},
                "result": {"item": "火焰精华", "quantity": 1},
                "description": "火焰元素的精华"
            },
            "冰霜精华": {
                "type": "material",
                "ingredients": {"冰元素": 1, "魔法水晶碎片": 3},
                "result": {"item": "冰霜精华", "quantity": 1},
                "description": "冰霜元素的精华"
            },
            "雷电精华": {
                "type": "material",
                "ingredients": {"雷元素": 1, "魔法水晶碎片": 3},
                "result": {"item": "雷电精华", "quantity": 1},
                "description": "雷电元素的精华"
            },
            "自然精华": {
                "type": "material",
                "ingredients": {"生命之花": 2, "魔法水晶碎片": 2, "精灵之尘": 1},
                "result": {"item": "自然精华", "quantity": 1},
                "description": "自然元素的精华"
            },
            "暗影精华": {
                "type": "material",
                "ingredients": {"暗影核心": 1, "魔法水晶碎片": 3, "黑暗水晶": 1},
                "result": {"item": "暗影精华", "quantity": 1},
                "description": "暗影元素的精华"
            },
            "光明精华": {
                "type": "material",
                "ingredients": {"光明核心": 1, "魔法水晶碎片": 3, "治疗水晶": 1},
                "result": {"item": "光明精华", "quantity": 1},
                "description": "光明元素的精华"
            },
        }
        
        # 锻造配方数据 - 武器
        self.smithing_recipes = {
            "铜剑": {
                "type": "weapon",
                "ingredients": {"铜矿石": 3, "木材": 2},
                "result": {"item": "铜剑", "quantity": 1},
                "description": "基础的铜制长剑，增加15点攻击力"
            },
            "铁剑": {
                "type": "weapon",
                "ingredients": {"铁矿石": 3, "铜剑": 1, "木材": 2},
                "result": {"item": "铁剑", "quantity": 1},
                "description": "坚固的铁制长剑，增加25点攻击力"
            },
            "银剑": {
                "type": "weapon",
                "ingredients": {"银矿石": 3, "铁剑": 1, "魔法水晶碎片": 2},
                "result": {"item": "银剑", "quantity": 1},
                "description": "锋利的银制长剑，增加35点攻击力"
            },
            "金剑": {
                "type": "weapon",
                "ingredients": {"金矿石": 3, "银剑": 1, "魔法水晶": 1},
                "result": {"item": "金剑", "quantity": 1},
                "description": "华丽的金制长剑，增加45点攻击力"
            },
            "秘银剑": {
                "type": "weapon",
                "ingredients": {"秘银矿石": 3, "金剑": 1, "元素精华": 2, "魔法水晶": 1},
                "result": {"item": "秘银剑", "quantity": 1},
                "description": "轻巧的秘银长剑，增加60点攻击力"
            },
            "精金剑": {
                "type": "weapon",
                "ingredients": {"精金矿石": 3, "秘银剑": 1, "龙鳞": 2, "灵魂石": 1},
                "result": {"item": "精金剑", "quantity": 1},
                "description": "坚不可摧的精金长剑，增加80点攻击力"
            },
            "奥金剑": {
                "type": "weapon",
                "ingredients": {"奥金矿石": 3, "精金剑": 1, "龙心": 1, "远古龙鳞": 1},
                "result": {"item": "奥金剑", "quantity": 1},
                "description": "蕴含魔法力量的奥金长剑，增加100点攻击力"
            },
            "星铁剑": {
                "type": "weapon",
                "ingredients": {"星铁矿石": 3, "奥金剑": 1, "创世宝石碎片": 1, "神之祝福": 1},
                "result": {"item": "星铁剑", "quantity": 1},
                "description": "来自星辰的创世之剑，增加150点攻击力"
            },
            "火焰剑": {
                "type": "weapon",
                "ingredients": {"精金剑": 1, "火焰精华": 3, "龙鳞": 2, "魔法水晶": 2},
                "result": {"item": "火焰剑", "quantity": 1},
                "description": "附魔火焰的长剑，对火系敌人有加成"
            },
            "冰霜剑": {
                "type": "weapon",
                "ingredients": {"精金剑": 1, "冰霜精华": 3, "龙鳞": 2, "魔法水晶": 2},
                "result": {"item": "冰霜剑", "quantity": 1},
                "description": "附魔冰霜的长剑，对冰系敌人有加成"
            },
            "雷电剑": {
                "type": "weapon",
                "ingredients": {"精金剑": 1, "雷电精华": 3, "龙鳞": 2, "魔法水晶": 2},
                "result": {"item": "雷电剑", "quantity": 1},
                "description": "附魔雷电的长剑，有几率麻痹敌人"
            },
            
            # 盔甲锻造
            "皮甲": {
                "type": "armor",
                "ingredients": {"皮革": 4, "木材": 2},
                "result": {"item": "皮甲", "quantity": 1},
                "description": "简单的皮甲，提供基础防护"
            },
            "铜甲": {
                "type": "armor",
                "ingredients": {"铜矿石": 4, "皮革": 2},
                "result": {"item": "铜甲", "quantity": 1},
                "description": "基础的铜制盔甲，增加10点防御力"
            },
            "铁甲": {
                "type": "armor",
                "ingredients": {"铁矿石": 4, "铜甲": 1, "皮革": 2},
                "result": {"item": "铁甲", "quantity": 1},
                "description": "坚固的铁制盔甲，增加20点防御力"
            },
            "银甲": {
                "type": "armor",
                "ingredients": {"银矿石": 4, "铁甲": 1, "魔法水晶碎片": 2},
                "result": {"item": "银甲", "quantity": 1},
                "description": "华丽的银制盔甲，增加30点防御力"
            },
            "金甲": {
                "type": "armor",
                "ingredients": {"金矿石": 4, "银甲": 1, "魔法水晶": 1},
                "result": {"item": "金甲", "quantity": 1},
                "description": "奢华的金制盔甲，增加40点防御力"
            },
            "秘银甲": {
                "type": "armor",
                "ingredients": {"秘银矿石": 4, "金甲": 1, "元素精华": 2, "魔法水晶": 1},
                "result": {"item": "秘银甲", "quantity": 1},
                "description": "轻便的秘银盔甲，增加50点防御力"
            },
            "精金甲": {
                "type": "armor",
                "ingredients": {"精金矿石": 4, "秘银甲": 1, "龙鳞": 2, "灵魂石": 1},
                "result": {"item": "精金甲", "quantity": 1},
                "description": "坚固的精金盔甲，增加70点防御力"
            },
            "奥金甲": {
                "type": "armor",
                "ingredients": {"奥金矿石": 4, "精金甲": 1, "龙心": 1, "远古龙鳞": 1},
                "result": {"item": "奥金甲", "quantity": 1},
                "description": "魔法增强的奥金盔甲，增加90点防御力"
            },
            "星铁甲": {
                "type": "armor",
                "ingredients": {"星铁矿石": 4, "奥金甲": 1, "创世宝石碎片": 1, "神之祝福": 1},
                "result": {"item": "星铁甲", "quantity": 1},
                "description": "星辰之力加持的创世盔甲，增加120点防御力"
            },
            "龙鳞甲": {
                "type": "armor",
                "ingredients": {"精金甲": 1, "龙鳞": 5, "龙血": 2, "远古龙鳞": 2},
                "result": {"item": "龙鳞甲", "quantity": 1},
                "description": "用龙鳞制作的强大盔甲"
            },
        }
        
        # 宝石合成配方
        self.gem_recipes = {
            # 普通宝石合成
            "普通红宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "火焰精华": 1},
                "result": {"item": "普通红宝石", "quantity": 1},
                "description": "增加5点攻击力"
            },
            "普通蓝宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "冰霜精华": 1},
                "result": {"item": "普通蓝宝石", "quantity": 1},
                "description": "增加5点防御力"
            },
            "普通绿宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "自然精华": 1},
                "result": {"item": "普通绿宝石", "quantity": 1},
                "description": "增加20点生命值"
            },
            "普通黄宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "金矿石": 1},
                "result": {"item": "普通黄宝石", "quantity": 1},
                "description": "增加10%金币掉落"
            },
            "普通紫宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "魔法水晶碎片": 2},
                "result": {"item": "普通紫宝石", "quantity": 1},
                "description": "增加10%经验获取"
            },
            "普通橙宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "幸运草": 2},
                "result": {"item": "普通橙宝石", "quantity": 1},
                "description": "增加5点幸运"
            },
            "普通青宝石": {
                "type": "gem",
                "ingredients": {"普通宝石碎片": 3, "风之精华": 1},
                "result": {"item": "普通青宝石", "quantity": 1},
                "description": "增加5点速度"
            },
            
            # 魔法宝石合成
            "魔法红宝石": {
                "type": "gem",
                "ingredients": {"普通红宝石": 2, "魔法宝石碎片": 3, "火焰精华": 2},
                "result": {"item": "魔法红宝石", "quantity": 1},
                "description": "增加10点攻击力"
            },
            "魔法蓝宝石": {
                "type": "gem",
                "ingredients": {"普通蓝宝石": 2, "魔法宝石碎片": 3, "冰霜精华": 2},
                "result": {"item": "魔法蓝宝石", "quantity": 1},
                "description": "增加10点防御力"
            },
            "魔法绿宝石": {
                "type": "gem",
                "ingredients": {"普通绿宝石": 2, "魔法宝石碎片": 3, "自然精华": 2},
                "result": {"item": "魔法绿宝石", "quantity": 1},
                "description": "增加50点生命值"
            },
            "魔法黄宝石": {
                "type": "gem",
                "ingredients": {"普通黄宝石": 2, "魔法宝石碎片": 3, "金矿石": 2},
                "result": {"item": "魔法黄宝石", "quantity": 1},
                "description": "增加20%金币掉落"
            },
            "魔法紫宝石": {
                "type": "gem",
                "ingredients": {"普通紫宝石": 2, "魔法宝石碎片": 3, "魔法水晶": 1},
                "result": {"item": "魔法紫宝石", "quantity": 1},
                "description": "增加20%经验获取"
            },
            "魔法橙宝石": {
                "type": "gem",
                "ingredients": {"普通橙宝石": 2, "魔法宝石碎片": 3, "幸运草": 3},
                "result": {"item": "魔法橙宝石", "quantity": 1},
                "description": "增加10点幸运"
            },
            "魔法青宝石": {
                "type": "gem",
                "ingredients": {"普通青宝石": 2, "魔法宝石碎片": 3, "风之精华": 2},
                "result": {"item": "魔法青宝石", "quantity": 1},
                "description": "增加10点速度"
            },
            
            # 稀有宝石合成
            "稀有红宝石": {
                "type": "gem",
                "ingredients": {"魔法红宝石": 2, "稀有宝石碎片": 3, "火焰精华": 3, "龙血": 1},
                "result": {"item": "稀有红宝石", "quantity": 1},
                "description": "增加20点攻击力"
            },
            "稀有蓝宝石": {
                "type": "gem",
                "ingredients": {"魔法蓝宝石": 2, "稀有宝石碎片": 3, "冰霜精华": 3, "龙血": 1},
                "result": {"item": "稀有蓝宝石", "quantity": 1},
                "description": "增加20点防御力"
            },
            "稀有绿宝石": {
                "type": "gem",
                "ingredients": {"魔法绿宝石": 2, "稀有宝石碎片": 3, "自然精华": 3, "生命之花": 2},
                "result": {"item": "稀有绿宝石", "quantity": 1},
                "description": "增加100点生命值"
            },
            "稀有黄宝石": {
                "type": "gem",
                "ingredients": {"魔法黄宝石": 2, "稀有宝石碎片": 3, "金矿石": 3, "龙鳞": 1},
                "result": {"item": "稀有黄宝石", "quantity": 1},
                "description": "增加30%金币掉落"
            },
            "稀有紫宝石": {
                "type": "gem",
                "ingredients": {"魔法紫宝石": 2, "稀有宝石碎片": 3, "魔法水晶": 2, "灵魂石": 1},
                "result": {"item": "稀有紫宝石", "quantity": 1},
                "description": "增加30%经验获取"
            },
            "稀有橙宝石": {
                "type": "gem",
                "ingredients": {"魔法橙宝石": 2, "稀有宝石碎片": 3, "幸运草": 5, "精灵之尘": 2},
                "result": {"item": "稀有橙宝石", "quantity": 1},
                "description": "增加15点幸运"
            },
            "稀有青宝石": {
                "type": "gem",
                "ingredients": {"魔法青宝石": 2, "稀有宝石碎片": 3, "风之精华": 3, "飞行羽毛": 2},
                "result": {"item": "稀有青宝石", "quantity": 1},
                "description": "增加15点速度"
            },
            
            # 史诗宝石合成
            "史诗红宝石": {
                "type": "gem",
                "ingredients": {"稀有红宝石": 2, "史诗宝石碎片": 3, "火焰精华": 4, "龙心": 1},
                "result": {"item": "史诗红宝石", "quantity": 1},
                "description": "增加35点攻击力"
            },
            "史诗蓝宝石": {
                "type": "gem",
                "ingredients": {"稀有蓝宝石": 2, "史诗宝石碎片": 3, "冰霜精华": 4, "龙心": 1},
                "result": {"item": "史诗蓝宝石", "quantity": 1},
                "description": "增加35点防御力"
            },
            "史诗绿宝石": {
                "type": "gem",
                "ingredients": {"稀有绿宝石": 2, "史诗宝石碎片": 3, "自然精华": 4, "世界之心": 1},
                "result": {"item": "史诗绿宝石", "quantity": 1},
                "description": "增加200点生命值"
            },
            "史诗黄宝石": {
                "type": "gem",
                "ingredients": {"稀有黄宝石": 2, "史诗宝石碎片": 3, "金矿石": 4, "龙之宝石": 1},
                "result": {"item": "史诗黄宝石", "quantity": 1},
                "description": "增加40%金币掉落"
            },
            "史诗紫宝石": {
                "type": "gem",
                "ingredients": {"稀有紫宝石": 2, "史诗宝石碎片": 3, "魔法水晶": 3, "知识结晶": 2},
                "result": {"item": "史诗紫宝石", "quantity": 1},
                "description": "增加40%经验获取"
            },
            "史诗橙宝石": {
                "type": "gem",
                "ingredients": {"稀有橙宝石": 2, "史诗宝石碎片": 3, "幸运草": 8, "命运水晶": 1},
                "result": {"item": "史诗橙宝石", "quantity": 1},
                "description": "增加20点幸运"
            },
            "史诗青宝石": {
                "type": "gem",
                "ingredients": {"稀有青宝石": 2, "史诗宝石碎片": 3, "风之精华": 4, "飞行核心": 1},
                "result": {"item": "史诗青宝石", "quantity": 1},
                "description": "增加20点速度"
            },
            
            # 传说宝石合成
            "传说红宝石": {
                "type": "gem",
                "ingredients": {"史诗红宝石": 2, "传说宝石碎片": 3, "火焰精华": 5, "远古龙鳞": 2},
                "result": {"item": "传说红宝石", "quantity": 1},
                "description": "增加50点攻击力"
            },
            "传说蓝宝石": {
                "type": "gem",
                "ingredients": {"史诗蓝宝石": 2, "传说宝石碎片": 3, "冰霜精华": 5, "远古龙鳞": 2},
                "result": {"item": "传说蓝宝石", "quantity": 1},
                "description": "增加50点防御力"
            },
            "传说绿宝石": {
                "type": "gem",
                "ingredients": {"史诗绿宝石": 2, "传说宝石碎片": 3, "自然精华": 5, "永恒水晶": 1},
                "result": {"item": "传说绿宝石", "quantity": 1},
                "description": "增加300点生命值"
            },
            "传说黄宝石": {
                "type": "gem",
                "ingredients": {"史诗黄宝石": 2, "传说宝石碎片": 3, "金矿石": 5, "创世神剑": 1},
                "result": {"item": "传说黄宝石", "quantity": 1},
                "description": "增加50%金币掉落"
            },
            "传说紫宝石": {
                "type": "gem",
                "ingredients": {"史诗紫宝石": 2, "传说宝石碎片": 3, "魔法水晶": 4, "神之祝福": 1},
                "result": {"item": "传说紫宝石", "quantity": 1},
                "description": "增加50%经验获取"
            },
            "传说橙宝石": {
                "type": "gem",
                "ingredients": {"史诗橙宝石": 2, "传说宝石碎片": 3, "幸运草": 10, "命运水晶": 2},
                "result": {"item": "传说橙宝石", "quantity": 1},
                "description": "增加25点幸运"
            },
            "传说青宝石": {
                "type": "gem",
                "ingredients": {"史诗青宝石": 2, "传说宝石碎片": 3, "风之精华": 5, "飞行精华": 3},
                "result": {"item": "传说青宝石", "quantity": 1},
                "description": "增加25点速度"
            },
            
            # 神话宝石合成
            "神话红宝石": {
                "type": "gem",
                "ingredients": {"传说红宝石": 2, "神话宝石碎片": 3, "火焰精华": 6, "创世宝石碎片": 1},
                "result": {"item": "神话红宝石", "quantity": 1},
                "description": "增加75点攻击力"
            },
            "神话蓝宝石": {
                "type": "gem",
                "ingredients": {"传说蓝宝石": 2, "神话宝石碎片": 3, "冰霜精华": 6, "创世宝石碎片": 1},
                "result": {"item": "神话蓝宝石", "quantity": 1},
                "description": "增加75点防御力"
            },
            "神话绿宝石": {
                "type": "gem",
                "ingredients": {"传说绿宝石": 2, "神话宝石碎片": 3, "自然精华": 6, "世界之心": 2},
                "result": {"item": "神话绿宝石", "quantity": 1},
                "description": "增加500点生命值"
            },
            "神话黄宝石": {
                "type": "gem",
                "ingredients": {"传说黄宝石": 2, "神话宝石碎片": 3, "金矿石": 6, "成神之证": 1},
                "result": {"item": "神话黄宝石", "quantity": 1},
                "description": "增加60%金币掉落"
            },
            "神话紫宝石": {
                "type": "gem",
                "ingredients": {"传说紫宝石": 2, "神话宝石碎片": 3, "魔法水晶": 5, "成神之证": 1},
                "result": {"item": "神话紫宝石", "quantity": 1},
                "description": "增加60%经验获取"
            },
            "神话橙宝石": {
                "type": "gem",
                "ingredients": {"传说橙宝石": 2, "神话宝石碎片": 3, "幸运草": 12, "命运水晶": 3},
                "result": {"item": "神话橙宝石", "quantity": 1},
                "description": "增加30点幸运"
            },
            "神话青宝石": {
                "type": "gem",
                "ingredients": {"传说青宝石": 2, "神话宝石碎片": 3, "风之精华": 6, "飞行精华": 4},
                "result": {"item": "神话青宝石", "quantity": 1},
                "description": "增加30点速度"
            },
            
            # 创世宝石合成
            "创世红宝石": {
                "type": "gem",
                "ingredients": {"神话红宝石": 2, "创世宝石碎片": 3, "火焰精华": 8, "创世神剑": 1},
                "result": {"item": "创世红宝石", "quantity": 1},
                "description": "增加100点攻击力"
            },
            "创世蓝宝石": {
                "type": "gem",
                "ingredients": {"神话蓝宝石": 2, "创世宝石碎片": 3, "冰霜精华": 8, "创世神剑": 1},
                "result": {"item": "创世蓝宝石", "quantity": 1},
                "description": "增加100点防御力"
            },
            "创世绿宝石": {
                "type": "gem",
                "ingredients": {"神话绿宝石": 2, "创世宝石碎片": 3, "自然精华": 8, "世界之心": 3},
                "result": {"item": "创世绿宝石", "quantity": 1},
                "description": "增加1000点生命值"
            },
            "创世黄宝石": {
                "type": "gem",
                "ingredients": {"神话黄宝石": 2, "创世宝石碎片": 3, "金矿石": 8, "成神之证": 2},
                "result": {"item": "创世黄宝石", "quantity": 1},
                "description": "增加75%金币掉落"
            },
            "创世紫宝石": {
                "type": "gem",
                "ingredients": {"神话紫宝石": 2, "创世宝石碎片": 3, "魔法水晶": 7, "成神之证": 2},
                "result": {"item": "创世紫宝石", "quantity": 1},
                "description": "增加75%经验获取"
            },
            "创世橙宝石": {
                "type": "gem",
                "ingredients": {"神话橙宝石": 2, "创世宝石碎片": 3, "幸运草": 15, "命运水晶": 4},
                "result": {"item": "创世橙宝石", "quantity": 1},
                "description": "增加50点幸运"
            },
            "创世青宝石": {
                "type": "gem",
                "ingredients": {"神话青宝石": 2, "创世宝石碎片": 3, "风之精华": 8, "飞行精华": 6},
                "result": {"item": "创世青宝石", "quantity": 1},
                "description": "增加50点速度"
            },
            
            # 特殊宝石合成
            "全能宝石": {
                "type": "gem",
                "ingredients": {"创世红宝石": 1, "创世蓝宝石": 1, "创世绿宝石": 1, "创世黄宝石": 1, "创世紫宝石": 1, "创世橙宝石": 1, "创世青宝石": 1},
                "result": {"item": "全能宝石", "quantity": 1},
                "description": "增加所有属性10%"
            },
            "生命宝石": {
                "type": "gem",
                "ingredients": {"创世绿宝石": 2, "世界之心": 2, "生命之花": 10},
                "result": {"item": "生命宝石", "quantity": 1},
                "description": "每回合恢复5点生命值"
            },
            "魔法宝石": {
                "type": "gem",
                "ingredients": {"创世紫宝石": 2, "永恒水晶": 2, "魔法水晶": 10},
                "result": {"item": "魔法宝石", "quantity": 1},
                "description": "每回合恢复5点魔法值"
            },
            "吸血宝石": {
                "type": "gem",
                "ingredients": {"创世红宝石": 2, "龙血": 5, "恶魔之血": 5},
                "result": {"item": "吸血宝石", "quantity": 1},
                "description": "造成伤害的10%转化为生命"
            },
            "反伤宝石": {
                "type": "gem",
                "ingredients": {"创世蓝宝石": 2, "龙鳞": 5, "远古龙鳞": 3},
                "result": {"item": "反伤宝石", "quantity": 1},
                "description": "反弹10%受到的伤害"
            },
            "格挡宝石": {
                "type": "gem",
                "ingredients": {"创世青宝石": 2, "精金矿石": 10, "奥金矿石": 5},
                "result": {"item": "格挡宝石", "quantity": 1},
                "description": "10%几率格挡伤害"
            },
            "暴击宝石": {
                "type": "gem",
                "ingredients": {"创世红宝石": 1, "创世青宝石": 1, "龙焰宝石": 3, "闪电水晶": 5},
                "result": {"item": "暴击宝石", "quantity": 1},
                "description": "增加10%暴击率"
            },
            "闪避宝石": {
                "type": "gem",
                "ingredients": {"创世青宝石": 2, "风之精华": 8, "轻盈羽毛": 10},
                "result": {"item": "闪避宝石", "quantity": 1},
                "description": "增加10%闪避率"
            },
            
            # 饰品合成
            "魔法戒指": {
                "type": "accessory",
                "ingredients": {"金矿石": 3, "魔法水晶": 2, "元素精华": 2},
                "result": {"item": "魔法戒指", "quantity": 1},
                "description": "增加15点魔法攻击力"
            },
            "防御戒指": {
                "type": "accessory",
                "ingredients": {"银矿石": 3, "魔法水晶碎片": 5, "守护精华": 2},
                "result": {"item": "防御戒指", "quantity": 1},
                "description": "增加10点防御力"
            },
            "生命戒指": {
                "type": "accessory",
                "ingredients": {"金矿石": 2, "生命之花": 3, "自然精华": 2},
                "result": {"item": "生命戒指", "quantity": 1},
                "description": "增加50点生命值"
            },
            "速度戒指": {
                "type": "accessory",
                "ingredients": {"秘银矿石": 2, "风之精华": 3, "轻盈羽毛": 5},
                "result": {"item": "速度戒指", "quantity": 1},
                "description": "增加10点速度"
            },
            "幸运护符": {
                "type": "accessory",
                "ingredients": {"金矿石": 2, "幸运草": 5, "精灵之尘": 3},
                "result": {"item": "幸运护符", "quantity": 1},
                "description": "增加10点幸运"
            },
        }
        
        # 宝石镶嵌规则
        self.gem_socket_rules = {
            "weapon": {
                "allowed_types": ["attack", "crit", "lifesteal", "speed", "luck"],
                "max_gems": 1,
                "description": "武器只能镶嵌攻击类宝石"
            },
            "armor": {
                "allowed_types": ["defense", "hp", "block", "thorns", "hp_regen"],
                "max_gems": 1,
                "description": "盔甲只能镶嵌防御类宝石"
            },
            "accessory": {
                "allowed_types": ["all", "gold", "exp", "luck", "speed", "dodge", "mana_regen", "magic"],
                "max_gems": 1,
                "description": "饰品可以镶嵌特殊类宝石"
            }
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
            "富甲一方": "拥有1000金币",
            "等级达人": "达到20级",
            "铁匠大师": "打造10件装备",
            "药剂师": "使用50个消耗品",
            "冒险家": "探索所有场景",
            "收藏家": "收集所有稀有物品",
            "战斗精英": "击败所有类型的敌人",
            "生存专家": "在游戏中生存30天",
            
            # 装备相关成就
            "装备收集家": "收集10件不同的装备",
            "武器大师": "拥有5件传说级武器",
            "防具大师": "拥有5件传说级防具",
            "宝石收藏家": "拥有10颗不同的宝石",
            "完美装备": "同时装备传说级武器、防具和饰品",
            
            # 合成/锻造/宝石成就
            "初级药剂师": "成功合成10瓶药水",
            "中级药剂师": "成功合成50瓶药水",
            "高级药剂师": "成功合成200瓶药水",
            "大师级药剂师": "成功合成500瓶药水",
            "宗师级药剂师": "成功合成1000瓶药水",
            
            "初级铁匠": "成功锻造10件装备",
            "中级铁匠": "成功锻造50件装备",
            "高级铁匠": "成功锻造200件装备",
            "大师级铁匠": "成功锻造500件装备",
            "宗师级铁匠": "成功锻造1000件装备",
            
            "初级宝石匠": "成功合成10颗宝石",
            "中级宝石匠": "成功合成50颗宝石",
            "高级宝石匠": "成功合成200颗宝石",
            "大师级宝石匠": "成功合成500颗宝石",
            "宗师级宝石匠": "成功合成1000颗宝石",
            
            "宝石收集家": "收集所有类型的宝石",
            "装备收藏家": "收集所有类型的装备",
            
            "剑术大师": "锻造出传说级武器",
            "宝石大师": "合成出传说级宝石",
            
            "完美镶嵌": "为所有装备镶嵌宝石",
            "最强装备": "拥有全套传说级装备和宝石",
        }
    
    def initialize_recruitable_npcs(self):
        """初始化可招募的NPC队友"""
        self.recruitable_npcs = {
            "战士_艾瑞克": {
                "name": "艾瑞克",
                "class": "战士",
                "level": 5,
                "hp": 200,
                "mp": 50,
                "attack": 40,
                "defense": 30,
                "magic_attack": 10,
                "skills": ["强力攻击", "盾牌格挡"],
                "recruitment_conditions": {
                    "required_level": 3,
                    "required_gold": 100,
                    "required_items": {}
                },
                "location": "town",
                "dialogue": "我是一名战士，擅长近战战斗。如果你需要一名可靠的伙伴，我愿意加入你的队伍。",
                "affection": 50
            },
            "法师_莉莉丝": {
                "name": "莉莉丝",
                "class": "法师",
                "level": 4,
                "hp": 120,
                "mp": 150,
                "attack": 15,
                "defense": 15,
                "magic_attack": 50,
                "skills": ["火球术", "魔法护盾"],
                "recruitment_conditions": {
                    "required_level": 2,
                    "required_gold": 150,
                    "required_items": {}
                },
                "location": "tower",
                "dialogue": "魔法的力量是无穷的，我可以为你提供强大的法术支持。",
                "affection": 50
            },
            "牧师_安娜": {
                "name": "安娜",
                "class": "牧师",
                "level": 3,
                "hp": 150,
                "mp": 120,
                "attack": 10,
                "defense": 20,
                "magic_attack": 30,
                "skills": ["治疗术", "神圣庇护"],
                "recruitment_conditions": {
                    "required_level": 2,
                    "required_gold": 80,
                    "required_items": {}
                },
                "location": "castle",
                "dialogue": "我是一名牧师，致力于帮助他人。让我加入你的队伍，为你提供治疗和保护。",
                "affection": 50
            },
            "弓箭手_罗宾": {
                "name": "罗宾",
                "class": "弓箭手",
                "level": 4,
                "hp": 140,
                "mp": 80,
                "attack": 35,
                "defense": 20,
                "magic_attack": 15,
                "skills": ["精准射击", "多重箭"],
                "recruitment_conditions": {
                    "required_level": 3,
                    "required_gold": 120,
                    "required_items": {}
                },
                "location": "forest",
                "dialogue": "我是一名弓箭手，擅长远程攻击。加入我，我们可以在战斗中互相配合。",
                "affection": 50
            },
            "战士_加里": {
                "name": "加里",
                "class": "战士",
                "level": 6,
                "hp": 250,
                "mp": 60,
                "attack": 50,
                "defense": 35,
                "magic_attack": 15,
                "skills": ["旋风斩", "嘲讽"],
                "recruitment_conditions": {
                    "required_level": 5,
                    "required_gold": 200,
                    "required_items": {}
                },
                "location": "castle",
                "dialogue": "我是一名经验丰富的战士，曾在战场上立下赫赫战功。如果你需要一名强大的近战伙伴，我很乐意加入。",
                "affection": 50
            },
            "法师_梅林": {
                "name": "梅林",
                "class": "法师",
                "level": 5,
                "hp": 130,
                "mp": 180,
                "attack": 20,
                "defense": 18,
                "magic_attack": 60,
                "skills": ["冰锥术", "闪电链"],
                "recruitment_conditions": {
                    "required_level": 4,
                    "required_gold": 250,
                    "required_items": {}
                },
                "location": "tower",
                "dialogue": "我是一名强大的法师，掌握着元素的力量。加入我，我们可以一起探索魔法的奥秘。",
                "affection": 50
            },
            "牧师_莎拉": {
                "name": "莎拉",
                "class": "牧师",
                "level": 4,
                "hp": 160,
                "mp": 140,
                "attack": 12,
                "defense": 22,
                "magic_attack": 35,
                "skills": ["群体治疗", "净化术"],
                "recruitment_conditions": {
                    "required_level": 3,
                    "required_gold": 100,
                    "required_items": {}
                },
                "location": "town",
                "dialogue": "我是一名虔诚的牧师，愿意用神圣的力量保护和治愈我的队友。",
                "affection": 50
            },
            "弓箭手_鹰眼": {
                "name": "鹰眼",
                "class": "弓箭手",
                "level": 5,
                "hp": 150,
                "mp": 90,
                "attack": 40,
                "defense": 22,
                "magic_attack": 20,
                "skills": ["瞄准射击", "箭雨"],
                "recruitment_conditions": {
                    "required_level": 4,
                    "required_gold": 180,
                    "required_items": {}
                },
                "location": "wilderness",
                "dialogue": "我的箭法精准无比，没有人能逃过我的鹰眼。加入我，我们可以在远处解决敌人。",
                "affection": 50
            }
        }
    
    def recruit_npc(self, npc_id):
        """招募NPC队友"""
        if npc_id not in self.recruitable_npcs:
            return False, "该NPC不存在！"
        
        npc = self.recruitable_npcs[npc_id]
        
        # 检查队伍是否已满
        if len(self.teammates) >= self.max_team_size:
            return False, "队伍已满，无法招募更多队友！"
        
        # 检查招募条件
        conditions = npc['recruitment_conditions']
        
        # 检查等级要求
        if self.player.level < conditions['required_level']:
            return False, f"需要达到 {conditions['required_level']} 级才能招募 {npc['name']}！"
        
        # 检查金币要求
        if self.player.gold < conditions['required_gold']:
            return False, f"需要 {conditions['required_gold']} 金币才能招募 {npc['name']}！"
        
        # 检查物品要求
        for item, quantity in conditions['required_items'].items():
            if self.player.inventory.get(item, 0) < quantity:
                return False, f"需要 {quantity} 个 {item} 才能招募 {npc['name']}！"
        
        # 扣除金币
        self.player.gold -= conditions['required_gold']
        
        # 扣除物品
        for item, quantity in conditions['required_items'].items():
            self.player.remove_item(item, quantity)
        
        # 添加队友
        teammate = {
            "name": npc['name'],
            "class": npc['class'],
            "level": npc['level'],
            "hp": npc['hp'],
            "mp": npc['mp'],
            "attack": npc['attack'],
            "defense": npc['defense'],
            "magic_attack": npc['magic_attack'],
            "skills": npc['skills'],
            "affection": npc['affection']
        }
        
        self.teammates.append(teammate)
        
        # 从可招募列表中移除
        del self.recruitable_npcs[npc_id]
        
        return True, f"成功招募 {npc['name']} 加入队伍！"
    
    def show_teammates(self):
        """显示队友信息"""
        if not self.teammates:
            messagebox.showinfo("队友列表", "当前没有队友！")
            return
        
        # 创建队友信息对话框
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("队友列表")
        dialog.geometry("400x300")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 队友列表
        listbox = tk.Listbox(
            dialog,
            font=self.gui.normal_font,
            bg='#1e1e1e',
            fg=self.gui.colors['fg'],
            height=10
        )
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        for i, teammate in enumerate(self.teammates):
            listbox.insert(tk.END, f"{teammate['name']} ({teammate['class']}) - 好感度: {teammate['affection']}")
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                teammate = self.teammates[index]
                
                # 显示队友详细信息
                detail_dialog = tk.Toplevel(dialog)
                detail_dialog.title(f"{teammate['name']} 详情")
                detail_dialog.geometry("300x250")
                detail_dialog.configure(bg=self.gui.colors['bg'])
                detail_dialog.transient(dialog)
                detail_dialog.grab_set()
                
                info_frame = tk.Frame(detail_dialog, bg=self.gui.colors['bg'])
                info_frame.pack(fill='both', expand=True, padx=10, pady=5)
                
                tk.Label(info_frame, text=f"姓名: {teammate['name']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"职业: {teammate['class']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"等级: {teammate['level']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"生命值: {teammate['hp']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"魔法值: {teammate['mp']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"攻击力: {teammate['attack']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"防御力: {teammate['defense']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"魔法攻击力: {teammate['magic_attack']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"好感度: {teammate['affection']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"技能: {', '.join(teammate['skills'])}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                
                tk.Button(detail_dialog, text="关闭", command=detail_dialog.destroy, font=self.gui.normal_font, bg=self.gui.colors['button_bg'], fg=self.gui.colors['button_fg']).pack(pady=5)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        tk.Button(dialog, text="关闭", command=dialog.destroy, font=self.gui.normal_font, bg=self.gui.colors['button_bg'], fg=self.gui.colors['button_fg']).pack(pady=5)
    
    def initialize_capturable_monsters(self):
        """初始化可捕获的野怪"""
        self.capturable_monsters = {
            "野狼": {
                "name": "野狼",
                "type": "野兽",
                "level": 2,
                "hp": 80,
                "mp": 20,
                "attack": 25,
                "defense": 15,
                "magic_attack": 5,
                "skills": ["撕咬", "猛扑"],
                "capture_chance": 0.4,
                "growth_rate": 1.2,
                "evolutions": [],
                "passive_bonus": {
                    "attack": 2
                }
            },
            "森林精灵": {
                "name": "森林精灵",
                "type": "精灵",
                "level": 3,
                "hp": 60,
                "mp": 80,
                "attack": 15,
                "defense": 10,
                "magic_attack": 30,
                "skills": ["自然魔法", "治愈术"],
                "capture_chance": 0.3,
                "growth_rate": 1.3,
                "evolutions": [],
                "passive_bonus": {
                    "magic_attack": 3
                }
            },
            "巨熊": {
                "name": "巨熊",
                "type": "野兽",
                "level": 4,
                "hp": 120,
                "mp": 30,
                "attack": 35,
                "defense": 25,
                "magic_attack": 10,
                "skills": ["熊掌拍击", "吼叫"],
                "capture_chance": 0.25,
                "growth_rate": 1.1,
                "evolutions": [],
                "passive_bonus": {
                    "defense": 3
                }
            },
            "野马": {
                "name": "野马",
                "type": "野兽",
                "level": 2,
                "hp": 70,
                "mp": 15,
                "attack": 20,
                "defense": 18,
                "magic_attack": 5,
                "skills": ["踢击", "冲刺"],
                "capture_chance": 0.35,
                "growth_rate": 1.15,
                "evolutions": [],
                "passive_bonus": {
                    "speed": 1
                }
            },
            "沙漠蝎子": {
                "name": "沙漠蝎子",
                "type": "昆虫",
                "level": 3,
                "hp": 65,
                "mp": 25,
                "attack": 30,
                "defense": 12,
                "magic_attack": 15,
                "skills": ["毒刺", "隐蔽"],
                "capture_chance": 0.3,
                "growth_rate": 1.25,
                "evolutions": [],
                "passive_bonus": {
                    "attack": 1,
                    "poison_damage": 5
                }
            },
            "游牧强盗": {
                "name": "游牧强盗",
                "type": "人类",
                "level": 4,
                "hp": 90,
                "mp": 40,
                "attack": 28,
                "defense": 20,
                "magic_attack": 20,
                "skills": ["剑击", "投掷"],
                "capture_chance": 0.2,
                "growth_rate": 1.2,
                "evolutions": [],
                "passive_bonus": {
                    "gold": 10
                }
            },
            "守卫": {
                "name": "守卫",
                "type": "人类",
                "level": 5,
                "hp": 100,
                "mp": 50,
                "attack": 32,
                "defense": 28,
                "magic_attack": 15,
                "skills": ["盾牌攻击", "嘲讽"],
                "capture_chance": 0.15,
                "growth_rate": 1.15,
                "evolutions": [],
                "passive_bonus": {
                    "defense": 2
                }
            },
            "幽灵": {
                "name": "幽灵",
                "type": " undead",
                "level": 6,
                "hp": 80,
                "mp": 100,
                "attack": 25,
                "defense": 10,
                "magic_attack": 40,
                "skills": ["灵魂攻击", "诅咒"],
                "capture_chance": 0.2,
                "growth_rate": 1.35,
                "evolutions": [],
                "passive_bonus": {
                    "magic_attack": 2
                }
            }
        }
    
    def show_pets(self):
        """显示宠物信息"""
        if not self.pets:
            messagebox.showinfo("宠物列表", "当前没有宠物！")
            return
        
        # 创建宠物信息对话框
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("宠物列表")
        dialog.geometry("400x300")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 宠物列表
        listbox = tk.Listbox(
            dialog,
            font=self.gui.normal_font,
            bg='#1e1e1e',
            fg=self.gui.colors['fg'],
            height=10
        )
        listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        for i, pet in enumerate(self.pets):
            listbox.insert(tk.END, f"{pet['name']} ({pet['type']}) - 等级: {pet['level']} - 忠诚度: {pet['loyalty']}")
        
        def on_select(event):
            selection = listbox.curselection()
            if selection:
                index = selection[0]
                pet = self.pets[index]
                
                # 显示宠物详细信息
                detail_dialog = tk.Toplevel(dialog)
                detail_dialog.title(f"{pet['name']} 详情")
                detail_dialog.geometry("300x250")
                detail_dialog.configure(bg=self.gui.colors['bg'])
                detail_dialog.transient(dialog)
                detail_dialog.grab_set()
                
                info_frame = tk.Frame(detail_dialog, bg=self.gui.colors['bg'])
                info_frame.pack(fill='both', expand=True, padx=10, pady=5)
                
                tk.Label(info_frame, text=f"姓名: {pet['name']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"类型: {pet['type']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"等级: {pet['level']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"生命值: {pet['hp']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"魔法值: {pet['mp']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"攻击力: 玩家攻击 ÷ 10", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"防御力: {pet['defense']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"魔法攻击力: {pet['magic_attack']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"忠诚度: {pet['loyalty']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                tk.Label(info_frame, text=f"技能: {', '.join(pet['skills'])}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                
                # 显示被动加成
                passive_bonus_text = "被动加成: "
                if pet['passive_bonus']:
                    bonus_items = []
                    for bonus, value in pet['passive_bonus'].items():
                        bonus_items.append(f"{bonus}: +{value}")
                    passive_bonus_text += ", ".join(bonus_items)
                else:
                    passive_bonus_text += "无"
                tk.Label(info_frame, text=passive_bonus_text, font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w')
                
                tk.Button(detail_dialog, text="关闭", command=detail_dialog.destroy, font=self.gui.normal_font, bg=self.gui.colors['button_bg'], fg=self.gui.colors['button_fg']).pack(pady=5)
        
        listbox.bind('<<ListboxSelect>>', on_select)
        
        tk.Button(dialog, text="关闭", command=dialog.destroy, font=self.gui.normal_font, bg=self.gui.colors['button_bg'], fg=self.gui.colors['button_fg']).pack(pady=5)
    
    def show_leaderboard(self):
        """显示排行榜"""
        # 创建排行榜对话框
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("排行榜")
        dialog.geometry("600x400")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 战斗数据统计标签页
        stats_frame = tk.Frame(notebook, bg=self.gui.colors['bg'])
        notebook.add(stats_frame, text="战斗数据")
        
        # 战斗数据统计
        stats_label = tk.Label(
            stats_frame,
            text="战斗数据统计",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg=self.gui.colors['bg']
        )
        stats_label.pack(pady=10)
        
        stats_info_frame = tk.Frame(stats_frame, bg=self.gui.colors['bg'])
        stats_info_frame.pack(fill='x', padx=10, pady=5)
        
        combat_stats = self.leaderboard['combat_stats']
        tk.Label(stats_info_frame, text=f"总击杀数: {combat_stats['total_kills']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w', pady=2)
        tk.Label(stats_info_frame, text=f"最高伤害: {combat_stats['highest_damage']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w', pady=2)
        tk.Label(stats_info_frame, text=f"总伤害: {combat_stats['total_damage']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w', pady=2)
        tk.Label(stats_info_frame, text=f"胜利场次: {combat_stats['battles_won']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w', pady=2)
        tk.Label(stats_info_frame, text=f"失败场次: {combat_stats['battles_lost']}", font=self.gui.normal_font, fg=self.gui.colors['fg'], bg=self.gui.colors['bg']).pack(anchor='w', pady=2)
        
        # 本地存档排名标签页
        ranking_frame = tk.Frame(notebook, bg=self.gui.colors['bg'])
        notebook.add(ranking_frame, text="本地排名")
        
        # 本地存档排名
        ranking_label = tk.Label(
            ranking_frame,
            text="本地存档排名",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg=self.gui.colors['bg']
        )
        ranking_label.pack(pady=10)
        
        # 读取本地存档
        save_files = self.get_save_files()
        ranking_list = []
        
        for save in save_files:
            try:
                save_path = os.path.join(self.saves_dir, save['file'])
                with open(save_path, 'r') as f:
                    save_data = {}
                    current_section = None
                    for line in f:
                        line = line.strip()
                        if line.startswith('[') and line.endswith(']'):
                            current_section = line[1:-1]
                            save_data[current_section] = {}
                        elif current_section and ': ' in line:
                            key, value = line.split(': ', 1)
                            save_data[current_section][key] = value
                    
                    if 'player' in save_data:
                        player_data = save_data['player']
                        level = int(player_data.get('level', 1))
                        gold = int(player_data.get('gold', 0))
                        exp = int(player_data.get('exp', 0))
                        
                        ranking_list.append({
                            'name': save['name'],
                            'date': save['date'],
                            'level': level,
                            'gold': gold,
                            'exp': exp
                        })
            except Exception as e:
                pass
        
        # 按等级、金币、经验排序
        ranking_list.sort(key=lambda x: (x['level'], x['gold'], x['exp']), reverse=True)
        
        # 显示排名
        ranking_listbox = tk.Listbox(
            ranking_frame,
            font=self.gui.normal_font,
            bg='#1e1e1e',
            fg=self.gui.colors['fg'],
            height=10
        )
        ranking_listbox.pack(fill='both', expand=True, padx=10, pady=5)
        
        for i, save in enumerate(ranking_list[:10]):  # 只显示前10名
            ranking_listbox.insert(tk.END, f"{i+1}. {save['name']} - 等级: {save['level']} - 金币: {save['gold']} - 经验: {save['exp']} - {save['date']}")
        
        if not ranking_list:
            ranking_listbox.insert(tk.END, "暂无存档数据")
        
        tk.Button(dialog, text="关闭", command=dialog.destroy, font=self.gui.normal_font, bg=self.gui.colors['button_bg'], fg=self.gui.colors['button_fg']).pack(pady=5)
    


    
    def update_compendium_completion(self):
        """更新图鉴完成度"""
        # 计算敌人图鉴完成度（假设总共有50种敌人）
        total_enemies = 50
        enemies_completed = len(self.compendium['enemies'])
        self.compendium['completion']['enemies'] = min(100, (enemies_completed / total_enemies) * 100)
        
        # 计算物品图鉴完成度（假设总共有100种物品）
        total_items = 100
        items_completed = len(self.compendium['items'])
        self.compendium['completion']['items'] = min(100, (items_completed / total_items) * 100)
        
        # 计算成就图鉴完成度（假设总共有30个成就）
        total_achievements = 30
        achievements_completed = len(self.compendium['achievements'])
        self.compendium['completion']['achievements'] = min(100, (achievements_completed / total_achievements) * 100)
        
        # 计算总完成度
        total_completion = (self.compendium['completion']['enemies'] + 
                           self.compendium['completion']['items'] + 
                           self.compendium['completion']['achievements']) / 3
        self.compendium['completion']['total'] = total_completion
        
        # 检查是否有新的奖励可以领取
        self.check_compendium_rewards()
    
    def check_compendium_rewards(self):
        """检查图鉴完成度奖励"""
        current_completion = self.compendium['completion']['total']
        
        for reward in self.compendium['rewards']:
            threshold = reward['threshold']
            if current_completion >= threshold and threshold not in self.compendium['rewards_claimed']:
                # 领取奖励
                self.compendium['rewards_claimed'].append(threshold)
                
                # 给予奖励
                self.player.gold += reward['reward']['gold']
                self.player.exp += reward['reward']['exp']
                
                # 添加物品
                for item in reward['reward']['items']:
                    if item in self.player.inventory:
                        self.player.inventory[item] += 1
                    else:
                        self.player.inventory[item] = 1
                
                # 显示奖励信息
                reward_msg = f"🎉 图鉴完成度达到 {threshold}%！获得奖励："
                reward_msg += f"{reward['reward']['gold']} 金币, {reward['reward']['exp']} 经验"
                if reward['reward']['items']:
                    reward_msg += f", 物品: {', '.join(reward['reward']['items'])}"
                
                self.gui.add_message(reward_msg, 'success')
                
                # 检查升级
                while self.player.exp >= self.player.exp_to_next_level():
                    self.player.level_up()
    
    

    

    

    

    


    def start_stamina_recovery(self):
        """启动自动体力恢复线程"""
        if not self.stamina_recovery_running and self.player:
            self.stamina_recovery_running = True
            self.stamina_recovery_thread = threading.Thread(target=self.auto_recover_stamina, daemon=True)
            self.stamina_recovery_thread.start()
    
    def auto_recover_stamina(self):
        """自动恢复体力（每分钟1点）"""
        while self.stamina_recovery_running and self.player and self.game_state == "playing":
            time.sleep(60)  # 等待60秒
            if self.player and self.player.stamina < self.player.max_stamina:
                self.player.stamina = min(self.player.max_stamina, self.player.stamina + 1)
                if self.gui:
                    self.gui.update_game_info()
                    self.add_message("体力自动恢复了1点。", 'info')
    
    def use_stamina(self, amount):
        """使用体力值"""
        if not self.player:
            return False
        
        if self.player.stamina < amount:
            if self.gui:
                messagebox.showwarning("体力不足", f"需要 {amount} 点体力，当前只有 {self.player.stamina} 点！\n可以花费金币恢复或等待自动恢复。")
            return False
        
        self.player.stamina -= amount
        if self.gui:
            self.gui.update_game_info()
        return True
    
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
            self.player.add_item(item_name, quantity, self)
            self.add_message(f"你发现了 {quantity} 个 {item_name}！", 'success')
        elif event_type == 'event' and scene['events']:
            event = random.choice(scene['events'])
            self.trigger_event(event)
        else:
            self.add_message("你没有发现任何特别的东西。", 'info')
        
        # 探索可能获得矿石和宝石碎片
        if random.random() < 0.2:
            ore_chance = random.random()
            if ore_chance < 0.4:
                self.player.add_item("铜矿石", 1, self)
                self.add_message("你发现了一些铜矿石！", 'success')
            elif ore_chance < 0.7:
                self.player.add_item("铁矿石", 1, self)
                self.add_message("你发现了一些铁矿石！", 'success')
            elif ore_chance < 0.9:
                self.player.add_item("银矿石", 1, self)
                self.add_message("你发现了一些银矿石！", 'success')
            else:
                self.player.add_item("金矿石", 1, self)
                self.add_message("你发现了一些金矿石！", 'success')
        
        if random.random() < 0.15:
            gem_chance = random.random()
            if gem_chance < 0.5:
                self.player.add_item("普通宝石碎片", 1, self)
                self.add_message("你发现了一些宝石碎片！", 'success')
            elif gem_chance < 0.8:
                self.player.add_item("魔法宝石碎片", 1, self)
                self.add_message("你发现了一些魔法宝石碎片！", 'success')
            else:
                self.player.add_item("稀有宝石碎片", 1, self)
                self.add_message("你发现了一些稀有宝石碎片！", 'success')
        
        exp_gained = random.randint(1, 5)
        self.player.gain_exp(exp_gained)
        self.add_message(f"探索获得 {exp_gained} 点经验值", 'info')
        
        self.update_game_time()
        self.gui.update_game_info()
    
    def start_battle(self, enemy_name, active_battle=False):
        """开始战斗 - 增强版战斗系统（支持队友）"""
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
        
        # 创建战斗对话框
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("战斗")
        dialog.geometry("600x500")  # 增加高度以容纳队友信息
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 禁用关闭按钮
        def disable_close():
            pass
        dialog.protocol("WM_DELETE_WINDOW", disable_close)
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 战斗信息
        info_frame = tk.Frame(dialog, bg=self.gui.colors['bg'])
        info_frame.pack(fill='x', padx=10, pady=5)
        
        enemy_hp_label = tk.Label(
            info_frame,
            text=f"👾 {enemy_name} HP: {enemy_hp}/{enemy_hp}",
            font=self.gui.normal_font,
            fg=self.gui.colors['warning'],
            bg=self.gui.colors['bg']
        )
        enemy_hp_label.pack()
        
        total_hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
        player_hp_label = tk.Label(
            info_frame,
            text=f"⚔️ {self.player.name} HP: {self.player.hp}/{total_hp}",
            font=self.gui.normal_font,
            fg=self.gui.colors['success'],
            bg=self.gui.colors['bg']
        )
        player_hp_label.pack()
        
        # 队友信息
        teammate_labels = []
        for i, teammate in enumerate(self.teammates):
            teammate_label = tk.Label(
                info_frame,
                text=f"🤝 {teammate['name']} ({teammate['class']}) HP: {teammate['hp']}/{teammate['hp']}",
                font=self.gui.small_font,
                fg=self.gui.colors['info'],
                bg=self.gui.colors['bg']
            )
            teammate_label.pack()
            teammate_labels.append((teammate, teammate_label))
        
        # 战斗消息区域
        message_text = scrolledtext.ScrolledText(
            dialog,
            wrap=tk.WORD,
            font=self.gui.small_font,
            bg='#1e1e1e',
            fg=self.gui.colors['fg'],
            height=10
        )
        message_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        def add_battle_message(msg, tag=None):
            message_text.insert(tk.END, msg + "\n", tag)
            message_text.see(tk.END)
            dialog.update()
        
        # 战斗选项
        action_frame = tk.Frame(dialog, bg=self.gui.colors['bg'])
        action_frame.pack(fill='x', padx=10, pady=5)
        
        battle_running = True
        current_enemy_hp = enemy_hp
        
        def get_item_effect_description(item_info):
            """获取物品效果的描述文字"""
            effect = item_info.get('effect', '')
            value = item_info.get('value', 0)
            
            if effect == 'heal':
                if value >= 9999:
                    return "完全恢复生命值"
                return f"恢复 {value} 点生命值"
            elif effect == 'mana':
                if value >= 9999:
                    return "完全恢复魔法值"
                return f"恢复 {value} 点魔法值"
            elif effect == 'exp':
                return f"获得 {value} 点经验值"
            elif effect == 'buff_attack':
                return f"临时增加 {value} 点攻击力"
            elif effect == 'buff_defense':
                return f"临时增加 {value} 点防御力"
            elif effect == 'buff_speed':
                return f"临时增加 {value} 点速度"
            elif effect == 'buff_luck':
                return f"临时增加 {value} 点幸运"
            elif effect == 'buff_magic':
                return f"临时增加 {value} 点魔法攻击力"
            elif effect == 'special':
                if '隐身' in item_info.get('description', ''):
                    return "让使用者隐身，避免战斗"
                elif '解毒' in item_info.get('description', ''):
                    return "解除中毒状态"
                elif '复活' in item_info.get('description', ''):
                    return "战斗中复活一次"
            return item_info.get('description', '未知效果')
        
        def apply_item_effect(item_name, item_info):
            """应用物品效果，返回效果结果字典"""
            result = {
                'messages': [],
                'tag': 'success'
            }
            
            effect = item_info.get('effect', '')
            value = item_info.get('value', 0)
            
            if effect == 'heal':
                # 计算总生命值上限
                total_max_hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
                if value >= 9999:
                    heal_amount = total_max_hp - self.player.hp
                    result['hp_change'] = heal_amount
                    result['messages'].append(f"✨ 你使用了 {item_name}，生命值完全恢复！")
                else:
                    old_hp = self.player.hp
                    heal_amount = value
                    result['hp_change'] = heal_amount
                    result['messages'].append(f"💚 你使用了 {item_name}，恢复了 {heal_amount} 点生命值！")
            
            elif effect == 'mana':
                result['messages'].append(f"🔮 你使用了 {item_name}，恢复了 {value} 点魔法值！")
            
            elif effect == 'exp':
                result['exp_gain'] = value
                result['messages'].append(f"📚 你使用了 {item_name}，获得了 {value} 点经验值！")
            
            elif effect == 'buff_attack':
                result['attack_change'] = value
                result['messages'].append(f"⚔️ 你使用了 {item_name}，攻击力临时增加 {value} 点！")
            
            elif effect == 'buff_defense':
                result['defense_change'] = value
                result['messages'].append(f"🛡️ 你使用了 {item_name}，防御力临时增加 {value} 点！")
            
            elif effect == 'buff_speed':
                result['speed_change'] = value
                result['messages'].append(f"💨 你使用了 {item_name}，速度临时增加 {value} 点！")
            
            elif effect == 'buff_luck':
                result['luck_change'] = value
                result['messages'].append(f"🍀 你使用了 {item_name}，幸运临时增加 {value} 点！")
            
            elif effect == 'buff_magic':
                result['magic_change'] = value
                result['messages'].append(f"🔮 你使用了 {item_name}，魔法攻击力临时增加 {value} 点！")
            
            elif effect == 'special':
                if '隐身' in item_info.get('description', ''):
                    result['messages'].append(f"🌫️ 你使用了 {item_name}，进入隐身状态！")
                    result['invisible'] = True
                elif '解毒' in item_info.get('description', ''):
                    result['messages'].append(f"💊 你使用了 {item_name}，中毒状态已解除！")
                    result['cure_poison'] = True
                elif '复活' in item_info.get('description', ''):
                    result['messages'].append(f"✨ 你使用了 {item_name}，获得了复活效果！")
                    result['revive'] = True
            
            return result
        
        def teammate_attack(teammate):
            nonlocal current_enemy_hp
            if not battle_running:
                return
            
            # 队友攻击
            base_damage = max(1, teammate['attack'] - enemy_defense // 2)
            damage_variation = random.randint(-2, 3)
            damage = max(1, base_damage + damage_variation)
            
            # 暴击计算（简化版）
            if random.random() < 0.1:
                damage = int(damage * 1.3)
                add_battle_message(f"⚡ {teammate['name']} 暴击！", 'warning')
            
            current_enemy_hp -= damage
            
            # 更新伤害统计
            self.leaderboard['combat_stats']['total_damage'] += damage
            if damage > self.leaderboard['combat_stats']['highest_damage']:
                self.leaderboard['combat_stats']['highest_damage'] = damage
            
            add_battle_message(f"{teammate['name']} 使用攻击，对 {enemy_name} 造成了 {damage} 点伤害！", 'info')
            enemy_hp_label.config(text=f"👾 {enemy_name} HP: {current_enemy_hp}/{enemy_hp}")
            
            if current_enemy_hp <= 0:
                battle_victory()
                return
        
        def physical_attack():
            nonlocal current_enemy_hp
            if not battle_running:
                return
            
            # 玩家物理攻击（包括宝石加成和装备加成）
            total_attack = self.player.attack + self.player.gem_bonus_attack + self.player.equipment_bonus_attack
            
            # 暴击计算
            crit_chance = self.player.equipment_bonus_crit
            is_crit = random.random() < (crit_chance / 100)
            
            base_damage = max(1, total_attack - enemy_defense)
            damage_variation = random.randint(-3, 5)
            damage = max(1, base_damage + damage_variation)
            
            if is_crit:
                damage = int(damage * 1.5)
                add_battle_message(f"⚡ 暴击！", 'warning')
            
            # 吸血效果
            lifesteal = self.player.equipment_bonus_lifesteal
            if lifesteal > 0 and damage > 0:
                heal = int(damage * lifesteal / 100)
                self.player.hp = min(total_hp, self.player.hp + heal)
                add_battle_message(f"💚 吸血恢复 {heal} 点生命", 'success')
            
            current_enemy_hp -= damage
            
            # 更新伤害统计
            self.leaderboard['combat_stats']['total_damage'] += damage
            if damage > self.leaderboard['combat_stats']['highest_damage']:
                self.leaderboard['combat_stats']['highest_damage'] = damage
            
            add_battle_message(f"你使用物理攻击，对 {enemy_name} 造成了 {damage} 点伤害！", 'success')
            enemy_hp_label.config(text=f"👾 {enemy_name} HP: {current_enemy_hp}/{enemy_hp}")
            
            if current_enemy_hp <= 0:
                battle_victory()
                return
            
            # 队友攻击
            for teammate, label in teammate_labels:
                if teammate['hp'] > 0:
                    teammate_attack(teammate)
                    if current_enemy_hp <= 0:
                        return
            
            # 宠物攻击
            pet_count = 0
            for pet in self.pets:
                if pet_count >= 3:  # 最多3只宠物同时攻击
                    break
                if pet['loyalty'] >= 30:  # 忠诚度足够高才会攻击
                    # 宠物攻击 - 基于玩家攻击力
                    player_attack = self.player.attack
                    pet_attack = player_attack // 10
                    base_damage = max(1, pet_attack - enemy_defense // 3)
                    damage_variation = random.randint(-1, 2)
                    damage = max(1, base_damage + damage_variation)
                    pet_count += 1
                    
                    # 宠物技能触发
                    if random.random() < 0.2 and pet['skills']:
                        skill = random.choice(pet['skills'])
                        damage = int(damage * 1.2)
                        add_battle_message(f"🐾 {pet['name']} 使用 {skill}！", 'info')
                    
                    current_enemy_hp -= damage
                    
                    # 更新伤害统计
                    self.leaderboard['combat_stats']['total_damage'] += damage
                    if damage > self.leaderboard['combat_stats']['highest_damage']:
                        self.leaderboard['combat_stats']['highest_damage'] = damage
                    
                    add_battle_message(f"🐾 {pet['name']} 攻击了 {enemy_name}，造成 {damage} 点伤害！", 'info')
                    enemy_hp_label.config(text=f"👾 {enemy_name} HP: {current_enemy_hp}/{enemy_hp}")
                    
                    if current_enemy_hp <= 0:
                        battle_victory()
                        return
            
            enemy_attack_turn()
        
        def magic_attack():
            nonlocal current_enemy_hp
            if not battle_running:
                return
            
            if not self.player.magic_affinity:
                add_battle_message("你还未掌握魔法力量！", 'warning')
                return
            
            
            # 魔法攻击（包括装备加成）
            magic_damage = self.player.calculate_magic_damage() + self.player.equipment_bonus_magic
            damage = max(1, magic_damage - enemy_defense // 2)
            current_enemy_hp -= damage
            
            # 更新伤害统计
            self.leaderboard['combat_stats']['total_damage'] += damage
            if damage > self.leaderboard['combat_stats']['highest_damage']:
                self.leaderboard['combat_stats']['highest_damage'] = damage
            
            #self.player.magic_power -= 1
            
            # 元素效果
            weapon = self.player.equipped.get('weapon')
            if weapon and weapon in self.items:
                weapon_info = self.items[weapon]
                if 'element' in weapon_info:
                    element = weapon_info['element']
                    if element == 'fire' and random.random() < 0.3:
                        add_battle_message(f"🔥 燃烧效果！敌人每回合受到额外伤害", 'warning')
                    elif element == 'ice' and random.random() < 0.2:
                        add_battle_message(f"❄️ 冰冻效果！敌人速度降低", 'info')
                    elif element == 'lightning' and random.random() < 0.25:
                        add_battle_message(f"⚡ 麻痹效果！敌人可能无法行动", 'warning')
            
            add_battle_message(f"你使用魔法攻击，对 {enemy_name} 造成了 {damage} 点伤害！", 'info')
            enemy_hp_label.config(text=f"👾 {enemy_name} HP: {current_enemy_hp}/{enemy_hp}")
            
            if current_enemy_hp <= 0:
                battle_victory()
                return
            
            enemy_attack_turn()
        
        def use_item():
            if not battle_running:
                return
            
            # 获取可用的战斗物品
            battle_items = []
            for item_name, quantity in self.player.inventory.items():
                if item_name in self.items:
                    item_info = self.items[item_name]
                    # 消耗品都可以在战斗中使用
                    if item_info['type'] == 'consumable':
                        battle_items.append((item_name, quantity, item_info))
            
            if not battle_items:
                add_battle_message("没有可用的物品！", 'warning')
                return
            
            # 创建物品选择对话框
            item_dialog = tk.Toplevel(dialog)
            item_dialog.title("选择物品")
            item_dialog.geometry("400x300")
            item_dialog.configure(bg=self.gui.colors['bg'])
            item_dialog.transient(dialog)
            item_dialog.grab_set()
            
            # 物品列表框架
            listbox_frame = tk.Frame(item_dialog, bg=self.gui.colors['bg'])
            listbox_frame.pack(fill='both', expand=True, padx=10, pady=5)
            
            listbox = tk.Listbox(
                listbox_frame,
                font=self.gui.normal_font,
                bg='#1e1e1e',
                fg=self.gui.colors['fg'],
                height=10
            )
            listbox.pack(side='left', fill='both', expand=True)
            
            scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=listbox.yview)
            scrollbar.pack(side='right', fill='y')
            
            listbox.config(yscrollcommand=scrollbar.set)
            
            # 显示物品列表
            for item_name, quantity, item_info in battle_items:
                effect_desc = get_item_effect_description(item_info)
                listbox.insert(tk.END, f"{item_name} x{quantity} - {effect_desc}")
            
            def on_item_select():
                selection = listbox.curselection()
                if selection:
                    index = selection[0]
                    item_name = battle_items[index][0]
                    item_info = battle_items[index][2]
                    
                    if self.player.use_item(item_name):
                        # 处理不同物品的效果
                        effect_result = apply_item_effect(item_name, item_info)
                        
                        if effect_result:
                            for msg in effect_result['messages']:
                                add_battle_message(msg, effect_result.get('tag', 'info'))
                            
                            if 'hp_change' in effect_result and effect_result['hp_change'] > 0:
                                # 重新计算总生命值上限（可能有装备/宝石变化）
                                total_max_hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
                                self.player.hp = min(total_max_hp, self.player.hp + effect_result['hp_change'])
                                add_battle_message(f"❤️ 当前生命值: {self.player.hp}/{total_max_hp}", 'success')
                    
                            # 应用其他属性变化
                            if 'attack_change' in effect_result:
                                self.player.attack += effect_result['attack_change']
                                add_battle_message(f"⚔️ 攻击力临时增加 {effect_result['attack_change']} 点", 'info')
                    
                            if 'defense_change' in effect_result:
                                self.player.defense += effect_result['defense_change']
                                add_battle_message(f"🛡️ 防御力临时增加 {effect_result['defense_change']} 点", 'info')
                    
                            if 'magic_change' in effect_result:
                                self.player.equipment_bonus_magic += effect_result['magic_change']
                                add_battle_message(f"🔮 魔法攻击力临时增加 {effect_result['magic_change']} 点", 'info')
                    
                            if 'exp_gain' in effect_result:
                                self.player.gain_exp(effect_result['exp_gain'])
                                add_battle_message(f"📚 获得 {effect_result['exp_gain']} 点经验值！", 'info')
                            
                            # 更新生命值显示
                            total_hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
                            player_hp_label.config(text=f"⚔️ {self.player.name} HP: {self.player.hp}/{total_hp}")
                            
                            item_dialog.destroy()
                    else:
                        messagebox.showerror("错误", "使用物品失败！")
            
            select_btn = tk.Button(
                item_dialog,
                text="使用",
                command=on_item_select,
                font=self.gui.normal_font,
                bg=self.gui.colors['button_bg'],
                fg=self.gui.colors['button_fg'],
                width=10
            )
            select_btn.pack(pady=5)
            
            cancel_btn = tk.Button(
                item_dialog,
                text="取消",
                command=item_dialog.destroy,
                font=self.gui.normal_font,
                bg=self.gui.colors['button_bg'],
                fg=self.gui.colors['button_fg'],
                width=10
            )
            cancel_btn.pack(pady=5)
        
        def run_away():
            nonlocal battle_running
            if not battle_running:
                return
            
            # 装备可能增加逃跑成功率
            escape_bonus = self.player.equipment_bonus_speed / 100
            escape_chance = 0.5 + escape_bonus
            
            if random.random() < escape_chance:
                battle_running = False
                add_battle_message("你成功逃跑了！", 'info')
                self.gui.update_game_info()
                dialog.destroy()
            else:
                add_battle_message("逃跑失败！", 'error')
                enemy_attack_turn()
        
        def capture_monster():
            nonlocal battle_running
            if not battle_running:
                return
            
            # 检查宠物数量是否已满
            if len(self.pets) >= self.max_pet_size:
                add_battle_message("宠物栏已满，无法捕获更多宠物！", 'warning')
                return
            
            # 检查该怪物是否可捕获
            if enemy_name not in self.capturable_monsters:
                add_battle_message("该怪物无法被捕获！", 'warning')
                return
            
            monster_data = self.capturable_monsters[enemy_name]
            capture_chance = monster_data['capture_chance']
            
            # 计算捕获成功率（根据敌人当前生命值）
            health_percentage = current_enemy_hp / enemy_hp
            adjusted_chance = capture_chance * (1 - health_percentage)
            
            if random.random() < adjusted_chance:
                # 成功捕获
                pet = {
                    "name": monster_data['name'],
                    "type": monster_data['type'],
                    "level": monster_data['level'],
                    "hp": monster_data['hp'],
                    "mp": monster_data['mp'],
                    "attack": monster_data['attack'],
                    "defense": monster_data['defense'],
                    "magic_attack": monster_data['magic_attack'],
                    "skills": monster_data['skills'],
                    "experience": 0,
                    "growth_rate": monster_data['growth_rate'],
                    "evolutions": monster_data['evolutions'],
                    "passive_bonus": monster_data['passive_bonus'],
                    "loyalty": 50
                }
                
                self.pets.append(pet)
                add_battle_message(f"🎉 成功捕获 {monster_data['name']}！", 'success')
                battle_running = False
                
                # 关闭对话框
                dialog.after(2000, dialog.destroy)
            else:
                # 捕获失败
                add_battle_message("捕获失败！怪物逃跑了！", 'error')
                enemy_attack_turn()
        
        def enemy_attack_turn():
            nonlocal battle_running
            if not battle_running:
                return
            
            # 选择攻击目标：玩家或队友
            targets = ['player']
            for teammate, label in teammate_labels:
                if teammate['hp'] > 0:
                    targets.append('teammate')
            
            target_type = random.choice(targets)
            
            if target_type == 'player':
                # 敌人攻击玩家（考虑宝石和装备加成防御）
                total_defense = self.player.defense + self.player.gem_bonus_defense + self.player.equipment_bonus_defense
                
                # 闪避计算
                dodge_chance = self.player.equipment_bonus_dodge
                if random.random() < (dodge_chance / 100):
                    add_battle_message(f"💨 你闪避了敌人的攻击！", 'success')
                    # 玩家回合继续
                    return
                
                base_damage = max(1, enemy_attack - total_defense)
                damage_variation = random.randint(-3, 5)
                damage = max(1, base_damage + damage_variation)
                
                # 格挡计算
                block_chance = self.player.equipment_bonus_block
                if random.random() < (block_chance / 100):
                    damage = int(damage * 0.5)
                    add_battle_message(f"🛡️ 格挡成功！伤害减半", 'info')
                
                # 反伤效果
                thorns = self.player.equipment_bonus_thorns
                if thorns > 0 and damage > 0:
                    reflect_damage = int(damage * thorns / 100)
                    current_enemy_hp -= reflect_damage
                    add_battle_message(f"💥 反伤效果对敌人造成 {reflect_damage} 点伤害", 'warning')
                
                self.player.hp = max(0, self.player.hp - damage)
                
                add_battle_message(f"{enemy_name} 对你造成了 {damage} 点伤害！", 'error')
                total_hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
                player_hp_label.config(text=f"⚔️ {self.player.name} HP: {self.player.hp}/{total_hp}")
                
                if self.player.hp <= 0:
                    battle_defeat()
            else:
                # 敌人攻击队友
                alive_teammates = [t for t, l in teammate_labels if t['hp'] > 0]
                if alive_teammates:
                    target_teammate = random.choice(alive_teammates)
                    
                    base_damage = max(1, enemy_attack - target_teammate.get('defense', 10))
                    damage_variation = random.randint(-2, 3)
                    damage = max(1, base_damage + damage_variation)
                    
                    target_teammate['hp'] = max(0, target_teammate['hp'] - damage)
                    
                    add_battle_message(f"{enemy_name} 对 {target_teammate['name']} 造成了 {damage} 点伤害！", 'error')
                    
                    # 更新队友生命值显示
                    for teammate, label in teammate_labels:
                        if teammate == target_teammate:
                            max_hp = teammate.get('hp', 100)  # 假设队友的最大生命值就是初始值
                            label.config(text=f"🤝 {teammate['name']} ({teammate['class']}) HP: {teammate['hp']}/{max_hp}")
        
        def battle_victory():
            nonlocal battle_running
            battle_running = False
            
            # 经验加成考虑宝石和装备效果
            exp_multiplier = 1.0 + (self.player.gem_bonus_exp / 100) + (self.player.equipment_bonus_exp / 100)
            exp_gained = int(enemy_data['exp'] * diff_settings['exp_multiplier'] * exp_multiplier)
            
            # 金币加成考虑宝石和装备效果
            gold_multiplier = 1.0 + (self.player.gem_bonus_gold / 100) + (self.player.equipment_bonus_gold / 100)
            gold_gained = int(enemy_data['gold'] * diff_settings['gold_multiplier'] * gold_multiplier)
            
            # 记录敌人到图鉴
            if enemy_name not in self.compendium['enemies']:
                self.compendium['enemies'][enemy_name] = {
                    'name': enemy_name,
                    'level': 1,  # 敌人数据中没有等级，默认设为1
                    'hp': enemy_data['hp'],
                    'attack': enemy_data['attack'],
                    'defense': enemy_data['defense'],
                    'exp': enemy_data['exp'],
                    'gold': enemy_data['gold'],
                    'drops': enemy_data.get('drops', []),
                    'defeated_count': 1
                }
            else:
                # 更新击败次数
                self.compendium['enemies'][enemy_name]['defeated_count'] += 1
            
            # 更新图鉴完成度
            self.update_compendium_completion()
            
            self.player.gain_exp(exp_gained)
            self.player.gold += gold_gained
            
            add_battle_message(f"🎉 战斗胜利！获得 {exp_gained} 经验值和 {gold_gained} 金币", 'success')
            
            if 'drops' in enemy_data and enemy_data['drops']:
                for drop_item in enemy_data['drops']:
                    if random.random() < diff_settings['item_drop_chance']:
                        self.player.add_item(drop_item, 1, self)
                        add_battle_message(f"🎁 {enemy_name} 掉落了 {drop_item}！", 'success')
            
            # 队友好感度提升
            for teammate, label in teammate_labels:
                if teammate['hp'] > 0:
                    # 增加好感度
                    teammate['affection'] = min(100, teammate['affection'] + 5)
                    add_battle_message(f"❤️ {teammate['name']} 的好感度增加了5点！", 'info')
            
            # 宠物经验值和忠诚度提升
            for pet in self.pets:
                # 获得经验值
                pet['experience'] += exp_gained // 2
                # 检查是否升级
                if pet['experience'] >= 100 * pet['level']:
                    pet['level'] += 1
                    pet['experience'] -= 100 * (pet['level'] - 1)
                    # 提升属性
                    pet['hp'] = int(pet['hp'] * pet['growth_rate'])
                    pet['mp'] = int(pet['mp'] * pet['growth_rate'])
                    pet['defense'] = int(pet['defense'] * pet['growth_rate'])
                    pet['magic_attack'] = int(pet['magic_attack'] * pet['growth_rate'])
                    add_battle_message(f"🐾 {pet['name']} 升级了！现在是 {pet['level']} 级！", 'success')
                # 提升忠诚度
                pet['loyalty'] = min(100, pet['loyalty'] + 3)
                add_battle_message(f"❤️ {pet['name']} 的忠诚度增加了3点！", 'info')
            
            self.enemies_defeated += 1
            if self.enemies_defeated >= 100:
                self.unlock_achievement("战斗大师")
            
            # 更新战斗数据统计
            self.leaderboard['combat_stats']['total_kills'] += 1
            self.leaderboard['combat_stats']['battles_won'] += 1
            
            self.gui.update_game_info()
            
            # 关闭对话框
            dialog.after(2000, dialog.destroy)
        
        def battle_defeat():
            nonlocal battle_running
            battle_running = False
            
            self.player.hp = 1
            self.player.gold = max(0, self.player.gold - 50)
            add_battle_message("💀 你被击败了！损失了一些金币，勉强活了下来。", 'error')
            
            # 更新战斗数据统计
            self.leaderboard['combat_stats']['battles_lost'] += 1
            
            self.gui.update_game_info()
            
            # 关闭对话框
            dialog.after(2000, dialog.destroy)
        
        # 创建战斗按钮
        physical_btn = tk.Button(
            action_frame,
            text="⚔️ 物理攻击",
            command=physical_attack,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        physical_btn.pack(side='left', padx=5, pady=5)
        
        magic_btn = tk.Button(
            action_frame,
            text="🔮 魔法攻击",
            command=magic_attack,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        magic_btn.pack(side='left', padx=5, pady=5)
        
        item_btn = tk.Button(
            action_frame,
            text="🧪 使用物品",
            command=use_item,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        item_btn.pack(side='left', padx=5, pady=5)
        
        capture_btn = tk.Button(
            action_frame,
            text="🐾 捕获",
            command=capture_monster,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        capture_btn.pack(side='left', padx=5, pady=5)
        
        run_btn = tk.Button(
            action_frame,
            text="🏃 逃跑",
            command=run_away,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        run_btn.pack(side='left', padx=5, pady=5)
        
        # 如果体力消耗了2点，主动战斗多消耗体力已经处理
        if not active_battle:
            self.use_stamina(1)
    
    def rest(self):
        """休息恢复生命值"""
        heal_amount = min(self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp - self.player.hp, 20)
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
            self.player.add_item(treasure, 1, self)
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
            self.player.add_item("矿石", ore_count, self)
            self.add_message(f"获得 {ore_count} 个矿石！", 'success')
        elif event_name == "节日庆典":
            self.player.hp = min(self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp, self.player.hp + 30)
            self.add_message("恢复了30点生命值！", 'success')
        elif event_name == "沙尘暴":
            self.update_game_time()
            self.add_message("你花了额外的时间才穿越过去。", 'info')
        elif event_name == "发现绿洲":
            self.player.hp = min(self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp, self.player.hp + 50)
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
                self.player.add_item("熔岩样本", 1, self)
                self.add_message("你成功采集了熔岩样本！", 'success')
                self.player.gain_exp(20)
            else:
                damage = random.randint(10, 30)
                self.player.hp = max(1, self.player.hp - damage)
                self.add_message(f"采集失败！你被熔岩烫伤了，受到 {damage} 点伤害。", 'error')
        
        elif action == "寻找龙蛋":
            if random.random() < 0.3:
                self.player.add_item("龙蛋", 1, self)
                self.add_message("你发现了一个龙蛋！这是极其珍贵的宝物！", 'success')
                self.unlock_achievement("龙蛋收集者")
            else:
                self.add_message("你仔细搜索了周围，但没有找到龙蛋。", 'info')
        
        elif action == "与火焰精灵交流":
            if random.random() < 0.6:
                self.player.add_item("火焰精华", 1, self)
                self.add_message("火焰精灵对你表示友好，赠予你火焰精华。", 'success')
                self.player.gain_exp(30)
            else:
                self.add_message("火焰精灵对你保持警惕，不愿与你交流。", 'info')
        
        elif action == "参加冰雕比赛":
            if random.random() < 0.5:
                self.player.add_item("冰雕大赛奖杯", 1, self)
                self.player.gold += 100
                self.add_message("恭喜你获得冰雕比赛冠军！获得奖杯和100金币！", 'success')
                self.unlock_achievement("冰雕大师")
            else:
                self.player.add_item("参与奖", 1, self)
                self.add_message("你参加了比赛，获得了参与奖。", 'info')
        
        elif action == "寻找雪精灵":
            if random.random() < 0.4:
                self.player.add_item("雪精灵的祝福", 1, self)
                self.player.gold += 50
                self.add_message("雪精灵赐予你祝福，你获得了50金币！", 'success')
            else:
                self.add_message("雪精灵隐藏得很好，你没有找到它们。", 'info')
        
        elif action == "攀登冰峰":
            if self.player.level >= 25:
                self.player.add_item("冰峰之顶的宝石", 1, self)
                self.add_message("你成功攀登到冰峰之顶，获得了传说中的宝石！", 'success')
                self.unlock_achievement("登山家")
            else:
                damage = random.randint(20, 40)
                self.player.hp = max(1, self.player.hp - damage)
                self.add_message(f"冰峰太陡峭了，你滑倒受伤，受到 {damage} 点伤害。", 'error')
        
        elif action == "参加神圣仪式":
            if random.random() < 0.7:
                self.player.add_item("神圣光环", 1, self)
                self.player.gold += 100
                self.add_message("神圣仪式赐予你祝福，你获得了100金币！", 'success')
            else:
                self.add_message("仪式过程中出现了一些小意外，没有获得特殊效果。", 'info')
        
        elif action == "学习飞行":
            if random.random() < 0.6:
                self.player.add_item("飞行药水", 2, self)
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
                self.player.add_item("古代知识卷轴", 1, self)
                self.add_message("你成功解读了古代文字，获得了珍贵的知识卷轴！", 'success')
            else:
                self.add_message("这些文字太古老了，你只能辨认出一些片段。", 'info')
        
        elif action == "与海洋生物交流":
            if random.random() < 0.5:
                self.player.add_item("海洋之心", 1, self)
                self.add_message("海洋生物对你表示友好，赠予你海洋之心！", 'success')
            else:
                self.add_message("海洋生物对你保持警惕，迅速游走了。", 'info')
        
        elif action == "参加幽灵舞会":
            if random.random() < 0.6:
                self.player.add_item("幽灵礼服", 1, self)
                self.add_message("幽灵们欢迎你的加入，赠予你一件幽灵礼服！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("舞会中有些幽灵表现得很不友好，你被阴气所伤。", 'error')
        
        elif action == "解开诅咒":
            if random.random() < 0.3:
                self.player.add_item("净化之石", 1, self)
                self.add_message("你成功解开了一部分诅咒，获得了净化之石！", 'success')
                self.unlock_achievement("驱魔师")
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("诅咒的力量比你想象的更强大，你受到了反噬。", 'error')
        
        elif action == "与亡灵对话":
            if random.random() < 0.5:
                self.player.add_item("亡灵的记忆", 1, self)
                self.add_message("亡灵向你透露了一些秘密，获得了亡灵的记忆！", 'success')
            else:
                self.add_message("亡灵似乎有太多的怨恨，不愿意与你交流。", 'info')
        
        elif action == "参加拍卖":
            if self.player.gold >= 50:
                item = random.choice(["稀有商品", "魔法水晶", "飞行药水"])
                self.player.add_item(item, 1, self)
                self.player.gold -= 50
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
                self.player.add_item(rare_item, 1, self)
                self.add_message(f"你找到了极其稀有的 {rare_item}！", 'success')
            else:
                self.add_message("今天的运气不太好，没有找到特别稀有的商品。", 'info')
        
        elif action == "学习锻造":
            if random.random() < 0.6:
                self.player.add_item("矮人锻造手册", 1, self)
                self.add_message("矮人铁匠教会了你一些锻造技巧，获得锻造手册！", 'success')
            else:
                self.add_message("锻造比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "打造神器":
            if self.player.gold >= 100 and "稀有金属" in self.player.inventory:
                self.player.gold -= 100
                self.player.remove_item("稀有金属", 1)
                weapon = random.choice(["烈焰剑", "雷霆斧", "冰霜匕首"])
                self.player.add_item(weapon, 1, self)
                self.add_message(f"你成功打造了 {weapon}！", 'success')
            else:
                self.add_message("你缺少必要的材料和金币来打造神器。", 'warning')
        
        elif action == "参加锻造比赛":
            if random.random() < 0.5:
                self.player.gold += 80
                self.player.add_item("锻造大赛奖牌", 1, self)
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
                self.player.add_item("书中世界的纪念品", 1, self)
                self.player.gain_exp(40)
                self.add_message("你在书中世界的冒险让你收获颇丰！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("书中世界的冒险充满危险，你受了一些伤。", 'error')
        
        elif action == "学习禁书知识":
            if random.random() < 0.3:
                self.player.add_item("禁书", 1, self)
                self.player.gold += 150
                self.add_message("禁书知识赐予你智慧，你获得了150金币！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("禁书的黑暗力量反噬了你，受到30点伤害。", 'error')
        
        elif action == "破解机关":
            if random.random() < 0.5:
                self.player.add_item("机关图纸", 1, self)
                self.add_message("你成功破解了神庙机关，获得了机关图纸！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("机关触发了陷阱，你勉强逃脱但受了伤。", 'error')
        
        elif action == "寻找宝藏":
            if random.random() < 0.2:
                self.player.gold += random.randint(200, 500)
                self.player.add_item("神秘宝物", 1, self)
                self.add_message("你找到了传说中的宝藏！获得大量金币和神秘宝物！", 'success')
                self.unlock_achievement("宝藏猎人")
            else:
                self.add_message("你搜索了很久，但宝藏似乎被藏在了更隐蔽的地方。", 'info')
        
        elif action == "接受神的试炼":
            if self.player.level >= 15:
                self.player.gain_exp(100)
                self.player.add_item("神的祝福", 1, self)
                self.add_message("你通过了神的试炼，获得100点经验值和神的祝福！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 50)
                self.add_message("试炼太困难了，你失败了并受到了严重的伤害。", 'error')
        
        elif action == "接受龙的试炼":
            if self.player.level >= 30:
                self.player.add_item("龙骑士徽章", 1, self)
                self.player.gold += 300
                self.add_message("你通过了龙的试炼，成为了一名龙骑士！获得300金币！", 'success')
                self.unlock_achievement("龙骑士")
            else:
                self.player.hp = max(1, self.player.hp - 60)
                self.add_message("龙的试炼极其危险，你被龙焰烧伤，受到60点伤害。", 'error')
        
        elif action == "学习龙语":
            if random.random() < 0.4:
                self.player.add_item("龙语词典", 1, self)
                self.add_message("你学会了基础的龙语，获得龙语词典！", 'success')
            else:
                self.add_message("龙语比你想象的要复杂，还需要更多练习。", 'info')
        
        # 大集市操作
        elif action == "随机商品购买":
            if self.player.gold >= 30:
                item = random.choice(["稀有药水", "魔法卷轴", "神秘水晶"])
                self.player.add_item(item, 1, self)
                self.player.gold -= 30
                self.add_message(f"你购买了 {item}，花费了30金币。", 'success')
            else:
                self.add_message("你没有足够的金币购买商品。", 'warning')
        
        elif action == "珍品拍卖":
            if self.player.gold >= 100:
                rare_item = random.choice(["传说武器", "稀有护甲", "魔法饰品"])
                self.player.add_item(rare_item, 1, self)
                self.player.gold -= 100
                self.add_message(f"你在拍卖会上拍到了 {rare_item}，花费了100金币。", 'success')
            else:
                self.add_message("你没有足够的金币参加珍品拍卖。", 'warning')
        
        elif action == "黑市交易":
            if random.random() < 0.6:
                self.player.gold += random.randint(80, 200)
                self.add_message("黑市交易成功，获得了丰厚的利润！", 'success')
            else:
                self.player.gold = max(0, self.player.gold - 50)
                self.add_message("交易被守卫发现了，你不得不交出一部分金币才得以脱身。", 'error')
        
        # 龙穴操作
        elif action == "获取龙之力":
            if random.random() < 0.3:
                self.player.gold += 100
                self.add_message("你成功获取了龙之力，金币增加100枚！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 40)
                self.add_message("获取龙之力失败，你被龙的力量反噬，受到40点伤害。", 'error')
        
        elif action == "成为龙骑士":
            if self.player.level >= 35:
                self.player.add_item("龙骑士套装", 1, self)
                self.add_message("你成功成为了一名龙骑士，获得了龙骑士套装！", 'success')
                self.unlock_achievement("龙骑士大师")
            else:
                self.add_message("你的等级还不足以成为龙骑士，需要达到35级。", 'warning')
        
        # 矮人矿坑操作
        elif action == "挖矿":
            if random.random() < 0.7:
                ore = random.choice(["秘银矿石", "精金矿石", "钻石"])
                self.player.add_item(ore, 1, self)
                self.add_message(f"你挖到了 {ore}！", 'success')
            else:
                self.add_message("你挖了很久，但没有找到有价值的矿石。", 'info')
        
        elif action == "锻造武器":
            if self.player.gold >= 50 and "秘银矿石" in self.player.inventory:
                self.player.gold -= 50
                self.player.remove_item("秘银矿石", 1)
                weapon = random.choice(["秘银剑", "精金斧", "钻石匕首"])
                self.player.add_item(weapon, 1, self)
                self.add_message(f"你成功锻造了 {weapon}！", 'success')
            else:
                self.add_message("你缺少必要的材料和金币来锻造武器。", 'warning')
        
        elif action == "参加矮人宴会":
            self.player.gold += 50
            self.player.gain_exp(30)
            self.add_message("你参加了矮人宴会，获得了50金币和30点经验值！", 'success')
        
        # 古代图书馆操作
        elif action == "学习禁术":
            if random.random() < 0.3:
                self.player.add_item("禁术卷轴", 1, self)
                self.player.gold += 100
                self.add_message("你学会了禁术，金币增加100枚！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 35)
                self.add_message("学习禁术失败，你被黑暗力量反噬，受到35点伤害。", 'error')
        
        # 机械都市操作
        elif action == "发明创造":
            if self.player.gold >= 80:
                self.player.gold -= 80
                invention = random.choice(["机械宠物", "自动采集器", "飞行装置"])
                self.player.add_item(invention, 1)
                self.add_message(f"你成功发明了 {invention}！", 'success')
            else:
                self.add_message("你没有足够的金币进行发明创造。", 'warning')
        
        elif action == "改造机械":
            if "机械零件" in self.player.inventory:
                self.player.remove_item("机械零件", 1)
                self.player.add_item("强化机械零件", 1)
                self.add_message("你成功改造了机械零件，获得了强化机械零件！", 'success')
            else:
                self.add_message("你缺少机械零件来进行改造。", 'warning')
        
        elif action == "参加科技展":
            if random.random() < 0.5:
                self.player.add_item("科技展览纪念品", 1)
                self.player.gold += 60
                self.add_message("你在科技展上获得了纪念品和60金币！", 'success')
            else:
                self.add_message("科技展很有趣，但你没有获得特别的奖励。", 'info')
        
        # 恶魔深渊操作
        elif action == "恶魔契约":
            if random.random() < 0.4:
                self.player.attack += 20
                self.player.hp -= 50
                self.add_message("你与恶魔签订了契约，攻击力增加20点，但生命值减少50点！", 'warning')
            else:
                self.player.hp = max(1, self.player.hp - 60)
                self.add_message("契约签订失败，你受到了恶魔的惩罚，受到60点伤害。", 'error')
        
        elif action == "灵魂救赎":
            if random.random() < 0.5:
                self.player.hp += 50
                self.add_message("你成功救赎了一个灵魂，生命值增加50点！", 'success')
            else:
                self.add_message("救赎失败，灵魂不愿被拯救。", 'info')
        
        elif action == "地狱探险":
            if random.random() < 0.3:
                self.player.add_item("地狱之火", 1)
                self.player.gain_exp(80)
                self.add_message("你在地狱探险中获得了地狱之火和80点经验值！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 45)
                self.add_message("地狱探险充满危险，你受了重伤。", 'error')
        
        # 云中村庄操作
        elif action == "云朵采集":
            if random.random() < 0.6:
                self.player.add_item("云朵精华", 1)
                self.add_message("你成功采集了云朵精华！", 'success')
            else:
                self.add_message("云朵太稀薄了，你没有采集到足够的精华。", 'info')
        
        elif action == "参加飞行比赛":
            if random.random() < 0.4:
                self.player.add_item("飞行比赛奖杯", 1)
                self.player.gold += 120
                self.add_message("你在飞行比赛中获得了冠军，获得奖杯和120金币！", 'success')
            else:
                self.add_message("比赛竞争很激烈，你没有获得名次。", 'info')
        
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
                self.player.hp = self.player.max_hp + self.player.gem_bonus_hp + self.player.equipment_bonus_hp
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
                self.player.add_item(treasure, 1, self)
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
                {"name": "魔法攻击药水", "price": 300, "effect": "魔法攻击+5"},
                {"name": "幸运符", "price": 250, "effect": "掉落率提升"}
            ]
            
            item = random.choice(random_items)
            self.add_message(f"🎪 商人向你推荐：{item['name']} - {item['price']}金币 - {item['effect']}", 'info')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("购买", f"要购买 {item['name']} 吗？"):
                    self.player.add_item(item['name'], 1)
                    self.player.gold -= item['price']
                    self.add_message(f"购买成功！获得 {item['name']}", 'success')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        elif action == "珍品拍卖":
            rare_items = [
                {"name": "传说武器", "price": 800, "effect": "攻击+15，魔法+10"},
                {"name": "史诗护甲", "price": 1000, "effect": "防御+15，生命+50"},
                {"name": "生命宝石", "price": 1200, "effect": "生命值+100"},
                {"name": "魔法宝石", "price": 1200, "effect": "魔法攻击+20"},
                {"name": "神圣护符", "price": 1500, "effect": "全属性+10"},
                {"name": "时光沙漏", "price": 2000, "effect": "立即升1级"}
            ]
            
            item = random.choice(rare_items)
            self.add_message(f"🏆 珍品拍卖：{item['name']} - 起拍价 {item['price']}金币 - {item['effect']}", 'info')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("竞拍", f"要出价 {item['price']} 金币竞拍 {item['name']} 吗？"):
                    if random.random() < 0.8:
                        self.player.add_item(item['name'], 1)
                        self.player.gold -= item['price']
                        self.add_message(f"竞拍成功！获得 {item['name']}", 'success')
                    else:
                        self.add_message("很遗憾，有人出价更高，你竞拍失败了。", 'warning')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        elif action == "黑市交易":
            black_market_items = [
                {"name": "诅咒之剑", "price": 500, "effect": "攻击+20，吸血5%"},
                {"name": "灵魂石", "price": 800, "effect": "可以复活一次"},
                {"name": "黑暗水晶", "price": 600, "effect": "战斗中20%概率秒杀敌人"},
                {"name": "命运骰子", "price": 1000, "effect": "使用后随机获得或失去物品"},
                {"name": "神秘药水", "price": 300, "effect": "效果随机"},
                {"name": "恶魔契约", "price": 1500, "effect": "全属性+15，但每回合损失5生命"}
            ]
            
            item = random.choice(black_market_items)
            self.add_message(f"🌑 黑市商人悄悄对你说：我有一些...特殊商品...", 'warning')
            self.add_message(f"🔪 商品：{item['name']} - {item['price']}金币 - {item['effect']}", 'warning')
            
            if self.player.gold >= item['price']:
                if messagebox.askyesno("黑市交易", f"要进行黑市交易，购买 {item['name']} 吗？"):
                    self.player.add_item(item['name'], 1)
                    self.player.gold -= item['price']
                    self.add_message(f"交易完成！获得 {item['name']}", 'success')
            else:
                self.add_message(f"金币不足！需要 {item['price']} 金币。", 'warning')
        
        # 花之森林操作
        elif action == "采集花粉":
            if random.random() < 0.7:
                self.player.add_item("花粉", random.randint(1, 3))
                self.add_message("你成功采集了一些花粉！", 'success')
            else:
                self.add_message("今天的花粉似乎特别少，你没有采集到多少。", 'info')
        
        elif action == "种植魔法植物":
            if "魔法种子" in self.player.inventory:
                self.player.remove_item("魔法种子", 1)
                self.player.add_item("魔法植物", 1)
                self.add_message("你成功种植了一株魔法植物！", 'success')
            else:
                self.add_message("你需要魔法种子才能种植魔法植物。", 'warning')
        
        elif action == "与花精灵交流":
            if random.random() < 0.5:
                self.player.add_item("花精灵的祝福", 1)
                self.add_message("花精灵对你表示友好，赠予你她们的祝福！", 'success')
            else:
                self.add_message("花精灵们正在忙碌，没有时间与你交流。", 'info')
        
        # 时间维度操作
        elif action == "时间旅行":
            if random.random() < 0.4:
                self.player.add_item("时间沙漏", 1)
                self.add_message("你成功进行了一次时间旅行，获得了时间沙漏！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("时间旅行过程中出现了异常，你受到了时间乱流的伤害。", 'error')
        
        # 天界王座操作
        elif action == "最终试炼":
            if self.player.level >= 35:
                self.player.gain_exp(150)
                self.player.add_item("最终试炼证明", 1)
                self.add_message("你通过了最终试炼，获得150点经验值和试炼证明！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 60)
                self.add_message("最终试炼太困难了，你失败了并受到了严重的伤害。", 'error')
        
        elif action == "成神之路":
            if self.player.level >= 40:
                self.player.add_item("神格", 1)
                self.add_message("你开始了成神之路，获得了神格！", 'success')
            else:
                self.add_message("你的等级还不足以踏上成神之路，需要达到40级。", 'warning')
        
        elif action == "世界拯救":
            if self.player.level >= 40:
                self.player.add_item("世界之心", 1)
                self.add_message("你成功拯救了世界，获得了世界之心！", 'success')
                self.unlock_achievement("世界守护者")
            else:
                self.add_message("你的力量还不足以拯救世界，需要达到40级。", 'warning')
        
        # 时间维度 - 远古时代操作
        elif action == "学习原始技能":
            if random.random() < 0.6:
                self.player.add_item("原始技能手册", 1)
                self.add_message("你学会了一些原始技能，获得技能手册！", 'success')
            else:
                self.add_message("原始技能比你想象的要难学，还需要更多练习。", 'info')
        
        elif action == "参与部落仪式":
            if random.random() < 0.5:
                self.player.add_item("部落勇士徽章", 1)
                self.add_message("部落接受了你，授予你勇士徽章！", 'success')
            else:
                self.add_message("部落仪式中出现了一些小意外，你没有获得特别的认可。", 'info')
        
        elif action == "探索史前遗迹":
            if random.random() < 0.3:
                self.player.add_item("史前 artifact", 1)
                self.add_message("你在史前遗迹中发现了一件珍贵的 artifact！", 'success')
            else:
                self.add_message("史前遗迹已经被探索过很多次，你没有发现特别的东西。", 'info')
        
        # 时间维度 - 中世纪操作
        elif action == "成为骑士":
            if self.player.level >= 25:
                self.player.add_item("骑士铠甲", 1)
                self.add_message("你成功成为了一名骑士，获得了骑士铠甲！", 'success')
            else:
                self.add_message("你的等级还不足以成为骑士，需要达到25级。", 'warning')
        
        elif action == "学习魔法":
            if random.random() < 0.5:
                self.player.add_item("魔法书", 1)
                self.add_message("你学会了基础的魔法，获得魔法书！", 'success')
            else:
                self.add_message("魔法学习比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "参与宫廷政治":
            if random.random() < 0.4:
                self.player.add_item("宫廷勋章", 1)
                self.add_message("你在宫廷政治中表现出色，获得了宫廷勋章！", 'success')
            else:
                self.add_message("宫廷政治复杂多变，你需要更多的经验。", 'info')
        
        # 时间维度 - 工业革命操作
        elif action == "发明新机器":
            if self.player.gold >= 100:
                self.player.gold -= 100
                invention = random.choice(["蒸汽机", "织布机", "火车模型"])
                self.player.add_item(invention, 1)
                self.add_message(f"你成功发明了 {invention}！", 'success')
            else:
                self.add_message("你没有足够的金币进行发明创造。", 'warning')
        
        elif action == "组织工人运动":
            if random.random() < 0.5:
                self.player.add_item("工人领袖徽章", 1)
                self.add_message("你成功组织了工人运动，获得了领袖徽章！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("工人运动中出现了冲突，你受了一些伤。", 'error')
        
        elif action == "参观工厂":
            if random.random() < 0.6:
                self.player.add_item("工厂参观纪念章", 1)
                self.add_message("你参观了工厂，了解了工业生产的流程，获得纪念章！", 'success')
            else:
                self.add_message("工厂正在忙碌，你只能简单地参观一下。", 'info')
        
        # 时间维度 - 未来都市操作
        elif action == "使用未来科技":
            if random.random() < 0.5:
                self.player.add_item("未来科技装置", 1)
                self.add_message("你体验了未来科技，获得了一个科技装置！", 'success')
            else:
                self.add_message("未来科技太先进了，你还需要时间适应。", 'info')
        
        elif action == "与AI交流":
            if random.random() < 0.6:
                self.player.add_item("AI助手", 1)
                self.add_message("AI对你表示友好，成为了你的助手！", 'success')
            else:
                self.add_message("AI似乎很忙，没有时间与你深入交流。", 'info')
        
        # 时间维度 - 末日后世界操作
        elif action == "探索废土":
            if random.random() < 0.6:
                item = random.choice(["废土物资", "战前科技", "辐射防护装备"])
                self.player.add_item(item, 1, self)
                self.add_message(f"你在废土中发现了 {item}！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("废土中充满了危险，你遇到了一些辐射生物。", 'error')
        
        elif action == "与掠夺者交易":
            if random.random() < 0.5:
                self.player.gold += random.randint(50, 150)
                self.add_message("掠夺者接受了你的交易，你获得了一些金币！", 'success')
            else:
                self.player.gold = max(0, self.player.gold - 50)
                self.add_message("交易过程中出现了冲突，你失去了一些金币。", 'error')
        
        elif action == "重建家园":
            if self.player.gold >= 200:
                self.player.gold -= 200
                self.player.add_item("重建许可证", 1)
                self.add_message("你开始了重建家园的计划，获得了重建许可证！", 'success')
            else:
                self.add_message("你没有足够的金币来重建家园。", 'warning')
        
        # 时间维度 - 古埃及操作
        elif action == "探索金字塔":
            if random.random() < 0.3:
                self.player.add_item("法老宝藏", 1)
                self.add_message("你在金字塔中发现了法老的宝藏！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("金字塔中充满了陷阱，你不小心触发了一个。", 'error')
        
        elif action == "学习象形文字":
            if random.random() < 0.4:
                self.player.add_item("象形文字词典", 1)
                self.add_message("你学会了象形文字，获得了词典！", 'success')
            else:
                self.add_message("象形文字太古老了，你只能辨认出一些简单的符号。", 'info')
        
        elif action == "参与宗教仪式":
            if random.random() < 0.5:
                self.player.add_item("宗教圣物", 1)
                self.add_message("你参与了宗教仪式，获得了宗教圣物！", 'success')
            else:
                self.add_message("仪式过程中出现了一些小意外，你没有获得特别的物品。", 'info')
        
        # 时间维度 - 维京时代操作
        elif action == "成为海盗":
            if self.player.level >= 25:
                self.player.add_item("海盗船长帽", 1)
                self.add_message("你成功成为了一名海盗，获得了船长帽！", 'success')
            else:
                self.add_message("你的等级还不足以成为海盗，需要达到25级。", 'warning')
        
        elif action == "探索北欧神话":
            if random.random() < 0.4:
                self.player.add_item("北欧神话书籍", 1)
                self.add_message("你深入了解了北欧神话，获得了神话书籍！", 'success')
            else:
                self.add_message("北欧神话非常复杂，你需要更多的时间来研究。", 'info')
        
        elif action == "参与维京盛宴":
            self.player.gold += 80
            self.player.gain_exp(40)
            self.add_message("你参加了维京盛宴，获得了80金币和40点经验值！", 'success')
        
        # 时间维度 - 封建日本操作
        elif action == "学习剑道":
            if random.random() < 0.5:
                self.player.add_item("剑道手册", 1)
                self.add_message("你学会了剑道的基础，获得了剑道手册！", 'success')
            else:
                self.add_message("剑道学习比你想象的要困难，还需要更多练习。", 'info')
        
        elif action == "成为忍者":
            if self.player.level >= 30:
                self.player.add_item("忍者套装", 1)
                self.add_message("你成功成为了一名忍者，获得了忍者套装！", 'success')
            else:
                self.add_message("你的等级还不足以成为忍者，需要达到30级。", 'warning')
        
        elif action == "参与樱花节":
            if random.random() < 0.6:
                self.player.add_item("樱花徽章", 1)
                self.add_message("你参加了樱花节，获得了樱花徽章！", 'success')
            else:
                self.add_message("樱花节很热闹，但你没有获得特别的物品。", 'info')
        
        # 时间维度 - 太空时代操作
        elif action == "星际旅行":
            if random.random() < 0.4:
                self.player.add_item("星际飞船模型", 1)
                self.add_message("你进行了一次星际旅行，获得了飞船模型！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("星际旅行过程中遇到了太空辐射，你受了一些伤。", 'error')
        
        elif action == "与外星人交流":
            if random.random() < 0.5:
                self.player.add_item("外星纪念品", 1)
                self.add_message("外星人对你表示友好，赠予你一件纪念品！", 'success')
            else:
                self.add_message("外星人对你保持警惕，没有与你深入交流。", 'info')
        
        elif action == "太空站工作":
            if random.random() < 0.6:
                self.player.gold += 100
                self.add_message("你在太空站工作了一段时间，获得了100金币！", 'success')
            else:
                self.add_message("太空站的工作很辛苦，你没有获得特别的奖励。", 'info')
        
        # 时间维度 - 时间虚空操作
        elif action == "修复时间线":
            if random.random() < 0.3:
                self.player.add_item("时间修复器", 1)
                self.add_message("你成功修复了时间线，获得了时间修复器！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 40)
                self.add_message("修复时间线的过程中出现了异常，你受到了时间乱流的伤害。", 'error')
        
        elif action == "挑战时间领主":
            if self.player.level >= 35:
                self.add_message("你准备挑战时间领主，这将是一场与时间的对决！", 'info')
                # 这里可以触发与时间领主的战斗
            else:
                self.add_message("你的等级还不足以挑战时间领主，需要达到35级。", 'warning')
        
        # 梦境维度 - 甜美梦境操作
        elif action == "重温美好回忆":
            if random.random() < 0.6:
                self.player.hp += 30
                self.add_message("重温美好回忆让你感到心情愉悦，恢复了30点生命值！", 'success')
            else:
                self.add_message("你尝试回忆美好时光，但有些记忆已经模糊了。", 'info')
        
        elif action == "与快乐精灵玩耍":
            if random.random() < 0.5:
                self.player.add_item("快乐精灵的礼物", 1)
                self.add_message("快乐精灵们喜欢你，赠予你一件礼物！", 'success')
            else:
                self.add_message("快乐精灵们正在玩耍，没有注意到你。", 'info')
        
        elif action == "收集梦境精华":
            if random.random() < 0.6:
                self.player.add_item("梦境精华", 1)
                self.add_message("你成功收集了梦境精华！", 'success')
            else:
                self.add_message("梦境精华很稀少，你没有收集到。", 'info')
        
        # 梦境维度 - 噩梦世界操作
        elif action == "面对恐惧":
            if random.random() < 0.5:
                self.player.add_item("勇气徽章", 1)
                self.add_message("你勇敢地面对了恐惧，获得了勇气徽章！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("恐惧的力量太强大了，你受到了一些精神伤害。", 'error')
        
        elif action == "挑战噩梦":
            if random.random() < 0.4:
                self.player.add_item("噩梦征服者徽章", 1)
                self.add_message("你成功挑战了噩梦，获得了征服者徽章！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("噩梦的力量太强大了，你暂时无法战胜它。", 'error')
        
        elif action == "收集勇气":
            if random.random() < 0.6:
                self.player.add_item("勇气结晶", 1)
                self.add_message("你成功收集了勇气结晶！", 'success')
            else:
                self.add_message("勇气结晶很稀少，你没有收集到。", 'info')
        
        # 梦境维度 - 奇幻梦境操作
        elif action == "学习梦境魔法":
            if random.random() < 0.5:
                self.player.add_item("梦境魔法书", 1)
                self.add_message("你学会了梦境魔法，获得了魔法书！", 'success')
            else:
                self.add_message("梦境魔法比你想象的要复杂，还需要更多练习。", 'info')
        
        elif action == "与奇幻生物交流":
            if random.random() < 0.5:
                self.player.add_item("奇幻生物的礼物", 1)
                self.add_message("奇幻生物对你表示友好，赠予你一件礼物！", 'success')
            else:
                self.add_message("奇幻生物对你保持警惕，没有与你深入交流。", 'info')
        
        elif action == "实现梦想":
            if random.random() < 0.3:
                self.player.add_item("梦想实现石", 1)
                self.add_message("你的梦想成真了，获得了梦想实现石！", 'success')
            else:
                self.add_message("梦想需要更多的努力才能实现。", 'info')
        
        # 梦境维度 - 冒险梦境操作
        elif action == "探索迷宫":
            if random.random() < 0.5:
                self.player.add_item("迷宫地图", 1)
                self.add_message("你成功探索了迷宫，获得了迷宫地图！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("迷宫中充满了陷阱，你不小心触发了一个。", 'error')
        
        elif action == "完成冒险":
            if random.random() < 0.4:
                self.player.add_item("冒险勋章", 1)
                self.add_message("你成功完成了冒险，获得了冒险勋章！", 'success')
            else:
                self.add_message("冒险还没有完全结束，你需要继续努力。", 'info')
        
        # 梦境维度 - 浪漫梦境操作
        elif action == "浪漫约会":
            if random.random() < 0.5:
                self.player.add_item("浪漫纪念品", 1)
                self.add_message("你度过了一个浪漫的约会，获得了纪念品！", 'success')
            else:
                self.add_message("约会过程中出现了一些小意外，没有特别的收获。", 'info')
        
        elif action == "爱情表白":
            if random.random() < 0.4:
                self.player.add_item("爱情结晶", 1)
                self.add_message("你的表白成功了，获得了爱情结晶！", 'success')
            else:
                self.add_message("表白没有成功，但至少你尝试了。", 'info')
        
        elif action == "收集幸福":
            if random.random() < 0.6:
                self.player.add_item("幸福结晶", 1)
                self.add_message("你成功收集了幸福结晶！", 'success')
            else:
                self.add_message("幸福结晶很稀少，你没有收集到。", 'info')
        
        # 梦境维度 - 神秘梦境操作
        elif action == "探索神秘":
            if random.random() < 0.4:
                self.player.add_item("神秘 artifact", 1)
                self.add_message("你在神秘梦境中发现了一件 artifact！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("神秘梦境中充满了未知的危险，你受了一些伤。", 'error')
        
        elif action == "解读预言":
            if random.random() < 0.3:
                self.player.add_item("预言卷轴", 1)
                self.add_message("你成功解读了预言，获得了预言卷轴！", 'success')
            else:
                self.add_message("预言太模糊了，你只能理解一部分。", 'info')
        
        elif action == "与神秘生物交流":
            if random.random() < 0.5:
                self.player.add_item("神秘生物的礼物", 1)
                self.add_message("神秘生物对你表示友好，赠予你一件礼物！", 'success')
            else:
                self.add_message("神秘生物对你保持警惕，没有与你深入交流。", 'info')
        
        # 梦境维度 - 童年梦境操作
        elif action == "重温童年游戏":
            if random.random() < 0.6:
                self.player.add_item("童年玩具", 1)
                self.add_message("你重温了童年游戏，获得了一个童年玩具！", 'success')
            else:
                self.add_message("童年游戏的记忆有些模糊了。", 'info')
        
        elif action == "与童年玩伴玩耍":
            if random.random() < 0.5:
                self.player.add_item("友谊徽章", 1)
                self.add_message("你与童年玩伴一起玩耍，获得了友谊徽章！", 'success')
            else:
                self.add_message("童年玩伴似乎很忙，没有时间与你玩耍。", 'info')
        
        elif action == "守护纯真":
            if random.random() < 0.4:
                self.player.add_item("纯真结晶", 1)
                self.add_message("你成功守护了纯真，获得了纯真结晶！", 'success')
            else:
                self.add_message("守护纯真需要更多的努力。", 'info')
        
        # 梦境维度 - 英雄梦境操作
        elif action == "成为英雄":
            if self.player.level >= 30:
                self.player.add_item("英雄套装", 1)
                self.add_message("你成功成为了一名英雄，获得了英雄套装！", 'success')
            else:
                self.add_message("你的等级还不足以成为英雄，需要达到30级。", 'warning')
        
        elif action == "执行英雄任务":
            if random.random() < 0.5:
                self.player.add_item("英雄任务完成证明", 1)
                self.add_message("你成功完成了英雄任务，获得了完成证明！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 25)
                self.add_message("英雄任务很困难，你受了一些伤。", 'error')
        
        elif action == "挑战邪恶":
            if random.random() < 0.4:
                self.player.add_item("正义结晶", 1)
                self.add_message("你成功挑战了邪恶，获得了正义结晶！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 30)
                self.add_message("邪恶的力量太强大了，你暂时无法战胜它。", 'error')
        
        # 梦境维度 - 宇宙梦境操作
        elif action == "宇宙探索":
            if random.random() < 0.4:
                self.player.add_item("宇宙尘埃", 1)
                self.add_message("你在宇宙中探索，获得了宇宙尘埃！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 20)
                self.add_message("宇宙中充满了危险，你遇到了一些太空辐射。", 'error')
        
        elif action == "与星际生物交流":
            if random.random() < 0.5:
                self.player.add_item("星际生物的礼物", 1)
                self.add_message("星际生物对你表示友好，赠予你一件礼物！", 'success')
            else:
                self.add_message("星际生物对你保持警惕，没有与你深入交流。", 'info')
        
        # 梦境维度 - 梦境核心操作
        elif action == "掌控梦境":
            if random.random() < 0.3:
                self.player.add_item("梦境控制器", 1)
                self.add_message("你成功掌控了梦境，获得了梦境控制器！", 'success')
            else:
                self.player.hp = max(1, self.player.hp - 40)
                self.add_message("掌控梦境的过程中出现了异常，你受到了精神伤害。", 'error')
        
        elif action == "平衡现实":
            if random.random() < 0.4:
                self.player.add_item("现实平衡器", 1)
                self.add_message("你成功平衡了现实与梦境，获得了现实平衡器！", 'success')
            else:
                self.add_message("平衡现实与梦境需要更多的努力。", 'info')
        
        elif action == "挑战梦境主宰":
            if self.player.level >= 40:
                self.add_message("你准备挑战梦境主宰，这将是一场史诗般的战斗！", 'info')
                # 这里可以触发与梦境主宰的战斗
            else:
                self.add_message("你的等级还不足以挑战梦境主宰，需要达到40级。", 'warning')
        
        else:
            self.add_message(f"你尝试了{action}，但没有特别的事情发生。", 'info')
        
        self.update_game_time()
        self.gui.update_game_info()
    
    def show_crafting_system(self):
        """显示合成系统"""
        if not self.player:
            messagebox.showinfo("提示", "请先开始游戏！")
            return
        
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("合成系统")
        dialog.geometry("700x600")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="合成系统",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg=self.gui.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 按类型分组
        recipe_types = {
            "药剂合成": [],
            "材料合成": [],
            "特殊合成": []
        }
        
        for recipe_name, recipe_data in self.crafting_recipes.items():
            if recipe_data['type'] in ['consumable']:
                recipe_types["药剂合成"].append((recipe_name, recipe_data))
            elif recipe_data['type'] in ['material']:
                recipe_types["材料合成"].append((recipe_name, recipe_data))
            else:
                recipe_types["特殊合成"].append((recipe_name, recipe_data))
        
        # 通用滚轮函数
        def on_mouse_wheel(event, canvas):
            if event.delta:
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        def bind_wheel_recursive(widget, canvas):
            widget.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            for child in widget.winfo_children():
                bind_wheel_recursive(child, canvas)
        
        for type_name, recipes in recipe_types.items():
            if not recipes:
                continue
                
            type_frame = tk.Frame(notebook, bg='#1e1e1e')
            notebook.add(type_frame, text=type_name)
            
            canvas = tk.Canvas(type_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(type_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 绑定滚轮
            canvas.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            
            for recipe_name, recipe_data in recipes:
                # 检查材料是否足够
                has_materials = True
                for material, amount in recipe_data['ingredients'].items():
                    if material not in self.player.inventory or self.player.inventory[material] < amount:
                        has_materials = False
                        break
                
                recipe_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=recipe_name,
                    font=self.gui.normal_font,
                    fg=self.gui.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge'
                )
                recipe_frame.pack(fill='x', padx=5, pady=5)
                
                desc_label = tk.Label(
                    recipe_frame,
                    text=recipe_data['description'],
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=500
                )
                desc_label.pack(fill='x', padx=5, pady=2)
                
                # 材料列表
                material_parts = []
                for material, amount in recipe_data['ingredients'].items():
                    if material in self.player.inventory:
                        current = self.player.inventory[material]
                        color = self.gui.colors['success'] if current >= amount else self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/{current}")
                    else:
                        color = self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/0")
                
                materials_label = tk.Label(
                    recipe_frame,
                    text="📦 所需材料: " + ", ".join(material_parts),
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                materials_label.pack(fill='x', padx=5, pady=2)
                
                # 结果信息
                result_info = f"✨ 结果: {recipe_data['result']['item']} x{recipe_data['result']['quantity']}"
                
                result_label = tk.Label(
                    recipe_frame,
                    text=result_info,
                    font=self.gui.small_font,
                    fg=self.gui.colors['success'],
                    bg='#1e1e1e'
                )
                result_label.pack(fill='x', padx=5, pady=2)
                
                # 合成按钮
                def craft(r_name=recipe_name, r_data=recipe_data, r_has_materials=has_materials):
                    # 再次检查材料，确保按钮亮起时一定有材料
                    if not r_has_materials:
                        # 如果按钮是亮的但材料不足，说明有问题，重新检查
                        has_materials_now = True
                        for material, amount in r_data['ingredients'].items():
                            if material not in self.player.inventory or self.player.inventory[material] < amount:
                                has_materials_now = False
                                break
                        
                        if not has_materials_now:
                            messagebox.showerror("错误", f"材料不足！\n请检查所需材料是否足够。")
                            # 刷新界面
                            dialog.destroy()
                            self.show_crafting_system()
                            return
                    
                    # 扣除材料
                    for material, amount in r_data['ingredients'].items():
                        self.player.remove_item(material, amount)
                    
                    # 添加结果
                    result_item = r_data['result']['item']
                    result_quantity = r_data['result']['quantity']
                    self.player.add_item(result_item, result_quantity)
                    
                    self.add_message(f"⚒️ 合成成功！获得 {result_item} x{result_quantity}", 'success')
                    
                    # 合成特殊物品时的额外效果
                    if result_item == "火焰精华":
                        self.add_message("🔥 火焰精华蕴含着强大的火焰能量，可用于附魔武器！", 'info')
                    elif result_item == "冰霜精华":
                        self.add_message("❄️ 冰霜精华蕴含着极寒的力量，可用于附魔武器！", 'info')
                    elif result_item == "雷电精华":
                        self.add_message("⚡ 雷电精华蕴含着雷霆之力，可用于附魔武器！", 'info')
                    
                    # 更新成就计数
                    if not hasattr(self.player, 'crafting_count'):
                        self.player.crafting_count = 0
                    self.player.crafting_count += 1
                    
                    if self.player.crafting_count >= 10:
                        self.unlock_achievement("初级药剂师")
                    if self.player.crafting_count >= 50:
                        self.unlock_achievement("中级药剂师")
                    if self.player.crafting_count >= 200:
                        self.unlock_achievement("高级药剂师")
                    if self.player.crafting_count >= 500:
                        self.unlock_achievement("大师级药剂师")
                    if self.player.crafting_count >= 1000:
                        self.unlock_achievement("宗师级药剂师")
                    
                    self.gui.update_game_info()
                    dialog.destroy()
                    self.show_crafting_system()
                
                craft_btn = tk.Button(
                    recipe_frame,
                    text="合成",
                    command=craft,
                    font=self.gui.small_font,
                    bg=self.gui.colors['button_bg'],
                    fg=self.gui.colors['button_fg'],
                    state='normal' if has_materials else 'disabled'
                )
                craft_btn.pack(pady=5)
            
            # 递归绑定所有子控件滚轮
            bind_wheel_recursive(scrollable_frame, canvas)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def show_smithing_system(self):
        """显示锻造系统"""
        if not self.player:
            messagebox.showinfo("提示", "请先开始游戏！")
            return
        
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("锻造系统")
        dialog.geometry("700x600")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 标题
        title_label = tk.Label(
            dialog,
            text="锻造系统",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg=self.gui.colors['bg']
        )
        title_label.pack(pady=10)
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 按类型分组
        recipe_types = {
            "武器锻造": [],
            "防具锻造": []
        }
        
        for recipe_name, recipe_data in self.smithing_recipes.items():
            if recipe_data['type'] == 'weapon':
                recipe_types["武器锻造"].append((recipe_name, recipe_data))
            elif recipe_data['type'] == 'armor':
                recipe_types["防具锻造"].append((recipe_name, recipe_data))
        
        # 通用滚轮函数
        def on_mouse_wheel(event, canvas):
            if event.delta:
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        def bind_wheel_recursive(widget, canvas):
            widget.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            for child in widget.winfo_children():
                bind_wheel_recursive(child, canvas)
        
        for type_name, recipes in recipe_types.items():
            if not recipes:
                continue
                
            type_frame = tk.Frame(notebook, bg='#1e1e1e')
            notebook.add(type_frame, text=type_name)
            
            canvas = tk.Canvas(type_frame, bg='#1e1e1e', highlightthickness=0)
            scrollbar = tk.Scrollbar(type_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#1e1e1e')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # 绑定滚轮
            canvas.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            canvas.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            
            for recipe_name, recipe_data in recipes:
                # 检查材料是否足够
                has_materials = True
                for material, amount in recipe_data['ingredients'].items():
                    if material not in self.player.inventory or self.player.inventory[material] < amount:
                        has_materials = False
                        break
                
                recipe_frame = tk.LabelFrame(
                    scrollable_frame,
                    text=recipe_name,
                    font=self.gui.normal_font,
                    fg=self.gui.colors['gold'],
                    bg='#1e1e1e',
                    relief='ridge'
                )
                recipe_frame.pack(fill='x', padx=5, pady=5)
                
                desc_label = tk.Label(
                    recipe_frame,
                    text=recipe_data['description'],
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=500
                )
                desc_label.pack(fill='x', padx=5, pady=2)
                
                # 材料列表
                material_parts = []
                for material, amount in recipe_data['ingredients'].items():
                    if material in self.player.inventory:
                        current = self.player.inventory[material]
                        color = self.gui.colors['success'] if current >= amount else self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/{current}")
                    else:
                        color = self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/0")
                
                materials_label = tk.Label(
                    recipe_frame,
                    text="📦 所需材料: " + ", ".join(material_parts),
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                materials_label.pack(fill='x', padx=5, pady=2)
                
                # 结果信息
                result_info = f"✨ 结果: {recipe_data['result']['item']} x{recipe_data['result']['quantity']}"
                
                result_label = tk.Label(
                    recipe_frame,
                    text=result_info,
                    font=self.gui.small_font,
                    fg=self.gui.colors['success'],
                    bg='#1e1e1e'
                )
                result_label.pack(fill='x', padx=5, pady=2)
                
                # 锻造按钮
                def craft(r_name=recipe_name, r_data=recipe_data, r_has_materials=has_materials):
                    # 再次检查材料，确保按钮亮起时一定有材料
                    if not r_has_materials:
                        # 如果按钮是亮的但材料不足，说明有问题，重新检查
                        has_materials_now = True
                        for material, amount in r_data['ingredients'].items():
                            if material not in self.player.inventory or self.player.inventory[material] < amount:
                                has_materials_now = False
                                break
                        
                        if not has_materials_now:
                            messagebox.showerror("错误", f"材料不足！\n请检查所需材料是否足够。")
                            # 刷新界面
                            dialog.destroy()
                            self.show_smithing_system()
                            return
                    
                    # 扣除材料
                    for material, amount in r_data['ingredients'].items():
                        self.player.remove_item(material, amount)
                    
                    # 添加结果
                    result_item = r_data['result']['item']
                    result_quantity = r_data['result']['quantity']
                    self.player.add_item(result_item, result_quantity)
                    
                    self.add_message(f"🔨 锻造成功！获得 {result_item} x{result_quantity}", 'success')
                    
                    # 更新成就计数
                    if not hasattr(self.player, 'smithing_count'):
                        self.player.smithing_count = 0
                    self.player.smithing_count += 1
                    
                    if self.player.smithing_count >= 10:
                        self.unlock_achievement("初级铁匠")
                    if self.player.smithing_count >= 50:
                        self.unlock_achievement("中级铁匠")
                    if self.player.smithing_count >= 200:
                        self.unlock_achievement("高级铁匠")
                    if self.player.smithing_count >= 500:
                        self.unlock_achievement("大师级铁匠")
                    if self.player.smithing_count >= 1000:
                        self.unlock_achievement("宗师级铁匠")
                    
                    # 检查传说级装备
                    if "传说" in result_item or "神话" in result_item or "创世" in result_item:
                        if r_data['type'] == 'weapon':
                            self.unlock_achievement("剑术大师")
                        else:
                            self.unlock_achievement("防具大师")
                    
                    self.gui.update_game_info()
                    dialog.destroy()
                    self.show_smithing_system()
                
                craft_btn = tk.Button(
                    recipe_frame,
                    text="锻造",
                    command=craft,
                    font=self.gui.small_font,
                    bg=self.gui.colors['button_bg'],
                    fg=self.gui.colors['button_fg'],
                    state='normal' if has_materials else 'disabled'
                )
                craft_btn.pack(pady=5)
            
            # 递归绑定所有子控件滚轮
            bind_wheel_recursive(scrollable_frame, canvas)
            
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
    def show_gem_system(self):
        """显示宝石系统"""
        if not self.player:
            messagebox.showinfo("提示", "请先开始游戏！")
            return
        
        dialog = tk.Toplevel(self.gui.root)
        dialog.title("宝石系统")
        dialog.geometry("800x600")
        dialog.configure(bg=self.gui.colors['bg'])
        dialog.transient(self.gui.root)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - dialog.winfo_width()) // 2
        y = (dialog.winfo_screenheight() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 创建笔记本
        notebook = ttk.Notebook(dialog)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # 宝石合成页面
        synthesis_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(synthesis_frame, text="宝石合成")
        
        # 标题
        title_label = tk.Label(
            synthesis_frame,
            text="宝石合成",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg='#1e1e1e'
        )
        title_label.pack(pady=10)
        
        # 按品质分组
        gem_types = {
            "普通宝石": [],
            "魔法宝石": [],
            "稀有宝石": [],
            "史诗宝石": [],
            "传说宝石": [],
            "神话宝石": [],
            "创世宝石": [],
            "特殊宝石": []
        }
        
        for recipe_name, recipe_data in self.gem_recipes.items():
            if "普通" in recipe_name:
                gem_types["普通宝石"].append((recipe_name, recipe_data))
            elif "魔法" in recipe_name:
                gem_types["魔法宝石"].append((recipe_name, recipe_data))
            elif "稀有" in recipe_name:
                gem_types["稀有宝石"].append((recipe_name, recipe_data))
            elif "史诗" in recipe_name:
                gem_types["史诗宝石"].append((recipe_name, recipe_data))
            elif "传说" in recipe_name:
                gem_types["传说宝石"].append((recipe_name, recipe_data))
            elif "神话" in recipe_name:
                gem_types["神话宝石"].append((recipe_name, recipe_data))
            elif "创世" in recipe_name:
                gem_types["创世宝石"].append((recipe_name, recipe_data))
            else:
                gem_types["特殊宝石"].append((recipe_name, recipe_data))
        
        # 通用滚轮函数
        def on_mouse_wheel(event, canvas):
            if event.delta:
                canvas.yview_scroll(-int(event.delta / 120), "units")
            else:
                if event.num == 4:
                    canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    canvas.yview_scroll(1, "units")
        
        def bind_wheel_recursive(widget, canvas):
            widget.bind("<MouseWheel>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-4>", lambda e, c=canvas: on_mouse_wheel(e, c))
            widget.bind("<Button-5>", lambda e, c=canvas: on_mouse_wheel(e, c))
            for child in widget.winfo_children():
                bind_wheel_recursive(child, canvas)
        
        synthesis_canvas = tk.Canvas(synthesis_frame, bg='#1e1e1e', highlightthickness=0)
        synthesis_scrollbar = tk.Scrollbar(synthesis_frame, orient='vertical', command=synthesis_canvas.yview)
        synthesis_scrollable = tk.Frame(synthesis_canvas, bg='#1e1e1e')
        
        synthesis_scrollable.bind(
            "<Configure>",
            lambda e: synthesis_canvas.configure(scrollregion=synthesis_canvas.bbox("all"))
        )
        
        synthesis_canvas.create_window((0, 0), window=synthesis_scrollable, anchor="nw")
        synthesis_canvas.configure(yscrollcommand=synthesis_scrollbar.set)
        
        # 绑定滚轮
        synthesis_canvas.bind("<MouseWheel>", lambda e, c=synthesis_canvas: on_mouse_wheel(e, c))
        synthesis_canvas.bind("<Button-4>", lambda e, c=synthesis_canvas: on_mouse_wheel(e, c))
        synthesis_canvas.bind("<Button-5>", lambda e, c=synthesis_canvas: on_mouse_wheel(e, c))
        
        for quality_name, recipes in gem_types.items():
            if not recipes:
                continue
                
            quality_frame = tk.LabelFrame(
                synthesis_scrollable,
                text=quality_name,
                font=self.gui.normal_font,
                fg=self.gui.colors['gold'],
                bg='#1e1e1e',
                relief='ridge'
            )
            quality_frame.pack(fill='x', padx=5, pady=5)
            
            for recipe_name, recipe_data in recipes:
                # 检查材料是否足够
                has_materials = True
                for material, amount in recipe_data['ingredients'].items():
                    if material not in self.player.inventory or self.player.inventory[material] < amount:
                        has_materials = False
                        break
                
                recipe_frame = tk.Frame(quality_frame, bg='#1e1e1e')
                recipe_frame.pack(fill='x', padx=5, pady=2)
                
                desc_label = tk.Label(
                    recipe_frame,
                    text=recipe_data['description'],
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w',
                    wraplength=600
                )
                desc_label.pack(fill='x', padx=5, pady=1)
                
                # 材料列表
                material_parts = []
                for material, amount in recipe_data['ingredients'].items():
                    if material in self.player.inventory:
                        current = self.player.inventory[material]
                        color = self.gui.colors['success'] if current >= amount else self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/{current}")
                    else:
                        color = self.gui.colors['warning']
                        material_parts.append(f"{material} {amount}/0")
                
                materials_label = tk.Label(
                    recipe_frame,
                    text="📦 所需材料: " + ", ".join(material_parts),
                    font=self.gui.small_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    anchor='w'
                )
                materials_label.pack(fill='x', padx=5, pady=1)
                
                # 结果信息
                result_info = f"✨ 结果: {recipe_data['result']['item']} x{recipe_data['result']['quantity']}"
                
                result_label = tk.Label(
                    recipe_frame,
                    text=result_info,
                    font=self.gui.small_font,
                    fg=self.gui.colors['success'],
                    bg='#1e1e1e'
                )
                result_label.pack(fill='x', padx=5, pady=1)
                
                # 合成按钮
                def craft(r_name=recipe_name, r_data=recipe_data, r_has_materials=has_materials):
                    # 再次检查材料，确保按钮亮起时一定有材料
                    if not r_has_materials:
                        # 如果按钮是亮的但材料不足，说明有问题，重新检查
                        has_materials_now = True
                        for material, amount in r_data['ingredients'].items():
                            if material not in self.player.inventory or self.player.inventory[material] < amount:
                                has_materials_now = False
                                break
                        
                        if not has_materials_now:
                            messagebox.showerror("错误", f"材料不足！\n请检查所需材料是否足够。")
                            # 刷新界面
                            dialog.destroy()
                            self.show_gem_system()
                            return
                    
                    # 扣除材料
                    for material, amount in r_data['ingredients'].items():
                        self.player.remove_item(material, amount)
                    
                    # 添加结果
                    result_item = r_data['result']['item']
                    result_quantity = r_data['result']['quantity']
                    self.player.add_item(result_item, result_quantity)
                    
                    self.add_message(f"💎 宝石合成成功！获得 {result_item} x{result_quantity}", 'success')
                    
                    # 更新成就计数
                    if not hasattr(self.player, 'gem_count'):
                        self.player.gem_count = 0
                    self.player.gem_count += 1
                    
                    if self.player.gem_count >= 10:
                        self.unlock_achievement("初级宝石匠")
                    if self.player.gem_count >= 50:
                        self.unlock_achievement("中级宝石匠")
                    if self.player.gem_count >= 200:
                        self.unlock_achievement("高级宝石匠")
                    if self.player.gem_count >= 500:
                        self.unlock_achievement("大师级宝石匠")
                    if self.player.gem_count >= 1000:
                        self.unlock_achievement("宗师级宝石匠")
                    
                    # 检查传说级宝石
                    if "传说" in result_item or "神话" in result_item or "创世" in result_item:
                        self.unlock_achievement("宝石大师")
                    
                    self.gui.update_game_info()
                    dialog.destroy()
                    self.show_gem_system()
                
                craft_btn = tk.Button(
                    recipe_frame,
                    text="合成",
                    command=craft,
                    font=self.gui.small_font,
                    bg=self.gui.colors['button_bg'],
                    fg=self.gui.colors['button_fg'],
                    state='normal' if has_materials else 'disabled'
                )
                craft_btn.pack(pady=2)
        
        bind_wheel_recursive(synthesis_scrollable, synthesis_canvas)
        synthesis_canvas.pack(side='left', fill='both', expand=True)
        synthesis_scrollbar.pack(side='right', fill='y')
        
        # 宝石镶嵌页面
        socket_frame = tk.Frame(notebook, bg='#1e1e1e')
        notebook.add(socket_frame, text="宝石镶嵌")
        
        socket_canvas = tk.Canvas(socket_frame, bg='#1e1e1e', highlightthickness=0)
        socket_scrollbar = tk.Scrollbar(socket_frame, orient='vertical', command=socket_canvas.yview)
        socket_scrollable = tk.Frame(socket_canvas, bg='#1e1e1e')
        
        socket_scrollable.bind(
            "<Configure>",
            lambda e: socket_canvas.configure(scrollregion=socket_canvas.bbox("all"))
        )
        
        socket_canvas.create_window((0, 0), window=socket_scrollable, anchor="nw")
        socket_canvas.configure(yscrollcommand=socket_scrollbar.set)
        
        # 绑定滚轮
        socket_canvas.bind("<MouseWheel>", lambda e, c=socket_canvas: on_mouse_wheel(e, c))
        socket_canvas.bind("<Button-4>", lambda e, c=socket_canvas: on_mouse_wheel(e, c))
        socket_canvas.bind("<Button-5>", lambda e, c=socket_canvas: on_mouse_wheel(e, c))
        
        # 标题
        socket_title = tk.Label(
            socket_scrollable,
            text="宝石镶嵌 - 为你的装备镶嵌宝石",
            font=self.gui.header_font,
            fg=self.gui.colors['gold'],
            bg='#1e1e1e'
        )
        socket_title.pack(pady=10)
        
        # 当前装备显示
        equipment_frame = tk.LabelFrame(
            socket_scrollable,
            text="当前装备",
            font=self.gui.normal_font,
            fg=self.gui.colors['gold'],
            bg='#1e1e1e',
            relief='ridge'
        )
        equipment_frame.pack(fill='x', padx=10, pady=5)
        
        for slot_name, slot_item in self.player.equipped.items():
            slot_frame = tk.Frame(equipment_frame, bg='#1e1e1e')
            slot_frame.pack(fill='x', padx=5, pady=2)
            
            slot_labels = {
                "weapon": "⚔️ 武器",
                "armor": "🛡️ 盔甲",
                "accessory": "💍 饰品"
            }
            
            slot_label = tk.Label(
                slot_frame,
                text=f"{slot_labels.get(slot_name, slot_name)}: {slot_item or '无'}",
                font=self.gui.normal_font,
                fg=self.gui.colors['fg'],
                bg='#1e1e1e',
                width=15
            )
            slot_label.pack(side='left', padx=5)
            
            # 当前镶嵌的宝石
            current_gem = self.player.gem_slots.get(slot_name, None)
            gem_text = f"镶嵌宝石: {current_gem or '无'}"
            gem_label = tk.Label(
                slot_frame,
                text=gem_text,
                font=self.gui.small_font,
                fg=self.gui.colors['info'],
                bg='#1e1e1e'
            )
            gem_label.pack(side='left', padx=5)
        
        # 可用宝石列表
        gems_frame = tk.LabelFrame(
            socket_scrollable,
            text="可用宝石",
            font=self.gui.normal_font,
            fg=self.gui.colors['gold'],
            bg='#1e1e1e',
            relief='ridge'
        )
        gems_frame.pack(fill='x', padx=10, pady=5)
        
        # 收集所有宝石类型的物品
        gem_items = []
        for item_name, quantity in self.player.inventory.items():
            if item_name in self.items and self.items[item_name]['type'] == 'gem':
                gem_items.append((item_name, quantity, self.items[item_name]))
        
        if not gem_items:
            empty_label = tk.Label(
                gems_frame,
                text="你没有任何宝石",
                font=self.gui.normal_font,
                fg=self.gui.colors['fg'],
                bg='#1e1e1e'
            )
            empty_label.pack(pady=10)
        else:
            for item_name, quantity, item_info in gem_items:
                gem_frame = tk.Frame(gems_frame, bg='#1e1e1e')
                gem_frame.pack(fill='x', padx=5, pady=2)
                
                gem_label = tk.Label(
                    gem_frame,
                    text=f"💎 {item_name} x{quantity}",
                    font=self.gui.normal_font,
                    fg=self.gui.colors['fg'],
                    bg='#1e1e1e',
                    width=20
                )
                gem_label.pack(side='left', padx=5)
                
                effect_desc = f"效果: "
                if item_info['effect'] == 'attack':
                    effect_desc += f"攻击力 +{item_info['value']}"
                elif item_info['effect'] == 'defense':
                    effect_desc += f"防御力 +{item_info['value']}"
                elif item_info['effect'] == 'hp':
                    effect_desc += f"生命值 +{item_info['value']}"
                elif item_info['effect'] == 'gold':
                    effect_desc += f"金币掉落 +{item_info['value']}%"
                elif item_info['effect'] == 'exp':
                    effect_desc += f"经验获取 +{item_info['value']}%"
                elif item_info['effect'] == 'luck':
                    effect_desc += f"幸运 +{item_info['value']}"
                elif item_info['effect'] == 'speed':
                    effect_desc += f"速度 +{item_info['value']}"
                elif item_info['effect'] == 'all':
                    effect_desc += f"全属性 +{item_info['value']}%"
                elif item_info['effect'] == 'hp_regen':
                    effect_desc += f"每回合回血 {item_info['value']}"
                elif item_info['effect'] == 'lifesteal':
                    effect_desc += f"吸血 {item_info['value']}%"
                elif item_info['effect'] == 'crit':
                    effect_desc += f"暴击率 +{item_info['value']}%"
                elif item_info['effect'] == 'dodge':
                    effect_desc += f"闪避率 +{item_info['value']}%"
                else:
                    effect_desc += item_info['description']
                
                effect_label = tk.Label(
                    gem_frame,
                    text=effect_desc,
                    font=self.gui.small_font,
                    fg=self.gui.colors['info'],
                    bg='#1e1e1e'
                )
                effect_label.pack(side='left', padx=5)
        
        # 镶嵌区域
        socket_action_frame = tk.LabelFrame(
            socket_scrollable,
            text="镶嵌操作",
            font=self.gui.normal_font,
            fg=self.gui.colors['gold'],
            bg='#1e1e1e',
            relief='ridge'
        )
        socket_action_frame.pack(fill='x', padx=10, pady=5)
        
        # 选择装备槽位
        slot_var = tk.StringVar(value="weapon")
        slot_frame = tk.Frame(socket_action_frame, bg='#1e1e1e')
        slot_frame.pack(pady=5)
        
        slot_label = tk.Label(
            slot_frame,
            text="选择装备槽位:",
            font=self.gui.normal_font,
            fg=self.gui.colors['fg'],
            bg='#1e1e1e'
        )
        slot_label.pack(side='left', padx=5)
        
        slot_combo = ttk.Combobox(
            slot_frame,
            textvariable=slot_var,
            values=["weapon", "armor", "accessory"],
            state="readonly",
            width=15
        )
        slot_combo.pack(side='left', padx=5)
        
        # 选择宝石
        gem_var = tk.StringVar()
        gem_frame = tk.Frame(socket_action_frame, bg='#1e1e1e')
        gem_frame.pack(pady=5)
        
        gem_label = tk.Label(
            gem_frame,
            text="选择宝石:",
            font=self.gui.normal_font,
            fg=self.gui.colors['fg'],
            bg='#1e1e1e'
        )
        gem_label.pack(side='left', padx=5)
        
        gem_values = [item[0] for item in gem_items] if gem_items else ["无可用宝石"]
        gem_combo = ttk.Combobox(
            gem_frame,
            textvariable=gem_var,
            values=gem_values,
            state="readonly" if gem_values else "disabled",
            width=20
        )
        gem_combo.pack(side='left', padx=5)
        
        # 镶嵌按钮
        def socket_gem():
            slot = slot_var.get()
            gem_name = gem_var.get()
            
            if not gem_name or gem_name == "无可用宝石":
                messagebox.showerror("错误", "请选择要镶嵌的宝石！")
                return
            
            if slot not in self.player.equipped or not self.player.equipped[slot]:
                messagebox.showerror("错误", "该装备槽位没有装备！")
                return
            
            if gem_name not in self.player.inventory:
                messagebox.showerror("错误", "你没有这个宝石！")
                return
            
            # 检查宝石类型是否适合该装备槽位
            gem_info = self.items[gem_name]
            gem_effect = gem_info['effect']
            
            rules = self.gem_socket_rules[slot]
            if gem_effect not in rules['allowed_types']:
                messagebox.showerror("错误", f"该宝石不能镶嵌在{slot}上！\n允许的类型: {', '.join(rules['allowed_types'])}")
                return
            
            # 如果已经有宝石，先移除
            if self.player.gem_slots[slot]:
                old_gem = self.player.gem_slots[slot]
                self.player.add_item(old_gem, 1)
                self.add_message(f"移除了 {old_gem}", 'info')
            
            # 镶嵌新宝石
            self.player.remove_item(gem_name, 1)
            self.player.gem_slots[slot] = gem_name
            
            # 应用宝石效果
            self.player.apply_gem_effects()
            
            self.add_message(f"✨ 成功将 {gem_name} 镶嵌到 {slot}！", 'success')
            
            # 检查成就
            if self.player.gem_slots['weapon'] and self.player.gem_slots['armor'] and self.player.gem_slots['accessory']:
                self.unlock_achievement("完美镶嵌")
            
            # 检查全套传说装备
            has_all_legendary = True
            for slot_name, gem in self.player.gem_slots.items():
                if not gem or "传说" not in gem and "神话" not in gem and "创世" not in gem:
                    has_all_legendary = False
                    break
            
            if has_all_legendary:
                self.unlock_achievement("最强装备")
            
            self.gui.update_game_info()
            dialog.destroy()
            self.show_gem_system()
        
        socket_btn = tk.Button(
            socket_action_frame,
            text="镶嵌宝石",
            command=socket_gem,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=15
        )
        socket_btn.pack(pady=10)
        
        # 移除宝石按钮
        def remove_gem():
            slot = slot_var.get()
            
            if not self.player.gem_slots[slot]:
                messagebox.showerror("错误", "该装备槽位没有镶嵌宝石！")
                return
            
            gem_name = self.player.gem_slots[slot]
            self.player.add_item(gem_name, 1)
            self.player.gem_slots[slot] = None
            
            # 重新应用宝石效果
            self.player.apply_gem_effects()
            
            self.add_message(f"移除了 {gem_name}", 'info')
            self.gui.update_game_info()
            dialog.destroy()
            self.show_gem_system()
        
        remove_btn = tk.Button(
            socket_action_frame,
            text="移除宝石",
            command=remove_gem,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=15
        )
        remove_btn.pack(pady=5)
        
        bind_wheel_recursive(socket_scrollable, socket_canvas)
        socket_canvas.pack(side='left', fill='both', expand=True)
        socket_scrollbar.pack(side='right', fill='y')
        
        # 关闭按钮
        close_btn = tk.Button(
            dialog,
            text="关闭",
            command=dialog.destroy,
            font=self.gui.normal_font,
            bg=self.gui.colors['button_bg'],
            fg=self.gui.colors['button_fg'],
            width=10
        )
        close_btn.pack(pady=10)
    
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
                            encrypted_data = f.read().strip()
                            
                            # 尝试解密数据
                            decrypted_data = self._decrypt_save_data(encrypted_data)
                            if decrypted_data:
                                timestamp = decrypted_data.get("timestamp", "未知")
                                player_data = decrypted_data.get("player", {})
                                player_name = player_data.get("name", "未知角色")
                                
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
                    except Exception as e:
                        # 静默处理解密失败的文件，不显示错误
                        continue
            
            saves.sort(key=lambda x: x['date'], reverse=True)
            
        except Exception as e:
            print(f"读取存档列表失败: {e}")
        
        return saves
    
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
    
    def save_game(self, slot=None, save_name=None):
        """保存游戏（加密版本）
        
        Args:
            slot: 存档位编号，如果提供则覆盖对应存档位
            save_name: 自定义存档文件名，如果提供则使用该文件名（用于覆盖特定存档）
        """
        if not self.player:
            return False
        
        if save_name:
            # 使用自定义文件名（用于覆盖特定存档）
            save_name = save_name
        elif slot is not None:
            # 使用存档位文件名
            save_name = f"save_slot_{slot}"
        elif self.current_save:
            # 使用当前存档文件名（覆盖保存）
            save_name = self.current_save
        else:
            # 创建新存档
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"save_{timestamp}"
            # 设置为当前存档
            self.current_save = save_name
        
        save_path = os.path.join(self.saves_dir, save_name)
        
        try:
            # 构建存档数据
            save_data = {
                "version": "2.0",
                "timestamp": datetime.datetime.now().isoformat(),
                "player": {
                    "name": self.player.name,
                    "level": self.player.level,
                    "exp": self.player.exp,
                    "hp": self.player.hp,
                    "max_hp": self.player.max_hp,
                    "attack": self.player.attack,
                    "defense": self.player.defense,
                    "gold": self.player.gold,
                    "stamina": self.player.stamina,
                    "max_stamina": self.player.max_stamina,
                    "magic_affinity": self.player.magic_affinity,
                    "magic_power": self.player.magic_power,
                    "magic_level": self.player.magic_level,
                    "magic_exp": self.player.magic_exp,
                    "gem_bonus_attack": self.player.gem_bonus_attack,
                    "gem_bonus_defense": self.player.gem_bonus_defense,
                    "gem_bonus_hp": self.player.gem_bonus_hp,
                    "gem_bonus_gold": self.player.gem_bonus_gold,
                    "gem_bonus_exp": self.player.gem_bonus_exp,
                    "gem_bonus_luck": self.player.gem_bonus_luck,
                    "gem_bonus_speed": self.player.gem_bonus_speed,
                    "equipment_bonus_attack": self.player.equipment_bonus_attack,
                    "equipment_bonus_defense": self.player.equipment_bonus_defense,
                    "equipment_bonus_magic": self.player.equipment_bonus_magic,
                    "equipment_bonus_hp": self.player.equipment_bonus_hp,
                    "equipment_bonus_speed": self.player.equipment_bonus_speed,
                    "equipment_bonus_crit": self.player.equipment_bonus_crit,
                    "equipment_bonus_dodge": self.player.equipment_bonus_dodge,
                    "equipment_bonus_block": self.player.equipment_bonus_block,
                    "equipment_bonus_thorns": self.player.equipment_bonus_thorns,
                    "equipment_bonus_lifesteal": self.player.equipment_bonus_lifesteal,
                    "equipment_bonus_gold": self.player.equipment_bonus_gold,
                    "equipment_bonus_exp": self.player.equipment_bonus_exp,
                    "inventory": self.player.inventory,
                    "equipped": self.player.equipped,
                    "gem_slots": self.player.gem_slots
                },
                "game_state": {
                    "current_scene": self.current_scene,
                    "game_time": self.game_time.isoformat(),
                    "day_count": self.day_count,
                    "achievements": list(self.achievements),
                    "unlocked_scenes": list(getattr(self, 'unlocked_scenes', {'forest', 'town'})),
                    "pets": self.pets
                }
            }
            
            # 加密数据
            encrypted_data = self._encrypt_save_data(save_data)
            
            # 写入文件
            with open(save_path, 'w') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"保存游戏失败: {e}")
            return False
    
    def load_save_game(self, save_file):
        """从文件加载游戏（只支持加密版本）"""
        try:
            save_path = os.path.join(self.saves_dir, save_file)
            
            with open(save_path, 'r') as f:
                encrypted_data = f.read().strip()
            
            # 解密数据
            save_data = self._decrypt_save_data(encrypted_data)
            if save_data is None:
                return False
            
            # 计算总生命值
            total_hp = save_data["player"]["max_hp"] + save_data["player"].get("gem_bonus_hp", 0) + save_data["player"].get("equipment_bonus_hp", 0)
            
            self.player = Player(
                save_data["player"]["name"],
                total_hp,
                save_data["player"]["attack"] + save_data["player"].get("gem_bonus_attack", 0) + save_data["player"].get("equipment_bonus_attack", 0),
                save_data["player"]["defense"] + save_data["player"].get("gem_bonus_defense", 0) + save_data["player"].get("equipment_bonus_defense", 0)
            )
            self.player.level = save_data["player"]["level"]
            self.player.exp = save_data["player"]["exp"]
            self.player.hp = save_data["player"]["hp"]
            self.player.max_hp = total_hp
            self.player.attack = save_data["player"]["attack"]
            self.player.defense = save_data["player"]["defense"]
            self.player.gold = save_data["player"]["gold"]
            self.player.stamina = save_data["player"].get("stamina", self.player.max_stamina)
            self.player.max_stamina = save_data["player"].get("max_stamina", 50)
            self.player.inventory = save_data["player"]["inventory"]
            self.player.equipped = save_data["player"]["equipped"]
            self.player.gem_slots = save_data["player"]["gem_slots"]
            self.player.magic_affinity = save_data["player"]["magic_affinity"]
            self.player.magic_power = save_data["player"]["magic_power"]
            self.player.magic_level = save_data["player"].get("magic_level", 1)
            self.player.magic_exp = save_data["player"].get("magic_exp", 0)
            
            # 加载宝石加成
            if "gem_bonus_attack" in save_data["player"]:
                self.player.gem_bonus_attack = save_data["player"]["gem_bonus_attack"]
                self.player.gem_bonus_defense = save_data["player"]["gem_bonus_defense"]
                self.player.gem_bonus_hp = save_data["player"]["gem_bonus_hp"]
                self.player.gem_bonus_gold = save_data["player"]["gem_bonus_gold"]
                self.player.gem_bonus_exp = save_data["player"]["gem_bonus_exp"]
                self.player.gem_bonus_luck = save_data["player"]["gem_bonus_luck"]
                self.player.gem_bonus_speed = save_data["player"]["gem_bonus_speed"]
            
            # 加载装备加成
            if "equipment_bonus_attack" in save_data["player"]:
                self.player.equipment_bonus_attack = save_data["player"]["equipment_bonus_attack"]
                self.player.equipment_bonus_defense = save_data["player"]["equipment_bonus_defense"]
                self.player.equipment_bonus_magic = save_data["player"]["equipment_bonus_magic"]
                self.player.equipment_bonus_hp = save_data["player"]["equipment_bonus_hp"]
                self.player.equipment_bonus_speed = save_data["player"]["equipment_bonus_speed"]
                self.player.equipment_bonus_crit = save_data["player"]["equipment_bonus_crit"]
                self.player.equipment_bonus_dodge = save_data["player"]["equipment_bonus_dodge"]
                self.player.equipment_bonus_block = save_data["player"]["equipment_bonus_block"]
                self.player.equipment_bonus_thorns = save_data["player"]["equipment_bonus_thorns"]
                self.player.equipment_bonus_lifesteal = save_data["player"]["equipment_bonus_lifesteal"]
                self.player.equipment_bonus_gold = save_data["player"]["equipment_bonus_gold"]
                self.player.equipment_bonus_exp = save_data["player"]["equipment_bonus_exp"]
            
            self.current_scene = save_data["game_state"]["current_scene"]
            self.game_time = datetime.datetime.fromisoformat(save_data["game_state"]["game_time"])
            self.day_count = save_data["game_state"]["day_count"]
            self.achievements = set(save_data["game_state"]["achievements"])
            self.unlocked_scenes = set(save_data["game_state"].get("unlocked_scenes", {'forest', 'town'}))
            self.pets = save_data["game_state"].get("pets", [])
            
            # 设置当前存档
            self.current_save = save_file
            
            return True
            
        except Exception as e:
            print(f"加载游戏失败: {e}")
            return False
    
    def load_decrypted_data(self, save_data):
        """加载解密后的数据"""
        try:
            # 计算总生命值
            total_hp = save_data["player"]["max_hp"] + save_data["player"].get("gem_bonus_hp", 0) + save_data["player"].get("equipment_bonus_hp", 0)
            
            self.player = Player(
                save_data["player"]["name"],
                total_hp,
                save_data["player"]["attack"] + save_data["player"].get("gem_bonus_attack", 0) + save_data["player"].get("equipment_bonus_attack", 0),
                save_data["player"]["defense"] + save_data["player"].get("gem_bonus_defense", 0) + save_data["player"].get("equipment_bonus_defense", 0)
            )
            self.player.level = save_data["player"]["level"]
            self.player.exp = save_data["player"]["exp"]
            self.player.hp = save_data["player"]["hp"]
            self.player.max_hp = total_hp
            self.player.attack = save_data["player"]["attack"]
            self.player.defense = save_data["player"]["defense"]
            self.player.gold = save_data["player"]["gold"]
            self.player.stamina = save_data["player"].get("stamina", self.player.max_stamina)
            self.player.max_stamina = save_data["player"].get("max_stamina", 50)
            self.player.inventory = save_data["player"]["inventory"]
            self.player.equipped = save_data["player"]["equipped"]
            self.player.gem_slots = save_data["player"]["gem_slots"]
            self.player.magic_affinity = save_data["player"]["magic_affinity"]
            self.player.magic_power = save_data["player"]["magic_power"]
            self.player.magic_level = save_data["player"].get("magic_level", 1)
            self.player.magic_exp = save_data["player"].get("magic_exp", 0)
            
            # 加载宝石加成
            if "gem_bonus_attack" in save_data["player"]:
                self.player.gem_bonus_attack = save_data["player"]["gem_bonus_attack"]
                self.player.gem_bonus_defense = save_data["player"]["gem_bonus_defense"]
                self.player.gem_bonus_hp = save_data["player"]["gem_bonus_hp"]
                self.player.gem_bonus_gold = save_data["player"]["gem_bonus_gold"]
                self.player.gem_bonus_exp = save_data["player"]["gem_bonus_exp"]
                self.player.gem_bonus_luck = save_data["player"]["gem_bonus_luck"]
                self.player.gem_bonus_speed = save_data["player"]["gem_bonus_speed"]
            
            # 加载装备加成
            if "equipment_bonus_attack" in save_data["player"]:
                self.player.equipment_bonus_attack = save_data["player"]["equipment_bonus_attack"]
                self.player.equipment_bonus_defense = save_data["player"]["equipment_bonus_defense"]
                self.player.equipment_bonus_magic = save_data["player"]["equipment_bonus_magic"]
                self.player.equipment_bonus_hp = save_data["player"]["equipment_bonus_hp"]
                self.player.equipment_bonus_speed = save_data["player"]["equipment_bonus_speed"]
                self.player.equipment_bonus_crit = save_data["player"]["equipment_bonus_crit"]
                self.player.equipment_bonus_dodge = save_data["player"]["equipment_bonus_dodge"]
                self.player.equipment_bonus_block = save_data["player"]["equipment_bonus_block"]
                self.player.equipment_bonus_thorns = save_data["player"]["equipment_bonus_thorns"]
                self.player.equipment_bonus_lifesteal = save_data["player"]["equipment_bonus_lifesteal"]
                self.player.equipment_bonus_gold = save_data["player"]["equipment_bonus_gold"]
                self.player.equipment_bonus_exp = save_data["player"]["equipment_bonus_exp"]
            
            self.current_scene = save_data["game_state"]["current_scene"]
            self.game_time = datetime.datetime.fromisoformat(save_data["game_state"]["game_time"])
            self.day_count = save_data["game_state"]["day_count"]
            self.achievements = set(save_data["game_state"]["achievements"])
            self.unlocked_scenes = set(save_data["game_state"].get("unlocked_scenes", {'forest', 'town'}))
            self.pets = save_data["game_state"].get("pets", [])
            
            # 注意：load_decrypted_data 方法没有 save_file 参数，所以这里不能设置 self.current_save
            
            return True
        except Exception as e:
            print(f"加载解密数据失败: {e}")
            return False
    
    def get_achievement_description(self, achievement_name):
        """获取成就描述"""
        descriptions = {
            "初次冒险": "开始你的冒险之旅",
            "战斗大师": "击败100个敌人",
            "龙蛋收集者": "找到并收集龙蛋",
            "冰雕大师": "在冰雕比赛中获得冠军",
            "登山家": "成功攀登到冰峰之顶",
            "驱魔师": "成功解开诅咒",
            "宝藏猎人": "找到传说中的宝藏",
            "龙骑士": "通过龙的试炼成为龙骑士",
            "龙骑士大师": "成为真正的龙骑士大师",
            "收集家": "收集50种不同的物品",
            "等级达人": "达到20级"
        }
        return descriptions.get(achievement_name, "完成了一项特殊成就")
    
    def unlock_achievement(self, achievement_name):
        """解锁成就"""
        if achievement_name in self.achievements_list and achievement_name not in self.achievements:
            self.achievements.add(achievement_name)
            self.add_message(f"🏆 成就解锁: {achievement_name}！", 'gold')
            
            # 记录成就到图鉴
            if achievement_name not in self.compendium['achievements']:
                self.compendium['achievements'][achievement_name] = {
                    'name': achievement_name,
                    'unlocked_date': self.day_count,
                    'description': self.get_achievement_description(achievement_name)
                }
                # 更新图鉴完成度
                self.update_compendium_completion()
            
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
        
        # 体力系统
        self.max_stamina = 50
        self.stamina = self.max_stamina
        
        self.inventory = {}
        self.equipped = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        # 宝石系统
        self.gem_slots = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        # 宝石效果加成
        self.gem_bonus_attack = 0
        self.gem_bonus_defense = 0
        self.gem_bonus_hp = 0
        self.gem_bonus_gold = 0
        self.gem_bonus_exp = 0
        self.gem_bonus_luck = 0
        self.gem_bonus_speed = 0
        
        # 装备效果加成
        self.equipment_bonus_attack = 0
        self.equipment_bonus_defense = 0
        self.equipment_bonus_magic = 0
        self.equipment_bonus_hp = 0
        self.equipment_bonus_speed = 0
        self.equipment_bonus_crit = 0
        self.equipment_bonus_dodge = 0
        self.equipment_bonus_block = 0
        self.equipment_bonus_thorns = 0
        self.equipment_bonus_lifesteal = 0
        self.equipment_bonus_gold = 0
        self.equipment_bonus_exp = 0
        
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
        damage += self.level * 6
        
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
        
        hp_increase = random.randint(5, 8)
        attack_increase = random.randint(2, 5)
        defense_increase = random.randint(1, 4)
        stamina_increase = 5  # 每次升级增加5最大体力
        
        self.max_hp += hp_increase
        self.hp = self.max_hp + self.gem_bonus_hp + self.equipment_bonus_hp
        self.attack += attack_increase
        self.defense += defense_increase
        self.max_stamina += stamina_increase  # 增加最大体力
        
        # 升级时体力恢复满
        self.stamina = self.max_stamina
        
        if game:
            game.add_message(f"\n🎉 {self.name} 升级了！现在是 {self.level} 级！", 'success')
            game.add_message(f"生命值 +{hp_increase}, 攻击力 +{attack_increase}, 防御力 +{defense_increase}, 体力上限 +{stamina_increase}", 'info')
            game.add_message(f"体力完全恢复！", 'info')
        
        if self.level >= 20 and game:
            game.unlock_achievement("等级达人")
    
    def add_item(self, item_name, quantity=1, game=None):
        """添加物品到背包"""
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity
            # 记录物品到图鉴
            if game and item_name not in game.compendium['items']:
                # 查找物品信息
                item_info = game.items.get(item_name, {
                    'name': item_name,
                    'type': 'unknown',
                    'description': '战利品',
                    'effect': '无'
                })
                game.compendium['items'][item_name] = {
                    'name': item_name,
                    'type': item_info.get('type', 'unknown'),
                    'description': item_info.get('description', '战利品'),
                    'effect': item_info.get('effect', '无'),
                    'collected_count': quantity
                }
                # 更新图鉴完成度
                game.update_compendium_completion()
            elif game and item_name in game.compendium['items']:
                # 更新收集数量
                game.compendium['items'][item_name]['collected_count'] += quantity
        
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
    
    # 装备系统方法
    def equip_item(self, item_name):
        """装备物品"""
        if item_name not in self.inventory:
            return False
        
        if item_name not in game.items:
            return False
        
        item_info = game.items[item_name]
        item_type = item_info['type']
        
        if item_type not in ['weapon', 'armor', 'accessory', 'gem']:
            return False
        
        # 确定装备槽位
        if item_type == 'weapon':
            slot = 'weapon'
        elif item_type == 'armor':
            slot = 'armor'
        elif item_type in ['accessory', 'gem']:
            slot = 'accessory'
        else:
            return False
        
        # 如果已经有装备，先卸下
        if self.equipped[slot]:
            self.unequip_from_slot(slot)
        
        # 装备新物品
        self.remove_item(item_name, 1)
        self.equipped[slot] = item_name
        
        # 应用装备效果
        self.apply_equipment_effects()
        
        return True
    
    def unequip_item(self, item_name):
        """卸下物品"""
        for slot, equipped_item in self.equipped.items():
            if equipped_item == item_name:
                return self.unequip_from_slot(slot)
        return False
    
    def unequip_from_slot(self, slot):
        """从指定槽位卸下物品"""
        if slot not in self.equipped or not self.equipped[slot]:
            return False
        
        item_name = self.equipped[slot]
        
        # 如果该装备槽位有宝石，先移除宝石
        if self.gem_slots[slot]:
            gem_name = self.gem_slots[slot]
            self.add_item(gem_name, 1)
            self.gem_slots[slot] = None
            self.apply_gem_effects()
        
        # 将装备放回背包
        self.equipped[slot] = None
        self.add_item(item_name, 1)
        
        # 重新应用装备效果
        self.apply_equipment_effects()
        
        return True
    
    def apply_equipment_effects(self):
        """应用所有装备的效果"""
        # 重置装备加成
        self.equipment_bonus_attack = 0
        self.equipment_bonus_defense = 0
        self.equipment_bonus_magic = 0
        self.equipment_bonus_hp = 0
        self.equipment_bonus_speed = 0
        self.equipment_bonus_crit = 0
        self.equipment_bonus_dodge = 0
        self.equipment_bonus_block = 0
        self.equipment_bonus_thorns = 0
        self.equipment_bonus_lifesteal = 0
        self.equipment_bonus_gold = 0
        self.equipment_bonus_exp = 0
        
        for slot, item_name in self.equipped.items():
            if item_name and item_name in game.items:
                item_info = game.items[item_name]
                
                # 武器加成
                if 'bonus_attack' in item_info:
                    self.equipment_bonus_attack += item_info['bonus_attack']
                if 'bonus_magic' in item_info:
                    self.equipment_bonus_magic += item_info['bonus_magic']
                if 'bonus_crit' in item_info:
                    self.equipment_bonus_crit += item_info['bonus_crit']
                if 'lifesteal' in item_info:
                    self.equipment_bonus_lifesteal += item_info['lifesteal']
                
                # 盔甲加成
                if 'bonus_defense' in item_info:
                    self.equipment_bonus_defense += item_info['bonus_defense']
                if 'bonus_hp' in item_info:
                    self.equipment_bonus_hp += item_info['bonus_hp']
                if 'bonus_dodge' in item_info:
                    self.equipment_bonus_dodge += item_info['bonus_dodge']
                if 'bonus_thorns' in item_info:
                    self.equipment_bonus_thorns += item_info['bonus_thorns']
                
                # 通用加成
                if 'bonus_speed' in item_info:
                    self.equipment_bonus_speed += item_info['bonus_speed']
                if 'bonus_gold' in item_info:
                    self.equipment_bonus_gold += item_info['bonus_gold']
                if 'bonus_exp' in item_info:
                    self.equipment_bonus_exp += item_info['bonus_exp']
                if 'block_chance' in item_info:
                    self.equipment_bonus_block += item_info['block_chance']
        
        # 应用生命值加成
        if self.equipment_bonus_hp > 0:
            self.max_hp += self.equipment_bonus_hp
            self.hp += self.equipment_bonus_hp
    
    # 应用宝石效果
    def apply_gem_effects(self):
        """应用所有镶嵌宝石的效果"""
        # 重置宝石加成
        self.gem_bonus_attack = 0
        self.gem_bonus_defense = 0
        self.gem_bonus_hp = 0
        self.gem_bonus_gold = 0
        self.gem_bonus_exp = 0
        self.gem_bonus_luck = 0
        self.gem_bonus_speed = 0
        
        for slot, gem_name in self.gem_slots.items():
            if gem_name and gem_name in game.items:
                gem_info = game.items[gem_name]
                
                if 'bonus_attack' in gem_info:
                    self.gem_bonus_attack += gem_info['bonus_attack']
                if 'bonus_defense' in gem_info:
                    self.gem_bonus_defense += gem_info['bonus_defense']
                if 'bonus_hp' in gem_info:
                    self.gem_bonus_hp += gem_info['bonus_hp']
                if 'bonus_gold' in gem_info:
                    self.gem_bonus_gold += gem_info['bonus_gold']
                if 'bonus_exp' in gem_info:
                    self.gem_bonus_exp += gem_info['bonus_exp']
                if 'bonus_luck' in gem_info:
                    self.gem_bonus_luck += gem_info['bonus_luck']
                if 'bonus_speed' in gem_info:
                    self.gem_bonus_speed += gem_info['bonus_speed']
                if 'bonus_all_percent' in gem_info:
                    percent = gem_info['bonus_all_percent'] / 100
                    self.gem_bonus_attack += int(self.attack * percent)
                    self.gem_bonus_defense += int(self.defense * percent)
                    self.gem_bonus_hp += int(self.max_hp * percent)
        
        # 应用生命值加成
        if self.gem_bonus_hp > 0:
            self.max_hp += self.gem_bonus_hp
            self.hp += self.gem_bonus_hp


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
