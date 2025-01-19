# 我的网站监控面板

## 项目描述

这是一个简单的网站监控面板，可以实时显示网站的运行状态。它可以监控多个网站，并显示每个网站的在线状态、响应时间、以及其他详细信息。

## 技术栈

*   **Python:** 后端开发语言
*   **Flask:** Python Web 框架
*   **HTML:** 页面结构
*   **CSS:** 页面样式
*   **JavaScript:** 页面交互
*   **Tkinter:** Python GUI 库

## 安装步骤

1.  **克隆仓库：**
    ```bash
    git clone https://github.com/yuhold/uwu.git
    ```
2.  **进入项目目录：**
    ```bash
    cd uwu
    ```
3.  **创建虚拟环境 (推荐):**
    ```bash
    python -m venv venv
    ```
4.  **激活虚拟环境：**
    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
5.  **安装依赖项：**
    ```bash
    pip install -r requirements.txt
    ```

## 运行步骤

1.  **启动 probe 服务:**
    ```bash
    python probe.py
    ```

2.  **启动 Flask 应用：**
    ```bash
    cd ../webapp
    python app.py
    ```

3.  **在浏览器中访问：**
    打开浏览器，访问 `http://127.0.0.1:5000`。

## 使用说明

*   监控面板会实时显示你配置的网站的运行状态。
*   每个网站的状态信息会以卡片的形式显示，包括网站地址、状态、时间、以及详情。
*   不同的状态会使用不同的颜色指示，例如：
    *   绿色表示在线
    *   红色表示离线
    *   黄色表示运行中
    *   蓝色表示成功
    *   灰色表示失败

## 管理网站

### 使用 `manage_websites_gui.py`

为了更方便地管理监控的网站，你可以使用 `manage_websites_gui.py` 脚本，它提供了一个图形用户界面 (GUI) 来添加、删除和修改网站。

1.  **运行 `manage_websites_gui.py`：**
    ```bash
    python manage_websites_gui.py
    ```
    或者，如果你已经将其转换为 exe 文件，可以直接运行 `manage_websites_gui.exe`。

2.  **使用界面：**
    *   **网站列表：** 窗口顶部显示当前监控的所有网站，包括编号、URL 和探测间隔。
    *   **添加网站：** 在 "添加网站" 部分，输入网站的 URL 和探测间隔，点击 "添加" 按钮。
    *   **删除网站：** 在 "删除网站" 部分，输入要删除的网站编号，点击 "删除" 按钮。
    *   **修改网站：** 在 "修改网站" 部分，输入要修改的网站编号、属性 (URL 或 probe_interval) 以及新的值，点击 "修改" 按钮。

3.  **注意事项：**
    *   在添加、删除或修改网站之后，你需要重新启动 `probe.py` 服务，才能使更改生效。
    *   `config.ini` 文件会保存你的配置。

## 贡献指南

如果你想为这个项目贡献代码，请按照以下步骤操作：

1.  **Fork 仓库**
2.  **创建新的分支：**
    ```bash
    git checkout -b feature/your-feature-name
    ```
3.  **修改代码并提交：**
    ```bash
    git add .
    git commit -m "Add your commit message"
    ```
4.  **推送分支：**
    ```bash
    git push origin feature/your-feature-name
    ```
5.  **创建 Pull Request**

## 许可证

本项目使用 MIT 许可证。
