# 我的网站监控面板

## 项目描述

这是一个简单的网站监控面板，可以实时显示网站的运行状态。它可以监控多个网站，并显示每个网站的在线状态、响应时间、以及其他详细信息。

## 技术栈

*   **Python:** 后端开发语言
*   **Flask:** Python Web 框架
*   **HTML:** 页面结构
*   **CSS:** 页面样式
*   **JavaScript:** 页面交互

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
    cd run_probe_service
    python run_probe.py
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
