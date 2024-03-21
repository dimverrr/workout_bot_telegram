from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Choose what you want to do: "
        "Create workout (/workout) or calculate body mass index (BMI) (/bmi).",
        reply_markup=ReplyKeyboardRemove(),
    )


# @router.message(Command(commands=["bmi"]))
# async def cmd_bmi(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer(
#         text="Coming soon. Try (/workout) command to create a workout.",
#         reply_markup=ReplyKeyboardRemove(),
#     )


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "cancel")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(text="Nothing to cancel.", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="The action was canceled.", reply_markup=ReplyKeyboardRemove()
    )
