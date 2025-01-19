import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import configparser
import os

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config

def save_config(config, config_path):
    with open(config_path, "w", encoding='utf-8') as configfile:
        config.write(configfile)

def list_websites(config, tree):
    for item in tree.get_children():
        tree.delete(item)
    for section in config.sections():
        if section.startswith('WEBSITE_'):
            website_number = section.split('_')[1]
            url = config[section]['url']
            interval = config[section]['probe_interval']
            tree.insert("", "end", values=(website_number, url, interval))

def add_website(config, url_entry, interval_entry, config_path, tree):
    url = url_entry.get()
    interval = interval_entry.get()
    if not url or not interval:
        messagebox.showerror("错误", "URL 和 探测间隔不能为空")
        return
    try:
        int(interval)
    except ValueError:
         messagebox.showerror("错误", "探测间隔必须为整数")
         return
    website_number = 1
    while f'WEBSITE_{website_number}' in config:
        website_number += 1
    section_name = f'WEBSITE_{website_number}'
    config[section_name] = {
        'url': url,
        'probe_interval': interval
    }
    save_config(config, config_path)
    messagebox.showinfo("成功", f"网站 {url} 添加成功，编号为 {website_number}")
    list_websites(config, tree)

def delete_website(config, website_number_entry, config_path, tree):
    website_number = website_number_entry.get()
    if not website_number:
        messagebox.showerror("错误", "网站编号不能为空")
        return
    section_name = f'WEBSITE_{website_number}'
    if section_name in config:
        config.remove_section(section_name)
        save_config(config, config_path)
        messagebox.showinfo("成功", f"网站 {website_number} 删除成功")
        list_websites(config, tree)
    else:
        messagebox.showerror("错误", f"网站 {website_number} 不存在")

def modify_website(config, website_number_entry, key_entry, value_entry, config_path, tree):
    website_number = website_number_entry.get()
    key = key_entry.get()
    value = value_entry.get()
    if not website_number or not key or not value:
        messagebox.showerror("错误", "网站编号、属性和值不能为空")
        return
    section_name = f'WEBSITE_{website_number}'
    if section_name in config:
        if key in config[section_name]:
            config[section_name][key] = value
            save_config(config, config_path)
            messagebox.showinfo("成功", f"网站 {website_number} 的 {key} 修改为 {value}")
            list_websites(config, tree)
        else:
            messagebox.showerror("错误", f"网站 {website_number} 没有 {key} 这个属性")
    else:
        messagebox.showerror("错误", f"网站 {website_number} 不存在")

def main():
    config_path = "config.ini"
    config = load_config(config_path)

    if not os.path.exists(config_path):
        with open(config_path, "w", encoding='utf-8') as f:
            f.write("[DEFAULT]\n")
        config = load_config(config_path)

    root = tk.Tk()
    root.title("网站管理工具")

    # 网站列表
    tree = ttk.Treeview(root, columns=("编号", "URL", "探测间隔"), show="headings")
    tree.heading("编号", text="编号")
    tree.heading("URL", text="URL")
    tree.heading("探测间隔", text="探测间隔")
    tree.pack(pady=10)

    list_websites(config, tree)

    # 添加网站
    add_frame = ttk.Frame(root)
    add_frame.pack(pady=5)
    ttk.Label(add_frame, text="URL:").grid(row=0, column=0, padx=5)
    url_entry = ttk.Entry(add_frame)
    url_entry.grid(row=0, column=1, padx=5)
    ttk.Label(add_frame, text="探测间隔:").grid(row=0, column=2, padx=5)
    interval_entry = ttk.Entry(add_frame)
    interval_entry.grid(row=0, column=3, padx=5)
    ttk.Button(add_frame, text="添加", command=lambda: add_website(config, url_entry, interval_entry, config_path, tree)).grid(row=0, column=4, padx=5)

    # 删除网站
    delete_frame = ttk.Frame(root)
    delete_frame.pack(pady=5)
    ttk.Label(delete_frame, text="网站编号:").grid(row=0, column=0, padx=5)
    website_number_entry_delete = ttk.Entry(delete_frame)
    website_number_entry_delete.grid(row=0, column=1, padx=5)
    ttk.Button(delete_frame, text="删除", command=lambda: delete_website(config, website_number_entry_delete, config_path, tree)).grid(row=0, column=2, padx=5)

    # 修改网站
    modify_frame = ttk.Frame(root)
    modify_frame.pack(pady=5)
    ttk.Label(modify_frame, text="网站编号:").grid(row=0, column=0, padx=5)
    website_number_entry_modify = ttk.Entry(modify_frame)
    website_number_entry_modify.grid(row=0, column=1, padx=5)
    ttk.Label(modify_frame, text="属性:").grid(row=0, column=2, padx=5)
    key_entry = ttk.Entry(modify_frame)
    key_entry.grid(row=0, column=3, padx=5)
    ttk.Label(modify_frame, text="值:").grid(row=0, column=4, padx=5)
    value_entry = ttk.Entry(modify_frame)
    value_entry.grid(row=0, column=5, padx=5)
    ttk.Button(modify_frame, text="修改", command=lambda: modify_website(config, website_number_entry_modify, key_entry, value_entry, config_path, tree)).grid(row=0, column=6, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()
