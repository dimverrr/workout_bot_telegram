from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
from keyboards.simple_keyboard import make_keyboard
from .exercice_request import request_exercice
from config_reader import config

router = Router()

url = "https://exercisedb.p.rapidapi.com/exercises/bodyPartList"

headers = {
    "X-RapidAPI-Key": config.api_key.get_secret_value(),
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com",
}

response = requests.get(url, headers=headers)

available_body_parts = response.json()
available_number_of_exercises = [str(i) for i in range(1, 6)]


class CreateWorkout(StatesGroup):
    choosing_body_part = State()
    choosing_number_of_exercices = State()


@router.message(StateFilter(None), Command("workout"))
async def workout_command(message: Message, state: FSMContext):
    await message.answer(
        text="Choose body part you want to train:",
        reply_markup=make_keyboard(available_body_parts),
    )
    await state.set_state(CreateWorkout.choosing_body_part)


@router.message(CreateWorkout.choosing_body_part, F.text.in_(available_body_parts))
async def body_part_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_body_part=message.text.lower())
    await message.answer(
        text="Choose number of exercices:",
        reply_markup=make_keyboard(available_number_of_exercises),
    )
    await state.set_state(CreateWorkout.choosing_number_of_exercices)


@router.message(CreateWorkout.choosing_body_part)
async def body_part_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer(
        text="Invalid body part. \n\n" "Please choose correct body part:",
        reply_markup=make_keyboard(available_body_parts),
    )


@router.message(
    CreateWorkout.choosing_number_of_exercices,
    F.text.in_(available_number_of_exercises),
)
async def number_of_exercices_chosen(message: Message, state: FSMContext):
    user_data = await state.get_data()
    exercices = request_exercice(user_data["chosen_body_part"], message.text.lower())
    for i in exercices:
        instructions = "\n".join(i["instructions"])
        await message.answer_animation(
            i["gifUrl"],
            caption=f"Exercice name - {i['name']}\n\n"
            f"Instructions: \n {instructions}",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.clear()


@router.message(CreateWorkout.choosing_number_of_exercices)
async def number_of_exercices_chosen_incorrectly(message: Message):
    await message.answer(
        text="Wrong number of exercices",
        reply_markup=make_keyboard(available_number_of_exercises),
    )
