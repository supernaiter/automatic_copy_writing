#!/usr/bin/env python3
"""
コンポーネント実行管理スクリプト
使用方法: python scripts/run_component.py [component-name] [framework-id] [options]
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# コンポーネント定義
COMPONENTS = {
    "framework-analysis": {
        "path": "components/framework-analysis",
        "frameworks": {
            5: "src/framework_05_share_of_search.py"
        }
    },
    "framework-creative": {
        "path": "components/framework-creative", 
        "frameworks": {
            12: "src/framework_12_copy_dna.py"
        }
    }
}

def list_components():
    """利用可能なコンポーネント一覧表示"""
    print("🔧 利用可能なコンポーネント:")
    for comp_name, comp_info in COMPONENTS.items():
        print(f"\n📦 {comp_name}")
        for fw_id, fw_path in comp_info["frameworks"].items():
            print(f"  • Framework {fw_id}: {fw_path}")

def run_framework(component_name: str, framework_id: int, extra_args: list = None):
    """指定されたフレームワークを実行"""
    if component_name not in COMPONENTS:
        print(f"❌ 未知のコンポーネント: {component_name}")
        list_components()
        return False
    
    component = COMPONENTS[component_name]
    if framework_id not in component["frameworks"]:
        print(f"❌ コンポーネント {component_name} にフレームワーク {framework_id} が見つかりません")
        return False
    
    # 実行パス構築
    framework_script = component["frameworks"][framework_id]
    
    # 絶対パスでスクリプトパスを構築
    script_path = os.path.abspath(os.path.join(component["path"], framework_script))
    
    if not os.path.exists(script_path):
        print(f"❌ スクリプトが見つかりません: {script_path}")
        return False
    
    # 実行コマンド構築（相対パスで実行）
    cmd = ["python", framework_script]
    if extra_args:
        cmd.extend(extra_args)
    
    print(f"🚀 実行中: {' '.join(cmd)}")
    print(f"📁 作業ディレクトリ: {component['path']}")
    
    try:
        # コンポーネントディレクトリで実行
        result = subprocess.run(
            cmd, 
            cwd=component["path"],
            check=True
        )
        print(f"✅ 実行完了: exit code {result.returncode}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 実行エラー: exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ Pythonが見つかりません。仮想環境がアクティブか確認してください。")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="コンポーネント実行管理システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python scripts/run_component.py --list                      # コンポーネント一覧
  python scripts/run_component.py framework-analysis 5        # Framework 5 実行
  python scripts/run_component.py framework-creative 12       # Framework 12 実行
  
  # カスタムオプション付き実行
  python scripts/run_component.py framework-analysis 5 --brand "トヨタ" --competitors "ホンダ" "日産"
        """
    )
    
    parser.add_argument('component', nargs='?', help='実行するコンポーネント名')
    parser.add_argument('framework', nargs='?', type=int, help='実行するフレームワークID')
    parser.add_argument('--list', action='store_true', help='利用可能なコンポーネント一覧表示')
    
    # 残りの引数をフレームワークに渡す
    args, extra_args = parser.parse_known_args()
    
    if args.list:
        list_components()
        return
    
    if not args.component or args.framework is None:
        print("❌ コンポーネント名とフレームワークIDが必要です")
        parser.print_help()
        return
    
    success = run_framework(args.component, args.framework, extra_args)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 