# 議事録テキストをAIで要約するシンプルなツール

import openai
import json
import sys

def summarize_meeting(text: str) -> str:
    """議事録テキストを要約し、構造化データとして返す"""
    
    prompt = f"""以下の議事録を分析し、JSON形式で出力してください。
    
出力フォーマット:
{{
    "summary":"会議の要約（200字以内）",
    "key_topics":["議題1", "議題2",...],
    "action_items":[
        {{"担当者":"名前","タスク":"内容","期限":"日付"}}
        ...
    ],
    "decisions":["決定事項1","決定事項2",...]
}}

議事録:
{text}
"""

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"system","content":"あなたは議事録分析の専門家です。"},
            {"role":"user","content":prompt}
        ],
        response_format={"type":"json_object"}
    )
    
    return json.loads(response.choices[0].message.content)

def main():
    if len(sys.argv) < 2:
        print("使用方法: python ai_meeting_summarizer.py <議事録ファイル>")
        sys.exit(1)
        
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
        
    result = summarize_meeting(text)
    
    print("=" * 50)
    print("【会議サマリー】")
    print(result["summary"])
    print("\n【主要議題】")
    for topic in result["key_topics"]:
        print(f" - {topic}")
    print("\n【アクションアイテム】")
    for item in result["action_items"]:
        print(f" - {item['担当者']}: {item['タスク']}, (期限: {item['期限']})")
    print("\n【決定事項】")
    for decision in result["decisions"]:
        print(f" - {decision}")
        
if __name__ == "__main__":
    main()