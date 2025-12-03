"""
游戏玩法状态 - 核心游戏逻辑 (精简版：移除储物柜)
"""
# ... (imports 保持不变) ...
import pygame, random, math, os
from config.settings import *
from game.entities.item import Item
from game.entities.customer import Customer
from game.managers.inventory_manager import InventoryManager
from game.ui.hud import HUD
from game.ui.popup import FloatingText

class GameplayState:
    # ... (__init__ 等方法保持不变) ...
    def __init__(self, game_manager, difficulty='normal'):
        self.game_manager = game_manager
        self.difficulty = difficulty
        self.settings = DIFFICULTY_SETTINGS[difficulty]
        self.money = 0;
        self.shift_time = 0; self.shift_duration = 180
        if 'money' in game_manager.game_data: self.money = game_manager.game_data['money']

        self.inventory_manager = InventoryManager()
        self.customers = []; self.customer_slots = [None] * len(CUSTOMER_SLOTS)
        self.customer_timer = 0
        self.conveyor_items = []; self.item_spawn_timer = 0
        self.item_spawn_interval = ITEM_SPAWN_INTERVAL
        self.current_batch_id = 0; self.batch_pause_states = {}
        self.conveyor_texture = None; self.scroll_offset = 0; self.scroll_speed = CONVEYOR_SPEED; self.belt_width = 160
        self.hud = HUD(); self.popups = []; self.sfx = {}; self._load_sfx()
        self.dragging_item = None; self.drag_offset = (0, 0); self.hovered_item = None
        self.font = pygame.font.Font(FONT_PATH, 36); self.font_small = pygame.font.Font(FONT_PATH, 24)
        self.background = None; self._load_background(); self._load_conveyor_texture()
        self.label_image = None
        try:
            # 确保文件名和你的素材一致
            path = 'assets/images/icons/label.png'
            if os.path.exists(path):
                self.label_image = pygame.image.load(path)
                print("✅ label 素材加载成功")
        except:
            print("⚠️ 未找到 label 素材，将使用默认方块")
        self._init_game()

    # ... (_load_xx, _spawn_xx 等保持不变) ...
    def _load_background(self):
        try:
            self.background = pygame.image.load(ASSETS.get('bg_main'))
            self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except: self.background = None
    def _load_conveyor_texture(self):
        paths = ['assets/images/belt_tile.png', 'assets/images/conveyor_4.jpg'];
        for p in paths:
            try:
                if os.path.exists(p): self.conveyor_texture = pygame.transform.scale(pygame.image.load(p), (self.belt_width, self.belt_width)); return
            except: pass
        s = pygame.Surface((self.belt_width, self.belt_width)); s.fill((60,64,68)); pygame.draw.rect(s,(30,30,30),(self.belt_width-5,0,5,self.belt_width)); self.conveyor_texture = s
    # TODO
    def _load_sfx(self):
        # ...
        pass
    # TODO
    def _play_sfx(self, name): pass
    def _spawn_popup(self, x, y, text, c=COLOR_WHITE): self.popups.append(FloatingText(x, y, text, c))
    def _init_game(self): self._spawn_item_on_conveyor(); self._spawn_customer(); self._play_music()
    def _play_music(self):
        try: pygame.mixer.music.load('assets/sounds/bgm_gameplay.mp3'); pygame.mixer.music.play(-1)
        except: pass

    def _spawn_item_on_conveyor(self):
        self.batch_pause_states[self.current_batch_id] = {'paused': False, 'timer': 0, 'triggered': False}
        for i in range(ITEMS_PER_BATCH):
            item = Item(random.choice(list(ITEM_DESCRIPTIONS.keys())))
            item.on_conveyor = True; item.item_index = i; item.batch_id = self.current_batch_id
            start = CONVEYOR_PATH[0]
            hoff = i * 80; voff = [35, 0, -35][i]
            item.conveyor_start_offset = hoff; item.conveyor_vertical_offset = voff
            item.set_position(start[0]-hoff-item.width//2, start[1]-item.height//2)
            self.conveyor_items.append(item)
        self.current_batch_id += 1

    def _spawn_customer(self):
        empty = [i for i, c in enumerate(self.customer_slots) if c is None]
        if not empty: return
        idx = random.choice(empty)
        desk_items = self.inventory_manager.get_all_items()
        type = random.choice(desk_items).item_type if desk_items and random.random() < 0.7 else random.choice(list(ITEM_DESCRIPTIONS.keys()))
        c = Customer(type, self.difficulty, CUSTOMER_SLOTS[idx])
        self.customer_slots[idx] = c; self.customers.append(c)

    def _remove_customer(self, c):
        if c in self.customers: self.customers.remove(c)
        if c in self.customer_slots: self.customer_slots[self.customer_slots.index(c)] = None

    def _handle_delivery(self, c, item):
        if c.check_item_match(item):
            self.money += REWARD_CORRECT; self._spawn_popup(c.x, c.y-50, f"+${REWARD_CORRECT}", COLOR_GREEN)
            self._remove_customer(c); return True
        else:
            self.money += PENALTY_WRONG; self._spawn_popup(c.x, c.y-50, "WRONG!", COLOR_RED); return False

    def _handle_rejection(self, c):
        has = any(i.item_type == c.sought_item_type for i in self.conveyor_items + self.inventory_manager.get_all_items())
        if has: self.money += PENALTY_WRONG*2; self._spawn_popup(c.x, c.y-50, "LIAR!", COLOR_RED)
        else: self.money += -10; self._spawn_popup(c.x, c.y-50, "-$10", COLOR_YELLOW)
        self._remove_customer(c)

    def _tell_customer_no_item(self): pass

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for c in self.customers:
                    if c.is_arrived and c.reject_button.handle_click(mouse): self._handle_rejection(c); return

                clicked = None
                for i in reversed(self.conveyor_items):
                    if i.contains_point(mouse): clicked = i; i.on_conveyor = False; self.conveyor_items.remove(i); break
                if not clicked:
                    clicked = self.inventory_manager.get_item_at_position(mouse)
                    if clicked: self.inventory_manager.remove_item(clicked)

                if clicked:
                    self.dragging_item = clicked; self.dragging_item.is_selected = True
                    self.drag_offset = (mouse[0]-clicked.x, mouse[1]-clicked.y)
            elif event.button == 3 and self.dragging_item:
                self.dragging_item.rotate()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging_item:
                self.dragging_item.is_selected = False
                delivered = False
                for c in self.customers:
                    if c.is_arrived and c.get_delivery_rect().collidepoint(mouse):
                        if self._handle_delivery(c, self.dragging_item): delivered = True
                        break

                if not delivered:
                    new_x = mouse[0] - self.drag_offset[0]; new_y = mouse[1] - self.drag_offset[1]
                    self.dragging_item.set_position(new_x, new_y)

                    # [修改] 不再判断 storage，直接全都放桌上
                    self.inventory_manager.add_item_to_desk(self.dragging_item)

                self.dragging_item = None

        elif event.type == pygame.MOUSEMOTION and self.dragging_item:
            self.dragging_item.set_position(mouse[0]-self.drag_offset[0], mouse[1]-self.drag_offset[1])

    def update(self, dt):
        self.shift_time += dt
        should_scroll = False
        if self.conveyor_items:
            for item in self.conveyor_items:
                if not self.batch_pause_states.get(item.batch_id, {'paused': False})['paused']: should_scroll = True; break
        if should_scroll: self.scroll_offset += CONVEYOR_SPEED * dt

        self.inventory_manager.update(dt)
        for p in self.popups[:]:
            if not p.update(dt): self.popups.remove(p)

        mouse = pygame.mouse.get_pos()
        if not self.dragging_item:
            self.hovered_item = None
            for i in reversed(self.conveyor_items):
                if i.contains_point(mouse): self.hovered_item = i; break
            if not self.hovered_item: self.hovered_item = self.inventory_manager.get_item_at_position(mouse)
        else: self.hovered_item = None

        if self.shift_time >= self.shift_duration: self._end_shift(); return

        self.item_spawn_timer += dt
        if self.item_spawn_timer >= self.item_spawn_interval: self.item_spawn_timer = 0; self._spawn_item_on_conveyor()

        # Conveyor Logic
        trigger_y = 420; pause_dur = 3.0
        batch_items = {}
        for i in self.conveyor_items:
            if i.batch_id not in batch_items: batch_items[i.batch_id] = []
            batch_items[i.batch_id].append(i)
        for bid, items in batch_items.items():
            if bid in self.batch_pause_states:
                st = self.batch_pause_states[bid]
                t_idx = CONVEYOR_PAUSE_AT_INDEX
                target = next((i for i in items if i.item_index == t_idx), None)
                if target and not st['triggered'] and target.y >= CONVEYOR_PAUSE_TRIGGER_Y: st['paused'] = True; st['triggered'] = True
                if st['paused']:
                    st['timer'] += dt
                    if st['timer'] >= pause_dur: st['paused'] = False

        removes = []
        for i in self.conveyor_items[:]:
            if i.on_conveyor:
                paused = self.batch_pause_states.get(i.batch_id, {'paused':False})
                if i.update_conveyor_movement(dt, CONVEYOR_SPEED, CONVEYOR_PATH, paused): removes.append(i)
        for r in removes: self.conveyor_items.remove(r)

        # Customer Logic
        self.customer_timer += dt
        if self.customer_timer >= self.settings['customer_interval']:
            if None in self.customer_slots: self._spawn_customer(); self.customer_timer = 0
            else: self.customer_timer -= 2
        for c in self.customers[:]:
            c.update(dt)
            if c.is_timeout(): self.money += PENALTY_TIMEOUT; self._spawn_popup(c.x, c.y-50, "Angry!", COLOR_RED); self._remove_customer(c)

    def _end_shift(self):
        from game.game_manager import GameState
        self.game_manager.change_state(GameState.GAME_OVER, money=self.money, difficulty=self.difficulty)

    def _render_conveyor_belt(self, screen):
        if not self.conveyor_texture: return
        path = CONVEYOR_PATH; tex = self.conveyor_texture; w = tex.get_width()
        for i in range(len(path)-1):
            s, e = path[i], path[i+1]
            dx, dy = e[0]-s[0], e[1]-s[1]; dist = math.hypot(dx, dy)
            if dist < 1: continue
            angle = math.degrees(math.atan2(-dy, dx))
            seg = pygame.Surface((int(dist), self.belt_width), pygame.SRCALPHA)
            off = int(self.scroll_offset) % w; x = off - w
            while x < dist: seg.blit(tex, (x, 0)); x += w
            rot = pygame.transform.rotate(seg, angle)
            screen.blit(rot, rot.get_rect(center=(s[0]+dx/2, s[1]+dy/2)))

    def _draw_item_shadow(self, screen, item, off=(5,5), sc=1.0):
        if not item.image: return
        img = item.image
        if sc != 1.0: img = pygame.transform.scale(img, (int(img.get_width()*sc), int(img.get_height()*sc)))
        try:
            mask = pygame.mask.from_surface(img)
            shad = mask.to_surface(setcolor=(0,0,0,100), unsetcolor=None)
            if sc != 1.0:
                r = shad.get_rect(center=item.get_rect().center); r.x+=off[0]; r.y+=off[1]; screen.blit(shad, r)
            else: screen.blit(shad, (item.x+off[0], item.y+off[1]))
        except: pass

    def _render_item_tooltip(self, screen):
        """渲染悬停提示 (纯图片背景，仅显示名字)"""
        if not self.hovered_item:
            return

        # 1. 准备文字 (只渲染名字)
        mouse_pos = pygame.mouse.get_pos()
        item_name = self.hovered_item.name

        # 名字设为白色，字体稍微大一点点或者保持原样
        name_surf = self.font_small.render(item_name, True, COLOR_WHITE)

        # 2. 计算尺寸
        padding_x = 10
        padding_y = 8

        width = name_surf.get_width() + padding_x * 2
        height = name_surf.get_height() + padding_y * 2

        # 3. 确定位置 (鼠标右下方)
        x = mouse_pos[0] + 20
        y = mouse_pos[1] + 20

        # 防止跑出屏幕
        if x + width > WINDOW_WIDTH:
            x = mouse_pos[0] - width - 10
        if y + height > WINDOW_HEIGHT:
            y = mouse_pos[1] - height - 10

        # 4. 绘制背景 (只使用图片)
        if self.label_image:
            # 拉伸图片以适应文字大小
            bg = pygame.transform.scale(self.label_image, (width, height))
            screen.blit(bg, (x, y))

            # 5. 绘制文字 (居中)
            text_x = x + (width - name_surf.get_width()) // 2
            text_y = y + (height - name_surf.get_height()) // 2
            screen.blit(name_surf, (text_x, text_y))

    def render(self, screen):
        if self.background: screen.blit(self.background, (0,0))
        else: screen.fill(COLOR_GRAY)

        self._render_conveyor_belt(screen)
        for i in self.conveyor_items: self._draw_item_shadow(screen, i); i.render(screen)

        # [修改] 只渲染桌面物品，不再渲染储物柜
        for i in self.inventory_manager.desk_items: self._draw_item_shadow(screen, i)
        self.inventory_manager.render(screen)

        for c in self.customers:
            c.render(screen)

        self.hud.render(screen, self.money, self.shift_time, self.shift_duration)

        if self.dragging_item:
            sc = 1.15
            self._draw_item_shadow(screen, self.dragging_item, (20,20), sc)
            simg = pygame.transform.rotozoom(self.dragging_item.image, 0, sc)
            screen.blit(simg, simg.get_rect(center=self.dragging_item.get_rect().center))

        if self.hovered_item and not self.dragging_item: self._render_item_tooltip(screen)
        for p in self.popups: p.render(screen)