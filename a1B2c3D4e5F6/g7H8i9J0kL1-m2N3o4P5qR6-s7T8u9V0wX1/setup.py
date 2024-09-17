import tkinter as tk
from tkinter import messagebox
import requests
import os
import win32com.client

class InstallWizard:
    def __init__(self, root):
        self.root = root
        self.step = 0  # 現在のステップを追跡
        self.install_path = ""
        self.icon_url = "https://huuze.f5.si/program2/a1B2c3D4e5F6/g7H8i9J0kL1-m2N3o4P5qR6-s7T8u9V0wX1/favicon.ico"  # アイコンのURL
        self.icon_path = os.path.join(os.path.expanduser("~"), "Downloads", "favicon.ico")  # ローカルのパスに保存

        self.root.title("インストールウィザード")
        self.label = tk.Label(root, text="")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root)
        self.entry.pack(pady=10)

        self.next_button = tk.Button(root, text="次へ", command=self.next_step)
        self.next_button.pack(pady=20)

        self.display_step()

    def display_step(self):
        if self.step == 0:
            self.label.config(text="ようこそ！インストールウィザードへ。")
            self.entry.pack_forget()
        elif self.step == 1:
            self.label.config(text="ライセンスに同意しますか？ (はい/いいえ)")
            self.entry.pack()
            self.entry.delete(0, tk.END)
        elif self.step == 2:
            self.label.config(text="インストール先を指定してください。")
            self.entry.pack()
            self.entry.delete(0, tk.END)
        elif self.step == 3:
            self.install_path = self.entry.get()
            warning_msg = "このプログラムを使用したことについての一切の責任を負いません。\n本当にインストールしますか？"
            if messagebox.askyesno("警告", warning_msg):
                # アイコンのダウンロードを開始
                self.download_icon()
            else:
                self.label.config(text="インストールがキャンセルされました。")
                self.root.quit()
        elif self.step == 4:
            self.label.config(text="インストールが完了しました！")
            self.create_shortcut()  # ショートカットを作成
            self.next_button.config(text="完了")

    def next_step(self):
        self.step += 1
        if self.step > 4:
            self.root.destroy()  # ウィンドウを閉じる
        else:
            self.display_step()

    def download_icon(self):
        try:
            response = requests.get(self.icon_url)
            response.raise_for_status()  # エラーがあれば例外を発生させる

            # アイコンを保存
            with open(self.icon_path, 'wb') as icon_file:
                icon_file.write(response.content)

            self.download_json(self.install_path)  # JSONファイルのダウンロードへ進む
        except requests.RequestException as e:
            messagebox.showerror("エラー", f"アイコンのダウンロード中にエラーが発生しました: {e}")
            self.root.quit()

    def download_json(self, path):
        # JSONファイルのURL
        url = "https://huuze.f5.si/program2/a1B2c3D4e5F6/g7H8i9J0kL1-m2N3o4P5qR6-s7T8u9V0wX1/"

        try:
            response = requests.get(url)
            response.raise_for_status()  # エラーがあれば例外を発生させる

            # JSONファイルを取得
            file_list = response.json()  # JSONデータを取得

            # 各ファイルをダウンロード
            for file_name in file_list:
                file_url = f"{url}{file_name}"  # ベースURLの後にファイル名を追加
                self.download_file(file_url, os.path.join(path, file_name))

            messagebox.showinfo("完了", "ファイルが正常にダウンロードされました。")
            self.next_step()  # 次のステップに進む

        except requests.RequestException as e:
            messagebox.showerror("エラー", f"ファイルのダウンロード中にエラーが発生しました: {e}")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("エラー", f"エラーが発生しました: {e}")
            self.root.quit()

    def download_file(self, file_url, file_path):
        try:
            response = requests.get(file_url)
            response.raise_for_status()  # エラーがあれば例外を発生させる

            # ディレクトリが存在しない場合、作成する
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'wb') as file:
                file.write(response.content)  # ファイルの内容を書き込む

            print(f"{file_path} が正常にダウンロードされました。")
        except requests.RequestException as e:
            messagebox.showerror("エラー", f"ファイルのダウンロード中にエラーが発生しました: {e}")

    def create_shortcut(self):
        # ショートカットをデスクトップに作成
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_name = "なんかやばいやつ.lnk"
        target_path = os.path.join(self.install_path, "app.exe")  # 実行ファイルのパスを指定

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(desktop, shortcut_name))
        shortcut.Targetpath = target_path
        shortcut.WorkingDirectory = self.install_path
        shortcut.IconLocation = self.icon_path  # ダウンロードしたアイコンのパスを指定
        shortcut.save()

        messagebox.showinfo("ショートカット作成", f"{shortcut_name}がデスクトップに作成されました。")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstallWizard(root)
    root.mainloop()
