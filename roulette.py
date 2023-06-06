import wx, random

width = 800
height = 600

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Roulette', size=(width, height))
        self.panel = wx.Panel(self)

        self.tanks = ['T1 Heavy Tank', 'M4 Sherman',
                      'AMX M4', 'IS-7', 'Leopard 1']
        
        self.win_chance = [0.2, 0.3, 0.1, 0.15, 0.25]

        self.images = [wx.Bitmap('data/img/t1.png'), wx.Bitmap('data/img/m4.png'), wx.Bitmap('data/img/amx.png'),
                       wx.Bitmap('data/img/is7.png'), wx.Bitmap('data/img/leopard.png')]
        
        self.roulette_text = wx.StaticText(self.panel, label='Spin the Roulette')
        self.spin_button = wx.Button(self.panel, label='Spin')
        self.result_text = wx.StaticText(self.panel, label='')

        roulette_width, roulette_height = self.roulette_text.GetSize()
        spin_button_width, spin_button_height = self.spin_button.GetSize()
        result_width, result_height = self.result_text.GetSize()

        x_roulette = (width - roulette_width) // 2
        x_spin_button = (width - spin_button_width) // 2
        x_result = (width - result_width) // 2

        self.roulette_text.SetPosition((x_roulette, 40))
        self.spin_button.SetPosition((x_spin_button, 100))
        self.result_text.SetPosition((x_result, 150))

        self.spin_button.Bind(wx.EVT_BUTTON, self.spin)
        menu_bar = wx.MenuBar()
        prize = wx.Menu()
        prize.Append(wx.ID_ANY, 'Prizes & Chances')
        menu_bar.Append(prize, 'Menu')
        prize.Bind(wx.EVT_MENU, self.show_prizes)
        color = wx.Menu()
        color.Append(wx.ID_ANY, 'Change Color')
        menu_bar.Append(color, 'Color')
        color.Bind(wx.EVT_MENU, self.change_color)
        self.SetMenuBar(menu_bar)
        self.colors = ['white', 'light gray', 'gray', 'dark gray']
        self.current_color = 0
        self.SetBackgroundColour(wx.WHITE)

    def spin(self, event):
        self.spin_button.Disable()
        self.spinning_results = [random.choices(
            self.tanks, weights=self.win_chance, k=1)[0] for i in range(10)]
        self.spinning_results.append(random.choices(
            self.tanks, weights=self.win_chance, k=1)[0])
        self.spin_index = 0
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_spin, self.timer)
        self.timer.Start(100)

    def update_spin(self, event):
        self.result_text.SetLabel(
            f'Spinning...{self.spinning_results[self.spin_index]}')
        self.tank_image = wx.StaticBitmap(self.panel, bitmap=self.images[self.tanks.index(self.spinning_results[-1])])
        image_width, image_height = self.tank_image.GetSize()
        x = (width - image_width) // 2
        y = (height - image_height) // 2
        self.tank_image.SetPosition((x, 170))
        self.spin_index += 1
        if self.spin_index >= len(self.spinning_results):
            self.timer.Stop()
            self.result_text.SetLabel(f'You won: {self.spinning_results[-1]}')
            self.spin_button.Enable()

    def change_color(self, event):
        self.current_color = (self.current_color + 1) % len(self.colors)
        color = self.colors[self.current_color]
        self.SetBackgroundColour(color)
        self.Refresh()

    def show_prizes(self, event):
        prize_dialog = wx.MessageDialog(
            self, '\n'.join([f'{tank}: {chance * 100}%' for tank, chance in zip(self.tanks, self.win_chance)]), 'Prizes & Chances', wx.OK)
        prize_dialog.ShowModal()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Center()
    frame.Show()
    app.MainLoop()
