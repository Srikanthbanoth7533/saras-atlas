import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    en_us = [v for v in voices if v["Locale"] == "en-US" and "Neural" in v["ShortName"]]
    for v in en_us:
        print(f"{v['ShortName']} ({v['Gender']}) - {v.get('FriendlyName', '')}")

if __name__ == "__main__":
    asyncio.run(main())
