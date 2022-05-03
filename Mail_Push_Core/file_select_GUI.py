from tkinter.filedialog import askopenfilename
import tkinter as tk


def file_select_GUI():
    # 配置文件选择的GUI界面
    filetypes = (
        ('config file', '*.ini'),
        ('All files', '*.*')
    )
    root = tk.Tk()
    root.title('配置文件选择界面')
    root.geometry('580x200')
    text = '''
    选择配置文件完毕后请关闭该对话框！
    
    邮箱监测任务将在对话框关闭后开始运行！
    '''

    lb = tk.Label(root, text=text,  # 设置文本内容
                  width=30,  # 设置label的宽度：30
                  height=10,  # 设置label的高度：10
                  justify='left',  # 设置文本对齐方式：左对齐
                  anchor='nw',  # 设置文本在label的方位：西北方位
                  font=('微软雅黑', 18),  # 设置字体：微软雅黑，字号：18
                  fg='white',  # 设置前景色：白色
                  bg='grey',  # 设置背景色：灰色
                  padx=50,  # 设置x方向内边距：20
                  pady=2)  # 设置y方向内边距：10
    lb.pack()

    config_filename = askopenfilename(initialdir="/", title='Open a file', filetypes=filetypes)
    root.mainloop()

    return config_filename
