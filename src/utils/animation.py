import asyncio
from itertools import cycle
from aiogram import types


async def show_loading_animation(message: types.Message, action_text: str, delay: float = 0.3):
    frames_obj = ["[ ░░░░░ ]", "[█░░░░░]", "[██░░░░]", "[███░░░]", "[████░░]", "[█████░]", "[██████]"]
    frames = cycle(frames_obj)
    for frame in frames:
        try:
            await message.edit_text(f"{frame} {action_text}")
            await asyncio.sleep(delay)
        except Exception:
            break