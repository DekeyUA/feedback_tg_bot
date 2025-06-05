
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, Router

from bot.classes import ReplyMessage
router = Router()


@router.callback_query(F.data.startswith("reply_message_"))
async def reply_message(callback: CallbackQuery, state: FSMContext):
    split = callback.data.split("_")
    user_id = split[2]
    await callback.answer("")
    await callback.message.answer("Введіть відповідь")
    await state.set_state(ReplyMessage.message)
    await state.update_data(user_id=user_id)

@router.message(ReplyMessage.message)
async def send_replied_message(message: Message, state: FSMContext):
    await state.update_data(message=message.text)
    data =  await state.get_data()
    reply_confirmation = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Відповісти", callback_data="reply_confirmed"),
         InlineKeyboardButton(text="Відхилити", callback_data="reply_declined")]
    ])
    await message.answer(f'Ви хочете надіслати повідомлення: '
                         f'\n\n {data["message"]} \n\n '
                         f'користувачу: {data["user_id"]}', reply_markup=reply_confirmation)

@router.callback_query(F.data == "reply_confirmed")
async def reply_confirmed(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer("")
        data = await state.get_data()
        await callback.bot.send_message(data["user_id"], data["message"])
        await callback.message.edit_text(f'Ви відповіли користувачу {data["user_id"]} повідомленням "{data["message"]}"')
    finally:
        await state.clear()

@router.callback_query(F.data == "reply_declined")
async def reply_declined(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer("")
        await callback.message.edit_text("Ви відхилили відповідь на повідомлення")
    finally:
        await state.clear()


@router.callback_query(F.data.startswith("dimon"))
async def dimon(callback: CallbackQuery):
    split = callback.data.split("_")
    user_id = split[1]
    await callback.answer("")
    await callback.message.answer(f"Replied to: {user_id}")
    await callback.bot.send_message(user_id,"Dima verni stol")