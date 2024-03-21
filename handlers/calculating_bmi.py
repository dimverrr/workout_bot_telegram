from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.simple_keyboard import make_keyboard
from .bmi_formulas import metric_bmi, imperial_bmi

router = Router()

available_measuring_systems = ["metric", "imperial"]
available_weights = float


class CalculateBMI(StatesGroup):
    choosing_measuring_systems = State()
    entering_height = State()
    entering_weight = State()


# Choosing measuring system validating wrong input
@router.message(StateFilter(None), Command("bmi"))
async def bmi_command(message: Message, state: FSMContext):
    await message.answer(
        text="Choose a measuring system:",
        reply_markup=make_keyboard(available_measuring_systems),
    )
    await state.set_state(CalculateBMI.choosing_measuring_systems)


# Entering weight
@router.message(
    CalculateBMI.choosing_measuring_systems, F.text.in_(available_measuring_systems)
)
async def measuring_system_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_measuring_system=message.text.lower())
    await message.answer(text="Enter your weight:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CalculateBMI.entering_weight)


# validating wrong input for measuring system
@router.message(CalculateBMI.choosing_measuring_systems)
async def measuring_system_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="Invalid measuring system. \n\n" "Please choose the correct one:",
        reply_markup=make_keyboard(available_measuring_systems),
    )


# Entering height
@router.message(CalculateBMI.entering_weight, F.text.regexp("^\d+(\.\d+)?$"))
async def weight_chosen(message: Message, state: FSMContext):
    await state.update_data(entered_weight=message.text.lower())
    await message.answer(
        text="Enter your height in m for metric or inches for imperial:",
    )
    await state.set_state(CalculateBMI.entering_height)


# validating wrong input for weight
@router.message(CalculateBMI.entering_weight)
async def weight_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="Invalid input. \n\n" "Use next formats: 62 or 62.5.",
    )


# Calculating bmi
@router.message(CalculateBMI.entering_height, F.text.regexp("^\d+(\.\d+)?$"))
async def height_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data["chosen_measuring_system"] == "metric":
        bmi = metric_bmi(float(message.text), float(user_data["entered_weight"]))
    else:
        bmi = imperial_bmi(float(message.text), float(user_data["entered_weight"]))
    await message.answer(
        text=bmi,
    )
    await state.clear()


# validating wrong input for height
@router.message(CalculateBMI.entering_height)
async def height_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="Invalid input. \n\n"
        "Use next formats: 1.65 for metric system or 55 for imperial.",
    )
