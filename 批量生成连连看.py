import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import pyperclip


def generate_panel(number,click_before1, click_after1,click_before2, click_after2,rect1,rect2):
    template = '''<g id="{number}">
    <g id="第一张图">
        <g id="1-点击前" transform="translate(0 0)" style="visibility: visible;">
            {click_before1}
        </g>
        <g id="1-点击后" transform="translate(2000 0)" style="visibility: visible;">
            {click_after1}
        </g>
        <g id="热区1" style="pointer-events: painted; visibility: visible;">
            {rect1}
        </g>
        <animateTransform attributeName="transform" data-txscript="hc" type="translate"
                          values="0 0;-2000 0;-2000 0" keyTimes="0;0.00000000001;1" begin="click" dur="2000s"
                          restart="never" fill="freeze"></animateTransform>
    </g>
    <g id="第二张图">
        <g id="2-点击前" transform="translate(0 0)">
             {click_before2}
        </g>
        <g id="2-点击后" transform="translate(2000 0)">
           {click_after2}
        </g>
        <g id="热区2" style="pointer-events: painted; visibility: visible;">
            {rect2}
        </g>

        <animateTransform attributeName="transform" data-txscript="hc" type="translate"
                          values="0 0;-2000 0;-2000 0" keyTimes="0;0.00000000001;1" begin="click" dur="2000s"
                          restart="never" fill="freeze"></animateTransform>
    </g>
    <g>
        <g>
            <g id="第一张图">
                <g id="1-点击后" transform="translate(2000 0)">
                   {click_after1}
                </g>
                <g id="热区1" style="pointer-events: painted; visibility: visible;">
                    <animateTransform attributeName="transform" type="translate" values="-2000 0" begin="touchstart"
                                      dur="1s" restart="whenNotActive"></animateTransform>

                    {rect1}

                </g>
            </g>
            <g id="第二张图">
                <g id="2-点击后" transform="translate(2000 0)">
                   {click_after2}
                </g>
                <g id="热区2" style="pointer-events: painted; visibility: visible;">
                    <animateTransform attributeName="transform" type="translate" values="-2000 0" begin="touchstart"
                                      dur="1s" restart="whenNotActive"></animateTransform>

                    {rect2}
                </g>
            </g>
            <animateTransform attributeName="transform" data-txscript="hc" type="translate"
                              values="0 0;-2000 0;-2000 0"
                              keyTimes="0;0.00000000001;1" begin="touchstart+1" dur="2000s" restart="never"
                              fill="freeze"></animateTransform>
        </g>
        <g>
            <g>
                <g id="1-点击后" transform="translate(2000 0)">
                    {click_after1}
                </g>
                <g id="热区2" style="pointer-events: painted; visibility: visible;">
                    <animateTransform attributeName="transform" type="translate" values="2000 0" begin="click"
                                      dur="2s" restart="whenNotActive"></animateTransform>

                    {rect2}
                </g>
                <animateTransform attributeName="transform" type="translate" values="2000 0" begin="click" dur="2s"
                                  restart="whenNotActive"></animateTransform>
            </g>
            <g>
                <g id="2-点击后" transform="translate(2000 0)">
                    {click_after2}
                </g>
                <g id="热区1" style="pointer-events: painted; visibility: visible;">
                     <animateTransform attributeName="transform" type="translate" values="2000 0" begin="click"
                                      dur="2s" restart="whenNotActive"></animateTransform>
                    {rect1}

                </g>

                <animateTransform attributeName="transform" type="translate" values="2000 0" begin="click" dur="2s"
                                  restart="whenNotActive"></animateTransform>
            </g>
            <animateTransform attributeName="transform" type="translate" values="-2000 0" begin="click" dur="2s"
                              restart="whenNotActive"></animateTransform>
        </g>
    </g>
</g>
'''

    panel_code = template.format(number=number,click_before1=click_before1, click_after1=click_after1,click_before2=click_before2,click_after2=click_after2,rect1=rect1,rect2=rect2)
    return panel_code


def generate_panel_button():
    global click_before1_entry, click_after1_entry,number_entry,click_before2_entry,click_after2_entry,rect1_entry,rect2_entry

    number = number_entry.get("1.0", "end-1c")
    click_before1 = click_before1_entry.get("1.0", "end-1c")
    click_after1 = click_after1_entry.get("1.0", "end-1c")
    click_before2=click_before2_entry.get("1.0", "end-1c")
    click_after2=click_after2_entry.get("1.0", "end-1c")
    rect1 = rect1_entry.get("1.0", "end-1c")
    rect2 = rect2_entry.get("1.0", "end-1c")

    generated_panel = generate_panel(number,click_before1, click_after1,click_before2,click_after2,rect1,rect2)
    pyperclip.copy(generated_panel)
    # messagebox.showinfo("生成消消乐代码", "代码已生成并复制到剪贴板。")
    print("代码已生成并复制到剪贴板")


def main():
    global click_before1_entry, click_after1_entry,number_entry,click_before2_entry,click_after2_entry,rect1_entry,rect2_entry

    root = tk.Tk()
    root.title("消消乐代码生成器")

    number_label = tk.Label(root, text="序列号:")
    number_label.pack()
    number_entry = tk.Text(root, height=5, width=10)
    number_entry.pack()

    click_before1_label = tk.Label(root, text="1-点击前:")
    click_before1_label.pack()
    click_before1_entry = tk.Text(root, height=5, width=30)
    click_before1_entry.pack()

    click_after1_label = tk.Label(root, text="1-点击后:")
    click_after1_label.pack()
    click_after1_entry = tk.Text(root, height=5, width=30)
    click_after1_entry.pack()

    click_before2_label = tk.Label(root, text="2-点击前:")
    click_before2_label.pack()
    click_before2_entry = tk.Text(root, height=5, width=30)
    click_before2_entry.pack()

    click_after2_label = tk.Label(root, text="2-点击后:")
    click_after2_label.pack()
    click_after2_entry = tk.Text(root, height=5, width=30)
    click_after2_entry.pack()

    rect1_label = tk.Label(root, text="热区1:")
    rect1_label.pack()
    rect1_entry = tk.Text(root, height=5, width=30)
    rect1_entry.pack()

    rect2_label = tk.Label(root, text="热区2:")
    rect2_label.pack()
    rect2_entry = tk.Text(root, height=5, width=30)
    rect2_entry.pack()

    generate_button = ttk.Button(root, text="生成代码", command=generate_panel_button)
    generate_button.pack()

    root.mainloop()


if __name__ == '__main__':
    main()