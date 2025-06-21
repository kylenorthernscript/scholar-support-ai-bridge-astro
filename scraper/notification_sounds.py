#!/usr/bin/env python3
"""
Notification sound system for task completion and user prompts
使用法: python notification_sounds.py [task_complete|yes_no]
"""

import subprocess
import sys
import os

def play_task_complete_sound():
    """タスク完了時の通知音を再生"""
    try:
        # システムの完了音を使用 (macOS)
        subprocess.run(['afplay', '/System/Library/Sounds/Glass.aiff'], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # フォールバック: ターミナルベル
        print('\a', end='', flush=True)

def play_yes_no_prompt_sound():
    """Yes/No質問時の通知音を再生"""
    try:
        # システムの質問音を使用 (macOS)
        subprocess.run(['afplay', '/System/Library/Sounds/Tink.aiff'], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # フォールバック: 2回のターミナルベル
        print('\a\a', end='', flush=True)

def main():
    if len(sys.argv) != 2:
        print("使用法: python notification_sounds.py [task_complete|yes_no]")
        sys.exit(1)
    
    sound_type = sys.argv[1]
    
    if sound_type == "task_complete":
        play_task_complete_sound()
        print("🔔 タスクが完了しました")
    elif sound_type == "yes_no":
        play_yes_no_prompt_sound()
        print("🔔 ユーザー確認が必要です")
    else:
        print("エラー: 不明な音声タイプ:", sound_type)
        sys.exit(1)

if __name__ == "__main__":
    main()